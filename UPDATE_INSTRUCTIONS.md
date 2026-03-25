# Agent Instructions — Update Indeed Jobs HTML

## What this does
Updates `Indeed jobs.html` with fresh data from a new Indeed jobs Excel file. The HTML is a self-contained interactive chart showing the US Job Postings Index by sector over time.

---

## Paths

| Resource | Path |
|---|---|
| HTML report | `/Users/rokoroic/dev/docs/Indeed jobs.html` |
| Current Excel | `/Users/rokoroic/dev/docs/jobs.xlsx` |

---

## Step-by-step

### Step 1 — Find the new Excel file
The new file is the most recent `.xlsx` in `~/Downloads/` with "Indeed" in the name:
```bash
ls -t ~/Downloads/*.xlsx | head -10
```
Pick the most recent one matching "Indeed".

### Step 2 — Copy it into the docs folder
```bash
cp "/Users/rokoroic/Downloads/Indeed jobs XXXXXXXX.xlsx" "/Users/rokoroic/dev/docs/jobs.xlsx"
```

### Step 3 — Extract and aggregate data with Python

Run this script. It reads the xlsx, aggregates daily data to monthly averages, and replaces the data constants in the HTML.

```python
import openpyxl, json, re
from collections import defaultdict

# Load xlsx
wb = openpyxl.load_workbook('/Users/rokoroic/dev/docs/jobs.xlsx')
ws = wb['Sheet1']

# Expected columns: date | jobcountry | indeed_job_postings_index | variable | display_name
# variable values: 'total postings', 'new postings'
# display_name = sector name

monthly = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
for row in ws.iter_rows(min_row=2, values_only=True):
    date, country, value, variable, sector = row
    if not date or value is None:
        continue
    try:
        monthly[(date.year, date.month)][variable][sector].append(float(value))
    except (TypeError, ValueError):
        pass

months = sorted(monthly.keys())
all_sectors = sorted({s for m in monthly.values() for v in m.values() for s in v})
month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def avg(lst): return round(sum(lst)/len(lst), 2) if lst else None

labels = [f"{month_names[m-1]} '{str(y)[2:]}" for y,m in months]

total     = {s: [avg(monthly[mo]['total postings'][s]) for mo in months] for s in all_sectors}
new_total = {s: [avg(monthly[mo]['new postings'][s])   for mo in months] for s in all_sectors}

overall = [round(sum(v for v in [total[s][i] for s in all_sectors] if v is not None) /
           max(1, len([s for s in all_sectors if total[s][i] is not None])), 2)
           for i in range(len(months))]
new_overall = [round(sum(v for v in [new_total[s][i] for s in all_sectors] if v is not None) /
               max(1, len([s for s in all_sectors if new_total[s][i] is not None])), 2)
               for i in range(len(months))]

def js_array(lst):
    return '[' + ','.join(str(v) if v is not None else 'null' for v in lst) + ']'

def js_obj(d):
    lines = [f'  {json.dumps(k)}: {js_array(v)}' for k, v in d.items()]
    return '{\n' + ',\n'.join(lines) + '\n}'

new_labels    = 'const LABELS = '         + json.dumps(labels)    + ';'
new_ovr       = 'const OVERALL = '        + js_array(overall)     + ';'
new_cats      = 'const CATEGORIES = '     + js_obj(total)         + ';'
new_new_ovr   = 'const NEW_OVERALL = '    + js_array(new_overall) + ';'
new_new_cats  = 'const NEW_CATEGORIES = ' + js_obj(new_total)     + ';'

with open('/Users/rokoroic/dev/docs/Indeed jobs.html', 'r') as f:
    html = f.read()

def replace_const(html, name, new_line):
    pattern = rf'const {name}\s*=\s*(?:\[[\s\S]*?\]|\{{[\s\S]*?\}});'
    return re.sub(pattern, new_line, html, count=1)

html = replace_const(html, 'LABELS',         new_labels)
html = replace_const(html, 'OVERALL',        new_ovr)
html = replace_const(html, 'CATEGORIES',     new_cats)
html = replace_const(html, 'NEW_OVERALL',    new_new_ovr)
html = replace_const(html, 'NEW_CATEGORIES', new_new_cats)

with open('/Users/rokoroic/dev/docs/Indeed jobs.html', 'w') as f:
    f.write(html)

print(f"Done. {len(months)} months ({labels[0]} → {labels[-1]}), {len(all_sectors)} sectors.")
```

### Step 4 — Verify
Check the output of the script. It should print:
- Number of months and date range
- Number of sectors (expected: 43, but may grow if Indeed adds new ones)

If the sector count changes, that is fine — new sectors will be added automatically.

### Step 5 — Commit
```bash
cd /Users/rokoroic/dev/docs
git add "Indeed jobs.html" jobs.xlsx
git commit -m "Update Indeed jobs data to YYYY-MM"
git push origin main
```

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: openpyxl` | Not installed | `pip3 install openpyxl` |
| `TypeError: unsupported operand type` | Non-numeric value in index column | Already handled by `try/except float()` in the script |
| Regex replacement fails (0 replacements) | Column order in xlsx changed | Check header row and update column unpacking: `date, country, value, variable, sector = row` |
| Sector count drops | Indeed renamed or removed sectors | Check `all_sectors` list against previous version |
| March/last month looks low | Partial month (data cut off mid-month) | Normal — monthly average of fewer days. No action needed. |

---

## HTML data structure reference

The HTML stores all data as inline JavaScript constants. Only these 5 need replacing on each update:

| Constant | Type | Content |
|---|---|---|
| `LABELS` | `string[]` | Month labels: `["Feb '20", "Mar '20", ...]` |
| `OVERALL` | `number[]` | Monthly mean of total postings index across all sectors |
| `CATEGORIES` | `{[sector]: number[]}` | Total postings index per sector per month |
| `NEW_OVERALL` | `number[]` | Monthly mean of new postings index across all sectors |
| `NEW_CATEGORIES` | `{[sector]: number[]}` | New postings index per sector per month |

All arrays are aligned to `LABELS` — index 0 = first month, index N = Nth month.
