import os

for file in os.listdir('.'):
    if file.endswith('.tex'):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Restore [H] because user complained about figures shifting!
        content = content.replace(r'\begin{figure}[!htbp]', r'\begin{figure}[H]')
        content = content.replace(r'\begin{figure}[htbp]', r'\begin{figure}[H]')
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Restored [H] to all figures.")
