"""hwpx 두 파일의 내용을 비교하기 위한 공통 도구 (build_all.py 와 compare.py 가 함께 쓴다).
-I 로 실행하면 이 폴더가 import 경로에 없으므로, 쓰는 쪽에서 sys.path 에 work 폴더를 먼저 넣는다."""
import zipfile
from lxml import etree

HP = "http://www.hancom.co.kr/hwpml/2011/paragraph"


def tokens(path):
    """(내용 토큰 목록, 그림 파일 [(이름, 크기)]) 를 돌려준다."""
    with zipfile.ZipFile(path) as z:
        root = etree.parse(z.open("Contents/section0.xml")).getroot()
        imgs = sorted((i.filename.split("/")[-1], i.file_size) for i in z.infolist()
                      if i.filename.startswith("BinData"))
    out = []
    for e in root.iter():
        n = etree.QName(e.tag).localname
        if n == "t":
            out.append(("t", e.text or "", tuple((x.get("width"), x.tail or "") for x in e
                                                  if etree.QName(x.tag).localname == "tab")))
        elif n == "script":
            out.append(("e", e.text or ""))
        elif n == "equation":
            sz = e.find("{%s}sz" % HP)
            out.append(("eq", sz.get("width"), sz.get("height"), e.get("baseLine")))
        elif n == "p":
            out.append(("p", e.get("paraPrIDRef"), e.get("styleIDRef"), e.get("pageBreak"), e.get("columnBreak")))
        elif n == "pic":
            out.append(("pic",))
    return out, imgs


def diff_positions(a, b):
    """다른 위치 목록. 길이가 다르면 짧은 쪽이 끝난 뒤의 위치도 차이로 센다."""
    n = max(len(a), len(b))
    return [i for i in range(n) if i >= len(a) or i >= len(b) or a[i] != b[i]]
