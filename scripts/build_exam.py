"""수능 스타일 문제지(공통 1~22 + 선택 23~30) 빌더. 양식(calc_x/prob_x/geo_x)의 문단을 복사해 내용만 바꾼다.
사용: (환경변수 TRACK=calc|prob|geo, KEY=0|1)  python -X utf8 -I build_exam.py <out.hwpx>
KEY=1 이면 문제 + 해설(미주) + 정답표를 함께 만든다.
"""
import copy, json, os, re, shutil, sys, zipfile
from lxml import etree

HP = "http://www.hancom.co.kr/hwpml/2011/paragraph"
W = (os.environ.get("EXAM_WORK") or (os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()))
os.environ.setdefault("EXAM_WORK", W)
KEY = os.environ.get("KEY", "0") == "1"      # 1이면 문제+해설(미주) 파일
TOTAL_STATIC = 12                            # 문제지만 있는 파일의 총 쪽수 표시
TRACK = os.environ.get("TRACK", "calc")      # calc(미적분) | prob(확률과 통계) | geo(기하)
SRC = os.path.join(W, TRACK + "_x")
OUT_DIR = os.path.join(W, "build_x")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(W, "exam_common.hwpx")
q = lambda n: "{%s}%s" % (HP, n)
ln = lambda e: etree.QName(e.tag).localname

SIZES = {}
_sp = os.path.join(W, "sizes.json")
if os.path.exists(_sp):
    SIZES = {k: tuple(v[:3]) for k, v in json.load(open(_sp, encoding="utf-8")).items()}
NEEDED = []
_ctr = [2100000000]


def est(script):
    """한글이 잰 실측값(sizes.json)이 있으면 사용, 없으면 임시 추정(측정 대상 목록에만 기록)."""
    if script in SIZES:
        return SIZES[script]
    return (len(script) * 450, 1125, 85)


def mk_eq(tpl, script):
    NEEDED.append(script)
    e = copy.deepcopy(tpl)
    w, h, bl = est(script)
    _ctr[0] += 1
    e.set("id", str(_ctr[0]))
    e.set("zOrder", str(6000 + _ctr[0] % 100000))
    e.set("baseLine", str(bl))
    sz = e.find(q("sz"))
    sz.set("width", str(w)); sz.set("height", str(h))
    for c in e.findall(q("shapeComment")):
        e.remove(c)
    e.find(q("script")).text = script
    return e, w


def strip_lineseg(p):
    for el in list(p.iter(q("linesegarray"))):
        el.getparent().remove(el)


def has_endnote(run):
    return any(ln(x) == "endNote" for x in run.iter())


def first_eq(p):
    for e in p.iter(q("equation")):
        return e
    return None


G = {}  # 전역 템플릿


def set_para(p, segs, tpl=None):
    """문단의 (미주가 없는) 첫 run 내용을 segs로 교체. segs: [('t',str)|('e',script)|('tab',폭,뒤글자[,개수])]"""
    runs = [r for r in p if ln(r) == "run"]
    target = next(r for r in runs if not has_endnote(r))
    tpl = first_eq(target) if first_eq(target) is not None else (tpl if tpl is not None else G["eq"])
    tpl = copy.deepcopy(tpl)
    for r in runs:
        if r is not target and not has_endnote(r):
            p.remove(r)
    for c in list(target):
        target.remove(c)
    for seg in segs:
        kind, v = seg[0], seg[1]
        if kind == "t":
            t = etree.SubElement(target, q("t")); t.text = v
        elif kind == "tab":  # ("tab", 폭, 탭 뒤 글자[, 개수])
            t = etree.SubElement(target, q("t"))
            for _ in range(seg[3] if len(seg) > 3 else 1):
                tb = etree.SubElement(t, q("tab"), width=str(v), leader="0", type="1")
            tb.tail = seg[2]
        else:
            target.append(mk_eq(tpl, v)[0])
    etree.SubElement(target, q("t"))
    strip_lineseg(p)


def rebuild_cell(cell, specs):
    """표 칸의 문단을 모두 지우고, 원래 문단을 틀로 복사해 specs=[(틀번호, segs)] 순서로 다시 채운다."""
    sub = cell.find(q("subList"))
    tpl = [copy.deepcopy(p) for p in sub.findall(q("p"))]
    for p in sub.findall(q("p")):
        sub.remove(p)
    for ti, segs in specs:
        np_ = copy.deepcopy(tpl[ti])
        set_para(np_, segs)
        sub.append(np_)
    return tpl


def fill_choice_row(p, marks, scripts, K):
    run = [r for r in p if ln(r) == "run"][0]
    tpl = copy.deepcopy(first_eq(run) if first_eq(run) is not None else G["eq"])
    for c in list(run):
        run.remove(c)
    prev_w = None
    for i, s in enumerate(scripts):
        t = etree.SubElement(run, q("t"))
        if i == 0:
            t.text = marks[i] + " "
        else:
            tab = etree.SubElement(t, q("tab"), width=str(max(K - prev_w, 200)), leader="0", type="1")
            tab.tail = marks[i] + " "
        e, w = mk_eq(tpl, s)
        run.append(e)
        prev_w = w
    etree.SubElement(run, q("t"))
    strip_lineseg(p)


MARKS = "①②③④⑤"


def choices(ps, idxs, scripts, rows=None):
    """idxs: 선택지 문단 인덱스(1개=한 줄 5개, 2개=3+2, 3개=2+2+1). K: 한 줄 5개 4684, 3+2줄 8848, 2줄씩 14032."""
    if len(idxs) == 1:
        fill_choice_row(ps[idxs[0]], MARKS, scripts, 4684)
    else:
        rows = rows or ([3, 2] if len(idxs) == 2 else [2, 2, 1])
        K = 8848 if rows == [3, 2] else 14032
        n = 0
        for idx, r in zip(idxs, rows):
            fill_choice_row(ps[idx], MARKS[n:n + r], scripts[n:n + r], K)
            n += r


def number_mark(p, n, keep_endnote=False):
    """문제 번호: 미주(해설) 대신 같은 글꼴의 일반 글자 'n.'로."""
    if keep_endnote:
        return
    run0 = [r for r in p if ln(r) == "run"][0]
    assert has_endnote(run0)
    for c in list(run0):
        run0.remove(c)
    t = etree.SubElement(run0, q("t")); t.text = "%d." % n


def is_blank(p):
    if p.get("paraPrIDRef") != "4":
        return False
    for x in p.iter():
        n = ln(x)
        if n in ("equation", "pic", "tbl", "ctrl", "rect", "line") or (n == "t" and (x.text or "").strip()):
            return False
    return True


def T(s): return ("t", s)
def E(s): return ("e", s)


def load_content(fname, *expected):
    """내용 파일(content_*.py)을 이 파일의 전역에 불러온다. 이 파일의 도구(q, T, E, set_para …)를 그대로 쓰기 때문에
    import 대신 exec 를 쓴다. 불러온 뒤 꼭 있어야 하는 이름이 빠졌으면 바로 알려 준다."""
    exec(open(os.path.join(W, fname), encoding="utf-8-sig").read(), globals())
    missing = [n for n in expected if n not in globals()]
    if missing:
        raise SystemExit("%s 에 필요한 이름이 없습니다: %s" % (fname, ", ".join(missing)))


def main():
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    shutil.copytree(SRC, OUT_DIR)
    path = os.path.join(OUT_DIR, "Contents", "section0.xml")
    tree = etree.parse(path)
    sec = tree.getroot()
    ps = [c for c in sec if ln(c) == "p"]
    G["eq"] = copy.deepcopy(ps[3].findall(q("run"))[1].find(q("equation")))
    load_content("content_q.py", "apply_questions")
    apply_questions(ps)
    load_content("content_sol.py", "apply_solutions", "fix_footer", "BLOCKS", "LAST_IN_COL",
                 "PAGE_FIRST", "COL2_FIRST", "END_IDX")
    global END_IDX_ORIG
    END_IDX_ORIG = END_IDX
    if KEY:
        apply_solutions(ps)          # 미주(해설) + 정답표
    fix_footer(ps[0], KEY)           # 바닥글의 총 쪽수

    # ---- 쪽/단 나눔과 빈 문단 정리 ----
    blocks = BLOCKS  # [(이름, 시작인덱스)] 순서대로, 마지막은 END
    starts = [b[1] for b in blocks]
    END = len(ps) if KEY else END_IDX    # 해설 포함이면 문서 끝까지 유지
    last_in_col = LAST_IN_COL      # 단의 마지막 블록 이름
    page_first = PAGE_FIRST        # 쪽 첫 블록
    col2_first = COL2_FIRST        # 2단 첫 블록
    for k, (name, st) in enumerate(blocks):
        en = starts[k + 1] if k + 1 < len(blocks) else END
        if name in last_in_col:
            for i in range(en - 1, st, -1):
                if i < len(ps) and is_blank(ps[i]) and ps[i].getparent() is not None:
                    sec.remove(ps[i])
                else:
                    break
        if name in page_first:
            ps[st].set("pageBreak", "1")
        if name in col2_first:
            ps[st].set("columnBreak", "1")
    for p in ps[END:]:
        if p.getparent() is not None:
            sec.remove(p)
    for p in sec:
        strip_lineseg(p)
    tree.write(path, xml_declaration=True, encoding="UTF-8", standalone=True)
    post_package()


def cleanup_bindata():
    """문서에서 참조하지 않는 그림 파일(원본 양식의 옛 그림)을 파일과 목록에서 모두 지운다."""
    sec_xml = open(os.path.join(OUT_DIR, "Contents", "section0.xml"), encoding="utf-8").read()
    used = set(re.findall(r'binaryItemIDRef="([^"]+)"', sec_xml))
    hdr = open(os.path.join(OUT_DIR, "Contents", "header.xml"), encoding="utf-8").read()
    used |= set(re.findall(r'binaryItemIDRef="([^"]+)"', hdr))
    hpf = os.path.join(OUT_DIR, "Contents", "content.hpf")
    t = etree.parse(hpf)
    OPF = "http://www.idpf.org/2007/opf/"
    for it in list(t.getroot().iter("{%s}item" % OPF)):
        href = it.get("href", "")
        if href.startswith("BinData/") and it.get("id") not in used:
            fp = os.path.join(OUT_DIR, href.replace("/", os.sep))
            if os.path.exists(fp):
                os.remove(fp)
            it.getparent().remove(it)
    t.write(hpf, xml_declaration=True, encoding="UTF-8", standalone=True)


def post_package():
    cleanup_bindata()
    TMP = OUT + ".tmp"       # 임시 파일에 먼저 완성한 뒤 교체 (중간에 실패해도 기존 파일이 남음)
    with zipfile.ZipFile(TMP, "w") as zf:
        zf.write(os.path.join(OUT_DIR, "mimetype"), "mimetype", compress_type=zipfile.ZIP_STORED)
        for d, _, fs in os.walk(OUT_DIR):
            for f in fs:
                fp = os.path.join(d, f)
                arc = os.path.relpath(fp, OUT_DIR).replace("\\", "/")
                if arc != "mimetype":
                    zf.write(fp, arc, compress_type=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(TMP) as zf:
        assert zf.testzip() is None
        etree.parse(zf.open("Contents/section0.xml"))
    os.replace(TMP, OUT)
    missing = sorted(set(s for s in NEEDED if s not in SIZES))
    if missing:
        print("경고: 한글로 측정하지 않은 수식 %d개(추정 크기 사용). sizes.py 실행 후 다시 빌드하세요. 예: %r"
              % (len(missing), missing[0][:40]))
    json.dump(sorted(set(NEEDED)), open(os.path.join(W, "scripts.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("built", OUT, os.path.getsize(OUT), "equations:", len(set(NEEDED)))


main()
