#!/bin/bash
file="chapter5.tex"

for i in {9..41}; do
    # 使用perl进行多行替换
    perl -i -0pe "s/\\[\s*图\s*5-$i\s+([^\]]+)\\]/\\begin{figure}[htbp]\n\\centering\n\\includegraphics[width=0.75\\textwidth]{..\/img\/5-$i.png}\n\\caption{\$1}\n\\label{fig:5-$i}\n\\end{figure}/g" "$file"
done

echo "处理完成"
