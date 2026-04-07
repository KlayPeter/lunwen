import re

with open('chapter4.tex', 'r', encoding='utf-8') as f:
    lines = f.readlines()

result = []
in_list = False
i = 0

while i < len(lines):
    line = lines[i]

    # 检查是否是列表项开始
    if line.startswith('- '):
        if not in_list:
            # 开始一个新的列表
            result.append('\\begin{itemize}\n')
            in_list = True
        # 转换列表项
        content = line[2:].strip()  # 去掉 "- " 前缀
        result.append(f'\\item {content}\n')
    else:
        # 如果之前在列表中，现在遇到非列表行，结束列表
        if in_list and line.strip() != '':
            result.append('\\end{itemize}\n')
            in_list = False

        # 删除markdown代码块标记
        if line.strip() == '```':
            i += 1
            continue

        result.append(line)

    i += 1

# 如果文件结尾还在列表中，关闭列表
if in_list:
    result.append('\\end{itemize}\n')

with open('chapter4.tex', 'w', encoding='utf-8') as f:
    f.writelines(result)

print('列表格式已修复')
