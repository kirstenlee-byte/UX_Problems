"""
Adds JP Excel issues to BOTH KR_DATA (Korean text) and JA_DATA (Japanese text)
so both tabs show the same issues in their respective languages.

Steps:
  1. Restore JA_DATA line from git (prev commit 9e3f644)
  2. Parse JP Excel sheet
  3. Build KR entries (col E text) + JA entries (col F text), IDs from 177
  4. Inject into the tail of KR_DATA and JA_DATA in dashboard.js & index.html
"""
import subprocess, re, json, openpyxl, glob as glob_module

EXCEL_PATH  = glob_module.glob("/home/user/UX_Problems/*.xlsx")[0]
SHEET_NAME  = "JP UX欠陥リストアップ"
JS_PATH     = "/home/user/UX_Problems/dashboard.js"
HTML_PATH   = "/home/user/UX_Problems/index.html"
PREV_COMMIT = "9e3f644"

# ── Funnel mapping: JP label → KR key ──────────────────────────────────────
JP_TO_KR = {
    "1. 登録/アクセス (Active User)": "2. 가입/접속 (Active User)",
    "2. 閲覧 (View User)":            "3. 조회 (View User)",
    "3. 候補探索 (Exploring User)":   "4. 후보군탐색 (Exploring User)",
    "4. 候補決定 (Interested User)":  "5. 후보군결정 (Interested User)",
    "5. 選択 (Select User)":          "6. 선택 (Select User)",
    "6. 予約確定 (Confirmed User)":   "7. 예약확정 (Confirmed User)",
    "7. 施術完了 (Treated User)":     "8. 시술완료 (Treated User)",
}

def map_funnels(raw):
    if not raw: return ""
    s = str(raw).strip()
    matched = [kr for jp, kr in JP_TO_KR.items() if jp in s]
    return ", ".join(matched) if matched else s

# ── Read Excel ──────────────────────────────────────────────────────────────
wb = openpyxl.load_workbook(EXCEL_PATH)
ws = wb[SHEET_NAME]
rows = list(ws.iter_rows(values_only=True))
data_rows = [r for r in rows[2:] if any(c for c in r[:10])]

kr_new_issues = []   # Korean text
ja_new_issues = []   # Japanese text
START_ID = 177

idx = START_ID
for row in data_rows:
    jp_problem = str(row[5] or "").strip()
    kr_problem = str(row[4] or "").strip()

    # Skip example rows / completely empty rows
    if jp_problem.startswith("(ex)") or kr_problem.startswith("(ex)"):
        continue
    if not jp_problem and not kr_problem:
        continue

    funnel    = map_funnels(row[0])
    ux_prob   = str(row[1] or "").strip()
    severity  = str(row[2] or "").strip()
    squad     = str(row[3] or "").strip()
    dev_dir_raw = str(row[8] or "").strip()
    ref_url   = str(row[6] or "").strip()
    dev_flag  = str(row[7] or "").strip()

    url = ref_url if ref_url not in ("", "(Optional)", "None") else ""

    # ── KR entry ─────────────────────────────────────────────
    kr_text = kr_problem or jp_problem
    kr_extra = ""
    if dev_dir_raw and dev_dir_raw not in ("(Optional)", ""):
        kr_extra = f"\n\n[개발 방향] {dev_dir_raw}"

    kr_new_issues.append({
        "id": idx,
        "funnel": funnel,
        "ux_problem": ux_prob,
        "severity": severity,
        "problem": kr_text + kr_extra,
        "problem_rewritten": kr_text,
        "related_url": url,
        "images": [],
        "origin": "jp",
        "squad": squad,
    })

    # ── JA entry ─────────────────────────────────────────────
    ja_text = jp_problem or kr_problem
    ja_extra = ""
    if dev_dir_raw and dev_dir_raw not in ("(Optional)", ""):
        ja_extra = f"\n\n【開発方針】{dev_dir_raw}"

    ja_new_issues.append({
        "id": idx,
        "funnel": funnel,
        "ux_problem": ux_prob,
        "severity": severity,
        "problem": ja_text + ja_extra,
        "problem_rewritten": ja_text,
        "related_url": url,
        "images": [],
        "origin": "jp",
        "squad": squad,
    })

    idx += 1

print(f"New issues to add: {len(kr_new_issues)}")

# ── Helpers ─────────────────────────────────────────────────────────────────
def issues_to_json_fragment(issues):
    """Return comma-prefixed JSON array elements (no outer brackets)."""
    return "".join("," + json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
                   for obj in issues)

def inject_into_data_line(line, new_fragment):
    """
    line looks like:  const KR_DATA = {"2026-1st":[...]};\n
    We need to insert new_fragment before the closing ]}.
    """
    # Find the last ]} before the trailing ;
    close_pos = line.rfind("]}")
    if close_pos == -1:
        raise ValueError("Could not find ']}' in data line")
    return line[:close_pos] + new_fragment + line[close_pos:]

# ── Build fragments ──────────────────────────────────────────────────────────
kr_frag = issues_to_json_fragment(kr_new_issues)
ja_frag = issues_to_json_fragment(ja_new_issues)

# ── Restore original JA_DATA from git and process JS ─────────────────────────
print("Restoring original JA_DATA from git...")
orig_ja_line = subprocess.check_output(
    f"git show {PREV_COMMIT}:dashboard.js | awk 'NR==2'",
    shell=True, cwd="/home/user/UX_Problems"
).decode("utf-8")

print(f"  Original JA_DATA size: {len(orig_ja_line)} chars")

# Inject into orig JA_DATA
new_ja_line = inject_into_data_line(orig_ja_line, ja_frag)
print(f"  New JA_DATA size: {len(new_ja_line)} chars")

# Now update dashboard.js
print("Updating dashboard.js...")
with open(JS_PATH, "r", encoding="utf-8") as f:
    js_lines = f.readlines()

print(f"  Lines: {len(js_lines)}")
print(f"  Line 1 starts: {js_lines[0][:60]}")
print(f"  Line 2 starts: {js_lines[1][:60]}")

assert js_lines[0].startswith("const KR_DATA"), "Line 1 must be KR_DATA"
# Line 2 is currently the bad JA_DATA I injected before — replace with restored+extended

js_lines[0] = inject_into_data_line(js_lines[0], kr_frag)
js_lines[1] = new_ja_line

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.writelines(js_lines)
print("  dashboard.js done")

# ── Now do index.html ────────────────────────────────────────────────────────
print("Restoring original JA_DATA from git for index.html...")
orig_ja_line_html = subprocess.check_output(
    f"git show {PREV_COMMIT}:index.html | awk 'NR==629'",
    shell=True, cwd="/home/user/UX_Problems"
).decode("utf-8")

new_ja_line_html = inject_into_data_line(orig_ja_line_html, ja_frag)

print("Updating index.html...")
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html_lines = f.readlines()

print(f"  Lines: {len(html_lines)}")

# Find KR_DATA and JA_DATA lines in index.html
kr_line_idx = next(i for i, l in enumerate(html_lines) if l.startswith("const KR_DATA"))
ja_line_idx = next(i for i, l in enumerate(html_lines) if l.startswith("const JA_DATA"))

print(f"  KR_DATA at line {kr_line_idx+1}, JA_DATA at line {ja_line_idx+1}")

html_lines[kr_line_idx] = inject_into_data_line(html_lines[kr_line_idx], kr_frag)
html_lines[ja_line_idx] = new_ja_line_html

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.writelines(html_lines)
print("  index.html done")

# ── Verify ────────────────────────────────────────────────────────────────────
print("\n✓ Summary:")
print(f"  Added {len(kr_new_issues)} new issues (IDs {START_ID}–{idx-1})")
print(f"  KR entries: Korean problem text (col E)")
print(f"  JA entries: Japanese problem text (col F)")
print(f"  Both KR_DATA and JA_DATA updated in dashboard.js and index.html")
