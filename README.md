# 毕业论文 LaTeX 编译说明

## 文件结构

```
latex/
├── main.tex              # 主文件（用于编译）
├── chapter1.tex          # 第1章
├── chapter2.tex          # 第2章
├── ...                   # 其他章节
├── chapter14.tex         # 第14章
├── thesis-cls-Miya.cls   # 模板类文件
├── BibTeX-style-hzu.bst  # 参考文献样式
└── bibHzu.bib            # 参考文献数据库
```

## 编译方法

### 方法一：使用 XeLaTeX（推荐）

```bash
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

### 方法二：使用 LaTeX 编辑器

1. 使用 TeXstudio、Overleaf 等编辑器打开 `main.tex`
2. 设置编译器为 XeLaTeX
3. 点击编译按钮

## 注意事项

1. 需要安装完整的 TeX 发行版（如 TeX Live 或 MiKTeX）
2. 确保支持中文字体
3. 首次编译需要运行多次以生成目录和交叉引用
4. 修改参考文献后需要重新运行 bibtex

## Markdown 文件

Markdown 格式的论文已保存在 `../markdown/` 目录下：
- `论文完整版.md` - 完整论文
- `第X章_xxx.md` - 各章节独立文件
