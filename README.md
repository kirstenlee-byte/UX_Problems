# Squad Research Roadmap Dashboard

22개 스쿼드의 OKR을 기반으로 **시기별 UX 리서치를 자동 추천**하는 모니터링 대시보드.

---

## 실행 방법

별도 설치 없음. 브라우저에서 바로 열기:

```
squad-research-roadmap.html
```

---

## 주요 기능

### 📊 전체 현황
- 22개 스쿼드 카드 그리드
- 스쿼드별 긴급도 자동 계산 (Critical / High / Normal)
- 전체 OKR 수, 추천 리서치 수, 이번 달 착수 필요 항목 요약

### 📅 리서치 로드맵
- Jan ~ Dec 2026 간트 차트
- 스쿼드 · 카테고리 · 리서치 유형 · 우선순위 필터
- 현재 시점(3월) 마커

### 🔍 스쿼드 상세
- 스쿼드 선택 → OKR별 추천 리서치 타이밍 + Decision Point
- 즉시 착수 필요 항목 자동 강조

---

## 추천 엔진 구조

OKR 카테고리(6종) → 리서치 메서드 자동 매핑 → 분기 기준 착수 시점 역산

| 카테고리 | 주요 추천 리서치 |
|---|---|
| 신규 획득 | 페르소나 인터뷰, 경쟁사 분석, 퍼널 분석, A/B 테스트 |
| 리텐션 | 이탈 인터뷰, 코호트 분석, Magic Moment 분석, 재참여 실험 |
| 수익화 | WTP 설문, 구매 결정 인터뷰, 결제 퍼널 분석, 프라이싱 A/B |
| 인게이지먼트 | 다이어리 스터디, 사용성 테스트, 참여도 분석, 만족도 설문 |
| 품질/성능 | 휴리스틱 평가, 사용성 테스트, 성능 측정, 접근성 감사 |
| 운영 효율 | 프로세스 인터뷰, 운영 지표 분석, 워크플로우 조사 |

---

## OKR 데이터 수정 방법

`squad-research-roadmap.html` 내 `SQUADS` 배열을 직접 수정:

```js
const SQUADS = [
  {
    id: 1,
    name: 'Growth',
    color: '#4ade80',
    okrs: [
      {
        obj: 'OKR 목표 텍스트',
        krs: ['KR1', 'KR2', 'KR3'],
        cat: 'acquisition', // acquisition | retention | revenue | engagement | quality | ops
        q: 1               // 1 | 2 | 3 | 4
      }
    ]
  },
  // ...
];
```

---

## 파일 목록

| 파일 | 설명 |
|---|---|
| `squad-research-roadmap.html` | 실행 파일 (단일 HTML) |
| `squad-research-roadmap-notes.md` | 설계 문서 및 상세 맥락 |
| `README.md` | 이 파일 |

---

## 기술 스택

HTML · CSS · Vanilla JS — 외부 의존성 없음
