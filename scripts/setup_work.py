"""작업 폴더를 준비한다: 이 스킬의 도구와 2026 수능 예제를 작업 폴더로 복사한다.

사용:  python -X utf8 -I setup_work.py <작업폴더> [--no-example] [--force]
  --no-example  2026 수능 예제(문항 데이터·그림)는 복사하지 않고 도구(scripts)만 복사
  --force       이미 있는 파일도 덮어씀(기본은 건너뜀)
복사 후 안내를 출력한다. 스킬 폴더 자체는 수정하지 않는다."""
import os, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if not args:
    raise SystemExit("사용: setup_work.py <작업폴더> [--no-example] [--force]")
work = os.path.abspath(args[0])
force = "--force" in sys.argv
os.makedirs(work, exist_ok=True)


def copy_tree(src, dst):
    n = 0
    for d, _, fs in os.walk(src):
        rel = os.path.relpath(d, src)
        for f in fs:
            if f == "setup_work.py" or f.endswith(".pyc"):
                continue
            t = os.path.join(dst, rel, f) if rel != "." else os.path.join(dst, f)
            os.makedirs(os.path.dirname(t), exist_ok=True)
            if os.path.exists(t) and not force:
                continue
            shutil.copy2(os.path.join(d, f), t)
            n += 1
    return n


n1 = copy_tree(os.path.join(SKILL, "scripts"), work)
n2 = 0
if "--no-example" not in sys.argv:
    n2 = copy_tree(os.path.join(SKILL, "examples", "csat2026"), work)
print("작업 폴더:", work)
print("복사한 파일: 도구 %d개, 예제 %d개 (이미 있는 파일은 건너뜀)" % (n1, n2))
print("""
다음 단계 (작업 폴더에서 실행):
  A) 2026 수능 3종 문제지를 그대로 다시 만들기
       원본 .hwp 3개가 작업 폴더의 상위 폴더에 있어야 합니다(다르면 환경변수 EXAM_DIR 로 지정).
       python -X utf8 -I build_all.py --out out --reconvert
  B) 다른 양식에 적용하기
       python -X utf8 -I analyze_template.py <양식.hwp>     -> 문단 지도와 쪽 배치 미리보기
       SKILL.md 의 '새 양식에 적용' 절차를 따릅니다.""")
