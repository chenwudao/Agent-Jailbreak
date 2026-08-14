"""Build jed-v26b.ipynb from attack_source.py (v26 skeleton + slow-row multipost)."""
import json
from pathlib import Path

base = Path(__file__).parent
attack_code = (base / "attack_source.py").read_text(encoding="utf-8")

cell_md = """# JED Attack — v26b (RPS_SELECT + VALIDATION_FILL + SLOW-ROW MULTIPOST)

Same engine as v26, plus one experiment: on the SLOW (Harmony/gpt_oss) row,
fill with a token-forged multi-post plan (SLOW_MULTIPOST_N=2) instead of a
single post. Each trace firing BOTH posts scores 16*2+2 = 34 raw (vs 18),
which is how the leaderboard exceeds the ~90 single-post ceiling.

Run: `kaggle kernels push -p <dir>`, then
`kaggle competitions submit -k jessewudao/jed-attack-v26b-multipost -f submission.csv -v <ver> -m "v26b"`.
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

out = base / "jed-v26b.ipynb"
out.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
print("wrote", out)
