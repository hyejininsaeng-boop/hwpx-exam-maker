"""완성된 '문제+해설' hwpx 에서 선택과목 23~30번 데이터를 data_p23_30.py / data_g23_30.py 로 복원한다.
사용: python -X utf8 -I extract_sel.py prob|geo"""
import sys, os, zipfile, re, shutil
from lxml import etree

HP = "http://www.hancom.co.kr/hwpml/2011/paragraph"
HC = "http://www.hancom.co.kr/hwpml/2011/core"
W = (os.environ.get("EXAM_WORK") or (os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()))
EXAM_DIR = os.environ.get("EXAM_DIR") or os.path.dirname(W)
q = lambda n: "{%s}%s" % (HP, n)
ln = lambda e: etree.QName(e.tag).localname

track = sys.argv[1]
SRCF = {"prob": os.path.join(EXAM_DIR, "수능스타일_확통_문제+해설.hwpx"),
        "geo": os.path.join(EXAM_DIR, "수능스타일_기하_문제+해설.hwpx")}[track]
z = zipfile.ZipFile(SRCF)
root = etree.parse(z.open("Contents/section0.xml")).getroot()
ps = [c for c in root if ln(c) == "p"]


def has_endnote(run):
    return any(ln(x) == "endNote" for x in run.iter())


def segs_of(p):
    """문단의 (미주 없는) 첫 run 내용을 [('t',글자)|('e',수식)|('tab',폭,뒤글자)] 로."""
    runs = [r for r in p if ln(r) == "run"]
    target = next(r for r in runs if not has_endnote(r))
    out = []
    for c in target:
        n = ln(c)
        if n == "t":
            tabs = [x for x in c if ln(x) == "tab"]
            if c.text:
                out.append(("t", c.text))
            for tb in tabs:
                out.append(("tab", int(tb.get("width")), tb.tail or ""))
        elif n == "equation":
            out.append(("e", c.find(q("script")).text or ""))
    return out


def eqs_of(p):
    return [s[1] for s in segs_of(p) if s[0] == "e"]


def text_of(p):
    return "".join(x.text or "" for x in p.iter(q("t")))


def kind_of(p):
    if any(True for _ in p.iter(q("pic"))):
        return "pic"
    if any(True for _ in p.iter(q("tbl"))):
        return "tbl"
    return "txt"


def src_segs(segs):
    parts = []
    for s in segs:
        if s[0] == "t":
            parts.append("T(%r)" % s[1])
        elif s[0] == "e":
            parts.append("E(%r)" % s[1])
        else:
            parts.append("TAB" if (s[1] == 4000 and s[2] == "") else "(%r, %d, %r)" % ("tab", s[1], s[2]))
    return "[" + ", ".join(parts) + "]"


# 줄기 문단(미주가 있는 문단) 위치
stems = [i for i, p in enumerate(ps) if any(has_endnote(r) for r in p if ln(r) == "run")]
assert len(stems) == 30, len(stems)
sel = stems[22:]      # 23~30번
end_i = len(ps)
data = {}
for k, n in enumerate(range(23, 31)):
    si = sel[k]
    nxt = sel[k + 1] if k + 1 < 8 else end_i
    foll = []
    for p in ps[si + 1:nxt]:
        if kind_of(p) == "txt" and not text_of(p).strip() and not eqs_of(p):
            continue
        foll.append(p)
    if n == 30:
        foll = foll[:2] if track == "geo" else foll[:1]   # 뒤의 확인 사항 상자 등은 제외
    d = {"stem": segs_of(ps[si])}
    # 정답/해설(미주)
    en = next(ps[si].iter(q("endNote"))).find(q("subList"))
    eps = en.findall(q("p"))
    ans = text_of(eps[0]).strip()
    d["ans"] = int(ans) if (ans.isascii() and ans.isdigit()) else ans
    d["sol"] = [segs_of(p) for p in eps[1:] if segs_of(p)]
    d["_foll"] = foll
    data[n] = d

out = []
out.append("# %s 23~30번 (완성된 문제+해설 hwpx 에서 복원한 데이터)" % ("확률과 통계" if track == "prob" else "기하"))
out.append("def T(s): return (\"t\", s)")
out.append("def E(s): return (\"e\", s)")
out.append("TAB = (\"tab\", 4000, \"\")")
out.append("")
name = "QP" if track == "prob" else "QG"
out.append("%s = {}" % name)


def emit(n, d):
    L = ["%s[%d] = {" % (name, n)]
    for key in ("stem", "center", "tail", "box", "choices", "fig"):
        if key not in d:
            continue
        v = d[key]
        if key in ("stem", "center", "tail"):
            L.append("    %r: %s," % (key, src_segs(v)))
        elif key == "box":
            L.append("    'box': [%s]," % ", ".join(src_segs(b) for b in v))
        elif key == "choices":
            L.append("    'choices': %r," % (v,))
        elif key == "fig":
            L.append("    'fig': %r," % (v,))
    L.append("    'ans': %r," % (d["ans"],))
    L.append("    'sol': [")
    for s in d["sol"]:
        L.append("        %s," % src_segs(s))
    L.append("    ],")
    L.append("}")
    return "\n".join(L)


def tbl_lines(p):
    t = next(p.iter(q("tbl")))
    cell = list(t.iter(q("tc")))[0]
    return [segs_of(cp) for cp in cell.find(q("subList")).findall(q("p"))]


def pic_png(p, outname):
    pic = next(p.iter(q("pic")))
    bid = pic.find("{%s}img" % HC).get("binaryItemIDRef")
    for nm in z.namelist():
        if nm.startswith("BinData/%s." % bid):
            os.makedirs(os.path.join(W, "figures"), exist_ok=True)
            open(os.path.join(W, "figures", outname), "wb").write(z.read(nm))
            return
    raise RuntimeError(bid)


for n, d in data.items():
    f = d.pop("_foll")
    if track == "prob":
        if n == 23:
            d["choices"] = eqs_of(f[0])
        elif n in (24, 27):
            d["center"] = segs_of(f[0]); d["tail"] = segs_of(f[1]); d["choices"] = eqs_of(f[2])
        elif n == 25:
            d["choices"] = eqs_of(f[0]); d["fig"] = {"white": [1, 2, 3, 4], "black": [4, 5, 6]}
        elif n == 26:
            d["choices"] = eqs_of(f[0])
        elif n == 28:
            d["box"] = tbl_lines(f[0]); d["tail"] = segs_of(f[1])
            ch = [p for p in f if text_of(p).strip().startswith("①")][0]
            d["choices"] = eqs_of(ch); d["fig"] = {"balls": 8, "boxes": 3}
        elif n == 29:
            d["box"] = tbl_lines(f[0]); d["tail"] = segs_of(f[1])
        elif n == 30:
            d["box"] = tbl_lines(f[0])
    else:
        if n in (23, 24, 25, 26):
            d["choices"] = eqs_of(f[0])
        elif n == 27:
            pic_png(f[0], "g27.png"); d["fig"] = {"kind": "png"}
            d["choices"] = eqs_of(f[1]) + eqs_of(f[2])
        elif n == 28:
            pic_png(f[0], "g28.png"); d["fig"] = {"kind": "png"}
            d["choices"] = eqs_of(f[1])
        elif n == 29:
            pic_png(f[0], "g29.png"); d["fig"] = {"kind": "png"}
        elif n == 30:
            d["center"] = segs_of(f[0]); d["tail"] = segs_of(f[1])
    out.append("")
    out.append(emit(n, d))

fn = os.path.join(W, "data_p23_30.py" if track == "prob" else "data_g23_30.py")
if os.path.exists(fn):   # 빌드가 쓰는 데이터라 덮어쓰기 전에 백업 (이미 있는 백업은 지우지 않음)
    import time
    bak = "%s.%s.bak" % (fn, time.strftime("%Y%m%d_%H%M%S"))
    shutil.copyfile(fn, bak)
    print("백업:", bak)
open(fn, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("wrote", fn, os.path.getsize(fn))
