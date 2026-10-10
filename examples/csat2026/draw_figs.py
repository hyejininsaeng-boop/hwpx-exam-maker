"""공통 7번(두 포물선 그래프), 14번(삼각형) 그림. 수식 좌표 그대로, 흑백, 가는 선, 수능 삽화 스타일.
실행 후 figures/meta.json 에 두 그림의 표시 크기(inch)를 저장한다."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "stix", "font.size": 8,
                     "axes.linewidth": 0.0})
import os
OUT = os.path.join((os.environ.get("EXAM_WORK") or (os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd())), "figures")
os.makedirs(OUT, exist_ok=True)
DPI = 600
LW = 0.7


def arrow_axes(ax, xr, yr):
    ax.annotate("", xy=(xr[1], 0), xytext=(xr[0], 0), arrowprops=dict(arrowstyle="-|>", lw=LW, color="k",
                                                                      mutation_scale=6, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(0, yr[1]), xytext=(0, yr[0]), arrowprops=dict(arrowstyle="-|>", lw=LW, color="k",
                                                                      mutation_scale=6, shrinkA=0, shrinkB=0))


# ---------------- 그림 1: 두 포물선 ----------------
W1 = 2.95  # inch (= 문서 표시 크기)
xr, yr = (-2.9, 6.1), (-2.3, 5.2)
H1 = W1 * (yr[1] - yr[0]) / (xr[1] - xr[0])
fig, ax = plt.subplots(figsize=(W1, H1), dpi=DPI)
fig.subplots_adjust(0, 0, 1, 1)
ax.set_xlim(*xr); ax.set_ylim(*yr); ax.axis("off")
x = np.linspace(0, 3, 400)
ax.fill_between(x, x**2 - 2 * x, -x**2 + 4 * x, color="0.80", lw=0)
arrow_axes(ax, xr, yr)
xa = np.linspace(-0.75, 3.45, 600); ax.plot(xa, xa**2 - 2 * xa, "k", lw=LW)
xb = np.linspace(-0.55, 4.55, 600); ax.plot(xb, -xb**2 + 4 * xb, "k", lw=LW)
ax.text(-0.22, -0.42, r"$\mathrm{O}$", ha="center", va="center")
ax.text(xr[1] - 0.08, -0.45, r"$x$", ha="right", va="center", style="italic")
ax.text(0.25, yr[1] - 0.05, r"$y$", ha="left", va="top", style="italic")
ax.text(-0.9, 2.7, r"$y=x^{2}-2x$", ha="right", va="center")
ax.text(3.95, 2.2, r"$y=-x^{2}+4x$", ha="left", va="center")
fig.savefig(OUT + r"\q07_graph.png", dpi=DPI, facecolor="white")
plt.close(fig)

# ---------------- 그림 2: 삼각형 ABC, 이등분선 AD ----------------
BC = 2 * np.sqrt(10)
B = np.array([0.0, 0.0]); C = np.array([BC, 0.0])
ax_ = (16 + 40 - 36) / (2 * BC); ay_ = np.sqrt(16 - ax_**2)
A = np.array([ax_, ay_]); D = np.array([BC * 0.4, 0.0])
W2 = 2.36; xr2, yr2 = (-0.75, 7.15), (-0.85, 4.45)
H2 = W2 * (yr2[1] - yr2[0]) / (xr2[1] - xr2[0])
fig, ax = plt.subplots(figsize=(W2, H2), dpi=DPI)
fig.subplots_adjust(0, 0, 1, 1)
ax.set_xlim(*xr2); ax.set_ylim(*yr2); ax.set_aspect("equal"); ax.axis("off")
ax.plot([B[0], C[0], A[0], B[0]], [B[1], C[1], A[1], B[1]], "k", lw=LW)
ax.plot([A[0], D[0]], [A[1], D[1]], "k", lw=LW)
# 이등분된 두 각 표시(같은 반지름의 호 하나씩)
def ang(v): return np.degrees(np.arctan2(v[1], v[0]))
aB, aD, aC = ang(B - A), ang(D - A), ang(C - A)
r = 0.62
ax.add_patch(Arc(A, 2 * r, 2 * r, theta1=aB, theta2=aD, lw=LW, color="k"))
ax.add_patch(Arc(A, 2 * r, 2 * r, theta1=aD, theta2=aC, lw=LW, color="k"))
ax.add_patch(Arc(A, 2 * (r + 0.13), 2 * (r + 0.13), theta1=aB, theta2=aD, lw=LW, color="k"))
ax.add_patch(Arc(A, 2 * (r + 0.13), 2 * (r + 0.13), theta1=aD, theta2=aC, lw=LW, color="k"))
ax.text(A[0], A[1] + 0.2, r"$\mathrm{A}$", ha="center", va="bottom")
ax.text(B[0] - 0.12, B[1] - 0.12, r"$\mathrm{B}$", ha="right", va="top")
ax.text(C[0] + 0.12, C[1] - 0.12, r"$\mathrm{C}$", ha="left", va="top")
ax.text(D[0], D[1] - 0.2, r"$\mathrm{D}$", ha="center", va="top")
mAB = (A + B) / 2; mAC = (A + C) / 2
ax.text(mAB[0] - 0.28, mAB[1] + 0.12, r"$4$", ha="right", va="center")
ax.text(mAC[0] + 0.28, mAC[1] + 0.12, r"$6$", ha="left", va="center")
fig.savefig(OUT + r"\q14_triangle.png", dpi=DPI, facecolor="white")
plt.close(fig)
from PIL import Image
for _n in ("q07_graph.png", "q14_triangle.png"):
    _im = Image.open(OUT + "\\" + _n).convert("RGB")
    _im.save(OUT + "\\" + _n)  # RGB, 해상도 정보 없음(원본 그림 파일과 같은 형식)
import json
json.dump({"q07_graph.png": [W1, H1], "q14_triangle.png": [W2, H2]}, open(OUT + r"\meta.json", "w"))
print("ok", W1, round(H1, 3), W2, round(H2, 3))
