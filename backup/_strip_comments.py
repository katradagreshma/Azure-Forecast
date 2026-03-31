import re

fp = 'streamlit_app.py'
lines = open(fp, 'r', encoding='utf-8').readlines()
out = []
in_css_block = False
skip_multiline_css_comment = False

for i, line in enumerate(lines):
    stripped = line.strip()

    if skip_multiline_css_comment:
        if '*/' in line:
            skip_multiline_css_comment = False
        continue

    if stripped.startswith('/*') and '*/' in stripped:
        continue

    if stripped.startswith('/*') and '*/' not in stripped:
        skip_multiline_css_comment = True
        continue

    if stripped.startswith('#'):
        if stripped == '#MainMenu, footer { visibility: hidden; }':
            out.append(line)
            continue
        if stripped.startswith('#!'):
            out.append(line)
            continue
        continue

    out.append(line)

cleaned = []
prev_blank = False
for line in out:
    is_blank = line.strip() == ''
    if is_blank and prev_blank:
        continue
    cleaned.append(line)
    prev_blank = is_blank

with open(fp, 'w', encoding='utf-8') as f:
    f.writelines(cleaned)

print(f'Original: {len(lines)} lines')
print(f'Cleaned: {len(cleaned)} lines')
print(f'Removed: {len(lines) - len(cleaned)} lines')
