import os, re

# 1. Update main.tex
with open('main.tex', 'r', encoding='utf-8') as f:
    main_tex = f.read()

main_tex = main_tex.replace(r'\documentclass[twoside]', r'\documentclass[oneside]')
if r'\renewcommand{\topfraction}' not in main_tex:
    float_fixes = r"""\renewcommand{\topfraction}{0.95}
\renewcommand{\bottomfraction}{0.95}
\renewcommand{\textfraction}{0.05}
\renewcommand{\floatpagefraction}{0.95}
"""
    main_tex = main_tex.replace(r'\begin{document}', float_fixes + r'\begin{document}')

with open('main.tex', 'w', encoding='utf-8') as f:
    f.write(main_tex)

# 2. Update all chapter tex files and main.tex
for file in os.listdir('.'):
    if file.endswith('.tex'):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Shrink images
        content = re.sub(r'width=(?:0\.\d+)?\\textwidth', r'width=0.75\\textwidth', content)
        content = re.sub(r'width=\\textwidth', r'width=0.75\\textwidth', content)
        content = re.sub(r'\\thesisfigureplaceholder\[0\.90\\textwidth\]', r'\\thesisfigureplaceholder[0.75\\textwidth]', content)
        content = re.sub(r'\\thesisfigureplaceholder\[0\.82\\textwidth\]', r'\\thesisfigureplaceholder[0.75\\textwidth]', content)
        
        # Change figure/table options to be more compact
        content = content.replace(r'\begin{figure}[htbp]', r'\begin{figure}[!htbp]')
        content = content.replace(r'\begin{figure}[h]', r'\begin{figure}[!htbp]')
        content = content.replace(r'\begin{figure}[H]', r'\begin{figure}[!htbp]')
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Fixed paper properties.")
