import re

with open('chapter6.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# 在每个表格的 \small 后添加 \renewcommand{\arraystretch}{1.2}
content = re.sub(
    r'(\\label\{tab:[^}]+\}\n)(\\small\n)',
    r'\1\2\\renewcommand{\\arraystretch}{1.2}\n',
    content
)

# 处理每个表格
tables = re.finditer(r'\\begin\{tabular\}.*?\\end\{tabular\}', content, re.DOTALL)
for match in reversed(list(tables)):
    table = match.group(0)
    lines = table.split('\n')
    new_lines = []
    hline_count = 0

    for i, line in enumerate(lines):
        if line.strip() == '\\hline':
            hline_count += 1
            if hline_count == 1:
                new_lines.append('\\toprule')
            elif hline_count == 2:
                new_lines.append('\\midrule')
            elif i == len(lines) - 2:  # 倒数第二行
                new_lines.append('\\bottomrule')
            # 其他 hline 跳过
        else:
            new_lines.append(line)

    new_table = '\n'.join(new_lines)
    content = content[:match.start()] + new_table + content[match.end():]

with open('chapter6.tex', 'w', encoding='utf-8') as f:
    f.write(content)

print('表格格式已更新为三线表')
