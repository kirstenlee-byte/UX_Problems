import openpyxl
import glob as glob_module
from github import Github
import os

_files = glob_module.glob("/home/user/UX_Problems/*.xlsx")
EXCEL_PATH = _files[0]
SHEET_NAME = "JP UX欠陥リストアップ"
REPO_NAME = "kirstenlee-byte/UX_Problems"

wb = openpyxl.load_workbook(EXCEL_PATH)
ws = wb[SHEET_NAME]

rows = list(ws.iter_rows(values_only=True))
header = rows[0]
print(f"Headers: {header[:10]}")
print(f"Total rows: {len(rows)}")

# Skip header (row 0) and example row (row 1, index 1 which is the (ex) row)
data_rows = []
for row in rows[2:]:
    if any(cell for cell in row[:10]):
        data_rows.append(row)

print(f"Data rows to process: {len(data_rows)}")

token = os.environ.get("GITHUB_TOKEN")
if not token:
    print("ERROR: GITHUB_TOKEN not set")
    exit(1)

g = Github(token)
repo = g.get_repo(REPO_NAME)

severity_labels = {
    "1 Irritant": "severity: 1-irritant",
    "2 Moderate": "severity: 2-moderate",
    "3 Severe": "severity: 3-severe",
    "4 Unusable": "severity: 4-unusable",
}

# Ensure labels exist
existing_labels = {l.name for l in repo.get_labels()}
for label_name in severity_labels.values():
    if label_name not in existing_labels:
        color_map = {
            "severity: 1-irritant": "c5def5",
            "severity: 2-moderate": "f9d0c4",
            "severity: 3-severe": "e4e669",
            "severity: 4-unusable": "d93f0b",
        }
        repo.create_label(label_name, color_map.get(label_name, "ededed"))
        print(f"Created label: {label_name}")

created = 0
for i, row in enumerate(data_rows):
    funnel    = row[0] or ""
    ux_type   = row[1] or ""
    severity  = row[2] or ""
    squad     = row[3] or ""
    kr_issue  = row[4] or ""
    jp_issue  = row[5] or ""
    ref       = row[6] or ""
    dev_flag  = row[7] or ""
    dev_dir   = row[8] or ""
    design    = row[9] or ""

    # Use JP issue as title, fallback to KR
    title_text = str(jp_issue).strip() if jp_issue else str(kr_issue).strip()
    if not title_text or title_text.startswith("(ex)"):
        continue

    # Truncate title if too long
    title = f"[JP] {title_text[:100]}"

    body_lines = [
        "## JP UX 欠陥 Issue",
        "",
        f"**User Funnel:** {funnel}",
        f"**UX Problem Type:** {ux_type}",
        f"**Severity:** {severity}",
        f"**연관 스쿼드:** {squad}" if squad else "",
        "",
        "### 問題点",
        f"- 🇰🇷 **KR:** {kr_issue}" if kr_issue else "",
        f"- 🇯🇵 **JP:** {jp_issue}" if jp_issue else "",
        "",
        f"**開発可否 (Dev Feasibility):** {dev_flag}" if dev_flag else "",
        f"**大体の開発方針 (Dev Direction):** {dev_dir}" if dev_dir else "",
        f"**Design Required Spec.:** {design}" if design else "",
        f"**関係資料 (Reference):** {ref}" if ref and ref != "(Optional)" else "",
    ]
    body = "\n".join(line for line in body_lines if line is not None)

    labels = ["JP UX Issue"]
    sev_label = severity_labels.get(str(severity).strip())
    if sev_label:
        labels.append(sev_label)

    # Ensure base label exists
    if "JP UX Issue" not in existing_labels:
        repo.create_label("JP UX Issue", "0075ca")
        existing_labels.add("JP UX Issue")
        print("Created label: JP UX Issue")

    issue = repo.create_issue(title=title, body=body, labels=labels)
    created += 1
    print(f"[{created}] Created: {issue.number} - {title[:60]}")

print(f"\nDone. Total issues created: {created}")
