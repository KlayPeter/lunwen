from __future__ import annotations

import datetime as dt
import html
import re
from pathlib import Path


ROOT = Path(__file__).parent


def find_source_txt(root: Path) -> Path:
    candidates = [
        path
        for path in root.glob("*.txt")
        if "14" in path.stem and path.stat().st_size > 7000
    ]
    if not candidates:
        raise FileNotFoundError("Could not find the guidance-record source txt file.")
    return sorted(candidates, key=lambda p: p.name)[0]


def parse_records(text: str) -> list[dict[str, object]]:
    pattern = re.compile(
        r"^第(?P<no>\d+)次指导记录\s*"
        r"\n日期：(?P<date>\d{4}\.\d{2}\.\d{2})\s*"
        r"\n检查进展：\s*"
        r"\n(?P<progress>.*?)"
        r"\n讨论问题：\s*"
        r"\n(?P<discussion>.*?)(?=\n第\d+次指导记录|\Z)",
        re.S | re.M,
    )
    records: list[dict[str, object]] = []
    for match in pattern.finditer(text.strip()):
        progress_lines = [
            line.strip()
            for line in match.group("progress").strip().splitlines()
            if line.strip()
        ]
        discussion_lines = [
            line.strip()
            for line in match.group("discussion").strip().splitlines()
            if line.strip()
        ]
        records.append(
            {
                "no": int(match.group("no")),
                "date": match.group("date"),
                "sort_date": dt.datetime.strptime(match.group("date"), "%Y.%m.%d"),
                "progress": progress_lines,
                "discussion": discussion_lines,
            }
        )
    if len(records) != 14:
        raise ValueError(f"Expected 14 records, found {len(records)}.")
    return sorted(records, key=lambda item: item["sort_date"])


def render_lines(lines: list[str]) -> str:
    return "\n".join(
        f'<div class="item">{html.escape(line)}</div>' for line in lines
    )


def build_html(title: str, topic: str, records: list[dict[str, object]]) -> str:
    record_blocks: list[str] = []
    for index, record in enumerate(records, start=1):
        block = f"""
        <table class="record" aria-label="第{index}次指导记录">
          <tr>
            <td class="meta">
              <div class="meta-inner">
                <div class="seq">第{index}次指导记录</div>
                <div class="date">日期：{html.escape(str(record["date"]))}</div>
              </div>
            </td>
            <td class="content">
              <div class="section-title">检查进展：</div>
              {render_lines(record["progress"])}
              <div class="section-title discuss">讨论问题：</div>
              {render_lines(record["discussion"])}
            </td>
          </tr>
        </table>
        """.strip()
        record_blocks.append(block)

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    @page {{
      size: A4;
      margin: 18mm 16mm 18mm 16mm;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      color: #000;
      font-family: "SimSun", "宋体", serif;
      font-size: 10.5pt;
      line-height: 1.42;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}

    .page {{
      width: 100%;
    }}

    .title {{
      margin: 0 0 8mm;
      text-align: center;
      font-size: 16pt;
      font-weight: 700;
      letter-spacing: 0.5px;
    }}

    .topic {{
      margin: 0 0 6mm;
      font-size: 11pt;
      line-height: 1.5;
    }}

    .topic-label {{
      font-weight: 700;
    }}

    .record {{
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
      page-break-inside: avoid;
      break-inside: avoid;
      margin: 0;
    }}

    .record + .record {{
      margin-top: -1px;
    }}

    .record td {{
      border: 1px solid #000;
      vertical-align: top;
      padding: 3mm 3.5mm;
    }}

    .meta {{
      width: 31mm;
      text-align: center;
      padding-left: 2.5mm;
      padding-right: 2.5mm;
    }}

    .meta-inner {{
      display: flex;
      min-height: 100%;
      flex-direction: column;
      gap: 5mm;
    }}

    .seq {{
      font-weight: 700;
      margin-top: 1mm;
    }}

    .date {{
      line-height: 1.5;
      word-break: break-all;
    }}

    .content {{
      font-size: 10.5pt;
    }}

    .section-title {{
      font-weight: 700;
      margin: 0 0 1mm;
    }}

    .section-title.discuss {{
      margin-top: 2mm;
    }}

    .item {{
      margin: 0;
      text-align: justify;
      text-justify: inter-ideograph;
    }}
  </style>
</head>
<body>
  <main class="page">
    <h1 class="title">{html.escape(title)}</h1>
    <p class="topic"><span class="topic-label">课题名称：</span>{html.escape(topic)}</p>
    {"".join(record_blocks)}
  </main>
</body>
</html>
"""


def main() -> None:
    source_path = find_source_txt(ROOT)
    raw_text = source_path.read_text(encoding="utf-8").strip()
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    title = lines[0]
    topic = lines[1].split("：", 1)[1]
    records = parse_records(raw_text)
    html_path = Path.cwd() / "guidance_record_fixed.html"
    html_path.write_text(build_html(title, topic, records), encoding="utf-8")
    print(html_path)


if __name__ == "__main__":
    main()
