# 기하 23~30번 (완성된 문제+해설 hwpx 에서 복원한 데이터)
def T(s): return ("t", s)
def E(s): return ("e", s)
TAB = ("tab", 4000, "")

QG = {}

QG[23] = {
    'stem': [T(' 두 벡터 '), E('{ vec{a}}=left(3,``-2 right)`'), T(', '), E('{ vec{b}}=left(1,``4 right)`'), T('에 대하여 '), E('left({ vec{a}}+{ vec{b}} right) bullet { vec{a}}`'), T('의 값은? [2점]')],
    'choices': ['6`', '7`', '8`', '9`', '10'],
    'ans': '③',
    'sol': [
        [E('{ vec{a}}+{ vec{b}}=left(4,``2 right)')],
        [E('left({ vec{a}}+{ vec{b}} right) bullet { vec{a}}=4 times 3+2 times left(-2 right)')],
        [E('THEREFORE left({ vec{a}}+{ vec{b}} right) bullet { vec{a}}=8')],
    ],
}

QG[24] = {
    'stem': [T(' 타원 '), E('{x^{2}} over {a^{2}}+{y^{2}} over {12}=1`'), T('의 한 초점의 좌표가 '), E('left(2,``0 right)`'), T('일 때, 이 타원의 장축의 길이는? (단, '), E('a>2 sqrt{3}`'), T(') [3점]')],
    'choices': ['6`', '8`', '10`', '12`', '14'],
    'ans': '②',
    'sol': [
        [E('a^{2}-12=2^{2}')],
        [E('a^{2}=16,~a=4')],
        [E('THEREFORE 2a=8')],
    ],
}

QG[25] = {
    'stem': [T(' 좌표공간의 점 '), E('{rm{A}it} left(2,``-1,``3 right)`'), T('을 '), E('xy`'), T('평면에 대하여 대칭이동한 점을 '), E('{rm{B}it}`'), T(', 점 '), E('{rm{A}it}`'), T('를 '), E('z`'), T('축에 대하여 대칭이동한 점을 '), E('{rm{C}it}`'), T('라 할 때, 삼각형 '), E('{rm{ABC}it}`'), T('의 넓이는? [3점]')],
    'choices': ['3 sqrt{5}`', '4 sqrt{5}`', '2 sqrt{30}`', '5 sqrt{5}`', '6 sqrt{5}'],
    'ans': '⑤',
    'sol': [
        [E('{rm{B}it} left(2,``-1,``-3 right),~{rm{C}it} left(-2,``1,``3 right)')],
        [E('{ vec{rm{AB}it}}=left(0,``0,``-6 right),~{ vec{rm{AC}it}}=left(-4,``2,``0 right),~{ vec{rm{AB}it}} bullet { vec{rm{AC}it}}=0')],
        [E('{ bar{rm{AB}it}}=6,~{ bar{rm{AC}it}}=2 sqrt{5}')],
        [E('THEREFORE {1} over {2} times 6 times 2 sqrt{5}=6 sqrt{5}')],
    ],
}

QG[26] = {
    'stem': [T(' 두 초점이 '), E('{rm{F}it}`'), T(', '), E("{rm{F}it}`'`"), T('인 쌍곡선 '), E('{x^{2}} over {4}-{y^{2}} over {b^{2}}=1`'), T(' 위의 점 '), E('{rm{P}it} left(4,``k right)`'), T('에 대하여 '), E("{ bar{{rm{PF}it}`'}}=2 { bar{rm{PF}it}}`"), T('이다. 점 '), E('{rm{P}it}`'), T('에서의 접선이 '), E('y`'), T('축과 만나는 점을 '), E('{rm{R}it}`'), T('라 할 때, 선분 '), E('{rm{PR}it}`'), T('의 길이는? (단, '), E('b`'), T(', '), E('k`'), T('는 양수이고, 점 '), E('{rm{F}it}`'), T('의 '), E('x`'), T('좌표는 양수이다.) [3점]')],
    'choices': ['{8 sqrt{6}} over {3}`', '3 sqrt{6}`', '{10 sqrt{6}} over {3}`', '{11 sqrt{6}} over {3}`', '4 sqrt{6}'],
    'ans': '①',
    'sol': [
        [E("{ bar{{rm{PF}it}`'}}-{ bar{rm{PF}it}}=4`, { bar{{rm{PF}it}`'}}=2 { bar{rm{PF}it}}`"), T(' 에서 '), E("{ bar{rm{PF}it}}=4,~{ bar{{rm{PF}it}`'}}=8")],
        [E('{rm{F}it} left(c,``0 right)`'), T(' 이라 하면 '), E('left(4+c right)^{2}+k^{2}=64,~ left(4-c right)^{2}+k^{2}=16')],
        [E('c=3,~k= sqrt{15},~b^{2}=c^{2}-4=5')],
        [T('접선: '), E('x-{sqrt{15}} over {5}y=1`, {rm{R}it} left(0,``-{sqrt{15}} over {3} right)')],
        [E('THEREFORE { bar{rm{PR}it}}= sqrt{4^{2}+ left({4 sqrt{15}} over {3} right)^{2}}={8 sqrt{6}} over {3}')],
    ],
}

QG[27] = {
    'stem': [T(' 그림과 같이 밑면의 반지름의 길이가 '), E('3`'), T('이고 높이가 '), E('4`'), T('인 원기둥이 있다. 원기둥의 한 밑면의 둘레 위의 세 점 '), E('{rm{A}it}`'), T(', '), E('{rm{B}it}`'), T(', '), E('{rm{H}it}`'), T('에 대하여 선분 '), E('{rm{AB}it}`'), T('는 이 밑면의 지름이고 '), E('{ bar{rm{AH}it}}=2`'), T('이다. 점 '), E('{rm{H}it}`'), T('를 지나고 이 밑면에 수직인 직선이 원기둥의 다른 밑면의 둘레와 만나는 점을 '), E('{rm{P}it}`'), T('라 할 때, 삼각형 '), E('{rm{PAB}it}`'), T('의 넓이는? [3점]')],
    'choices': ['2 sqrt{30}`', '8 sqrt{2}`', '2 sqrt{35}`', '4 sqrt{11}`', '6 sqrt{5}'],
    'fig': {'kind': 'png'},
    'ans': '④',
    'sol': [
        [E('angle{rm{AHB}it}={pi} over {2}`'), T(' 이므로 '), E('{ bar{rm{HB}it}}= sqrt{6^{2}-2^{2}}=4 sqrt{2}')],
        [T('점 '), E('{rm{H}it}`'), T(' 에서 선분 '), E('{rm{AB}it}`'), T(' 에 내린 수선의 발을 '), E('{rm{K}it}`'), T(' 라 하면 '), E('{ bar{rm{HK}it}}={2 times 4 sqrt{2}} over {6}={4 sqrt{2}} over {3}')],
        [T('삼수선의 정리에 의하여 선분 '), E('{rm{PK}it}`'), T(' 와 직선 '), E('{rm{AB}it}`'), T(' 는 서로 수직이다.')],
        [E('{ bar{rm{PK}it}}= sqrt{4^{2}+ left({4 sqrt{2}} over {3} right)^{2}}={4 sqrt{11}} over {3}')],
        [E('THEREFORE {1} over {2} times 6 times {4 sqrt{11}} over {3}=4 sqrt{11}')],
    ],
}

QG[28] = {
    'stem': [T(' 그림과 같이 한 모서리의 길이가 '), E('6`'), T('인 정사면체 '), E('{rm{ABCD}it}`'), T('가 있다. 점 '), E('{rm{A}it}`'), T('를 중심으로 하고 세 직선 '), E('{rm{BC}it}`'), T(', '), E('{rm{CD}it}`'), T(', '), E('{rm{DB}it}`'), T('에 모두 접하는 구를 '), E('S`'), T('라 하자. 구 '), E('S`'), T('와 평면 '), E('{rm{BCD}it}`'), T('가 만나서 생기는 원으로 둘러싸인 부분의 평면 '), E('{rm{ABC}it}`'), T(' 위로의 정사영의 넓이는? [4점]')],
    'choices': ['{pi} over {3}`', 'pi`', '{3} over {2} pi`', '2 pi`', '3 pi'],
    'fig': {'kind': 'png'},
    'ans': '②',
    'sol': [
        [T('점 '), E('{rm{A}it}`'), T(' 와 직선 '), E('{rm{BC}it}`'), T(' 사이의 거리는 정삼각형 '), E('{rm{ABC}it}`'), T(' 의 높이 '), E('3 sqrt{3}`'), T(' 이므로 구 '), E('S`'), T(' 의 반지름의 길이는 '), E('3 sqrt{3}')],
        [T('점 '), E('{rm{A}it}`'), T(' 에서 평면 '), E('{rm{BCD}it}`'), T(' 에 내린 수선의 발 '), E('{rm{G}it}`'), T(' 는 삼각형 '), E('{rm{BCD}it}`'), T(' 의 무게중심이고 '), E('{ bar{rm{AG}it}}=2 sqrt{6}')],
        [T('원의 반지름의 길이는 '), E('sqrt{27-24}= sqrt{3}`,'), T(' 원의 넓이는 '), E('3 pi')],
        [T('두 평면 '), E('{rm{BCD}it},~{rm{ABC}it}`'), T(' 가 이루는 각의 크기를 '), E('theta`'), T(' 라 하면 '), E('cos theta={1} over {3}')],
        [E('THEREFORE 3 pi times {1} over {3}= pi')],
    ],
}

QG[29] = {
    'stem': [T(' 그림과 같이 초점이 '), E('{rm{F}it} left(p,``0 right)~ left(p>0 right)`'), T('인 포물선 '), E('y^{2}=4px`'), T('와 두 초점이 '), E('{rm{F}it}`'), T(', '), E("{rm{F}it}`' left(-p,``0 right)`"), T('인 타원이 제1사분면에서 만나는 점을 '), E('{rm{P}it}`'), T('라 하자. 점 '), E('{rm{P}it}`'), T('에서 포물선의 준선에 내린 수선의 발을 '), E('{rm{H}it}`'), T('라 할 때, 두 삼각형 '), E("{rm{PHF}it}`'`"), T(', '), E("{rm{PF}it}`'{rm{F}it}`"), T('의 넓이의 비가 '), E('5`:`4`'), T('이고 타원의 장축의 길이가 '), E('18`'), T('이다. 삼각형 '), E("{rm{PF}it}`'{rm{F}it}`"), T('의 넓이를 '), E('S`'), T('라 할 때, '), E('S^{2}`'), T('의 값을 구하시오. [4점]')],
    'fig': {'kind': 'png'},
    'ans': 486,
    'sol': [
        [E('{rm{P}it} left(x_{1},``y_{1} right)`'), T(' 이라 하면 '), E('{ bar{rm{PH}it}}={ bar{rm{PF}it}}=x_{1}+p')],
        [E('{1} over {2} left(x_{1}+p right)y_{1}`:`{1} over {2} times 2p times y_{1}=5`:`4`'), T(' 에서 '), E('x_{1}={3} over {2}p')],
        [E("y_{1}^{2}=4px_{1}=6p^{2}`, { bar{rm{PF}it}}={5} over {2}p`, { bar{{rm{PF}it}`'}}= sqrt{{25} over {4}p^{2}+6p^{2}}={7} over {2}p")],
        [E("{ bar{rm{PF}it}}+{ bar{{rm{PF}it}`'}}=6p=18`"), T(' 에서 '), E('p=3')],
        [E('S={1} over {2} times 2p times y_{1}= sqrt{6}p^{2}=9 sqrt{6}')],
        [E('THEREFORE S^{2}=486')],
    ],
}

QG[30] = {
    'stem': [T(' 좌표평면에서 '), E('{ bar{rm{AB}it}}={ bar{rm{AC}it}}=5`'), T(', '), E('{ bar{rm{BC}it}}=6`'), T('인 삼각형 '), E('{rm{ABC}it}`'), T('에 대하여 두 점 '), E('{rm{P}it}`'), T(', '), E('{rm{Q}it}`'), T('가')],
    'center': [TAB, E('2 { vec{rm{PA}it}}+{ vec{rm{PB}it}}+{ vec{rm{PC}it}}={ vec{0}},~~~left|` { vec{rm{QB}it}}+{ vec{rm{QC}it}}`right| = left|` { vec{rm{QA}it}}`right|`')],
    'tail': [T('를 만족시킨다. '), E('{ vec{rm{QP}it}} bullet { vec{rm{QA}it}}`'), T('의 최댓값을 '), E('M`'), T(', 최솟값을 '), E('m`'), T('이라 할 때, '), E('M+m={q} over {p}`'), T('이다. '), E('p+q`'), T('의 값을 구하시오. (단, '), E('p`'), T('와 '), E('q`'), T('는 서로소인 자연수이다.) [4점]')],
    'ans': 457,
    'sol': [
        [T('선분 '), E('{rm{BC}it}`'), T(' 의 중점을 '), E('{rm{M}it}`'), T(' 이라 하면 '), E('2 { vec{rm{PA}it}}+2 { vec{rm{PM}it}}={ vec{0}}`'), T(' 이므로 점 '), E('{rm{P}it}`'), T(' 는 선분 '), E('{rm{AM}it}`'), T(' 의 중점')],
        [E('{rm{M}it} left(0,``0 right),~{rm{A}it} left(0,``4 right),~{rm{B}it} left(-3,``0 right),~{rm{C}it} left(3,``0 right)`'), T(' 으로 놓으면 '), E('{rm{P}it} left(0,``2 right)')],
        [E('2 left|` { vec{rm{QM}it}}`right| = left|` { vec{rm{QA}it}}`right|`'), T(' 에서 점 '), E('{rm{Q}it}`'), T(' 는 원 '), E('x^{2}+ left(y+{4} over {3} right)^{2}= left({8} over {3} right)^{2}`'), T(' 위의 점')],
        [T('선분 '), E('{rm{PA}it}`'), T(' 의 중점 '), E('{rm{N}it} left(0,``3 right)`'), T(' 에 대하여 '), E('{ vec{rm{QP}it}} bullet { vec{rm{QA}it}}= left|` { vec{rm{QN}it}}`right| ^{2}-1')],
        [E('{5} over {3} le left|` { vec{rm{QN}it}}`right| le 7`'), T(' 이므로 '), E('M=48,~m={16} over {9}')],
        [E('M+m={448} over {9}`, THEREFORE p+q=9+448=457')],
    ],
}
