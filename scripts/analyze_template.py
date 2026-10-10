"""새 양식(.hwp 또는 .hwpx)의 구조를 분석한다. 다른 문제지에 이 스킬을 적용할 때 가장 먼저 실행한다.

사용:  python -X utf8 -I analyze_template.py <양식파일> [이름]
  .hwp 이면 한글(COM)로 .hwpx 복사본을 만든 뒤 분석한다(원본은 수정하지 않음).
결과(작업 폴더 안):
  <이름>_x\\            압축을 푼 hwpx (Contents\\section0.xml 이 본문)
  <이름>_map.txt       문단 지도: 번호, 문단모양(pr)/스타일(st), 내용 요약, 빈 문단 개수
                        표시: [EN]=미주(문제번호·해설), <PIC 가로x세로>=그림, <TBL 행x열>=표/상자, <RECT>=글상자
  <이름>_sheet_N.png   쪽 배치 미리보기(4쪽씩) -- 어느 문제가 어느 쪽·단에 있는지 눈으로 확인
  <이름>.pdf           미리보기용 임시 PDF (작업 폴더 안에만 둠)
환경변수 EXAM_WORK 로 작업 폴더를 정한다(기본: 이 파일이 있는 폴더)."""
import os, sys, shutil, zipfile
from lxml import etree

W = os.environ.get("EXAM_WORK") or (os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd())
HP = "http://www.hancom.co.kr/hwpml/2011/paragraph"
ln = lambda e: etree.QName(e.tag).localname

src = os.path.abspath(sys.argv[1])
name = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(os.path.basename(src))[0]
hwpx = os.path.join(W, name + "_template.hwpx")
pdf = os.path.join(W, name + ".pdf")

# 1) .hwp -> .hwpx 복사본 + PDF (한글 COM)
import win32com.client as w
hwp = w.gencache.EnsureDispatch("HWPFrame.HwpObject")
try:
    try:
        hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
    except Exception:
        pass
    fmt = "HWP" if src.lower().endswith(".hwp") else "HWPX"
    print("open", hwp.Open(src, fmt, ""))
    print("save hwpx", hwp.SaveAs(hwpx, "HWPX", ""))
    print("save pdf", hwp.SaveAs(pdf, "PDF", ""))
finally:
    hwp.Quit()

# 2) 압축 해제
x = os.path.join(W, name + "_x")
if os.path.exists(x):
    shutil.rmtree(x)
zipfile.ZipFile(hwpx).extractall(x)

# 3) 문단 지도
root = etree.parse(os.path.join(x, "Contents", "section0.xml")).getroot()
ps = [c for c in root if ln(c) == "p"]


def vis(el):
    out = []

    def walk(e):
        n = ln(e)
        if n == "endNote":
            out.append("[EN]"); return
        if n == "t":
            if e.text:
                out.append(e.text)
            for c in e:
                if ln(c) == "tab":
                    out.append("\t")
                if c.tail:
                    out.append(c.tail)
            return
        if n == "script":
            out.append("{" + (e.text or "").strip()[:55] + "}"); return
        if n == "pic":
            sz = e.find("{%s}sz" % HP)
            out.append("<PIC %sx%s>" % (sz.get("width"), sz.get("height"))); return
        if n == "tbl":
            out.append("<TBL %sx%s>" % (e.get("rowCnt"), e.get("colCnt")))
            for tc in e.iter("{%s}tc" % HP):
                out.append("(cell:" + " ".join(vis(tc))[:90] + ")")
            return
        if n == "rect":
            out.append("<RECT>")
        for c in e:
            walk(c)
    walk(el)
    return out


lines, blank = [], 0
for i, p in enumerate(ps):
    v = "".join(vis(p)).strip()
    if v == "" and p.get("paraPrIDRef") == "4":      # 빈 문단(양식이 여백 확보용으로 씀)
        blank += 1
        continue
    if blank:
        lines.append("      ...빈 문단 x%d" % blank)
        blank = 0
    lines.append("%d\tpr=%s\tst=%s\tpageBreak=%s\tcolBreak=%s\t%s" % (
        i, p.get("paraPrIDRef"), p.get("styleIDRef"), p.get("pageBreak"), p.get("columnBreak"), v[:200]))
if blank:
    lines.append("      ...빈 문단 x%d" % blank)
mp = os.path.join(W, name + "_map.txt")
open(mp, "w", encoding="utf-8").write("\n".join(lines))
print("문단 수:", len(ps), "| 지도:", mp)

# 4) 쪽 배치 미리보기
try:
    import fitz
    from PIL import Image
    d = fitz.open(pdf)
    print("PDF 쪽수:", len(d))
    for s in range(0, len(d), 4):
        ims = []
        for i in range(s, min(s + 4, len(d))):
            pm = d[i].get_pixmap(dpi=55)
            ims.append(Image.frombytes("RGB", (pm.width, pm.height), pm.samples))
        w_, h_ = ims[0].size
        S = Image.new("RGB", (w_ * len(ims), h_), "white")
        for k, im in enumerate(ims):
            S.paste(im, (k * w_, 0))
        S.save(os.path.join(W, "%s_sheet_%d.png" % (name, s // 4 + 1)))
except Exception as ex:
    print("미리보기 생략:", ex)
