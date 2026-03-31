import re

files = [
    'streamlit_app.py',
    'batch/batch_predict.py',
    'api/app.py',
    'monitoring/monitor.py',
    'scheduler/run_scheduler.py',
]

for fp in files:
    lines = open(fp, 'r', encoding='utf-8').readlines()
    found = []
    for i, l in enumerate(lines, 1):
        s = l.strip()
        if s.startswith('#'):
            found.append((i, l.rstrip()))
    if found:
        print(f'\n=== {fp} ({len(found)} comment lines) ===')
        for ln, txt in found:
            print(f'  {ln}: {txt}')
    else:
        print(f'\n=== {fp} (0 comments) ===')
