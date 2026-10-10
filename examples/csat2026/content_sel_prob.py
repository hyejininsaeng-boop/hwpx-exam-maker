# 확률과 통계 선택과목 23~30번. content_q.py 의 apply_questions 에서 exec 된다.


def _mpl():
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "stix", "font.size": 8})
    return np, plt


def _save_rgb(fg, name):
    from PIL import Image
    out = os.path.join(W, "figures", name)
    fg.savefig(out, dpi=600, facecolor="white")
    Image.open(out).convert("RGB").save(out)
    return out


def draw_bag(white, black):
    """25번: 주머니 속 흰 공/검은 공(숫자 표기). (파일명, 폭in, 높이in) 반환."""
    np, plt = _mpl()
    from matplotlib.patches import Circle
    W_IN, H_IN = 1.95, 2.0
    fg, ax = plt.subplots(figsize=(W_IN, H_IN), dpi=600)
    fg.subplots_adjust(0, 0, 1, 1)
    ax.set_xlim(-1.0, 1.0); ax.set_ylim(-1.15, 1.05); ax.set_aspect("equal"); ax.axis("off")
    LW = 0.8
    # 주머니 몸통(타원의 윗부분만 비움) + 목 + 묶은 끈 + 윗부분 주름
    cy, ax_, by_ = -0.40, 0.88, 0.72
    t = np.radians(np.linspace(110, 430, 400))
    ax.plot(ax_ * np.cos(t), cy + by_ * np.sin(t), "k", lw=LW)
    nx = 0.30
    ny = cy + by_ * np.sqrt(1 - (nx / ax_) ** 2)
    for s in (-1, 1):
        ax.plot([s * nx, s * 0.15], [ny, 0.58], "k", lw=LW)                       # 목
        xs_ = np.linspace(0, 1, 40)
        bx = (1 - xs_) ** 2 * s * 0.15 + 2 * (1 - xs_) * xs_ * s * 0.52 + xs_ ** 2 * s * 0.62
        by = (1 - xs_) ** 2 * 0.70 + 2 * (1 - xs_) * xs_ * 0.72 + xs_ ** 2 * 0.98
        ax.plot(bx, by, "k", lw=LW)                                                 # 벌어진 입구
    ax.plot([-0.15, 0.15], [0.58, 0.58], "k", lw=LW)
    ax.plot([-0.15, 0.15], [0.70, 0.70], "k", lw=LW)                                 # 끈
    for s in (-1, 1):
        ax.plot([s * 0.15, s * 0.15], [0.58, 0.70], "k", lw=LW)                      # 끈 옆선
    xs = np.linspace(-0.62, 0.62, 200)
    ax.plot(xs, 0.98 + 0.05 * np.sin(xs * 14), "k", lw=LW)                           # 입구 주름
    # 공: 육각 격자 배치(타원 안쪽)
    n = len(white) + len(black)
    r = 0.165
    cand = []
    for row in range(-3, 4):
        for col in range(-4, 5):
            x = col * 2.35 * r + (row % 2) * 1.17 * r
            y = cy + row * 2.05 * r
            if (x / 0.74) ** 2 + ((y - cy) / 0.52) ** 2 <= 1.0:
                cand.append((x, y))
    cand.sort(key=lambda p: (p[0] / 0.74) ** 2 + ((p[1] - cy) / 0.52) ** 2)
    cand = cand[:n]
    order = []
    wi, bi = list(white), list(black)
    while wi or bi:                                   # 흰/검은 공을 번갈아 배치
        if wi: order.append(("w", wi.pop(0)))
        if bi: order.append(("b", bi.pop(0)))
    rng = np.random.RandomState(7)
    idx = rng.permutation(len(cand))
    for (kind, num), k in zip(order, idx):
        x, y = cand[k]
        ax.add_patch(Circle((x, y), r, fc="white" if kind == "w" else "black", ec="k", lw=LW))
        ax.text(x, y - 0.005, str(num), ha="center", va="center", fontsize=7.5,
                color="black" if kind == "w" else "white")
    _save_rgb(fg, "p25_bag.png")
    plt.close(fg)
    return "p25_bag.png", W_IN, H_IN


def draw_boxes(balls, boxes):
    """28번: 공 더미와 번호가 적힌 빈 상자 여러 개. (파일명, 폭in, 높이in) 반환."""
    np, plt = _mpl()
    from matplotlib.patches import Circle, Polygon
    LW = 0.8
    r = 0.20
    bw, bh, dx, dy = 1.00, 1.05, 0.32, 0.26      # 상자 앞면 폭/높이, 윗면 깊이 이동
    gap = 0.22
    base = 1
    while base * (base + 1) // 2 < balls:        # 맨 아랫줄 공 개수(삼각 쌓기)
        base += 1
    pile_w = base * 2 * r
    x_boxes0 = pile_w + 0.8
    total_w = x_boxes0 + boxes * (bw + gap) + dx
    nrows, _left = 0, balls
    while _left > 0:
        _left -= min(max(base - nrows, 1), _left)
        nrows += 1
    pile_h = 2 * r + (nrows - 1) * 1.75 * r
    total_h = max(bh + dy, pile_h) + 0.25
    W_IN = 4.15
    H_IN = W_IN * total_h / total_w
    fg, ax = plt.subplots(figsize=(W_IN, H_IN), dpi=600)
    fg.subplots_adjust(0, 0, 1, 1)
    ax.set_xlim(0, total_w); ax.set_ylim(-0.08, total_h - 0.08); ax.set_aspect("equal"); ax.axis("off")
    # 공 더미(삼각 쌓기, 아래 줄부터)
    left = balls
    row = 0
    while left > 0:
        cnt = max(base - row, 1)
        k = min(cnt, left)
        for c in range(k):
            x = r + row * r + c * 2 * r
            y = r + row * 1.75 * r
            ax.add_patch(Circle((x, y), r, fc="0.80", ec="k", lw=LW))
        left -= k
        row += 1
    for i in range(boxes):
        x0 = x_boxes0 + i * (bw + gap)
        front = [(x0, 0), (x0 + bw, 0), (x0 + bw, bh), (x0, bh)]
        top = [(x0, bh), (x0 + bw, bh), (x0 + bw + dx, bh + dy), (x0 + dx, bh + dy)]
        side = [(x0 + bw, 0), (x0 + bw + dx, dy), (x0 + bw + dx, bh + dy), (x0 + bw, bh)]
        ax.add_patch(Polygon(front, closed=True, fc="white", ec="k", lw=LW))
        ax.add_patch(Polygon(top, closed=True, fc="white", ec="k", lw=LW))
        ax.add_patch(Polygon(side, closed=True, fc="0.88", ec="k", lw=LW))
        ax.text(x0 + bw / 2, bh * 0.38, str(i + 1), ha="center", va="center", fontsize=9)
    _save_rgb(fg, "p28_boxes.png")
    plt.close(fg)
    return "p28_boxes.png", W_IN, H_IN


def _drop(p):
    p.getparent().remove(p)


def apply_sel(ps):
    ns = {}
    src = open(os.path.join(W, "data_p23_30.py"), encoding="utf-8-sig").read()
    for old, new in [("neq", "ne")]:
        src = src.replace(old, new)
    exec(src, ns)
    QP = ns["QP"]

    # 23
    stem(ps, 722, QP[23]["stem"]); choices(ps, [723], QP[23]["choices"])
    # 24
    d = QP[24]
    stem(ps, 769, d["stem"]); set_para(ps[770], d["center"]); set_para(ps[771], d["tail"])
    choices(ps, [772], d["choices"])
    # 25 (그림: 주머니)
    d = QP[25]
    stem(ps, 817, d["stem"]); choices(ps, [818], d["choices"])
    if d.get("fig"):
        png, w_in, h_in = draw_bag(d["fig"]["white"], d["fig"]["black"])
        put_figure(ps[819], png, w_in, h_in)
    else:
        _drop(ps[819])
    # 26
    stem(ps, 858, QP[26]["stem"]); choices(ps, [859], QP[26]["choices"])
    # 27
    d = QP[27]
    stem(ps, 907, d["stem"]); set_para(ps[908], d["center"]); set_para(ps[909], d["tail"])
    choices(ps, [910], d["choices"])
    # 28 (상자 조건 + 그림: 공과 상자)
    d = QP[28]
    stem(ps, 957, d["stem"])
    cell = list(ps[958].iter(q("tc")))[0]
    rebuild_cell(cell, [(0, line) for line in d["box"]])
    set_para(ps[959], d["tail"])
    choices(ps, [961], d["choices"])
    if d.get("fig"):
        png, w_in, h_in = draw_boxes(d["fig"]["balls"], d["fig"]["boxes"])
        put_figure(ps[962], png, w_in, h_in)
    else:
        _drop(ps[962])
    # 29 (상자 조건 + 표준정규분포표(그대로 유지) + 글)
    d = QP[29]
    stem(ps, 997, d["stem"])
    cell = list(ps[998].iter(q("tc")))[0]
    rebuild_cell(cell, [(0, line) for line in d["box"]])
    run = [r for r in ps[999] if ln(r) == "run"][0]
    tbl = run.find(q("tbl"))
    run.remove(tbl)
    set_para(ps[999], d["tail"])
    run = [r for r in ps[999] if ln(r) == "run"][0]
    run.insert(0, tbl)
    # 30 (조건 상자)
    d = QP[30]
    stem(ps, 1039, d["stem"])
    cell = list(ps[1040].iter(q("tc")))[0]
    rebuild_cell(cell, [(0, d["box"][0]), (0, d["box"][1])])
