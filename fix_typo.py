#!/usr/bin/env python3
"""Fix sheets_names typo in main.py"""

def fix_typo():
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the typo: sheets_names -> sheet_names
    content = content.replace("'sheets_names'", "'sheet_names'")
    
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed typo: sheets_names -> sheet_names")

if __name__ == '__main__':
    fix_typo()