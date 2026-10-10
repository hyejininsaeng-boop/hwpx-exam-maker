"""세 과목 '문제+해설' hwpx 를 한 번에 만들고, 기준 파일과 내용을 대조한다.

사용:  python -X utf8 -I build_all.py [--out 폴더] [--ref 기준폴더] [--reconvert] [--fresh-sizes] [--yes]
  --out          결과를 저장할 폴더 (기본: work\\out)  ※ 완성본이 있는 폴더를 주면 --yes 가 있어야 덮어씀
  --ref          대조할 기준 폴더 (기본: 작업 폴더의 상위 폴더, 같은 파일 이름이 있을 때만 대조)
  --reconvert    원본 .hwp 3개를 다시 .hwpx 로 변환(conv_all.py)해서 처음부터 시작
  --fresh-sizes  수식 크기(sizes.json)를 지우고 한글로 전부 다시 측정
"""
import os, sys, subprocess, argparse, shutil

W = (os.environ.get("EXAM_WORK") or (os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()))
EXAM_DIR = os.environ.get("EXAM_DIR") or os.path.dirname(W)
sys.path.insert(0, W)
from hwpx_tokens import tokens, diff_positions
NAMES = {"calc": "미적분", "prob": "확통", "geo": "기하"}

ap = argparse.ArgumentParser()
ap.add_argument("--out", default=os.path.join(W, "out"))
ap.add_argument("--ref", default=EXAM_DIR)
ap.add_argument("--reconvert", action="store_true")
ap.add_argument("--fresh-sizes", action="store_true")
ap.add_argument("--yes", action="store_true", help="--out 폴더에 같은 이름 파일이 있어도 덮어쓰기 허용")
a = ap.parse_args()
STAGE = os.path.join(W, "_stage")   # 항상 여기서 먼저 만들고, 다 끝난 뒤에만 --out 으로 복사


def run(script, env_extra=None, *args):
    env = dict(os.environ)
    env.update(env_extra or {})
    env["EXAM_WORK"] = W
    env["EXAM_DIR"] = EXAM_DIR
    r = subprocess.run([sys.executable, "-X", "utf8", "-I", os.path.join(W, script), *args],
                       env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    last = (r.stdout.strip().splitlines() or [""])[-1]
    if r.returncode != 0:
        print("  [실패]", script, "\n", (r.stderr or r.stdout)[-1500:])
        sys.exit(1)
    return last


targets = [os.path.join(a.out, "수능스타일_%s_문제+해설.hwpx" % n) for n in NAMES.values()]
exists = [t for t in targets if os.path.exists(t)]
if exists and not a.yes and os.path.abspath(a.out) != os.path.abspath(os.path.join(W, "out")):
    print("중단: 아래 파일이 이미 있어 덮어쓰게 됩니다. 확인 후 --yes 를 붙여 다시 실행하세요.")
    for t in exists:
        print("  ", t)
    sys.exit(1)
os.makedirs(STAGE, exist_ok=True)
print("결과 폴더:", a.out, "(작업은 %s 에서 먼저 진행)" % STAGE)
if a.reconvert:
    print("1) 원본 .hwp -> .hwpx 변환:", run("conv_all.py"))
if a.fresh_sizes:
    for f in ("sizes.json", "scripts.json"):
        p = os.path.join(W, f)
        if os.path.exists(p):
            os.remove(p)
    print("   수식 크기 파일 초기화")
print("2) 공통 그림(7번, 14번):", run("draw_figs.py"))

results = {}
for track, name in NAMES.items():
    fn = "수능스타일_%s_문제+해설.hwpx" % name
    out = os.path.join(STAGE, fn)
    env = {"TRACK": track, "KEY": "1"}
    print("3) [%s] 1차 빌드:" % name, run("build_exam.py", env, out))
    print("   [%s] 수식 크기 측정:" % name, run("sizes.py", env))
    print("   [%s] 최종 빌드:" % name, run("build_exam.py", env, out))
    results[name] = (fn, out)

print("\n4) 기준 파일과 대조 (기준 폴더: %s)" % a.ref)
ok_all = True
for name, (fn, out) in results.items():
    ref = os.path.join(a.ref, fn)
    if os.path.abspath(ref) == os.path.abspath(out):
        print("  %s: 결과가 기준 파일 자신이라 대조 생략" % name); continue
    if not os.path.exists(ref):
        print("  %s: 기준 파일 없음(대조 생략)" % name); continue
    ta, ia = tokens(ref)
    tb, ib = tokens(out)
    diffs = diff_positions(ta, tb)
    same = (ta == tb) and (ia == ib)
    ok_all &= same
    print("  %s: 내용 토큰 %d vs %d, 그림 %s -> %s" % (name, len(ta), len(tb),
          "동일" if ia == ib else "다름", "일치" if same else "불일치 %d곳" % len(diffs)))
    if not same and diffs:
        k = diffs[0]
        print("     첫 차이:", ta[k] if k < len(ta) else "(없음)", "|", tb[k] if k < len(tb) else "(없음)")
print("\n결론:", "세 과목 모두 기준 파일과 일치" if ok_all else "일치하지 않는 항목 있음")

os.makedirs(a.out, exist_ok=True)
for name, (fn, out) in results.items():
    shutil.copyfile(out, os.path.join(a.out, fn) + ".tmp")
    os.replace(os.path.join(a.out, fn) + ".tmp", os.path.join(a.out, fn))
print("복사 완료 ->", a.out)
