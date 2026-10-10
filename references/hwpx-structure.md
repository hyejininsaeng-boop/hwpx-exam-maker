# hwpx 양식 구조 메모 (2026 수능 수학 양식에서 확인한 사실)

## 파일
- `.hwp`(이진)는 압축을 풀 수 없다 → 한글 COM(`HWPFrame.HwpObject`)으로 `Open(hwp,"HWP","")` 후 `SaveAs(hwpx,"HWPX","")` 로 **복사본**을 만든다. `RegisterModule("FilePathCheckDLL","FilePathCheckerModule")` 로 보안 대화상자를 피한다.
- hwpx = zip. 본문 `Contents/section0.xml`(문단 전부가 `<hs:sec>`의 직계 자식 `<hp:p>`), 서식 `Contents/header.xml`, 파일 목록 `Contents/content.hpf`, 그림 `BinData/`.
- 재압축: `mimetype`을 **압축 없이 첫 번째**로 넣고 나머지는 deflate.
- 같은 시험의 과목별 양식(미적분/확통/기하)은 공통 1~22번 구간의 문단 번호가 **같다**(문단 모양 번호 `pr`만 다름). 선택과목 구간만 다르다.

## 문단 종류
| 종류 | 특징 |
|---|---|
| 문제 줄기 | 첫 run에 `<hp:endNote>`(문제 번호 자동 표시 + 해설 내용), 둘째 run에 글자/수식 |
| 가운데 수식 줄 | 맨 앞 `<hp:t>`에 `<hp:tab width=4000>` 하나(들여쓰기) |
| 점수 줄 | 오른쪽 정렬 `[3점]` (줄기 안에 붙어 있는 문제도 있음) |
| 선택지 | 한 문단에 `① 수식 <탭> ② 수식 ...`, 탭 폭 = K − (앞 선택지 수식 폭). K: 5개 한 줄 4684, 3+2줄 8848, 2개씩 14032 |
| 상자 | `<hp:tbl>` 1x1, 칸 안에 문단 여러 개(`subList`) |
| 그림 | 글자처럼 취급(`treatAsChar=1`)되는 `<hp:pic>`; 크기 정보가 여러 곳(아래) |
| 빈 문단 | `pr=4`의 빈 문단 덩어리 = 원본이 여백을 만드는 방식 |

## 쪽·단 배치
- 원본은 빈 문단 개수로 문제 위치를 잡는다(문제 길이가 바뀌면 틀어짐). → 문제를 **쪽/단 첫 문단에 `pageBreak="1"`/`columnBreak="1"`** 로 고정하고, **단의 마지막 문제 뒤 빈 문단은 지운다**. 단 안에서 두 문제 사이의 빈 문단은 유지.
- "확인 사항" 상자를 단 맨 아래에 두려면 그 앞 문제(선택 30번)의 빈 문단을 지우지 않는다.

## 문제 번호 / 해설
- 번호 = 미주 번호(자동). 미주 안: 첫 문단 `autoNum` + 정답(" ②" 또는 " 27"), 이어서 풀이 줄들(수식 문단).
- 문제지만: 미주 run을 일반 글자 `"N."` 로 교체(같은 글꼴 `charPr`), 해설 쪽 제거(문서 끝 해설 제목·정답표 표 삭제).
- 해설 포함: 미주 유지, 문서 끝의 `해설 제목 문단(pageBreak=1)` + `정답표 표(6행x10열, 번호/정답 칸이 번갈아)` 유지하고 정답 칸 글자만 교체.
- 바닥글: `autoNum numType="PAGE"`(현재 쪽) + 고정 글자 `16`(총 쪽수). 해설 포함 파일은 고정 글자를 `autoNum numType="TOTAL_PAGE"`로 교체, 문제지만이면 실제 쪽수(12) 글자로.

## 그림 교체
- `hc:img binaryItemIDRef="imageN"` 이 가리키는 `BinData/imageN.<확장자>` 와 `content.hpf` 의 해당 `opf:item`(href, media-type)을 PNG로 맞춘다.
- 크기: `orgSz`/`imgRect`/`imgClip` = (픽셀 × 75), `curSz`/`sz` = 표시 크기(inch × 7200), `rotationInfo` 중심 = 표시 크기/2, `renderingInfo` 안 0이 아닌 `scaMatrix` = 표시/원본.
- 그림 파일은 **RGB PNG, 해상도(dpi) 정보 없음**이어야 한글이 읽는다(RGBA·dpi 있는 PNG는 안 보였음).
- 안 쓰는 원본 그림은 `BinData`와 `content.hpf` 목록에서 모두 제거(원본 기출 그림이 남지 않게).

## 수식 객체
- `<hp:equation>` 안 `<hp:script>`(한글 수식 문법), `<hp:sz width height>`, 속성 `baseLine`. **한글은 열고 저장해도 크기를 다시 계산하지 않는다.**
- 크기 측정: COM `HAction.GetDefault("EquationCreate", HParameterSet.HEqEdit.HSet)` → `SetItem("String", 식)`, `SetItem("BaseUnit",1100)`, `SetItem("EqFontName","HYhwpEQ")` → `Execute` → 문서를 hwpx로 저장 → 수식 순서대로 `sz`·`baseLine` 읽기(`sizes.py`).
- 복사한 수식은 `id`·`zOrder`를 새로 부여하고, 원 제작자 이름이 든 `shapeComment`는 제거한다.

## 선택 구간 인덱스 (2026 양식)
미적분 714~1081 / 확통 719~1080 / 기하 708~1061 (헤더 글상자, 5지선다형 라벨 → 문제들 → 확인 사항 상자). 정확한 문단 번호는 `examples/csat2026/content_q.py`.
