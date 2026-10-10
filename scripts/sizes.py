"""scripts.json 의 수식을 한글에게 직접 만들게 해서 (가로, 세로, 기준선)을 sizes.json 에 저장한다."""
import win32com.client as w, json, os, zipfile
from lxml import etree

W = (os.environ.get("EXAM_WORK") or (os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()))
HP = "http://www.hancom.co.kr/hwpml/2011/paragraph"
need = json.load(open(os.path.join(W, "scripts.json"), encoding="utf-8"))
sp = os.path.join(W, "sizes.json")
known = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
# 기준선까지 포함된 값이 이미 있으면(길이 4) 건너뛴다
todo = [s for s in need if s not in known or len(known[s]) < 4]
tmp = os.path.join(W, "_measure.hwpx")

if todo:
    hwp = w.gencache.EnsureDispatch("HWPFrame.HwpObject")
    try:
        try:
            hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
        except Exception:
            pass
        for s in todo:
            ps = hwp.HParameterSet.HEqEdit
            hwp.HAction.GetDefault("EquationCreate", ps.HSet)
            ps.HSet.SetItem("String", s); ps.HSet.SetItem("BaseUnit", 1100)
            ps.HSet.SetItem("EqFontName", "HYhwpEQ")
            hwp.HAction.Execute("EquationCreate", ps.HSet)
            hwp.HAction.Run("BreakPara")  # 수식마다 새 문단(저장본에서 순서 대응이 쉽도록)
        if os.path.exists(tmp):
            os.remove(tmp)
        hwp.SaveAs(tmp, "HWPX", "")
    finally:
        hwp.Quit()
    with zipfile.ZipFile(tmp) as zf:
        root = etree.parse(zf.open("Contents/section0.xml")).getroot()
    eqs = list(root.iter("{%s}equation" % HP))
    assert len(eqs) == len(todo), (len(eqs), len(todo))
    new = {}
    bad = []
    for s, e in zip(todo, eqs):
        got = e.find("{%s}script" % HP).text or ""
        if got.strip() != s.strip():
            bad.append((s, got))
            continue
        sz = e.find("{%s}sz" % HP)
        new[s] = [int(sz.get("width")), int(sz.get("height")), int(e.get("baseLine")), 1]
    if bad:   # 순서가 어긋났을 수 있으므로 아무것도 저장하지 않고 중단
        for s, got in bad[:5]:
            print("스크립트 불일치:", repr(s)[:50], "->", repr(got)[:50])
        raise SystemExit("수식 %d개가 요청과 달라 sizes.json 을 저장하지 않았습니다." % len(bad))
    known.update(new)
    json.dump(known, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("measured", len(todo), "total", len(known))
