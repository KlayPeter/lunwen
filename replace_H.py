import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    text = text.replace(r'\begin{figure}[H]', r'\begin{figure}[!htbp]')
    text = text.replace(r'\begin{table}[H]', r'\begin{table}[!htbp]')
    
    text = re.sub(r'（见表\s*([0-9\-\.]+)）', r'，如表\1所示', text)
    text = re.sub(r'\(见表\s*([0-9\-\.]+)\)', r'，如表\1所示', text)
    text = re.sub(r'（见表~?\\ref\{([^}]+)\}）', r'，如表~\ref{\1}所示', text)
    text = re.sub(r'\(见表~?\\ref\{([^}]+)\}\)', r'，如表~\ref{\1}所示', text)

    text = re.sub(r'（见图\s*([0-9\-\.]+)）', r'，如图\1所示', text)
    text = re.sub(r'\(见图\s*([0-9\-\.]+)\)', r'，如图\1所示', text)
    text = re.sub(r'（见图~?\\ref\{([^}]+)\}）', r'，如图~\ref{\1}所示', text)
    text = re.sub(r'\(见图~?\\ref\{([^}]+)\}\)', r'，如图~\ref{\1}所示', text)
    
    # special case like （如图...）
    text = re.sub(r'（如图~?\\ref\{([^}]+)\}）', r'，如图~\ref{\1}', text)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

fix_file('/Users/admin/Desktop/Peter/docs 2/latex/chapter4.tex')
fix_file('/Users/admin/Desktop/Peter/docs 2/latex/chapter5.tex')
