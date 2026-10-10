"""기하 문제 그림 도구 (흑백, 가는 선, 수능 삽화 스타일).
 - draw_solid3d(spec, out_name, w_in, h_in): 볼록 입체(면 목록) + 보조선 + 원기둥 + 구
 - draw_plane2d(spec, out_name, w_in, h_in): 좌표평면 위의 이차곡선(타원/포물선/쌍곡선/원), 점, 선분
결과 PNG(RGB)는 <작업폴더>\\figures\\<out_name> 에 저장되고 (경로, w_in, h_in)를 반환한다.
python -X utf8 으로 실행하는 파일에서 `exec(open(r"<작업폴더>\\figlib.py", encoding="utf-8").read())  # 작업 폴더를 환경변수 EXAM_WORK 로 지정` 로 불러 쓴다.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

FIGDIR = os.path.join((os.environ.get("EXAM_WORK") or (os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd())), "figures")
LW = 0.8
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "stix", "font.size": 9})


def _save(fg, name):
    os.makedirs(FIGDIR, exist_ok=True)
    out = os.path.join(FIGDIR, name)
    fg.savefig(out, dpi=600, facecolor="white")
    plt.close(fg)
    Image.open(out).convert("RGB").save(out)
    return out


def _label(ax, text, xy, center, push=0.06, span=1.0, offset=None, style="rm"):
    x, y = xy
    if offset is not None:
        dx, dy = offset
    else:
        v = np.array([x - center[0], y - center[1]], dtype=float)
        n = np.linalg.norm(v)
        v = v / n if n > 1e-9 else np.array([0.0, 1.0])
        dx, dy = v[0] * push * span, v[1] * push * span
    if style == "rm":
        s = r"$\mathrm{%s}$" % text
    else:
        s = r"$%s$" % text
    ax.text(x + dx, y + dy, s, ha="center", va="center", zorder=5)


# ------------------------------------------------------------------ 입체도형
def _basis(az, el):
    a, e = np.radians(az), np.radians(el)
    c = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])   # 보는 쪽(카메라) 방향
    right = np.array([-np.sin(a), np.cos(a), 0.0])
    up = np.cross(c, right)
    return c, right, up


def draw_solid3d(spec, out_name, w_in, h_in):
    pts = {k: np.array(v, dtype=float) for k, v in spec["points"].items()}
    view = spec.get("view", {})
    c, right, up = _basis(view.get("az", -60), view.get("el", 22))
    P = lambda p: np.array([np.dot(p, right), np.dot(p, up)])
    segs = []          # (p3, q3, dashed)
    allxy = []

    # 볼록 입체: 면 목록에서 변 추출, 앞/뒤 면 판별
    faces = spec.get("faces", [])
    if faces:
        allv = np.array([pts[n] for f in faces for n in f])
        cen = allv.mean(axis=0)
        edge_faces = {}
        for f in faces:
            vs = [pts[n] for n in f]
            nrm = np.cross(vs[1] - vs[0], vs[2] - vs[0])
            if np.dot(nrm, np.mean(vs, axis=0) - cen) < 0:
                nrm = -nrm
            front = np.dot(nrm, c) > 1e-9
            for i in range(len(f)):
                e = tuple(sorted((f[i], f[(i + 1) % len(f)])))
                edge_faces.setdefault(e, []).append(front)
        for (a, b), fr in edge_faces.items():
            segs.append((pts[a], pts[b], not any(fr)))
    for a, b in spec.get("extra", []):
        segs.append((pts[a], pts[b], False))
    for a, b in spec.get("extra_dashed", []):
        segs.append((pts[a], pts[b], True))

    arcs = []          # (xy 배열, dashed)
    for cy in spec.get("cylinders", []):
        b, t, r = np.array(cy["bottom"], float), np.array(cy["top"], float), cy["radius"]
        th = np.linspace(0, 2 * np.pi, 400)
        for center, top in ((b, False), (t, True)):
            circ = np.array([center + r * np.array([np.cos(x), np.sin(x), 0.0]) for x in th])
            front = np.array([np.dot(p - center, c) > 0 for p in circ])
            if top:
                arcs.append((np.array([P(p) for p in circ]), False))
            else:
                for mask, dashed in ((front, False), (~front, True)):
                    idx = np.where(mask)[0]
                    if len(idx) == 0:
                        continue
                    splits = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
                    for sp in splits:
                        arcs.append((np.array([P(circ[i]) for i in sp]), dashed))
        a0 = np.arctan2(c[1], c[0])
        for sgn in (-1, 1):
            tt = a0 + sgn * np.pi / 2
            d = r * np.array([np.cos(tt), np.sin(tt), 0.0])
            segs.append((b + d, t + d, False))
    spheres = spec.get("spheres", [])
    sph_draw = []
    for sp in spheres:
        cen = P(np.array(sp["center"], float)); R = sp["radius"]
        sph_draw.append((cen, R, sp))

    # 그리기 범위
    for p, q_, _ in segs:
        allxy += [P(p), P(q_)]
    for xy, _ in arcs:
        allxy += list(xy[::20])
    for cen, R, _ in sph_draw:
        allxy += [cen + np.array([R, R]), cen - np.array([R, R])]
    allxy = np.array(allxy)
    lo, hi = allxy.min(axis=0), allxy.max(axis=0)
    pad = 0.12 * max(hi - lo)
    lo, hi = lo - pad, hi + pad
    W, H = hi - lo
    # 캔버스에 맞춰 같은 비율로 맞춤
    scale = min(w_in / W, h_in / H)
    fg, ax = plt.subplots(figsize=(w_in, h_in), dpi=600)
    fg.subplots_adjust(0, 0, 1, 1)
    mx, my = (w_in / scale - W) / 2, (h_in / scale - H) / 2
    ax.set_xlim(lo[0] - mx, hi[0] + mx); ax.set_ylim(lo[1] - my, hi[1] + my)
    ax.set_aspect("equal"); ax.axis("off")
    for p, q_, dashed in segs:
        a, b = P(p), P(q_)
        ax.plot([a[0], b[0]], [a[1], b[1]], "k", lw=LW, ls=(0, (3, 2)) if dashed else "-", zorder=2)
    for xy, dashed in arcs:
        ax.plot(xy[:, 0], xy[:, 1], "k", lw=LW, ls=(0, (3, 2)) if dashed else "-", zorder=2)
    th = np.linspace(0, 2 * np.pi, 400)
    for cen, R, sp in sph_draw:
        ax.plot(cen[0] + R * np.cos(th), cen[1] + R * np.sin(th), "k", lw=LW, zorder=2)
        # 적도(수평 원): 앞쪽 실선, 뒤쪽 점선
        eq = np.array([np.array(sp["center"], float) + R * np.array([np.cos(x), np.sin(x), 0.0]) for x in th])
        fr = np.array([np.dot(p - np.array(sp["center"], float), c) > 0 for p in eq])
        xy = np.array([P(p) for p in eq])
        for mask, dashed in ((fr, False), (~fr, True)):
            idx = np.where(mask)[0]
            if len(idx) == 0:
                continue
            for s_ in np.split(idx, np.where(np.diff(idx) > 1)[0] + 1):
                ax.plot(xy[s_, 0], xy[s_, 1], "k", lw=LW * 0.8, ls=(0, (3, 2)) if dashed else "-", zorder=2)
        ax.plot(*cen, "k.", ms=2.5, zorder=3)
        if sp.get("label"):
            _label(ax, sp["label"], cen, cen, offset=(0.0, -0.10 * H))
    ctr = (lo + hi) / 2
    offs = spec.get("label_offsets", {})
    for n in spec.get("labels", []):
        _label(ax, n, P(pts[n]), ctr, push=0.07, span=max(W, H), offset=offs.get(n))
        ax.plot(*P(pts[n]), "k.", ms=2.5, zorder=3)
    _save(fg, out_name)
    return os.path.join(FIGDIR, out_name), w_in, h_in


# ------------------------------------------------------------------ 좌표평면
def draw_plane2d(spec, out_name, w_in, h_in):
    x0, x1 = spec["xlim"]
    y0, y1 = spec["ylim"]
    X, Y = x1 - x0, y1 - y0
    fg, ax = plt.subplots(figsize=(w_in, h_in), dpi=600)
    fg.subplots_adjust(0, 0, 1, 1)
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1); ax.axis("off")
    ar = dict(arrowstyle="-|>", lw=LW, color="k", mutation_scale=6, shrinkA=0, shrinkB=0)
    if spec.get("axes", True):
        ax.annotate("", xy=(x1, 0), xytext=(x0, 0), arrowprops=ar)
        ax.annotate("", xy=(0, y1), xytext=(0, y0), arrowprops=ar)
        ax.text(-0.025 * X, -0.05 * Y, r"$\mathrm{O}$", ha="right", va="top")
        ax.text(x1 - 0.01 * X, -0.05 * Y, r"$x$", ha="right", va="top", style="italic")
        ax.text(0.025 * X, y1 - 0.01 * Y, r"$y$", ha="left", va="top", style="italic")
    th = np.linspace(0, 2 * np.pi, 800)

    def plot_clip(x, y, dashed=False):
        x = np.array(x, float); y = np.array(y, float)
        m = (x < x0) | (x > x1) | (y < y0) | (y > y1)
        x[m] = np.nan; y[m] = np.nan
        ax.plot(x, y, "k", lw=LW, ls=(0, (3, 2)) if dashed else "-", zorder=2)
    for cv in spec.get("curves", []):
        t = cv["type"]
        if t == "ellipse":
            plot_clip(cv["cx"] + cv["a"] * np.cos(th), cv["cy"] + cv["b"] * np.sin(th))
        elif t == "circle":
            plot_clip(cv["cx"] + cv["r"] * np.cos(th), cv["cy"] + cv["r"] * np.sin(th))
        elif t == "parabola":      # 꼭짓점 (vx,vy), (y-vy)^2=4p(x-vx) 등
            vx, vy = cv["vertex"]; p = cv["p"]; o = cv.get("orient", "right")
            s = np.linspace(-1, 1, 1200) * max(X, Y) * 2
            if o == "right":
                plot_clip(vx + s ** 2 / (4 * p), vy + s)
            elif o == "left":
                plot_clip(vx - s ** 2 / (4 * p), vy + s)
            elif o == "up":
                plot_clip(vx + s, vy + s ** 2 / (4 * p))
            else:
                plot_clip(vx + s, vy - s ** 2 / (4 * p))
        elif t == "hyperbola":
            cx, cy, a, b = cv["cx"], cv["cy"], cv["a"], cv["b"]
            s = np.linspace(-4, 4, 1600)
            if cv.get("orient", "x") == "x":
                for sg in (-1, 1):
                    plot_clip(cx + sg * a * np.cosh(s), cy + b * np.sinh(s))
            else:
                for sg in (-1, 1):
                    plot_clip(cx + b * np.sinh(s), cy + sg * a * np.cosh(s))
        elif t == "line":
            (ax_, ay_), (bx_, by_) = cv["p1"], cv["p2"]
            d = np.array([bx_ - ax_, by_ - ay_], float)
            s = np.linspace(-50, 50, 4000) if cv.get("extend", True) else np.linspace(0, 1, 100)
            plot_clip(ax_ + s * d[0], ay_ + s * d[1], cv.get("dashed", False))
    pts = spec.get("points", {})
    for a, b in spec.get("segments", []):
        ax.plot([pts[a][0], pts[b][0]], [pts[a][1], pts[b][1]], "k", lw=LW, zorder=2)
    for a, b in spec.get("dashed", []):
        ax.plot([pts[a][0], pts[b][0]], [pts[a][1], pts[b][1]], "k", lw=LW, ls=(0, (3, 2)), zorder=2)
    ctr = ((x0 + x1) / 2, (y0 + y1) / 2)
    labs = spec.get("labels", {})
    items = labs.items() if isinstance(labs, dict) else [(n, None) for n in labs]
    for n, off in items:
        ax.plot(*pts[n], "k.", ms=3, zorder=3)
        _label(ax, n, pts[n], ctr, push=0.05, span=max(X, Y), offset=off)
    for tx in spec.get("texts", []):                  # [("y=-p", (x,y)), ...] 수식 글자 직접 배치
        ax.text(tx[1][0], tx[1][1], r"$%s$" % tx[0], ha="center", va="center")
    _save(fg, out_name)
    return os.path.join(FIGDIR, out_name), w_in, h_in
