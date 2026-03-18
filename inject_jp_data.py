"""
Reads JP UX issues from Excel and replaces JA_DATA in dashboard.js (line 2).
"""
import openpyxl
import glob as glob_module
import json
import re

# ── Excel path ─────────────────────────────────────────────────────────────
EXCEL_PATH = glob_module.glob("/home/user/UX_Problems/*.xlsx")[0]
SHEET_NAME = "JP UX欠陥リストアップ"
DASHBOARD_JS = "/home/user/UX_Problems/dashboard.js"

# ── Funnel mapping: JP label → KR key used by FUNNEL_ORDER ─────────────────
JP_TO_KR_FUNNEL = {
    "1. 登録/アクセス (Active User)":  "2. 가입/접속 (Active User)",
    "2. 閲覧 (View User)":             "3. 조회 (View User)",
    "3. 候補探索 (Exploring User)":    "4. 후보군탐색 (Exploring User)",
    "4. 候補決定 (Interested User)":   "5. 후보군결정 (Interested User)",
    "5. 選択 (Select User)":           "6. 선택 (Select User)",
    "6. 予約確定 (Confirmed User)":    "7. 예약확정 (Confirmed User)",
    "7. 施術完了 (Treated User)":      "8. 시술완료 (Treated User)",
}

ALL_KR_FUNNELS = ", ".join(JP_TO_KR_FUNNEL.values())

def map_funnels(raw_funnel):
    """Return comma-separated KR funnel key(s) from a JP funnel cell."""
    if not raw_funnel:
        return ""
    raw = str(raw_funnel).strip()
    # Check if multiple JP funnels are listed
    mapped = []
    for jp_key, kr_key in JP_TO_KR_FUNNEL.items():
        if jp_key in raw:
            mapped.append(kr_key)
    if mapped:
        return ", ".join(mapped)
    # Fallback: if nothing matched, return as-is (shouldn't happen)
    return raw

# ── Read Excel ──────────────────────────────────────────────────────────────
wb = openpyxl.load_workbook(EXCEL_PATH)
ws = wb[SHEET_NAME]

rows = list(ws.iter_rows(values_only=True))
# Row 0 = header, Row 1 = example row (skip both)
data_rows = [r for r in rows[2:] if any(c for c in r[:10])]

issues = []
for idx, row in enumerate(data_rows, start=1):
    funnel_raw  = row[0] or ""
    ux_problem  = str(row[1] or "").strip()
    severity    = str(row[2] or "").strip()
    squad       = str(row[3] or "").strip()
    kr_problem  = str(row[4] or "").strip()
    jp_problem  = str(row[5] or "").strip()
    ref_url     = str(row[6] or "").strip()
    dev_flag    = str(row[7] or "").strip()
    dev_dir     = str(row[8] or "").strip()

    # Skip example rows
    if jp_problem.startswith("(ex)") or kr_problem.startswith("(ex)"):
        continue

    funnel = map_funnels(funnel_raw)

    # Use JP problem as primary; fall back to KR
    primary_problem = jp_problem or kr_problem

    # Build richer problem text including dev direction if available
    problem_text = primary_problem
    if dev_dir and dev_dir not in ("(Optional)", ""):
        problem_text += f"\n\n【開発方針】{dev_dir}"

    # ref_url cleanup
    url = ref_url if ref_url not in ("", "(Optional)", "None") else ""

    issues.append({
        "id": idx,
        "funnel": funnel,
        "ux_problem": ux_problem,
        "severity": severity,
        "problem": problem_text,
        "problem_rewritten": primary_problem,
        "related_url": url,
        "images": [],
        "origin": "jp",
        "squad": squad,
        "kr_problem": kr_problem,
    })

print(f"Extracted {len(issues)} JP issues")

# ── Build JA_DATA ───────────────────────────────────────────────────────────
ja_data = {"2026-1st": issues}
ja_data_str = json.dumps(ja_data, ensure_ascii=False, separators=(",", ":"))
new_line2 = f"const JA_DATA = {ja_data_str};\n"

# ── Replace line 2 in dashboard.js ─────────────────────────────────────────
with open(DASHBOARD_JS, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"dashboard.js has {len(lines)} lines")
print(f"Line 2 starts with: {lines[1][:80]}")

# Verify line 2 is JA_DATA
if not lines[1].startswith("const JA_DATA"):
    print("ERROR: Line 2 is not JA_DATA!")
    print(f"Actual: {lines[1][:100]}")
    exit(1)

lines[1] = new_line2

with open(DASHBOARD_JS, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("dashboard.js updated successfully!")
print(f"New JA_DATA size: {len(new_line2)} chars")
