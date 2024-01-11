import difflib
from pathlib import Path

first_file_lines = Path(
    'outputcmd/20240111_2249/n1psefwan1301_172.31.211.17_fgate_status.txt').read_text().splitlines()
second_file_lines = Path(
    'outputcmd/20240111_2334/n1psefwan1301_172.31.211.17_fgate_status.txt').read_text().splitlines()

html_diff = difflib.HtmlDiff().make_table(
    first_file_lines, second_file_lines, context=True, numlines=1)
Path('diff.html').write_text(html_diff)
