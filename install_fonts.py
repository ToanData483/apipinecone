#!/usr/bin/env python3
"""
Download and install Vietnamese fonts for Windows
"""

import os
import urllib.request
import zipfile
import shutil

def download_dejavu_fonts():
    """Download DejaVu fonts với Vietnamese support"""
    
    fonts_dir = "fonts"
    os.makedirs(fonts_dir, exist_ok=True)
    
    print("📥 Downloading DejaVu fonts...")
    
    # DejaVu fonts download URL
    dejavu_url = "https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.zip"
    
    try:
        # Download
        zip_path = os.path.join(fonts_dir, "dejavu-fonts.zip")
        urllib.request.urlretrieve(dejavu_url, zip_path)
        print("✅ Downloaded DejaVu fonts")
        
        # Extract
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(fonts_dir)
        
        # Find TTF files
        for root, dirs, files in os.walk(fonts_dir):
            for file in files:
                if file.endswith('.ttf'):
                    ttf_path = os.path.join(root, file)
                    print(f"📄 Found: {file}")
        
        print("✅ DejaVu fonts extracted to fonts/ folder")
        return True
        
    except Exception as e:
        print(f"❌ Failed to download fonts: {e}")
        return False

def install_windows_fonts():
    """Copy fonts to Windows Fonts folder (requires admin)"""
    try:
        windows_fonts = "C:/Windows/Fonts"
        
        if not os.path.exists(windows_fonts):
            print("❌ Windows Fonts folder not found")
            return False
        
        # Copy DejaVu fonts
        fonts_to_copy = [
            "fonts/dejavu-fonts-ttf-2.37/ttf/DejaVuSans.ttf",
            "fonts/dejavu-fonts-ttf-2.37/ttf/DejaVuSans-Bold.ttf",
            "fonts/dejavu-fonts-ttf-2.37/ttf/DejaVuSans-Oblique.ttf"
        ]
        
        for font_file in fonts_to_copy:
            if os.path.exists(font_file):
                font_name = os.path.basename(font_file)
                dest_path = os.path.join(windows_fonts, font_name)
                
                try:
                    shutil.copy2(font_file, dest_path)
                    print(f"✅ Installed: {font_name}")
                except PermissionError:
                    print(f"⚠️ Need admin rights to install: {font_name}")
                    print(f"💡 Manually copy {font_file} to {windows_fonts}")
        
        return True
        
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        return False

def main():
    print("🔤 Installing Vietnamese fonts...")
    
    # Download fonts
    if download_dejavu_fonts():
        print("\n📁 Fonts downloaded successfully!")
        print("💡 To install system-wide (optional):")
        print("   1. Run as Administrator")
        print("   2. Or manually copy TTF files to C:/Windows/Fonts/")
    
    print(f"\n📍 Fonts location: {os.path.abspath('fonts')}")
    print("\n🔧 Next: Run update_style_manager.py to use local fonts")

if __name__ == '__main__':
    main()