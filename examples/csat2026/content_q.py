# 문항별 내용. build_exam.py 에서 exec 된다 (set_para, choices, number_mark, T, E, G, ln, q 사용 가능)

BLOCKS = [("Q1", 3), ("Q2", 23), ("Q3", 49), ("Q4", 70), ("Q5", 96), ("Q6", 118), ("Q7", 147),
          ("Q8", 188), ("Q9", 210), ("Q10", 238), ("Q11", 286), ("Q12", 331), ("Q13", 382),
          ("Q14", 432), ("Q15", 467), ("단답", 513), ("Q16", 515), ("Q17", 538), ("Q18", 564),
          ("Q19", 587), ("Q20", 614), ("Q21", 642), ("Q22", 686),
          ]
if TRACK == "calc":   # 미적분 양식의 선택과목 구간
    BLOCKS += [("선택헤더", 714), ("Q23", 717), ("Q24", 764), ("Q25", 812), ("Q26", 862), ("Q27", 903),
               ("Q28", 953), ("단답2", 998), ("Q29", 1000), ("Q30", 1043), ("확인", 1080)]
    END_IDX = 1081
    SEL_STEMS = {717: 23, 764: 24, 812: 25, 862: 26, 903: 27, 953: 28, 1000: 29, 1043: 30}
    PAGE_FIRST_SEL = {"선택헤더", "Q25", "Q27", "단답2"}
    COL2_FIRST_SEL = {"Q24", "Q26", "Q28", "Q30", "단답2_NONE"}
elif TRACK == "prob":  # 확률과 통계 양식의 선택과목 구간
    BLOCKS += [("선택헤더", 719), ("Q23", 722), ("Q24", 769), ("Q25", 817), ("Q26", 858), ("Q27", 907),
               ("Q28", 957), ("Q29", 997), ("Q30", 1039), ("확인", 1079)]
    END_IDX = 1080
    SEL_STEMS = {722: 23, 769: 24, 817: 25, 858: 26, 907: 27, 957: 28, 997: 29, 1039: 30}
    PAGE_FIRST_SEL = {"선택헤더", "Q25", "Q27", "Q29"}
    COL2_FIRST_SEL = {"Q24", "Q26", "Q28", "Q30"}
else:                  # 기하 양식의 선택과목 구간
    BLOCKS += [("선택헤더", 708), ("Q23", 711), ("Q24", 758), ("Q25", 808), ("Q26", 858), ("Q27", 907),
               ("Q28", 945), ("Q29", 980), ("Q30", 1018), ("확인", 1060)]
    END_IDX = 1061
    SEL_STEMS = {711: 23, 758: 24, 808: 25, 858: 26, 907: 27, 945: 28, 980: 29, 1018: 30}
    PAGE_FIRST_SEL = {"선택헤더", "Q25", "Q27", "Q29"}
    COL2_FIRST_SEL = {"Q24", "Q26", "Q28", "Q30"}
LAST_IN_COL = {"Q2", "Q4", "Q6", "Q7", "Q9", "Q10", "Q11", "Q12", "Q13", "Q14", "Q15", "Q17",
               "Q19", "Q20", "Q21", "Q22", "Q23", "Q24", "Q25", "Q26", "Q27", "Q28", "Q29", "확인"}
PAGE_FIRST = {"Q5", "Q8", "Q11", "Q13", "Q15", "Q18", "Q21"} | PAGE_FIRST_SEL
COL2_FIRST = {"Q3", "Q7", "Q10", "Q12", "Q14", "단답", "Q20", "Q22"} | COL2_FIRST_SEL

TAB = ("tab", 4000, "")
TAB2 = ("tab", 4000, "", 2)

STEMS = {3: 1, 23: 2, 49: 3, 70: 4, 96: 5, 118: 6, 147: 7, 188: 8, 210: 9, 238: 10, 286: 11,
         331: 12, 382: 13, 432: 14, 467: 15, 515: 16, 538: 17, 564: 18, 587: 19, 614: 20,
         642: 21, 686: 22}
STEMS.update(SEL_STEMS)


def stem(ps, idx, segs):
    set_para(ps[idx], segs)


def setattrs(el, **kw):
    for k, v in kw.items():
        el.set(k, v)


def put_figure(p, png, w_in, h_in):
    """문단 p 안의 그림을 새 PNG(RGB)로 교체. 표시 크기는 inch(w_in x h_in).
    원본 그림이 bmp 등 다른 형식이면 목록(content.hpf)의 형식도 png로 바꾼다."""
    from PIL import Image
    src = os.path.join(W, "figures", png)
    HC = "http://www.hancom.co.kr/hwpml/2011/core"
    pic = next(p.iter(q("pic")))
    img = pic.find("{%s}img" % HC)
    bid = img.get("binaryItemIDRef")
    hpf = os.path.join(OUT_DIR, "Contents", "content.hpf")
    ht = etree.parse(hpf)
    OPF = "http://www.idpf.org/2007/opf/"
    for it in ht.getroot().iter("{%s}item" % OPF):
        if it.get("id") == bid:
            oldp = os.path.join(OUT_DIR, it.get("href").replace("/", os.sep))
            if os.path.exists(oldp):
                os.remove(oldp)
            it.set("href", "BinData/%s.png" % bid); it.set("media-type", "image/png")
    ht.write(hpf, xml_declaration=True, encoding="UTF-8", standalone=True)
    shutil.copyfile(src, os.path.join(OUT_DIR, "BinData", bid + ".png"))
    pxw, pxh = Image.open(src).size
    ow, oh = pxw * 75, pxh * 75                    # 원본 그림과 같은 기준: 1px = 75 HWPUNIT(96dpi)
    cw, ch = int(round(w_in * 7200)), int(round(h_in * 7200))
    setattrs(pic.find(q("orgSz")), width=str(ow), height=str(oh))
    setattrs(pic.find(q("curSz")), width=str(cw), height=str(ch))
    setattrs(pic.find(q("rotationInfo")), centerX=str(cw // 2), centerY=str(ch // 2))
    for sm in pic.find(q("renderingInfo")).findall("{%s}scaMatrix" % HC):
        if sm.get("e1") != "1":
            sm.set("e1", repr(cw / ow)); sm.set("e5", repr(ch / oh))
    pts = pic.find(q("imgRect"))
    for k, (x, y) in enumerate([(0, 0), (ow, 0), (ow, oh), (0, oh)]):
        pt = pts.find("{%s}pt%d" % (HC, k)); pt.set("x", str(x)); pt.set("y", str(y))
    setattrs(pic.find(q("imgClip")), left="0", top="0", right=str(ow), bottom=str(oh))
    setattrs(pic.find(q("sz")), width=str(cw), height=str(ch))
    for c in pic.findall(q("shapeComment")):
        pic.remove(c)
    strip_lineseg(p)


def apply_questions(ps):
    # ---------- 1 ~ 4 ----------
    stem(ps, 3, [T(" "), E("16 ^{ { 3} over { 4} }times2 ^{ -2}`"), T("의 값은? [2점]")])
    choices(ps, [4], ["1`", "2`", "4`", "8`", "16"])

    stem(ps, 23, [T(" 함수 "), E("f LEFT ( x RIGHT )=x ^{ 3} -2x ^{ 2} +5`"), T("에 대하여 "),
                  E("lim _{h`` rarrow ``0} {{f LEFT ( 2+h RIGHT )-f LEFT ( 2 RIGHT )} over {h}}`"), T("의 값은?")])
    choices(ps, [25], ["2`", "3`", "4`", "5`", "6"])

    stem(ps, 49, [T(" 수열 "), E("LEFT { a _{n} RIGHT }`"), T("에 대하여 "),
                  E("sum _{k=1} ^{5} LEFT ( 3a _{k} -k RIGHT )=39`"), T("일 때, "),
                  E("sum _{k=1} ^{5} a _{k}`"), T("의 값은?")])
    choices(ps, [51], ["12`", "14`", "16`", "18`", "20"])

    stem(ps, 70, [T(" 함수")])
    set_para(ps[71], [TAB, E("f left(x right)= cases {``x^{2}+ax & & left(x < 1 right) #``4x-1 & & left(x ge 1 right)}`")])
    choices(ps, [73], ["1`", "2`", "3`", "4`", "5"])

    # ---------- 5 ----------
    stem(ps, 96, [T(" 함수 "), E("f left(x right)= left(x^{2}+1 right) left(2x-3 right)"), T("에 대하여 "),
                  E("f`' left(2 right)`"), T("의 값은? [3점]")])
    choices(ps, [97], ["14`", "15`", "16`", "17`", "18"])

    # ---------- 6 ----------
    stem(ps, 118, [T(" "), E("1`"), T("보다 큰 두 실수 "), E("a`"), T(", "), E("b`"), T("가")])
    set_para(ps[119], [TAB2, E("log`_{a}`b=2`"), T(", "), E("log`_{2}`ab=3`")])
    set_para(ps[120], [T("을 만족시킬 때, "), E("log`_{8}`ab^{2}`"), T("의 값은? [3점]")])
    choices(ps, [121], ["1`", "{4} over {3}`", "{5} over {3}`", "2`", "{7} over {3}"])

    # ---------- 7 (그림) ----------
    stem(ps, 147, [T(" 그림과 같이 두 곡선 "), E("y=x^{2}-2x`"), T(", "), E("y=-x^{2}+4x`"),
                   T("로 둘러싸인 부분의 넓이는? [3점]")])
    choices(ps, [148], ["5`", "6`", "7`", "8`", "9"])

    # ---------- 8 ----------
    stem(ps, 188, [T(" "), E("sin` theta -2 cos` theta =0`"), T("이고 "),
                   E("sin` left( pi + theta right) > 0`"), T("일 때, "), E("cos` theta`"), T("의 값은? [3점]")])
    choices(ps, [189, 190], ["{2 sqrt{5}} over {5}`", "{ sqrt{5}} over {5}`", "0`",
                              "-{ sqrt{5}} over {5}`", "-{2 sqrt{5}} over {5}"])

    # ---------- 9 ----------
    stem(ps, 210, [T(" 양수 "), E("a`"), T("에 대하여 함수 "), E("f left(x right)`"), T("를")])
    set_para(ps[211], [TAB, E("f left(x right)=x^{3}-6ax^{2}+9a^{2}x+2`")])
    set_para(ps[212], [T("라 하자. 직선 "), E("y=6`"), T("이 곡선 "), E("y=f left(x right)`"),
                       T("에 접할 때, "), E("f left(6 right)`"), T("의 값은?")])
    choices(ps, [214], ["50`", "56`", "58`", "60`", "62"])

    # ---------- 10 ----------
    stem(ps, 238, [T(" 상수 "), E("a~ left(a > 1 right)`"), T("에 대하여 곡선 "), E("y=a^{x}-1`"),
                   T(" 위의 제"), E("1`"), T("사분면에 있는 점 "), E("{rm{P}it}`"), T("를 지나고 "), E("y`"),
                   T("축에 평행한 직선이 "), E("x`"), T("축과 만나는 점을 "), E("{rm{Q}it}`"),
                   T(", 곡선 "), E("y=a^{x}-1`"), T("의 점근선과 만나는 점을 "), E("{rm{R}it}`"),
                   T("이라 하자. "), E("{ bar{rm{PQ}it}}={ bar{rm{QR}it}}`"), T("이고 삼각형 "),
                   E("{rm{OPR}it}`"), T("의 넓이가 "), E("4`"), T("일 때, "), E("a^{11}`"),
                   T("의 값은? (단, "), E("{rm{O}it}`"), T("는 원점이다.) [4점]")])
    choices(ps, [239], ["2^{{11} over {4}}`", "2^{3}`", "2^{{13} over {4}}`", "2^{{7} over {2}}`",
                        "2^{{15} over {4}}"])

    # ---------- 11 (보기) ----------
    stem(ps, 286, [T(" 수직선 위를 움직이는 점 "), E("{rm{P}it}`"), T("가 시각 "), E("t=0`"),
                   T("일 때 원점을 출발한다. 실수 "), E("k`"), T("에 대하여 시각 "),
                   E("t~ left(t ge 0 right)`"), T("에서의 점 "), E("{rm{P}it}`"), T("의 속도 "),
                   E("v left(t right)`"), T("가")])
    set_para(ps[287], [TAB, E("v left(t right)=t^{2}-6t+k`")])
    tbl = ps[289].find(".//" + q("tbl"))
    cell = list(tbl.iter(q("tc")))[5]
    cps = {}
    for cp in cell.iter(q("p")):
        tx = "".join(x.text or "" for x in cp.iter(q("t"))).strip()
        for key in "ㄱㄴㄷ":
            if tx.startswith(key + "."):
                cps[key] = cp
    assert set(cps) == set("ㄱㄴㄷ"), cps.keys()
    set_para(cps["ㄱ"], [T("ㄱ. "), E("k=5`"), T("이면, 시각 "), E("t=1`"), T("일 때 점 "), E("{rm{P}it}`"),
                        T("의 위치는 "), E("{7} over {3}`"), T("이다.")])
    set_para(cps["ㄴ"], [T("ㄴ. "), E("k=8`"), T("이면, 출발한 후 점 "), E("{rm{P}it}`"),
                        T("의 운동 방향이 한 번 바뀐다.")])
    set_para(cps["ㄷ"], [T("ㄷ. "), E("k=5`"), T("이면, 시각 "), E("t=0`"), T("부터 "), E("t=5`"),
                        T("까지 점 "), E("{rm{P}it}`"), T("가 움직인 거리는 "), E("13`"), T("이다.")])

    # ---------- 12 ----------
    stem(ps, 331, [T(" 모든 항이 양수인 등비수열 "), E("left {a_{n} right }`"), T("이")])
    set_para(ps[332], [TAB, E("a_{2}a_{4}=16`"), T(", "), E("a_{3}+a_{5}=20`")])
    set_para(ps[333], [T("을 만족시킬 때, "), E("a_{6}`"), T("의 값은? [4점]")])
    choices(ps, [334], ["16`", "20`", "24`", "28`", "32"])

    # ---------- 13 ----------
    stem(ps, 382, [T(" 함수 "), E("f left(x right)=x^{2}-3x+1`"), T("에 대하여 곡선 "),
                   E("y=f left(x right)`"), T(" 위의 점 "), E("left(1,``-1 right)`"), T("에서의 접선을 "),
                   E("l`"), T("이라 하고, 함수 "), E("g left(x right)= left(x^{2}+2 right)f left(x right)`"),
                   T("에 대하여 곡선 "), E("y=g left(x right)`"), T(" 위의 점 "),
                   E("left(1,``g left(1 right) right)`"), T("에서의 접선을 "), E("m`"), T("이라 하자. 두 직선 "),
                   E("l`"), T(", "), E("m`"), T("과 "), E("y`"), T("축으로 둘러싸인 삼각형의 넓이를 "),
                   E("S`"), T("라 할 때, "), E("16S`"), T("의 값은? [4점]")])
    choices(ps, [383], ["4`", "6`", "8`", "10`", "12"])

    # ---------- 14 (그림) ----------
    stem(ps, 432, [T(" 그림과 같이 "), E("{ bar{rm{AB}it}}=4`"), T(", "), E("{ bar{rm{AC}it}}=6`"),
                   T("이고 "), E("cos` left( angle{rm{BAC}it} right)={1} over {4}`"), T("인 삼각형 "),
                   E("{rm{ABC}it}`"), T("가 있다. "), E("angle{rm{BAC}it}`"), T("의 이등분선이 선분 "),
                   E("{rm{BC}it}`"), T("와 만나는 점을 "), E("{rm{D}it}`"), T("라 할 때, 선분 "),
                   E("{rm{AD}it}`"), T("의 길이는? [4점]")])
    choices(ps, [434, 435], ["sqrt{10}`", "{6 sqrt{10}} over {5}`", "{7 sqrt{10}} over {5}`",
                              "{8 sqrt{10}} over {5}`", "{9 sqrt{10}} over {5}"])

    # ---------- 15 ----------
    stem(ps, 467, [T(" 상수 "), E("k`"), T("에 대하여 함수")])
    set_para(ps[468], [TAB, E("f left(x right)=x^{3}-6x^{2}+9x+k`")])
    set_para(ps[469], [T("라 하자. 실수 "), E("t`"), T("에 대하여 직선 "), E("y=t`"), T("가 곡선 "),
                       E("y=f left(x right)`"), T("와 만나는 점의 개수를 "), E("g left(t right)`"), T("라 하자.")])
    sec_el = ps[470].getparent()
    sec_el.remove(ps[470])
    set_para(ps[471], [T(" 함수 "), E("g left(t right)`"), T("가 "), E("t=a`"), T("에서 불연속인 모든 실수 "),
                       E("a`"), T("의 값의 합이 "), E("10`"), T("일 때, "), E("f left(4 right)`"),
                       T("의 값은? [4점]")])
    choices(ps, [472], ["5`", "7`", "8`", "9`", "10"])

    # ---------- 16 ----------
    stem(ps, 515, [T(" 수열 "), E("left {a_{n} right }`"), T("은 "), E("a_{1}=2`"), T("이고, 모든 자연수 "),
                   E("n`"), T("에 대하여")])
    set_para(ps[516], [TAB, E("a_{n+1}=2a_{n}+n`")])
    set_para(ps[517], [T("을 만족시킨다. "), E("a_{4}`"), T("의 값을 구하시오. [3점]")])

    # ---------- 17 ----------
    stem(ps, 538, [T(" 함수 "), E("f left(x right)=6x^{2}-2x`"), T("의 한 부정적분 "), E("F` left(x right)`"),
                   T("에 대하여 "), E("F` left(0 right)=3`"), T("일 때, "), E("F` left(2 right)`"),
                   T("의 값을 구하시오. [3점]")])

    # ---------- 18 ----------
    stem(ps, 564, [T(" "), E("{ bar{rm{AB}it}}=5`"), T(", "), E("{ bar{rm{AC}it}}=7`"), T("이고 "),
                   E("cos` left( angle{rm{BAC}it} right)={3} over {5}`"), T("인 삼각형 "),
                   E("{rm{ABC}it}`"), T("의 넓이를 구하시오. [3점]")])

    # ---------- 19 ----------
    stem(ps, 587, [T(" "), E("-1 le x le 4`"), T("인 모든 실수 "), E("x`"), T("에 대하여 부등식")])
    set_para(ps[588], [TAB, E("-k le x^{3}-6x^{2}+9x-2 le k`")])
    set_para(ps[589], [T("가 성립하도록 하는 양수 "), E("k`"), T("의 최솟값을 구하시오. [3점]")])

    # ---------- 20~22 : 별도 파일(content_q20_22.py)이 있으면 적용 ----------
    p20 = os.path.join(W, "content_q20_22.py")
    if os.path.exists(p20):
        exec(open(p20, encoding="utf-8-sig").read(), globals())
        apply_q20_22(ps)

    # ---------- 그림 교체 (7번, 14번) ----------
    meta = json.load(open(os.path.join(W, "figures", "meta.json"), encoding="utf-8"))
    put_figure(ps[149], "q07_graph.png", *meta["q07_graph.png"])
    put_figure(ps[433], "q14_triangle.png", *meta["q14_triangle.png"])

    # ---------- 선택과목 23~30 (출제 데이터가 있으면 적용) ----------
    psel = os.path.join(W, {"calc": "content_sel.py", "prob": "content_sel_prob.py", "geo": "content_sel_geo.py"}[TRACK])
    pdata = os.path.join(W, {"calc": "data_q23_30.py", "prob": "data_p23_30.py", "geo": "data_g23_30.py"}[TRACK])
    if os.path.exists(psel) and os.path.exists(pdata):
        exec(open(psel, encoding="utf-8-sig").read(), globals())
        apply_sel(ps)

    # ---------- 문제 번호 ----------
    for idx, n in STEMS.items():
        if not KEY:
            number_mark(ps[idx], n)
