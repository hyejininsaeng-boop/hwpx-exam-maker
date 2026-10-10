# hwpx-exam-maker

한글(.hwp/.hwpx) 시험지 **양식은 그대로 두고, 문제만 새로 출제**해서 `.hwpx` 문제지(+정답표·해설)를 만드는 도구입니다.
2026학년도 수능 수학(미적분·확률과통계·기하) 양식으로 "문제+해설" 3종을 다시 만드는 예제가 들어 있고, 같은 방법으로 다른 시험지 양식에도 적용할 수 있습니다.

## 먼저 알아둘 것

| 필요한 것 | 설명 |
|---|---|
| Windows + **한컴오피스(한글)** | 양식 변환과 수식 크기 측정에 한글을 직접 사용합니다. |
| Python 3.10 이상 | `pip install -r requirements.txt` |
| **본인이 구한 원본 `.hwp` 양식** | 수능 시험지는 한국교육과정평가원의 저작물이라 이 저장소에 **포함하지 않았습니다**. 직접 내려받아 사용하세요. |

> 이 저장소의 예제 문제·그림은 새로 만든 것입니다. 원본 수능 문제·그림은 들어 있지 않습니다.
> 저작권이 있는 원본 시험지와 그것으로 만든 파일을 공개 저장소에 올리지 마세요.

## 빠른 시작

```
pip install -r requirements.txt
python -X utf8 -I scripts\setup_work.py <원본폴더>\work
cd <원본폴더>\work
python -X utf8 -I build_all.py --out out --reconvert
```

- `<원본폴더>` 에는 `2026학년도 수능 수학(미적분).hwp`, `(확통).hwp`, `(기하).hwp` 가 있어야 합니다.
- 결과는 `work\out` 에 만들어집니다. 완성본이 있는 폴더를 `--out` 으로 주면 `--yes` 를 붙여야 덮어씁니다.
- 자세한 절차, 수식 문법 함정, 검수 체크리스트는 [SKILL.md](SKILL.md) 와 `references/` 를 보세요.

## 구성

- `scripts/` 엔진과 도구 (빌더, 수식 크기 측정, 그림 도구, 양식 분석 등)
- `examples/csat2026/` 2026 수능 3종 예제 데이터(새로 출제한 문제·해설)와 그림 코드
- `references/` 한글 수식 문법, hwpx 구조, 출제 에이전트 지시문, 검수 체크리스트
- `SKILL.md` [Claude Code](https://claude.com/claude-code) 스킬 설명서 (스킬 폴더로 쓸 때)

## 한계

- 한글 프로그램 없이는 동작하지 않습니다(Windows 전용).
- 다른 양식에 적용하려면 `scripts/analyze_template.py` 로 구조를 분석하고 내용 파일을 새로 써야 합니다.
