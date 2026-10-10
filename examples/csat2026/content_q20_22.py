# 20~22번 (Opus 출제). content_q.py 의 apply_questions 에서 exec 된다.

def apply_q20_22(ps):
    # ---------- 20 ----------
    # 조건 상자 (ps[615])
    cell = list(ps[615].iter(q("tc")))[0]
    bul = cell.find(".//" + q("t")).text  # 원본 글머리 기호(전용 글꼴 문자) 그대로 사용
    rebuild_cell(cell, [
        (0, [T(bul), E("a_{1}=5`")]),
        (1, [T(bul), E("2"), T(" 이상의 자연수 "), E("n`"), T("에 대하여"), ("tab", 1500, ""),
             E("sum_{k=1}^{n}a_{k}={1} over {2}a_{n}+n^{2}+3n+2`"), T("이다.")]),
    ])
    set_para(ps[616], [T("다음은 "), E("sum_{k=1}^{10}a_{2k}`"), T("의 값을 구하는 과정이다.")])
    # 증명 상자 (ps[617])
    cell = list(ps[617].iter(q("tc")))[0]
    GA = "box{~ left(가 right)~}"
    NA = "box{~ left(나 right)~}"
    DA = "box{~ left(다 right)~}"
    rebuild_cell(cell, [
        (0, [E("2"), T(" 이상의 자연수 "), E("n`"), T("에 대하여 "),
             E("a_{n+1}= sum_{k=1}^{n+1}a_{k}- sum_{k=1}^{n}a_{k}`"), T("이므로")]),
        (1, [T("     "), E("a_{n+1}={1} over {2} left(a_{n+1}-a_{n} right)+" + GA + "`")]),
        (2, [T("이고, 이 식을 정리하면")]),
        (3, [T("     "), E("a_{n}+a_{n+1}=2 times " + GA + "`"), T("    "), E("CDOTS"), E("cdots"), T(" ㉠")]),
        (4, [T("이다. ㉠의 "), E("n`"), T("에 "), E("n+1`"), T("을 대입한 식에서 ㉠을 변끼리 빼면")]),
        (3, [T("     "), E("a_{n+2}-a_{n}=4~ left(n ge 2 right)`"), T("    "), E("CDOTS"), E("cdots"), T(" ㉡")]),
        (5, [T("이다. 한편 "),
             E("sum_{k=1}^{n}a_{k}={1} over {2}a_{n}+n^{2}+3n+2~ left(n ge 2 right)`")]),
        (6, [T("에서 양변에 "), E("n=2`"), T("를 대입하면")]),
        (7, [T("     "), E("a_{2}= " + NA + "`")]),
        (8, [T("이다. ㉡에 의하여 "), E("a_{2},~a_{4},~a_{6},~ cdots`"), T("은 첫째항이 (나)이고 공차가 "),
             E("4`"), T("인 등차수열이므로")]),
        (9, [T("     "), E("sum_{k=1}^{10}a_{2k}= " + DA + "`")]),
        (10, [T("이다.")]),
    ])
    # (질문 문단 ps[618]은 원본과 같은 형식 문장이라 그대로 둔다)

    # ---------- 21 ----------
    set_para(ps[642], [T(" 최고차항의 계수가 "), E("1`"), T("인 삼차함수 "), E("f left(x right)`"),
                       T("가 있다. 실수 "), E("t`"), T("에 대하여 "), E("x`"), T("에 대한 함수 "),
                       E("left| f left(x right)-t right|`"), T("가 미분가능하지 않은 실수 "), E("x`"),
                       T("의 개수를 "), E("g left(t right)`"), T("라 하자. 함수 "), E("f left(x right)`"),
                       T("는 다음 조건을 만족시킨다.")])
    for i in (643, 644):
        ps[i].getparent().remove(ps[i])
    cell = list(ps[645].iter(q("tc")))[0]
    rebuild_cell(cell, [
        (0, [T("(가) 함수 "), E("g left(t right)`"), T("가 불연속인 실수 "), E("t`"), T("의 값은 "),
             E("-4`"), T("와 "), E("0`"), T("뿐이다.")]),
        (1, [T("(나) 함수 "), E("g left(f left(x right) right)`"), T("가 불연속인 모든 실수 "), E("x`"),
             T("의 값의 합은 "), E("12`"), T("이다.")]),
    ])
    set_para(ps[646], [E("f left(8 right)`"), T("의 값을 구하시오. [4점]")])

    # ---------- 22 ----------
    set_para(ps[686], [T(" 첫째항이 자연수인 수열 "), E("left {a_{n} right }`"), T("이 모든 자연수 "), E("n`"),
                       T("에 대하여")])
    sec_el = ps[686].getparent()
    pos = list(sec_el).index(ps[686])
    center = copy.deepcopy(ps[516])
    set_para(center, [TAB, E("a_{n+1}= cases {``a_{n}-n & & left(a_{n} > n right) #``a_{n}+2n & & left(a_{n} le n right)}`")])
    last = copy.deepcopy(ps[517])
    set_para(last, [T("을 만족시킨다. "), E("a_{7}=7`"), T("이 되도록 하는 모든 "), E("a_{1}`"),
                    T("의 값의 합을 구하시오. [4점]")])
    sec_el.insert(pos + 1, center)
    sec_el.insert(pos + 2, last)
