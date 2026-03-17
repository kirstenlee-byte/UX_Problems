# UX Dashboard 작업 대화 기록

> 파일 대상: `ux_dashboard_4.html`
> 기간: 2026년 3월

---

## 1. JA → JP 전환 + 국가 뱃지 토글 제거 + 필터 드롭다운 추가

**요청**
1. JA → JP 로 바꿔줘.
2. KR 뱃지를 눌러서 JP로 바뀌면 안돼. 반대도 마찬가지야.
3. 대신 칼럼에 국가를 필터링해서 볼 수 있는 컴포넌트가 추가되면 좋겠어. 예를 들어 '국가↓'를 누르면 '전체', 'KR', 'JP'를 선택할 수 있게

**작업 내용**
- `I18N.ja` → `I18N.jp`, 버튼/클래스/ID 전체 rename
- KR/JP 뱃지 클릭 시 전환되던 동작 제거 (`cursor: default`, hover 효과 제거)
- 테이블 칼럼 헤더에 "국가🔽" 드롭다운 추가 → 전체 / KR / JP 필터링 기능 구현
- `currentOriginFilter` 전역 변수, `toggleOriginDropdown()`, `setOriginFilter()` 함수 추가
- `renderTable()`에 필터 로직 적용

---

## 2. 필터 바 divider + JP 테이블 헤더 번역

**요청**
- 이슈목록의 심각도 필터와 개발가능 버튼은 구분해야 할듯. 1 Irritant와 개발 가능 사이에 divider 넣어줘.
- 일본 이슈목록 테이블의 '개발 가능 여부', '대략적 개발 방향', '자료' → 일본어로 번역해줘

**작업 내용**
- `<span class="filter-divider"></span>` 추가 (1px 세로 구분선)
- I18N 키 추가: `thServerSpec`, `thDevDir`, `thMedia` (KR/JP 양쪽)
- JP 번역: 開発可否 / 開発概要 / 資料
- `applyI18n()`에 반영

---

## 3. 신규 이슈(174, 175, 176) 검색 안 되던 문제 수정

**요청**
- 어제 넣은 데이터들은 검색이 안돼. 이슈 내용을 입력했을 때 검색 결과가 나오게 해줘

**원인**
- 검색이 `problem_rewritten`, `problem`, `ux_problem` 필드만 대상으로 했음
- `related_url`(Jira URL 포함)과 이슈 `id` 숫자가 검색 대상에서 누락

**작업 내용**
- `getFiltered()` 함수에 `related_url`, `String(id)` 필드 추가
- 모든 필드에 null safety (`|| ""`) 처리

---

## 4. 차트 너비 통일 + JP 번역 확장 + 국가🔽 점선 밑줄

**요청**
- 'Funnel 단계별 이슈 수' 차트와 'UX 문제 유형별 빈도' 차트의 width를 '한국 요청' / '일본 요청' 그래프 크기에 맞춰줄 수 있어?
- 일본어 탭의 '한국 요청', '일본 요청', '해결 완료 n건', '개발 가능'도 일본어로 바꿔줘.
- 일본어 탭 툴팁 설명도 일본어로 바꿔줘.
- '국가↓' 칼럼 제목을 '국가🔽'로 바꾸고, 점선을 그려서 클릭 가능하다는 것을 보여줘.

**작업 내용**
- `country-row` gap 16px → 24px (charts-row와 통일)
- `↓` → `🔽`, `.origin-filter-btn`에 dotted underline CSS 적용
- I18N 키 추가: `countryKr`, `countryJp`, `countryTotal`, `countryUnit`, `undecided`, `serverSpec`
- JP 툴팁 번역: `.tooltip-item-jp`, `.tooltip-prob-desc-jp` div 추가, CSS로 언어별 show/hide
- `refreshOriginCards()`에서 `t()` 통해 텍스트 렌더링

---

## 5. JP 탭 '해결 완료 0건' 미번역 수정 + 차트 반응형

**요청**
1. 일본어 탭의 '해결 완료 0건'은 번역되지 않음
2. Funnel/UX 문제 차트가 중간 사이즈 화면에도 5:5 크기를 유지했으면 좋겠어. 모바일 크기가 되었을 때 세로로 나오는 반응형으로 수정해줘

**원인 및 작업 내용**
- `applyI18n()` 에서 `refreshOriginCards()` 호출 누락 → 추가
- `.charts-row`를 960px 미디어쿼리에서 제외
- 600px 이하에서만 `.charts-row { grid-template-columns: 1fr; }` 적용

---

## 6. 국가 요청 차트에서 '미정' 제거

**요청**
- 요청 차트에서 '미정' 부분은 빼줘

**작업 내용**
- `refreshOriginCards()`의 `segs` 배열에서 `{val:none, color:'var(--border)'}` 제거
- legend에서 미정 항목 제거

---

## 7. '해결 완료'만 국가 카드에 표시

**요청**
- 'status'에서 '해결완료'만 상단 '한국 요청', '일본 요청'에 반영되어야 해

**작업 내용**
- `segs` 배열을 `[{val:done, color:'#4ade80'}]` 단일 항목으로 축소
- legend도 해결 완료 단일 항목만 유지

---

## 8. 진행 상태 세로 차트 추가

**요청**
- '미정', '진행 예정', '진행 중', '해결 완료'의 개수가 차트로도 보여지면 좋을 것 같아. 막대에는 일본 요청과 한국 요청이 구분되었으면 좋겠어.

**UI 옵션 제안 후 선택**
- A. 별도 카드에 그룹형 가로 막대
- B. 국가 카드 내 확장
- C. **스택 바 (1개 막대)** ← 선택

**1차 구현 후 피드백**
- "너무 이상한데? 새로 차트로 보여줬으면 좋겠어."
- 이전 카드 제거 → 각 국가 카드 하단에 버튼 방식으로 변경

**최종 구현**
- 각 카드 하단에 **"진행 상황 상세 보기 ▾"** 버튼 추가
- 클릭 시 카드 내부에서 세로 바 차트 슬라이드 다운
- 4개 막대: 미정(회색) · 진행 예정(파랑) · 진행 중(주황) · 해결 완료(초록)
- 버튼 클릭 시 KR/JP 양쪽 동시 열림/닫힘 동기화
- JP 탭: "進捗の詳細を見る" / "閉じる"

---

## 툴팁 내용

### Funnel 단계별 이슈 수 — Severity Scale

| 등급 | EN | JP |
|---|---|---|
| **4 Unusable** | The user is not able to or will not want to use a particular part of the product because of the way that the product has been designed and implemented. | 製品の設計・実装により、ユーザーが製品の特定部分を使用できない、または使いたくない状態。 |
| **3 Severe** | The user will probably use or attempt to use the product here, but will be severely limited in his or her ability to do so. | ユーザーは製品を使用または使用を試みるが、深刻な制約が伴う。 |
| **2 Moderate** | The user will be able to use the product in most cases, but will have to undertake some moderate effort in getting around the problem. | ほとんどの場合、製品を使用できるが、問題を回避するためにある程度の努力が必要。 |
| **1 Irritant** | The problem occurs only intermittently, can be circumvented easily, or is dependent on a standard that is outside the product's boundaries. Could also be a cosmetic problem. | 問題は散発的・容易に回避可能か、製品範囲外の基準に関わるもの。外観や美観上の問題も含む。 |

### UX 문제 유형별 빈도 — UX問題タイプ

| 유형 | JP |
|---|---|
| **UX Writing Fail** | ラベル・案内文など、顧客が認識する言葉や文章に関する問題。 |
| **Priority Fail** | 画面上の優先順位が不明確で生じる問題。 |
| **Cognitive Load Problem** | 顧客に認知的負荷を与え、選択を困難にする問題。 |
| **Domain Knowledge Problem** | 顧客に高い専門知識を要求する問題。 |
| **Expectation Fail** | 操作に対する出力が顧客の期待と合わず生じる問題全般。 |
| **UX Consistency Fail** | 一貫性のないUX/UIにより生じる問題。 |
| **Poor UX Problem** | 製品が備えるべき基本的な機能性が不足している問題。 |
