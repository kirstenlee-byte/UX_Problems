# Montage Design System Loader

Wanted Lab의 Montage 웹 디자인 시스템(https://github.com/wanteddev/montage-web)을 불러와서 디자인 작업을 시작합니다.

## 실행 단계

아래 순서대로 진행하세요:

### 1단계: 코딩 가이드라인 확인

MCP 서버(`montage-mcp-server`)의 `get_coding_guidelines` 도구를 사용하여 WDS 코딩 가이드라인을 먼저 가져오세요.

MCP 서버를 사용할 수 없는 경우 WebFetch로 아래 GitHub 페이지에서 정보를 수집하세요:
- https://raw.githubusercontent.com/wanteddev/montage-web/main/docs/README.md (있을 경우)

### 2단계: 컴포넌트 목록 조회

MCP 서버의 `list_components` 도구를 사용하여 사용 가능한 모든 WDS 컴포넌트 목록을 가져오세요.

MCP 서버를 사용할 수 없는 경우 WebFetch로 다음 카테고리별 컴포넌트 문서를 확인하세요:
- https://api.github.com/repos/wanteddev/montage-web/git/trees/HEAD?recursive=1

불러온 트리에서 `docs/` 하위 파일들을 파악하여 아래 카테고리를 정리하세요:
- **Actions**: Button, Chip, IconButton
- **Contents**: Card, Avatar, List, Table, Thumbnail
- **Feedback**: Alert, Toast, Badge, Snackbar
- **Navigations**: Tab, Pagination, ProgressTracker
- **Selection & Input**: Checkbox, Form, DatePicker, Slider
- **Presentation**: Popover, Tooltip, Menu, Modal

### 3단계: 디자인 토큰 로드

MCP 서버의 `get_design_tokens` 도구를 사용하거나, WebFetch로 다음 URL에서 토큰 정보를 확인하세요:
- https://raw.githubusercontent.com/wanteddev/montage-web/main/packages/tokens/src/index.ts (혹은 유사 경로)

색상, 타이포그래피, 그림자, 보더 토큰을 파악하세요.

### 4단계: 아이콘 목록 확인

MCP 서버의 `list_icons` 도구를 사용하거나 WebFetch로 아이콘 패키지를 확인하세요.

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
