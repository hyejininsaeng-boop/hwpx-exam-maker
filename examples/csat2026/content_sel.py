# 선택과목(미적분) 23~30번. content_q.py 의 apply_questions 에서 exec 된다.


def draw_q26(fig):
    """26번: 곡선 아래 밑면 + x=c 에서의 수직 단면(정삼각형/정사각형/반원)을 사영도로 그린다. (png, 폭in, 높이in) 반환."""
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image
    plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "stix", "font.size": 8})
    LW = 0.7
    f = eval("lambda x: " + fig["expr"], {"np": np})
    a, b = float(fig["a"]), float(fig["b"])
    xs = np.linspace(a, b, 500)
    ys = f(xs)
    ymax = float(np.max(ys))
    span = b - a
    x0, x1 = min(0.0, a - 0.5 * span), b + 0.6 * span
    W_IN, H_IN = 3.1, 2.15
    y0, y1 = -0.2 * ymax, 1.85 * ymax
    X, Y = x1 - x0, y1 - y0
    kx, ky = X / W_IN, Y / H_IN          # 화면 1인치당 데이터 길이
    fg, ax = plt.subplots(figsize=(W_IN, H_IN), dpi=600)
    fg.subplots_adjust(0, 0, 1, 1)
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1); ax.axis("off")
    ax.fill_between(xs, 0, ys, color="0.86", lw=0)
    ax.plot(xs, ys, "k", lw=LW)
    for xv in (a, b):
        ax.plot([xv, xv], [0, float(f(xv))], "k", lw=LW)
    ar = dict(arrowstyle="-|>", lw=LW, color="k", mutation_scale=6, shrinkA=0, shrinkB=0)
    ax.annotate("", xy=(x1, 0), xytext=(x0, 0), arrowprops=ar)
    yaxis_x = 0.0 if x0 < 0 else x0
    ax.annotate("", xy=(yaxis_x, y1), xytext=(yaxis_x, 0), arrowprops=ar)
    ax.text(yaxis_x - 0.03 * X, -0.07 * Y, r"$\mathrm{O}$", ha="right", va="top")
    ax.text(x1 - 0.01 * X, -0.07 * Y, r"$x$", ha="right", va="top", style="italic")
    ax.text(yaxis_x + 0.03 * X, y1 - 0.01 * Y, r"$y$", ha="left", va="top", style="italic")

    def fmt(v):
        return ("%g" % v)
    ax.text(a, -0.07 * Y, r"$%s$" % fmt(a), ha="center", va="top")
    ax.text(b, -0.07 * Y, r"$%s$" % fmt(b), ha="center", va="top")
    if fig.get("label"):
        ax.text(b + 0.04 * X, float(f(b)), fig["label"], ha="left", va="center")

    # 단면 (x=c)
    c = a + 0.55 * span
    s = float(f(c))
    s_in = s / ky                                   # 단면 한 변의 화면 길이(인치)

    def P(L_in):                                   # 깊이 방향(화면 왼쪽 위)으로 L_in 인치 이동 -> 데이터 좌표
        return np.array([-0.55 * L_in * kx, 0.40 * L_in * ky])
    base0, base1 = np.array([c, 0.0]), np.array([c, s])
    kind = fig.get("section", "정삼각형")
    if kind == "정삼각형":
        apex = (base0 + base1) / 2 + P(np.sqrt(3) / 2 * s_in)
        poly = np.array([base0, base1, apex, base0])
        ax.plot(poly[:, 0], poly[:, 1], "k", lw=LW)
        ax.fill(poly[:, 0], poly[:, 1], color="0.72", lw=0, zorder=1)
    elif kind == "정사각형":
        poly = np.array([base0, base1, base1 + P(s_in), base0 + P(s_in), base0])
        ax.plot(poly[:, 0], poly[:, 1], "k", lw=LW)
        ax.fill(poly[:, 0], poly[:, 1], color="0.72", lw=0, zorder=1)
    else:  # 반원
        th = np.linspace(0, np.pi, 100)
        m = (base0 + base1) / 2
        pts = np.array([m + (s / 2) * np.cos(t) * np.array([0, 1.0]) + (s_in / 2) * np.sin(t) * P(1.0) / 1.0
                        for t in th])
        ax.plot(pts[:, 0], pts[:, 1], "k", lw=LW)
        ax.plot([base0[0], base1[0]], [base0[1], base1[1]], "k", lw=LW)
        ax.fill(pts[:, 0], pts[:, 1], color="0.72", lw=0, zorder=1)
    out = os.path.join(W, "figures", "q26_solid.png")
    fg.savefig(out, dpi=600, facecolor="white")
    plt.close(fg)
    Image.open(out).convert("RGB").save(out)
    return "q26_solid.png", W_IN, H_IN


def apply_sel(ps):
    ns = {}
    src = open(os.path.join(W, "data_q23_30.py"), encoding="utf-8-sig").read()
    # 한글 수식 표기 보정: 제곱 표기, 함수 이름 뒤 얇은 띄어쓰기, 지원이 불확실한 기호
    for old, new in [("{a_{n}}^{2}", "a_{n}^{2}"), ("{a_{1}}^{2}", "a_{1}^{2}"),
                     ("tan 4x", "tan` 4x"), ("ln x dx", "ln` x`dx"), ("ln t`", "ln` t`"),
                     ("ln s", "ln` s"), ("x+ ln x~", "x+ ln` x~"),
                     ("{h left(x right)}dx`", "{h left(x right)}`dx`"), ("neq", "ne")]:
        src = src.replace(old, new)
    exec(src, ns)
    QS = ns["QS"]

    # 23, 24 : 한 줄 문제 + 선택지 한 줄
    for n, si, ci in ((23, 717, 718), (24, 764, 765)):
        stem(ps, si, QS[n]["stem"])
        choices(ps, [ci], QS[n]["choices"])

    # 25 : 문제 / 가운데 수식 / 이어지는 글 / 선택지 한 줄
    d = QS[25]
    stem(ps, 812, d["stem"]); set_para(ps[813], d["center"]); set_para(ps[814], d["tail"])
    choices(ps, [815], d["choices"])

    # 26 : 그림 + 선택지 3줄(2+2+1)
    d = QS[26]
    stem(ps, 862, d["stem"])
    png, w_in, h_in = draw_q26(d["fig"])
    put_figure(ps[863], png, w_in, h_in)
    choices(ps, [864, 865, 866], d["choices"])

    # 27, 28 : 문제 / 가운데 수식 / 이어지는 글 / 선택지 3+2줄
    for n, si, ci, cj in ((27, 903, 906, 907), (28, 953, 956, 957)):
        d = QS[n]
        stem(ps, si, d["stem"]); set_para(ps[si + 1], d["center"]); set_para(ps[si + 2], d["tail"])
        choices(ps, [ci, cj], d["choices"])

    # 29 : 조건 상자(3줄) / 한 줄 글 / 가운데 수식 / 마지막 질문
    d = QS[29]
    stem(ps, 1000, d["stem"])
    cell = list(ps[1001].iter(q("tc")))[0]
    rebuild_cell(cell, [(0, d["box"][0]), (1, d["box"][1]), (2, d["box"][2])])
    set_para(ps[1002], d["text2"]); set_para(ps[1003], d["center"]); set_para(ps[1004], d["tail"])

    # 30 : 조건 상자(가)(나) / 마지막 질문
    d = QS[30]
    stem(ps, 1043, d["stem"])
    cell = list(ps[1044].iter(q("tc")))[0]
    rebuild_cell(cell, [(0, d["box"][0]), (1, d["box"][1])])
    set_para(ps[1045], d["tail"])
