# Montage Design System Loader

Wanted Lab의 Montage 웹 디자인 시스템(https://github.com/wanteddev/montage-web)을 불러와서 디자인 작업을 시작합니다.

## MCP 서버 설정 (최초 1회)

MCP 서버가 설정되지 않은 경우, 아래 내용을 프로젝트 루트의 `.mcp.json`에 추가하세요:

```json
{
  "mcpServers": {
    "montage-mcp-server": {
      "type": "http",
      "url": "https://montage.wanted.co.kr/mcp"
    }
  }
}
```

## 실행 단계

아래 순서대로 진행하세요:

### 1단계: 코딩 가이드라인 확인

MCP 서버(`montage-mcp-server`)의 `get_coding_guidelines` 도구를 사용하여 WDS 코딩 가이드라인을 먼저 가져오세요.

MCP 서버를 사용할 수 없는 경우 WebFetch로 아래 GitHub 페이지에서 정보를 수집하세요:
- https://raw.githubusercontent.com/wanteddev/montage-web/main/.claude-plugin/montage-web-guide/skills/montage-react/SKILL.md

### 2단계: 컴포넌트 목록 조회

MCP 서버의 `list_components` 도구를 사용하여 사용 가능한 모든 WDS 컴포넌트 목록을 가져오세요.

MCP 서버를 사용할 수 없는 경우 WebFetch로 다음 URL에서 실제 컴포넌트 목록을 확인하세요:
- https://api.github.com/repos/wanteddev/montage-web/git/trees/HEAD?recursive=1

불러온 트리에서 `docs/` 하위 파일들을 파악하여 아래 카테고리를 정리하세요:
- **Actions**: action-area, Button, Chip, IconButton, TextButton
- **Contents**: Accordion, Avatar, Card, ListCell, Table, Thumbnail
- **Feedback**: Alert, Snackbar, Toast, PushBadge
- **Loading**: LoadingSpinner, Skeleton
- **Navigations**: Tabs, Pagination, ProgressTracker, TopNavigation
- **Presentation**: BottomSheet, Menu, Popover, Tooltip
- **Selection & Input**: Checkbox, Radio, TextField, DatePicker, Select, Slider

### 3단계: 디자인 토큰 로드

MCP 서버의 `get_design_tokens` 도구를 사용하거나, WebFetch로 다음 URL에서 토큰 정보를 확인하세요:
- https://api.github.com/repos/wanteddev/montage-web/contents/packages/wds-theme/src/theme

토큰 카테고리: atomic(색상 원자값), semantic(의미 기반 색상), typography, spacing, breakpoint, opacity, z-index

### 4단계: 아이콘 목록 확인

MCP 서버의 `list_icons` 도구를 사용하거나 WebFetch로 아이콘 패키지를 확인하세요:
- https://api.github.com/repos/wanteddev/montage-web/contents/packages/wds-icon/src

### 5단계: 현황 요약 출력

수집한 정보를 바탕으로 다음 형식으로 사용자에게 보고하세요:

```
## Montage 디자인 시스템 로드 완료

### 사용 가능한 컴포넌트 카테고리
[카테고리별 컴포넌트 목록]

### 주요 디자인 토큰
[색상, 타이포그래피 등 핵심 토큰]

### 코딩 원칙
1. WDS 컴포넌트를 우선 사용하고, 커스텀 구현 최소화
2. 색상은 hex 코드 대신 WDS 색상 토큰 사용
3. WDS 컴포넌트 확장이 필요할 때는 WDS를 기반으로 확장
4. 아이콘은 WDS 아이콘 라이브러리 활용

이제 디자인 작업을 시작할 준비가 완료되었습니다.
어떤 컴포넌트/화면을 디자인할까요?
```

## 디자인 작업 시 체크리스트

- [ ] WDS 코딩 가이드라인 준수 확인
- [ ] 기존 WDS 컴포넌트 최대한 활용
- [ ] 하드코딩 스타일 대신 디자인 토큰 사용
- [ ] WDS 아이콘 라이브러리에서 아이콘 선택
- [ ] WDS 유틸리티 함수 활용

## 참고 링크

- 저장소: https://github.com/wanteddev/montage-web
- MCP 서버: https://montage.wanted.co.kr/mcp
- 플러그인 가이드: https://github.com/wanteddev/montage-web/tree/main/.claude-plugin/montage-web-guide
