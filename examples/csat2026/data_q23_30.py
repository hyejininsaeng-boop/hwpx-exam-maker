# 미적분 23~30번 (새로 출제). 정답 검증은 sympy로 완료.
def T(s): return ("t", s)          # 일반 글자
def E(s): return ("e", s)          # 한글(HWP) 수식 문법의 수식
TAB = ("tab", 4000, "")            # 가운데 수식 줄 맨 앞 들여쓰기

QS = {}

# ---------- 23 (함수의 극한) ----------
QS[23] = {
    "stem": [T(" "), E("lim_{x rarrow 0}{e^{2x}-1} over {tan 4x}`"), T("의 값은? [2점]")],
    "choices": ["{1} over {4}`", "{1} over {2}`", "1`", "2`", "4"],
    "ans": "②",
    "sol": [
        "lim_{x rarrow 0}{e^{2x}-1} over {tan 4x}= lim_{x rarrow 0} left({e^{2x}-1} over {2x} times {4x} over {tan 4x} times {2x} over {4x} right)",
        "=1 times 1 times {1} over {2}={1} over {2}",
    ],
}

# ---------- 24 (정적분: 부분적분) ----------
QS[24] = {
    "stem": [T(" "), E("int_{1}^{e} left(2x+1 right) ln x dx`"), T("의 값은? [3점]")],
    "choices": ["{e^{2}-3} over {2}`", "{e^{2}-1} over {2}`", "{e^{2}+1} over {2}`",
                "{e^{2}+3} over {2}`", "{e^{2}+5} over {2}"],
    "ans": "④",
    "sol": [
        "int_{1}^{e} left(2x+1 right) ln x dx= left[ left(x^{2}+x right) ln x right]_{1}^{e}- int_{1}^{e}{x^{2}+x} over {x}dx",
        "= left(e^{2}+e right)- left[{1} over {2}x^{2}+x right]_{1}^{e}",
        "= left(e^{2}+e right)- left({e^{2}} over {2}+e-{3} over {2} right)",
        "={e^{2}+3} over {2}",
    ],
}

# ---------- 25 (수열의 극한: 급수 조건) ----------
QS[25] = {
    "stem": [T(" 수열 "), E("left {a_{n} right }`"), T("이")],
    "center": [TAB, E("sum_{n=1}^{inf} left({a_{n}} over {n}-3 right)=5`")],
    "tail": [T("를 만족시킬 때, "), E("lim_{n rarrow inf}{na_{n}+2n^{2}} over {{a_{n}}^{2}+n}`"),
             T("의 값은? [3점]")],
    "choices": ["{1} over {3}`", "{4} over {9}`", "{5} over {9}`", "{2} over {3}`", "{7} over {9}"],
    "ans": "③",
    "sol": [
        "sum_{n=1}^{inf} left({a_{n}} over {n}-3 right)`이 수렴하므로 lim_{n rarrow inf} left({a_{n}} over {n}-3 right)=0",
        "THEREFORE lim_{n rarrow inf}{a_{n}} over {n}=3",
        "lim_{n rarrow inf}{na_{n}+2n^{2}} over {{a_{n}}^{2}+n}= lim_{n rarrow inf}{{a_{n}} over {n}+2} over {left({a_{n}} over {n} right)^{2}+{1} over {n}}",
        "={3+2} over {9+0}={5} over {9}",
    ],
}

# ---------- 26 (입체도형의 부피: 단면 반원) ----------
QS[26] = {
    "stem": [T(" 그림과 같이 곡선 "), E("y= sqrt{xe^{x}}`"), T("와 "), E("x`"), T("축 및 두 직선 "),
             E("x=1`"), T(", "), E("x=2`"), T("로 둘러싸인 부분을 밑면으로 하는 입체도형이 있다. 이 입체도형을 "),
             E("x`"), T("축에 수직인 평면으로 자른 단면이 모두 밑면 위의 선분을 지름으로 하는 반원일 때, "
                       "이 입체도형의 부피는? [3점]")],
    "choices": ["{pi e^{2}} over {8}`", "{pi left(e^{2}+e right)} over {8}`", "{pi e^{2}} over {4}`",
                "{pi left(e^{2}+e right)} over {4}`", "{pi e^{2}} over {2}"],
    "ans": "①",
    "sol": [
        "S left(x right)={1} over {2} pi left({sqrt{xe^{x}}} over {2} right)^{2}={pi} over {8}xe^{x}",
        "V= int_{1}^{2}{pi} over {8}xe^{x}dx={pi} over {8} left[ left(x-1 right)e^{x} right]_{1}^{2}",
        "={pi} over {8} left(e^{2}-0 right)={pi e^{2}} over {8}",
    ],
    "fig": {"expr": "np.sqrt(x*np.exp(x))", "a": 1, "b": 2, "section": "반원"},
}

# ---------- 27 (매개변수로 나타낸 함수의 미분) ----------
QS[27] = {
    "stem": [T(" 매개변수 "), E("t~ left(t>0 right)`"), T("로 나타내어진 곡선")],
    "center": [TAB, E("x=t^{2}+e^{t-1},~~y=t^{3}+2 ln t`")],
    "tail": [T("를 "), E("C`"), T("라 하자. 곡선 "), E("C`"), T("가 직선 "), E("x=2`"),
             T("와 만나는 점을 "), E("{rm{P}it}`"), T("라 할 때, 곡선 "), E("C`"), T(" 위의 점 "),
             E("{rm{P}it}`"), T("에서의 접선의 기울기는? [3점]")],
    "choices": ["{3} over {5}`", "1`", "{4} over {3}`", "{3} over {2}`", "{5} over {3}"],
    "ans": "⑤",
    "sol": [
        "{dx} over {dt}=2t+e^{t-1} > 0`이므로 x=2`인 t`는 t=1`뿐이다.",
        "{dy} over {dt}=3t^{2}+{2} over {t}",
        "{dy} over {dx}={3t^{2}+{2} over {t}} over {2t+e^{t-1}}",
        "t=1`일 때 {dy} over {dx}={3+2} over {2+1}={5} over {3}",
    ],
}

# ---------- 28 (역함수의 미분과 정적분) ----------
QS[28] = {
    "stem": [T(" 함수")],
    "center": [TAB, E("f left(x right)=x+ ln x~ left(x>0 right)`")],
    "tail": [T("의 역함수를 "), E("g left(x right)`"), T("라 하자. 실수 "), E("t`"), T("에 대하여 곡선 "),
             E("y=g left(x right)`"), T(" 위의 점 "), E("left(t,~g left(t right) right)`"),
             T("에서의 접선의 기울기를 "), E("h left(t right)`"), T("라 할 때, "),
             E("int_{1}^{e+1}{g left(x right)} over {h left(x right)}dx`"), T("의 값은? [4점]")],
    "choices": ["{e^{2}+2e-3} over {2}`", "{e^{2}+4e-3} over {2}`", "{e^{2}+4e-1} over {2}`",
                "{e^{2}+4e+1} over {2}`", "{e^{2}+6e-3} over {2}"],
    "ans": "②",
    "sol": [
        "h left(x right)=g` ' left(x right)={1} over {f` ' left(g left(x right) right)}={1} over {1+{1} over {g left(x right)}}",
        "{g left(x right)} over {h left(x right)}=g left(x right)+1",
        "g left(x right)=s`로 놓으면 x=s+ ln s,~dx= left(1+{1} over {s} right)ds,~g left(1 right)=1,~g left(e+1 right)=e",
        "int_{1}^{e+1} left{g left(x right)+1 right}dx= int_{1}^{e} left(s+1 right) left(1+{1} over {s} right)ds= int_{1}^{e} left(s+2+{1} over {s} right)ds",
        "= left[{1} over {2}s^{2}+2s+ ln s right]_{1}^{e}={e^{2}+4e-3} over {2}",
    ],
}

# ---------- 29 (등비급수, 상자 조건) ----------
QS[29] = {
    "stem": [T(" 첫째항이 자연수인 등비수열 "), E("left {a_{n} right }`"), T("이 다음 조건을 만족시킨다.")],
    "box": [
        [T("모든 자연수 "), E("n`"), T("에 대하여")],
        [TAB, E("sum_{k=n}^{inf}a_{k}={9} over {2}a_{n+1}`")],
        [T("이다.")],
    ],
    "text2": [T("부등식")],
    "center": [TAB, E("11< sum_{n=1}^{inf}{a_{n}}^{2}<17`")],
    "tail": [T("이 성립할 때, "), E("sum_{n=1}^{inf}a_{n}a_{n+1}={q} over {p}`"), T("이다. "),
             E("p+q`"), T("의 값을 구하시오. (단, "), E("p`"), T("와 "), E("q`"),
             T("는 서로소인 자연수이다.) [4점]")],
    "ans": 59,
    "sol": [
        "공비를 r`라 하면 {a_{n}} over {1-r}={9} over {2}a_{n}r~ left(0< left| r right|<1 right)",
        "9r^{2}-9r+2=0`에서 r={1} over {3}`또는 r={2} over {3}",
        "sum_{n=1}^{inf}{a_{n}}^{2}={{a_{1}}^{2}} over {1-r^{2}}: r={1} over {3}`이면 {9} over {8}{a_{1}}^{2},~r={2} over {3}`이면 {9} over {5}{a_{1}}^{2}",
        "11<{9} over {8}{a_{1}}^{2}<17`인 자연수 a_{1}`은 없고, 11<{9} over {5}{a_{1}}^{2}<17`에서 a_{1}=3",
        "sum_{n=1}^{inf}a_{n}a_{n+1}={{a_{1}}^{2}r} over {1-r^{2}}={9 times {2} over {3}} over {{5} over {9}}={54} over {5}",
        "THEREFORE p+q=5+54=59",
    ],
}

# ---------- 30 (미분법 종합: 접선의 y절편 함수) ----------
QS[30] = {
    "stem": [T(" 두 상수 "), E("a`"), T(", "), E("b`"), T("에 대하여 함수 "),
             E("f left(x right)= left(x^{2}+ax+b right)e^{-x}`"), T("이 있다. 실수 "), E("t`"),
             T("에 대하여 곡선 "), E("y=f left(x right)`"), T(" 위의 점 "),
             E("left(t,~f left(t right) right)`"), T("에서의 접선의 "), E("y`"), T("절편을 "),
             E("g left(t right)`"), T("라 하자. 두 함수 "), E("f left(x right)`"), T(", "),
             E("g left(t right)`"), T("가 다음 조건을 만족시킨다.")],
    "box": [
        [T("(가) 함수 "), E("g left(t right)`"), T("가 극값을 갖는 실수 "), E("t`"), T("의 개수는 "),
         E("1`"), T("이다.")],
        [T("(나) "), E("f` ' left(0 right)=0`"), T("이고, 함수 "), E("g left(t right)`"), T("는 "),
         E("t=0`"), T("에서 극값을 갖지 않는다.")],
    ],
    "tail": [T("함수 "), E("g left(t right)`"), T("의 극값을 "), E("M`"), T("이라 할 때, "),
             E("e^{2} times M`"), T("의 값을 구하시오. [4점]")],
    "ans": 18,
    "sol": [
        "g left(t right)=f left(t right)-tf` ' left(t right)`이므로 g` ' left(t right)=-tf` '' left(t right)",
        "f` '' left(t right)=e^{-t}q left(t right),~q left(t right)=t^{2}+ left(a-4 right)t+2-2a+b",
        "f` ' left(0 right)=a-b=0`이므로 b=a,~q left(t right)=t^{2}+ left(a-4 right)t+2-a",
        "q left(0 right) neq 0`이면 g` ' left(t right)`의 부호가 t=0`에서 바뀌므로 (나)에 모순, 따라서 q left(0 right)=2-a=0,~a=b=2",
        "g` ' left(t right)=-t^{2} left(t-2 right)e^{-t}`이므로 극값은 t=2`에서만 갖는다.",
        "g left(t right)= left(t^{3}+t^{2}+2t+2 right)e^{-t},~M=g left(2 right)=18e^{-2}",
        "THEREFORE e^{2} times M=18",
    ],
}
