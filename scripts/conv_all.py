"""원본 .hwp 양식(2026 수능 수학 3종)을 .hwpx 로 변환하고 압축을 풀어 calc_x / prob_x / geo_x 폴더로 만든다.
환경변수: EXAM_WORK(작업 폴더, 기본=이 파일이 있는 폴더), EXAM_DIR(원본 .hwp 가 있는 폴더, 기본=작업 폴더의 상위 폴더)
원본 .hwp 는 열기만 하고 수정하지 않는다(복사본으로 저장)."""
import win32com.client as w, os, shutil, zipfile

W = os.environ.get("EXAM_WORK") or (os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd())
EXAM_DIR = os.environ.get("EXAM_DIR") or os.path.dirname(W)
SRC = {"calc": os.path.join(EXAM_DIR, "2026학년도 수능 수학(미적분).hwp"),
       "prob": os.path.join(EXAM_DIR, "2026학년도 수능 수학(확통).hwp"),
       "geo": os.path.join(EXAM_DIR, "2026학년도 수능 수학(기하).hwp")}
for k, p in SRC.items():
    if not os.path.exists(p):
        raise SystemExit("원본 양식이 없습니다: " + p)
hwp = w.gencache.EnsureDispatch("HWPFrame.HwpObject")
try:
    try:
        hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
    except Exception:
        pass
    for k, src in SRC.items():
        dst = os.path.join(W, "2026_%s_template.hwpx" % k)
        tmp = dst + ".tmp.hwpx"          # 먼저 임시 파일로 저장 (실패해도 기존 양식 보존)
        if os.path.exists(tmp):
            os.remove(tmp)
        if not hwp.Open(src, "HWP", ""):
            raise SystemExit("원본을 열지 못했습니다: %s (기존 양식 폴더는 건드리지 않았습니다)" % src)
        if not hwp.SaveAs(tmp, "HWPX", "") or not os.path.exists(tmp):
            raise SystemExit("hwpx 저장 실패: %s" % k)
        print(k, "converted")
finally:
    hwp.Quit()
for k in SRC:
    dst = os.path.join(W, "2026_%s_template.hwpx" % k)
    os.replace(dst + ".tmp.hwpx", dst)
    x = os.path.join(W, k + "_x")
    if os.path.exists(x):
        shutil.rmtree(x)
    with zipfile.ZipFile(dst) as zf:
        zf.extractall(x)
    print(k, "unzipped", os.path.getsize(dst))
