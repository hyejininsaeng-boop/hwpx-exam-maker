# 해설 데이터와 해설 삽입(미주 방식) / 정답표 / 바닥글. KEY=1 일 때 build_exam.py 가 사용한다.
import re

# 공통 1~22번 해설: n: (정답 표시, [풀이 줄들]) ; 한글은 자동으로 글자로, 나머지는 수식으로 변환된다.
SOL_COMMON = {
    1: ("②", ["16 ^{ { 3} over { 4} }times2 ^{ -2}",
              "=LEFT ( 2 ^{ 4} RIGHT ) ^{ { 3} over { 4} }times2 ^{ -2}",
              "=2 ^{ 3}times2 ^{ -2}=2 ^{ 3-2}=2"]),
    2: ("③", ["f`' left(x right)=3x^{2}-4x",
              "lim_{h`` rarrow ``0} {{f left(2+h right)-f left(2 right)} over {h}}=f`' left(2 right)",
              "=3 times 2^{2}-4 times 2=4"]),
    3: ("④", ["sum _{k=1} ^{5} LEFT ( 3a _{k} -k RIGHT )=3 sum _{k=1} ^{5} a _{k} - sum _{k=1} ^{5} k",
              "=3 sum _{k=1} ^{5} a _{k} -15=39",
              "THEREFORE  sum _{k=1} ^{5} a _{k} =18"]),
    4: ("②", ["lim _{x`` rarrow ``1-} f LEFT ( x RIGHT )=1+a",
              "lim _{x`` rarrow ``1+} f LEFT ( x RIGHT )=f LEFT ( 1 RIGHT )=3",
              "1+a=3  THEREFORE  a=2"]),
    5: ("①", ["f left(x right)=2x^{3}-3x^{2}+2x-3",
              "f`' left(x right)=6x^{2}-6x+2",
              "THEREFORE f`' left(2 right)=24-12+2=14"]),
    6: ("③", ["log`_{a}`b=2에서 b=a^{2}",
              "log`_{2}`ab=log`_{2}`a^{3}=3에서 a=2, b=4",
              "log`_{8}`ab^{2}=log`_{8}`2 times 4^{2}=log`_{2^{3}}`2^{5}={5} over {3}"]),
    7: ("⑤", ["두 곡선의 교점의 x좌표는 x^{2}-2x=-x^{2}+4x에서 x=0 또는 x=3",
              "S=int_{0}^{3} left{ left(-x^{2}+4x right)- left(x^{2}-2x right) right}dx=int_{0}^{3} left(-2x^{2}+6x right)dx",
              "=left[-{2} over {3}x^{3}+3x^{2} right]_{0}^{3}=-18+27=9"]),
    8: ("④", ["sin` theta -2cos` theta =0에서 tan` theta =2",
              "sin` left(pi+theta right)=-sin` theta >0이므로 sin` theta <0",
              "따라서 theta는 제3사분면의 각이므로 cos` theta <0",
              "cos^{2}` theta ={1} over {1+tan^{2}` theta }={1} over {5}",
              "THEREFORE cos` theta =-{ sqrt{5}} over {5}"]),
    9: ("②", ["f`' left(x right)=3x^{2}-12ax+9a^{2}=3 left(x-a right) left(x-3a right)",
              "a>0이므로 x=a에서 극대, x=3a에서 극소이고 f left(a right)=4a^{3}+2, f left(3a right)=2",
              "직선 y=6이 접하려면 4a^{3}+2=6, a=1",
              "f left(x right)=x^{3}-6x^{2}+9x+2이므로 f left(6 right)=216-216+54+2=56"]),
    10: ("①", ["점 P의 x좌표를 t라 하면 P left(t,``a^{t}-1 right), Q left(t,``0 right), R left(t,``-1 right)",
               "{ bar{rm{PQ}it}}={ bar{rm{QR}it}}이므로 a^{t}-1=1, a^{t}=2",
               "삼각형 OPR의 넓이는 {1} over {2} times 2 times t=t이므로 t=4",
               "a^{4}=2이므로 a^{11}=2^{{11} over {4}}"]),
    11: ("③", ["ㄱ. int_{0}^{1} left(t^{2}-6t+5 right)dt=left[{1} over {3}t^{3}-3t^{2}+5t right]_{0}^{1}={7} over {3} (참)",
               "ㄴ. v left(t right)=left(t-2 right) left(t-4 right)이므로 t=2, t=4에서 부호가 바뀌어 방향이 두 번 바뀐다. (거짓)",
               "ㄷ. v left(t right)=left(t-1 right) left(t-5 right)이므로 이동 거리는 int_{0}^{1}v left(t right)dt-int_{1}^{5}v left(t right)dt={7} over {3}+{32} over {3}=13 (참)",
               "따라서 옳은 것은 ㄱ, ㄷ"]),
    12: ("⑤", ["a_{3}^{2}=a_{2}a_{4}=16이고 a_{3}>0이므로 a_{3}=4",
               "공비를 r라 하면 a_{3}+a_{5}=4+4r^{2}=20에서 r^{2}=4, r=2",
               "THEREFORE a_{6}=a_{3}r^{3}=4 times 8=32"]),
    13: ("③", ["f`' left(x right)=2x-3, f left(1 right)=-1, f`' left(1 right)=-1이므로 l: y=-x",
               "g`' left(x right)=2xf left(x right)+left(x^{2}+2 right)f`' left(x right)에서 g left(1 right)=-3, g`' left(1 right)=-5",
               "m: y=-5x+2",
               "두 직선의 교점의 x좌표는 -x=-5x+2에서 x={1} over {2}",
               "S={1} over {2} times 2 times {1} over {2}={1} over {2}, THEREFORE 16S=8"]),
    14: ("②", ["코사인법칙에서 { bar{rm{BC}it}}^{2}=16+36-2 times 4 times 6 times {1} over {4}=40",
               "angle{rm{BAD}it}=angle{rm{DAC}it}= alpha 라 하면 cos^{2}` alpha ={1+cos` left(2 alpha right)} over {2}={5} over {8}",
               "삼각형 ABD+삼각형 ADC=삼각형 ABC에서 {1} over {2} times 4 times { bar{rm{AD}it}}sin` alpha +{1} over {2} times 6 times { bar{rm{AD}it}}sin` alpha ={1} over {2} times 4 times 6 times sin` left(2 alpha right)",
               "5{ bar{rm{AD}it}}=24cos` alpha 이므로 { bar{rm{AD}it}}={24} over {5} times {sqrt{10}} over {4}={6 sqrt{10}} over {5}"]),
    15: ("②", ["f`' left(x right)=3x^{2}-12x+9=3 left(x-1 right) left(x-3 right)",
               "극댓값 f left(1 right)=k+4, 극솟값 f left(3 right)=k",
               "g left(t right)는 t=k, t=k+4에서 불연속이므로 2k+4=10, k=3",
               "THEREFORE f left(4 right)=64-96+36+3=7"]),
    16: ("27", ["a_{2}=2a_{1}+1=5",
               "a_{3}=2a_{2}+2=12",
               "a_{4}=2a_{3}+3=27"]),
    17: ("15", ["F left(x right)=int left(6x^{2}-2x right)dx=2x^{3}-x^{2}+C",
               "F left(0 right)=3에서 C=3",
               "THEREFORE F left(2 right)=16-4+3=15"]),
    18: ("14", ["sin` left(angle{rm{BAC}it} right)= sqrt{1-{9} over {25}}={4} over {5}",
               "삼각형 ABC의 넓이는 {1} over {2} times 5 times 7 times {4} over {5}=14"]),
    19: ("18", ["h left(x right)=x^{3}-6x^{2}+9x-2라 하면 h`' left(x right)=3 left(x-1 right) left(x-3 right)",
               "h left(-1 right)=-18, h left(1 right)=2, h left(3 right)=-2, h left(4 right)=2",
               "구간 -1 le x le 4에서 left|h left(x right) right| le 18이므로 k의 최솟값은 18"]),
    20: ("160", ["a_{n+1}=sum_{k=1}^{n+1}a_{k}-sum_{k=1}^{n}a_{k}={1} over {2} left(a_{n+1}-a_{n} right)+ left(2n+4 right)이므로 (가)=2n+4, f left(n right)=2n+4",
               "정리하면 a_{n}+a_{n+1}=2 left(2n+4 right)  ……㉠",
               "㉠에서 n 대신 n+1을 넣은 식과 ㉠을 변끼리 빼면 a_{n+2}-a_{n}=4~ left(n ge 2 right)  ……㉡",
               "n=2를 대입하면 a_{1}+a_{2}={1} over {2}a_{2}+12에서 a_{2}=14, (나)=14",
               "a_{2k}=14+4 left(k-1 right)=4k+10이므로 sum_{k=1}^{10}a_{2k}=220+100=320, (다)=320",
               "p=14, q=320, f left(12 right)=28 THEREFORE {p times q} over {f left(12 right)}=160"]),
    21: ("108", ["left| f left(x right)-t right|는 방정식 f left(x right)=t의 실근 중 중근이 아닌 근에서만 미분가능하지 않다",
               "f left(x right)가 극값을 갖지 않으면 g left(t right)의 불연속인 t가 많아야 1개이므로 (가)에 모순이다",
               "극댓값 M, 극솟값 m이라 하면 g left(t right)=3~ left(m<t<M right), g left(t right)=1~ left(t le m 또는 t ge M right)",
               "(가)에서 M=0, m=-4이고 M-m={ left(beta - alpha right)^{3}} over {2}=4이므로 beta - alpha =2",
               "f left(x right)= left(x-alpha right)^{2} left(x-alpha -3 right)이고 g left(f left(x right) right)는 x=alpha -1, alpha , alpha +2, alpha +3에서 불연속",
               "(나)에서 4 alpha +4=12, alpha =2이므로 f left(x right)= left(x-2 right)^{2} left(x-5 right)",
               "THEREFORE f left(8 right)=36 times 3=108"]),
    22: ("46", ["a_{1}이 자연수이면 모든 항이 자연수이고, a_{n+1}=v일 때 a_{n}=v+n 또는 a_{n}=v-2n left(2n+1 le v le 3n right)",
               "a_{7}=7에서 a_{6}=13, a_{6}=13에서 a_{5}=18 또는 a_{5}=3",
               "a_{5}=18에서 a_{4}=22, a_{5}=3에서 a_{4}=7",
               "a_{4}=22에서 a_{3}=25, a_{4}=7에서 a_{3}=10 또는 a_{3}=1",
               "a_{3}=25에서 a_{2}=27, a_{3}=10에서 a_{2}=12, a_{3}=1에서 a_{2}=3",
               "a_{2}=27에서 a_{1}=28, a_{2}=12에서 a_{1}=13, a_{2}=3에서 a_{1}=4 또는 a_{1}=1",
               "THEREFORE 1+4+13+28=46"]),
}


def line_segs(line):
    """풀이 줄을 [글자, 수식, ...] 로 쪼갠다. 이미 [(kind,값),...] 목록이면 그대로 쓴다.
    문자열이면 한글이 들어간 덩어리는 글자, 나머지는 수식으로 변환한다."""
    if isinstance(line, (list, tuple)):
        return list(line)
    out, pos = [], 0
    for m in re.finditer(r"[가-힣ㄱ-ㅎ][가-힣ㄱ-ㅎ ,.:;()·\-]*", line):
        pre = line[pos:m.start()].strip()
        if pre:
            out.append(E(pre))
        txt = m.group(0)
        if pre or out:
            txt = " " + txt
        out.append(T(txt))
        pos = m.end()
    rest = line[pos:].strip()
    if rest:
        out.append(E(rest))
    return out


def load_sel_solutions():
    """선택과목 23~30번의 (정답, 풀이줄) 을 과목별 데이터 파일에서 읽는다."""
    fn = {"calc": "data_q23_30.py", "prob": "data_p23_30.py", "geo": "data_g23_30.py"}[TRACK]
    src = open(os.path.join(W, fn), encoding="utf-8-sig").read()
    for old, new in [("{a_{n}}^{2}", "a_{n}^{2}"), ("{a_{1}}^{2}", "a_{1}^{2}"), ("neq", "ne"), ("!=", "!`=")]:
        src = src.replace(old, new)
    ns = {}
    exec(src, ns)
    d = ns.get("QS") or ns.get("QP") or ns.get("QG")
    return {n: (str(d[n]["ans"]), d[n]["sol"]) for n in range(23, 31)}


def apply_solutions(ps):
    sols = dict(SOL_COMMON)
    sols.update(load_sel_solutions())
    # 틀: 첫 문제(1번)의 미주 안쪽 문단(원본 그대로)
    en0 = next(ps[3].iter(q("endNote"))).find(q("subList")).findall(q("p"))
    sol_p_tpl = copy.deepcopy(en0[1])
    for idx, n in STEMS.items():
        mark, lines = sols[n]
        en = next(ps[idx].iter(q("endNote")))
        sub = en.find(q("subList"))
        paras = sub.findall(q("p"))
        paras[0].find(".//" + q("t")).text = " " + mark
        for p in paras[1:]:
            sub.remove(p)
        for line in lines:
            np_ = copy.deepcopy(sol_p_tpl)
            run = np_.find(q("run"))
            tpl_eq = first_eq(np_)
            for c in list(run):
                run.remove(c)
            for seg in line_segs(line):
                kind, v = seg[0], seg[1]
                if kind == "t":
                    t = etree.SubElement(run, q("t")); t.text = v
                elif kind == "tab":
                    t = etree.SubElement(run, q("t"))
                    for _ in range(seg[3] if len(seg) > 3 else 1):
                        tb = etree.SubElement(t, q("tab"), width=str(v), leader="0", type="1")
                    tb.tail = seg[2]
                else:
                    run.append(mk_eq(tpl_eq, v)[0])
            etree.SubElement(run, q("t"))
            strip_lineseg(np_)
            sub.append(np_)
        strip_lineseg(paras[0])

    # 정답표 (해설 제목 문단 바로 뒤의 표): 번호/정답 칸이 번갈아 나온다
    tbl = None
    for p in ps[END_IDX_ORIG:]:
        tbl = next(p.iter(q("tbl")), None)
        if tbl is not None:
            break
    cells = list(tbl.iter(q("tc")))
    for n in range(1, 31):
        cell = cells[2 * (n - 1) + 1]
        t = next(x for x in cell.iter(q("t")))
        t.text = sols[n][0]


def fix_footer(ps0, key):
    """바닥글의 총 쪽수: 해설 포함 파일은 자동(전체 쪽수), 문제지만 있는 파일은 문제지 쪽수(12)."""
    foot = next(ps0.iter(q("footer")))
    for t in foot.iter(q("t")):
        if t.text == "16":
            run = t.getparent()
            if key:
                ctrl = etree.Element(q("ctrl"))
                an = etree.SubElement(ctrl, q("autoNum"), num="1", numType="TOTAL_PAGE")
                etree.SubElement(an, q("autoNumFormat"), type="DIGIT", userChar="", prefixChar="", suffixChar="", supscript="0")
                run.remove(t)
                run.insert(0, ctrl)
                etree.SubElement(run, q("t"))
            else:
                t.text = str(TOTAL_STATIC)
            break
