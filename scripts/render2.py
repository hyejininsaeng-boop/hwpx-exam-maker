"""(확인용) hwpx 를 한글로 열어 PDF 와 쪽별 PNG 를 work 폴더 안에만 만든다. 결과물로 내놓는 용도가 아님.
사용: python -X utf8 -I render2.py <in.hwpx> <태그>"""
import win32com.client as w, os, sys, fitz
WW = (os.environ.get("EXAM_WORK") or (os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()))

src, tag = sys.argv[1], sys.argv[2]
hwp = w.gencache.EnsureDispatch("HWPFrame.HwpObject")
try:
    try:
        hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
    except Exception:
        pass
    pdf = os.path.join(WW, tag + ".pdf")
    if not hwp.Open(src, "HWPX", ""):
        raise SystemExit("파일을 열지 못했습니다: %s" % src)
    print("open ok")
    if not hwp.SaveAs(pdf, "PDF", "") or not os.path.exists(pdf):
        raise SystemExit("PDF 저장 실패")
    print("pdf", pdf)
finally:
    hwp.Quit()
with fitz.open(pdf) as d:
    print("pages", len(d))
    for i in range(len(d)):
        d[i].get_pixmap(dpi=100).save(os.path.join(WW, "%s_p%d.png" % (tag, i + 1)))
