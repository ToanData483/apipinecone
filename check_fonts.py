#!/usr/bin/env python3
"""
Check available Windows fonts for Vietnamese
"""

import os

def check_windows_fonts():
    """Check Windows fonts directory"""
    
    fonts_dir = "C:/Windows/Fonts"
    vietnamese_fonts = []
    
    if not os.path.exists(fonts_dir):
        print("❌ Windows Fonts directory not found")
        return
    
    # Look for Vietnamese-compatible fonts
    target_fonts = [
        ('arial.ttf', 'Arial'),
        ('arialbd.ttf', 'Arial Bold'),  
        ('calibri.ttf', 'Calibri'),
        ('calibrib.ttf', 'Calibri Bold'),
        ('times.ttf', 'Times New Roman'),
        ('timesbd.ttf', 'Times Bold'),
        ('DejaVuSans.ttf', 'DejaVu Sans'),
        ('DejaVuSans-Bold.ttf', 'DejaVu Bold')
    ]
    
    print("🔍 Checking Windows fonts for Vietnamese support...")
    print(f"📁 Fonts directory: {fonts_dir}")
    print()
    
    for font_file, font_name in target_fonts:
        font_path = os.path.join(fonts_dir, font_file)
        if os.path.exists(font_path):
            size_kb = round(os.path.getsize(font_path) / 1024)
            vietnamese_fonts.append(font_name)
            print(f"✅ {font_name:<20} | {font_file:<25} | {size_kb} KB")
        else:
            print(f"❌ {font_name:<20} | {font_file:<25} | Not found")
    
    print(f"\n📊 Found {len(vietnamese_fonts)} Vietnamese-compatible fonts:")
    for font in vietnamese_fonts:
        print(f"   • {font}")
    
    if vietnamese_fonts:
        print(f"\n🎯 Recommendation: Use {vietnamese_fonts[0]} for best results")
    else:
        print("\n⚠️ No Vietnamese fonts found!")
        print("💡 Consider installing Arial or DejaVu fonts")

if __name__ == '__main__':
    check_windows_fonts()