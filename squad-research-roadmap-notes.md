# Squad Research Roadmap Tracking System
> 작성일: 2026-03-16 | 상태: 초기 프로토타입 완성

---

## 프로젝트 개요

### 목적
22개 스쿼드의 OKR 및 로드맵 상에서 **리서치가 필요한 'Decision Point'를 사전에 포착**하는 모니터링 체계 구축.
각 스쿼드의 OKR을 기반으로 **시기별 리서치 추천 로드맵**을 자동 생성하는 대시보드.

### 핵심 문제 정의
- 개발 완료 후 방향 전환 → 높은 비용 발생
- 로드맵 작성 시 리서치 시점을 놓치는 구조적 문제
- 22개 스쿼드 × 2~3 OKR = 50~66개 OKR의 리서치 계획을 수동 관리 불가

---

## 핵심 개념

### Decision Point란?
로드맵 실행 중 **"이 방향이 맞는가?"를 검증하기 위해 리서치/데이터가 필요한 게이트**.

### Decision Point 발굴 체크리스트
로드맵 아이템 작성 시 아래 중 하나라도 No면 → Decision Point 등록:
- [ ] 이 기능을 만들어야 하는 근거가 데이터로 검증됐나?
- [ ] 유저가 이 방식을 선호한다는 증거가 있나?
- [ ] 기술 구현 방식이 확정됐나?
- [ ] 의존 팀/시스템의 협력이 전제되나?
- [ ] 규제/법적 검토가 필요한가?

---

## 데이터 모델

### OKR 카테고리 (6종)

| 카테고리 | 키 | 색상 | 설명 |
|---|---|---|---|
| 신규 획득 | `acquisition` | `#4ade80` | 신규 유저 획득 관련 OKR |
| 리텐션 | `retention` | `#60a5fa` | 유저 유지/재참여 관련 OKR |
| 수익화 | `revenue` | `#fb923c` | 결제/구독/매출 관련 OKR |
| 인게이지먼트 | `engagement` | `#c084fc` | 기능 사용/참여도 관련 OKR |
| 품질/성능 | `quality` | `#f87171` | UX 품질/기술 성능 관련 OKR |
| 운영 효율 | `ops` | `#94a3b8` | 내부 프로세스/생산성 관련 OKR |

### 리서치 유형 (3종)

| 유형 | 키 | 색상 |
|---|---|---|
| 질적 리서치 | `qual` | `#a78bfa` |
| 양적 리서치 | `quant` | `#34d399` |
| 2차 리서치/분석 | `secondary` | `#fbbf24` |

### 리서치 항목 스키마
```js
{
  name: string,          // 리서치 방법명
  type: 'qual' | 'quant' | 'secondary',
  wb: number,            // weeksBefore — 분기 마일스톤 몇 주 전에 착수
  dur: number,           // duration — 수행 기간 (주)
  pri: 'critical' | 'high' | 'medium',
  desc: string,          // 리서치 목적 설명
  dp: string,            // 이 리서치가 답해야 할 Decision Point 질문
}
```

### 타이밍 계산 로직
```js
// 분기 마일스톤 기준 역산
// Q1 = 3월, Q2 = 6월, Q3 = 9월, Q4 = 12월
function getResearchTiming(quarter, weeksBefore, duration) {
  const milestone = quarter * 3; // 해당 분기 마지막 월
  const startMonth = Math.max(1, Math.min(12, Math.round(milestone - weeksBefore / 4.33)));
  const endMonth   = Math.min(12, Math.max(startMonth + 1, startMonth + Math.ceil(duration / 4.33)));
  return { startMonth, endMonth };
}
```

---

## 리서치 추천 엔진

### OKR 카테고리별 추천 리서치 메서드

#### 신규 획득 (acquisition)
| 순서 | 메서드 | 유형 | 착수 시점 | 기간 | 우선순위 | Decision Point |
|---|---|---|---|---|---|---|
| 1 | 타겟 페르소나 심층 인터뷰 | 질적 | 분기 10주 전 | 3주 | Critical | 어떤 메시지/채널이 타겟에게 효과적인가? |
| 2 | 경쟁사 획득 전략 벤치마킹 | 2차 | 분기 8주 전 | 2주 | 높음 | 우리 제품의 차별화 포인트는 무엇인가? |
| 3 | 유입 채널 퍼널 분석 | 양적 | 분기 6주 전 | 2주 | 높음 | 어느 채널에 예산을 집중해야 하는가? |
| 4 | 랜딩페이지 메시지 A/B 테스트 | 양적 | 분기 3주 전 | 5주 | 보통 | 어떤 가치 제안 메시지가 가장 효과적인가? |

#### 리텐션 (retention)
| 순서 | 메서드 | 유형 | 착수 시점 | 기간 | 우선순위 | Decision Point |
|---|---|---|---|---|---|---|
| 1 | 이탈 유저 심층 인터뷰 | 질적 | 분기 10주 전 | 3주 | Critical | 유저가 떠나는 핵심 이유는 무엇인가? |
| 2 | 코호트 & 리텐션 곡선 분석 | 양적 | 분기 8주 전 | 2주 | Critical | 어느 시점에 재참여 개입이 필요한가? |
| 3 | Magic Moment 행동 분석 | 양적 | 분기 6주 전 | 2주 | 높음 | 첫 경험에서 무엇을 달성시켜야 하는가? |
| 4 | 재참여 실험 (알림/이메일) | 양적 | 분기 3주 전 | 5주 | 보통 | 어떤 재참여 전략이 ROI가 가장 높은가? |

#### 수익화 (revenue)
| 순서 | 메서드 | 유형 | 착수 시점 | 기간 | 우선순위 | Decision Point |
|---|---|---|---|---|---|---|
| 1 | 지불 의향(WTP) 설문 | 양적 | 분기 10주 전 | 2주 | Critical | 적정 가격대 및 최적 플랜 구조는? |
| 2 | 구매 결정 과정 심층 인터뷰 | 질적 | 분기 8주 전 | 3주 | Critical | 전환을 막는 가장 큰 장벽은 무엇인가? |
| 3 | 결제 퍼널 이탈 분석 | 양적 | 분기 6주 전 | 2주 | 높음 | 결제 플로우에서 어디를 개선해야 하는가? |
| 4 | 프라이싱 A/B 테스트 | 양적 | 분기 3주 전 | 5주 | 높음 | 어떤 가격/플랜 구조가 전환율이 높은가? |

#### 인게이지먼트 (engagement)
| 순서 | 메서드 | 유형 | 착수 시점 | 기간 | 우선순위 | Decision Point |
|---|---|---|---|---|---|---|
| 1 | 다이어리 스터디 (2주) | 질적 | 분기 10주 전 | 4주 | 높음 | 유저 일상에서 우리 제품의 역할은 무엇인가? |
| 2 | 사용성 테스트 (Think-Aloud) | 질적 | 분기 7주 전 | 2주 | 높음 | 어떤 UX 마찰이 인게이지먼트를 저해하는가? |
| 3 | 기능 사용 패턴 & 참여도 분석 | 양적 | 분기 5주 전 | 2주 | 보통 | 어떤 기능이 인게이지먼트를 주도하는가? |
| 4 | UX 만족도 설문 (CSAT/SUS) | 양적 | 분기 3주 전 | 2주 | 보통 | 유저가 가장 원하는 개선 사항은? |

#### 품질/성능 (quality)
| 순서 | 메서드 | 유형 | 착수 시점 | 기간 | 우선순위 | Decision Point |
|---|---|---|---|---|---|---|
| 1 | 휴리스틱 UX 평가 | 2차 | 분기 9주 전 | 1주 | 보통 | 어떤 UX 원칙 위반이 존재하는가? |
| 2 | 사용성 테스트 (과업 성공률) | 질적 | 분기 7주 전 | 2주 | 높음 | 핵심 플로우에서 실패 포인트는 어디인가? |
| 3 | 성능 & 기술 지표 측정 | 양적 | 분기 5주 전 | 2주 | 높음 | 성능 병목은 어디이며 개선 우선순위는? |
| 4 | 접근성 감사 (WCAG) | 2차 | 분기 3주 전 | 2주 | 보통 | 접근성 위반 사항과 우선 개선 영역은? |

#### 운영 효율 (ops)
| 순서 | 메서드 | 유형 | 착수 시점 | 기간 | 우선순위 | Decision Point |
|---|---|---|---|---|---|---|
| 1 | 내부 프로세스 인터뷰 | 질적 | 분기 7주 전 | 2주 | 높음 | 어디에 운영 비효율이 집중되어 있는가? |
| 2 | 운영 지표 현황 분석 | 양적 | 분기 5주 전 | 2주 | 높음 | 현재 상태 대비 목표 달성 가능성은? |
| 3 | 도구/워크플로우 만족도 조사 | 양적 | 분기 3주 전 | 2주 | 보통 | 어떤 도구·프로세스 변경이 가장 효과적인가? |

---

## 22개 스쿼드 OKR 목록

| # | 스쿼드 | OKR | 카테고리 | 분기 |
|---|---|---|---|---|
| 1 | Growth | 신규 유저 획득 30% 증대 | acquisition | Q1 |
| 1 | Growth | 레퍼럴 프로그램으로 바이럴 계수 1.2 달성 | acquisition | Q2 |
| 1 | Growth | 핵심 획득 퍼널 전환율 40% 개선 | engagement | Q3 |
| 2 | Retention | D30 리텐션 25%→35% 개선 | retention | Q1 |
| 2 | Retention | 휴면 유저 재활성화율 15% 달성 | retention | Q2 |
| 3 | Monetization | 프리미엄 전환율 3%→6% 달성 | revenue | Q1 |
| 3 | Monetization | 연간 구독 전환율 30% 달성 | revenue | Q2 |
| 3 | Monetization | 신규 수익 모델 검증 및 론칭 | revenue | Q3 |
| 4 | Onboarding | Aha Moment 도달 시간 50% 단축 | engagement | Q1 |
| 4 | Onboarding | 온보딩 퍼널 완료율 70% 달성 | engagement | Q2 |
| 5 | Search | 검색 결과 클릭율 30% 개선 | engagement | Q1 |
| 5 | Search | 개인화 추천 인게이지먼트 40% 향상 | engagement | Q2 |
| 5 | Search | 제로 결과율 5% 이하 달성 | quality | Q3 |
| 6 | Content | 콘텐츠 소비 시간 주간 20분 달성 | engagement | Q1 |
| 6 | Content | UGC 생성량 MoM 25% 성장 | engagement | Q2 |
| 7 | Community | 커뮤니티 활성 멤버 비율 20% | engagement | Q1 |
| 7 | Community | 커뮤니티 기반 리텐션 향상 | retention | Q2 |
| 7 | Community | 커뮤니티 신뢰도 지수 4.0/5 달성 | quality | Q3 |
| 8 | Notifications | 알림 클릭율 15% 달성 | engagement | Q1 |
| 8 | Notifications | 개인화 알림 재참여율 30% 개선 | retention | Q2 |
| 9 | Performance | 앱 로딩 시간 2초 이내 달성 | quality | Q1 |
| 9 | Performance | 크래시율 0.1% 이하 달성 | quality | Q2 |
| 10 | Core Product | 핵심 기능 만족도 4.2/5 달성 | quality | Q1 |
| 10 | Core Product | 핵심 과업 완료율 85% 달성 | engagement | Q2 |
| 10 | Core Product | 신규 핵심 기능 성공적 론칭 | engagement | Q3 |
| 11 | Mobile | 모바일 앱 평점 4.5 달성 | quality | Q1 |
| 11 | Mobile | 모바일 특화 기능 인게이지먼트 향상 | engagement | Q2 |
| 12 | Web | 웹 핵심 퍼널 전환율 25% 개선 | acquisition | Q1 |
| 12 | Web | SEO 오가닉 유입 MoM 20% 성장 | acquisition | Q2 |
| 13 | API Platform | API 안정성 99.9% SLA 달성 | quality | Q1 |
| 13 | API Platform | 내부 개발자 경험 점수 4.0/5 달성 | ops | Q2 |
| 14 | Data Platform | 데이터 파이프라인 안정성 99.5% | ops | Q1 |
| 14 | Data Platform | 셀프서브 분석 도입률 70% | ops | Q2 |
| 15 | Trust & Safety | 악성 콘텐츠 탐지율 98% 달성 | quality | Q1 |
| 15 | Trust & Safety | 정책 위반 처리 시간 24h 달성 | ops | Q2 |
| 16 | Payments | 결제 성공률 99% 달성 | quality | Q1 |
| 16 | Payments | 결제 완료 시간 30% 단축 | revenue | Q2 |
| 17 | Analytics | 데이터 기반 의사결정 팀 비율 80% | ops | Q1 |
| 17 | Analytics | A/B 테스트 사이클 타임 30% 단축 | ops | Q2 |
| 18 | Internationalization | 해외 MAU 비율 25% 달성 | acquisition | Q1 |
| 18 | Internationalization | 현지화 품질 지수 4.0/5 달성 | quality | Q3 |
| 19 | Accessibility | WCAG 2.1 AA 준수율 90% | quality | Q2 |
| 19 | Accessibility | 접근성 관련 CS 50% 감소 | quality | Q3 |
| 20 | Dev Experience | 개발자 생산성 지수 20% 향상 | ops | Q1 |
| 20 | Dev Experience | 개발 환경 안정성 99% 달성 | ops | Q2 |
| 21 | Customer Success | NPS 30점 → 45점 달성 | retention | Q1 |
| 21 | Customer Success | CS 해결 시간 24h→8h 단축 | ops | Q2 |
| 22 | Marketing Tech | 마케팅 캠페인 ROI 30% 개선 | acquisition | Q1 |
| 22 | Marketing Tech | 개인화 마케팅 전환율 25% 향상 | engagement | Q2 |

---

## 현재 산출물

### 파일
| 파일명 | 위치 | 설명 |
|---|---|---|
| `squad-research-roadmap.html` | `/Users/hp-mbp250730/Downloads/` | 완성된 대시보드 (단일 HTML 파일) |
| `squad-research-roadmap-notes.md` | `/Users/hp-mbp250730/Downloads/` | 이 문서 |

### 대시보드 기능 요약
- **탭 1 - 전체 현황**: 22개 스쿼드 카드 그리드. 긴급도(Critical/High/Normal) 자동 계산. 요약 통계 (총 OKR 수, 추천 리서치 수, 이번 달 착수 필요 항목)
- **탭 2 - 리서치 로드맵**: Jan~Dec 2026 간트 차트. 스쿼드·카테고리·리서치유형·우선순위 필터. 현재 시점 마커(3월)
- **탭 3 - 스쿼드 상세**: 스쿼드 선택 → OKR 목록 + 추천 리서치 항목별 타이밍·우선순위·Decision Point. 즉시 착수 필요 항목 빨간 강조

### 기술 스택
- 순수 HTML + CSS + Vanilla JS (단일 파일, 의존성 없음)
- 다크 테마 (#0d1117 베이스)
- 브라우저에서 바로 열기 가능

---

## 다음 단계 (To-Do)

### 단기
- [ ] 실제 스쿼드 OKR 데이터로 `SQUADS` 배열 업데이트
- [ ] OKR 직접 입력 UI 추가 (현재는 코드 수정 필요)
- [ ] 리서치 항목 완료 체크 기능 추가
- [ ] 리서치 담당자(Owner) 지정 필드 추가

### 중기
- [ ] Notion / Linear 연동으로 OKR 데이터 자동 동기화
- [ ] 슬랙 알림 연동 (착수 시점 자동 알림)
- [ ] 리서치 결과 및 인사이트 기록 기능
- [ ] Decision Point 상태 트래킹 (미결/진행중/완료)

### 장기
- [ ] 스쿼드 간 리서치 협업 가능 항목 자동 감지
- [ ] 리서치 부하 캘린더 (리서처 리소스 관리)
- [ ] OKR 달성률과 리서치 실행률 상관관계 리포트

---

## 운영 원칙

1. **로드맵 작성과 Decision Point 등록을 분리하지 말 것** — 동시에 해야 누락 없음
2. **Research Owner를 명시적으로 지정** — 담당자 없으면 아무도 안 함
3. **priority=critical인 항목은 착수 전까지 스쿼드 주간 회의 필수 안건**
4. **confidence_level이 낮으면 일정에 버퍼 추가** — 시스템이 강제해야 함
5. **주간 스쿼드 리뷰에 Decision Point 현황을 의무 안건으로** — 문화로 정착

---

## 참고: 모니터링 타임라인 구조

```
[Decision Point 등록]
       │
       ▼
  착수 6주 전: 리서치 계획 수립 알림 → Research Owner
  착수 3주 전: 착수 준비 확인 알림   → Squad Lead
  착수 시점:   미착수 시 에스컬레이션 → 팀 전체
  분기 마일스톤: 결과 공유 및 결정 확정
```
