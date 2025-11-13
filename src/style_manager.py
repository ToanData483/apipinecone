#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Business Style Manager - FIXED VERSION  
Professional business book styling với Vietnamese font support
"""

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
import logging
import os

class BusinessStyleManager:
    """Professional business book styles with Vietnamese support"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.styles = getSampleStyleSheet()
        self.base_font = self._register_vietnamese_fonts()
        self._create_business_styles()
    
    def _register_vietnamese_fonts(self):
        """Register Vietnamese-compatible fonts"""
        # Windows fonts that support Vietnamese  
        font_paths = [
            ('C:/Windows/Fonts/arial.ttf', 'Arial'),
            ('C:/Windows/Fonts/calibri.ttf', 'Calibri'),
            ('C:/Windows/Fonts/DejaVuSans.ttf', 'DejaVu'),
            # Linux fonts
            ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 'DejaVu'),
            ('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', 'Liberation'),
        ]
        
        for font_path, font_name in font_paths:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    
                    # Try to register bold variant
                    bold_variants = [
                        font_path.replace('.ttf', 'b.ttf'),  # arialb.ttf  
                        font_path.replace('.ttf', '-Bold.ttf'),
                        font_path.replace('Regular', 'Bold'),
                        font_path.replace('arial.ttf', 'arialbd.ttf'),  # Windows Arial Bold
                        font_path.replace('calibri.ttf', 'calibrib.ttf'),  # Windows Calibri Bold
                    ]
                    
                    bold_registered = False
                    for bold_path in bold_variants:
                        if os.path.exists(bold_path):
                            try:
                                pdfmetrics.registerFont(TTFont(f'{font_name}-Bold', bold_path))
                                bold_registered = True
                                break
                            except:
                                continue
                    
                    # Register font mappings
                    addMapping(font_name, 0, 0, font_name)
                    if bold_registered:
                        addMapping(font_name, 1, 0, f'{font_name}-Bold')
                    
                    self.logger.info(f"✅ Registered Vietnamese font: {font_name}")
                    return font_name
                    
                except Exception as e:
                    self.logger.debug(f"Failed to register {font_name}: {e}")
                    continue
        
        # Fallback to Helvetica with warning
        self.logger.warning("⚠️ No Vietnamese fonts found, using Helvetica")
        self.logger.info("💡 Install Arial or Calibri for better Vietnamese support")
        return 'Helvetica'
    
    def _create_business_styles(self):
        """Create business book paragraph styles"""
        
        bold_font = f'{self.base_font}-Bold' if self.base_font != 'Helvetica' else 'Helvetica-Bold'
        italic_font = f'{self.base_font}-Italic' if self.base_font != 'Helvetica' else 'Helvetica-Oblique'
        
        # CHAPTER TITLE
        self.styles.add(ParagraphStyle(
            name='BusinessChapter',
            fontSize=24,
            textColor=HexColor('#1a1a1a'),
            spaceAfter=24,
            spaceBefore=12,
            alignment=TA_LEFT,
            fontName=bold_font,
            leading=30
        ))
        
        # BODY TEXT  
        self.styles.add(ParagraphStyle(
            name='BusinessBody',
            fontSize=12,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            spaceBefore=0,
            firstLineIndent=0,
            fontName=self.base_font,
            textColor=HexColor('#1a1a1a'),
            wordWrap='CJK'  # Better for Vietnamese
        ))
        
        # DIALOG
        self.styles.add(ParagraphStyle(
            name='BusinessDialog',
            parent=self.styles['BusinessBody'],
            leftIndent=0.25*inch,
            fontName=italic_font,
            textColor=HexColor('#2a2a2a')
        ))
        
        # FIRST PARAGRAPH (no spacing)
        self.styles.add(ParagraphStyle(
            name='BusinessFirst',
            parent=self.styles['BusinessBody'],
            spaceBefore=0
        ))
        
        self.logger.info(f"✅ Business styles created with {self.base_font} font")
    
    def get_style(self, style_name):
        """Get style by name"""
        if style_name in self.styles:
            return self.styles[style_name]
        else:
            self.logger.warning(f"Style {style_name} not found, using BusinessBody")
            return self.styles['BusinessBody']

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("🧪 Testing Business Style Manager...")
    style_manager = BusinessStyleManager()
    print(f"✅ Base font: {style_manager.base_font}")
