# 기하 선택과목 23~30번. content_q.py 의 apply_questions 에서 exec 된다.

FIG_SIZES = {27: (1.95, 2.56), 28: (2.8, 2.8), 29: (2.8, 2.7)}


def _fig(n, fig):
    """fig = {"kind": "solid3d"|"plane2d", "spec": {...}} 또는 {"kind": "png"} (이미 그려 둔 figures\\g<번호>.png 사용)
    -> (png 파일명, w_in, h_in)"""
    w_in, h_in = FIG_SIZES[n]
    name = "g%d.png" % n
    if fig["kind"] == "png":
        return name, w_in, h_in
    ns = {}
    exec(open(os.path.join(W, "figlib.py"), encoding="utf-8").read(), ns)
    fn = ns["draw_solid3d"] if fig["kind"] == "solid3d" else ns["draw_plane2d"]
    fn(fig["spec"], name, w_in, h_in)
    return name, w_in, h_in


def _drop(p):
    p.getparent().remove(p)


def apply_sel(ps):
    ns = {}
    src = open(os.path.join(W, "data_g23_30.py"), encoding="utf-8-sig").read()
    src = src.replace("neq", "ne")
    exec(src, ns)
    QG = ns["QG"]

    # 23 ~ 26 : 한 문단 문제 + 선택지 한 줄
    for n, si, ci in ((23, 711, 712), (24, 758, 759), (25, 808, 809), (26, 858, 859)):
        stem(ps, si, QG[n]["stem"])
        choices(ps, [ci], QG[n]["choices"])

    # 27 : 문제 / 그림 / 선택지 3+2줄
    d = QG[27]
    stem(ps, 907, d["stem"])
    if d.get("fig"):
        png, w_in, h_in = _fig(27, d["fig"])
        put_figure(ps[908], png, w_in, h_in)
    else:
        _drop(ps[908])
    choices(ps, [909, 910], d["choices"])

    # 28 : 문제 / 그림 / 선택지 한 줄
    d = QG[28]
    stem(ps, 945, d["stem"])
    if d.get("fig"):
        png, w_in, h_in = _fig(28, d["fig"])
        put_figure(ps[946], png, w_in, h_in)
    else:
        _drop(ps[946])
    choices(ps, [947], d["choices"])

    # 29 : 단답형, 문제 / 그림
    d = QG[29]
    stem(ps, 980, d["stem"])
    if d.get("fig"):
        png, w_in, h_in = _fig(29, d["fig"])
        put_figure(ps[981], png, w_in, h_in)
    else:
        _drop(ps[981])

    # 30 : 단답형, 문제 / 가운데 수식 / 이어지는 글
    d = QG[30]
    stem(ps, 1018, d["stem"])
    set_para(ps[1019], d["center"])
    set_para(ps[1020], d["tail"])
