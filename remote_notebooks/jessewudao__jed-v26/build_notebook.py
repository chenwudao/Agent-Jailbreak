"""Build jed-v26.ipynb from attack_source.py (jed-v25 skeleton + v26 engine)."""
import json
from pathlib import Path

base = Path(__file__).parent
attack_code = (base / "attack_source.py").read_text(encoding="utf-8")

cell_md = """# JED Attack — v26 (RPS_SELECT + VALIDATION_FILL)

Target: push past the ~88 public plateau toward 90+.

Merges the two community-proven ~88 engines:
- jed-v25 validation-fill (keep only fired candidates, replay-safe wall)
- yw8837's N32 raw-per-second selector (probe template bank, rank by
  raw reward / second with a fire-rate floor, pick best PER MODEL ROW)

Template bank blends the methodology doc (multi-step, marker systems,
authoritative tone) with the community-proven single-post line. The eval
update (Aug 2026) preserves partial scores on replay timeout, so the replay
wall is slightly looser than v25.

Run: `kaggle kernels push -p <dir>`, then
`kaggle competitions submit -k jessewudao/jed-v26-rps -f submission.csv -v <ver> -m "v26"`.
"""

cell_setup = """import sys, glob
from pathlib import Path
sys.argv = [sys.argv[0]]
for candidate in glob.glob('/kaggle/input/**/kaggle_evaluation', recursive=True):
    root = str(Path(candidate).parent)
    if root not in sys.path:
        sys.path.insert(0, root)
    print('Dataset root:', root)
    break
print('Setup complete')
"""

cell_write = (
    "attack_code = r'''\n"
    + attack_code
    + "'''\n\n"
    "with open('/kaggle/working/attack.py', 'w') as f:\n"
    "    f.write(attack_code)\n"
    "print('attack.py written, chars:', len(attack_code))\n"
)

cell_serve = """import os, csv
if os.getenv('KAGGLE_IS_COMPETITION_RERUN'):
    import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server as server
    server.JEDAttackInferenceServer().serve()
else:
    with open('/kaggle/working/submission.csv', 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(['Id', 'Score'])
        w.writerows([['gpt_oss_public', 0.0], ['gpt_oss_private', 0.0], ['gemma_public', 0.0], ['gemma_private', 0.0]])
    print('placeholder submission.csv written. Set GPU T4 x2, Internet Off, then Submit.')
"""


def src_lines(text: str) -> list[str]:
    return [line + "\n" for line in text.split("\n")]


nb = {
    "cells": [
        {"cell_type": "markdown", "metadata": {}, "source": src_lines(cell_md)},
        {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": src_lines(cell_setup)},
        {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": src_lines(cell_write)},
        {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": src_lines(cell_serve)},
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.5"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

out = base / "jed-v26.ipynb"
out.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
print("wrote", out)
