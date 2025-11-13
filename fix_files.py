#!/usr/bin/env python3
"""
Auto-generate all missing source files with correct classes
"""

import os

def create_content_processor():
    content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
Content Processor
Xử lý nội dung từ Google Sheets - CHỈ format, KHÔNG thêm content
\"\"\"

import re
import unicodedata
import logging

class ContentProcessor:
    \"\"\"Process raw content from Google Sheets Column D\"\"\"
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.paragraph_min_length = 10
    
    def clean_vietnamese_text(self, text):
        \"\"\"Clean and normalize Vietnamese text ONLY - no content changes\"\"\"
        if not text:
            return ""
        
        text = unicodedata.normalize('NFC', text)
        
        replacements = {
            '"': '"',
            '"': '"',
            ''': "'",
            ''': "'",
            '–': '—',
            '...': '…',
            '  ': ' ',
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text.strip()
    
    def detect_content_type(self, text):
        \"\"\"Detect content type WITHOUT changing content\"\"\"
        if not text:
            return 'empty'
        
        text_clean = text.strip()
        
        if ('"' in text_clean or 
            text_clean.startswith('"') or 
            text_clean.startswith('—')):
            return 'dialog'
        
        if len(text_clean) < 100:
            if (text_clean.isupper() or 
                any(keyword in text_clean.lower() for keyword in ['chương', 'phần', 'mục'])):
                return 'header'
        
        return 'paragraph'
    
    def process_sheet_content(self, raw_content_list):
        \"\"\"Process raw content from Google Sheets Column D\"\"\"
        if not raw_content_list:
            self.logger.warning("⚠️ No content to process")
            return []
        
        processed_blocks = []
        
        for i, raw_text in enumerate(raw_content_list):
            if not raw_text or not raw_text.strip():
                continue
            
            cleaned_text = self.clean_vietnamese_text(raw_text)
            
            if len(cleaned_text) < self.paragraph_min_length:
                continue
            
            content_type = self.detect_content_type(cleaned_text)
            
            block = {
                'type': content_type,
                'content': cleaned_text,
                'original_index': i,
                'original_length': len(raw_text)
            }
            
            processed_blocks.append(block)
        
        self.logger.info(f"📝 Processed {len(processed_blocks)} content blocks")
        return processed_blocks

if __name__ == '__main__':
    print("🧪 Testing Content Processor...")
    processor = ContentProcessor()
    print("✅ ContentProcessor class available")
"""
    return content

def create_style_manager():
    content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
Business Style Manager
Professional business book styling với Vietnamese font support
\"\"\"

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
    \"\"\"Professional business book styles with Vietnamese support\"\"\"
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.styles = getSampleStyleSheet()
        self.base_font = self._register_vietnamese_fonts()
        self._create_business_styles()
    
    def _register_vietnamese_fonts(self):
        \"\"\"Register Vietnamese-compatible fonts\"\"\"
        font_paths = [
            ('C:/Windows/Fonts/DejaVuSans.ttf', 'DejaVu'),
            ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 'DejaVu'),
            ('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', 'Liberation'),
        ]
        
        for font_path, font_name in font_paths:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    
                    bold_path = font_path.replace('Regular', 'Bold').replace('.ttf', '-Bold.ttf')
                    if os.path.exists(bold_path):
                        pdfmetrics.registerFont(TTFont(f'{font_name}-Bold', bold_path))
                    
                    addMapping(font_name, 0, 0, font_name)
                    if os.path.exists(bold_path):
                        addMapping(font_name, 1, 0, f'{font_name}-Bold')
                    
                    self.logger.info(f"✅ Registered Vietnamese font: {font_name}")
                    return font_name
                    
                except Exception:
                    continue
        
        self.logger.warning("⚠️ Using Helvetica")
        return 'Helvetica'
    
    def _create_business_styles(self):
        \"\"\"Create business book paragraph styles\"\"\"
        
        self.styles.add(ParagraphStyle(
            name='BusinessChapter',
            fontSize=24,
            textColor=HexColor('#1a1a1a'),
            spaceAfter=24,
            spaceBefore=12,
            alignment=TA_LEFT,
            fontName=f'{self.base_font}-Bold' if self.base_font != 'Helvetica' else 'Helvetica-Bold',
            leading=30
        ))
        
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
            wordWrap='CJK'
        ))
        
        self.styles.add(ParagraphStyle(
            name='BusinessDialog',
            parent=self.styles['BusinessBody'],
            leftIndent=0.25*inch,
            fontName=f'{self.base_font}-Italic' if self.base_font != 'Helvetica' else 'Helvetica-Oblique',
        ))
        
        self.logger.info("✅ Business styles created")
    
    def get_style(self, style_name):
        \"\"\"Get style by name\"\"\"
        if style_name in self.styles:
            return self.styles[style_name]
        else:
            return self.styles['BusinessBody']

if __name__ == '__main__':
    print("🧪 Testing Business Style Manager...")
    style_manager = BusinessStyleManager()
    print(f"✅ Base font: {style_manager.base_font}")
"""
    return content

def create_pdf_generator():
    content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
Business PDF Generator
Generate professional business-style PDFs from processed content
\"\"\"

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfgen import canvas
import os
import logging
import re

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self):
        self.saveState()
        self.setFont("Helvetica", 9)
        page_num = f"{self._pageNumber}"
        self.drawCentredString(A4[0] / 2, 0.6 * inch, page_num)
        self.restoreState()

class BusinessPDFGenerator:
    \"\"\"Generate professional business-style PDFs\"\"\"
    
    def __init__(self, style_manager, output_dir='output/temp'):
        self.style_manager = style_manager
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_sheet_pdf(self, sheet_name, content_blocks, metadata=None):
        \"\"\"Generate PDF for a single sheet\"\"\"
        if not content_blocks:
            self.logger.warning(f"⚠️ No content blocks for {sheet_name}")
            return None
        
        safe_filename = self._sanitize_filename(sheet_name)
        output_path = os.path.join(self.output_dir, f"{safe_filename}.pdf")
        
        self.logger.info(f"📄 Generating PDF: {sheet_name}")
        
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=0.8*inch,
                leftMargin=0.8*inch,
                topMargin=0.9*inch,
                bottomMargin=0.8*inch,
                title=sheet_name
            )
            
            story = self._build_story(sheet_name, content_blocks)
            doc.build(story, canvasmaker=NumberedCanvas)
            
            self.logger.info(f"✅ PDF generated: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"❌ Failed to generate PDF for {sheet_name}: {e}")
            return None
    
    def _build_story(self, sheet_name, content_blocks):
        \"\"\"Build ReportLab story from content blocks\"\"\"
        story = []
        
        if self._is_chapter_title(sheet_name):
            title_para = Paragraph(sheet_name, self.style_manager.get_style('BusinessChapter'))
            story.append(title_para)
            story.append(Spacer(1, 0.2*inch))
        
        for block in content_blocks:
            if not block['content'].strip():
                continue
            
            content = block['content']
            content_type = block['type']
            
            if content_type == 'dialog':
                style = self.style_manager.get_style('BusinessDialog')
            else:
                style = self.style_manager.get_style('BusinessBody')
            
            para = Paragraph(content, style)
            story.append(para)
            story.append(Spacer(1, 0.05*inch))
        
        return story
    
    def _is_chapter_title(self, text):
        \"\"\"Check if text looks like a chapter title\"\"\"
        if not text:
            return False
        return any(keyword in text.lower() for keyword in ['chương', 'chapter', 'phần'])
    
    def _sanitize_filename(self, filename):
        \"\"\"Sanitize filename for filesystem\"\"\"
        safe_name = re.sub(r'[<>:"/\\\\|?*]', '_', filename)
        return safe_name[:50] if len(safe_name) > 50 else safe_name

if __name__ == '__main__':
    print("🧪 Testing PDF Generator...")
    print("✅ BusinessPDFGenerator class available")
"""
    return content

def create_pdf_merger():
    content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
PDF Merger
Combine multiple sheet PDFs into final ebook
\"\"\"

from PyPDF2 import PdfMerger
import os
import logging

class BusinessPDFMerger:
    \"\"\"Merge multiple PDFs into final business ebook\"\"\"
    
    def __init__(self, output_dir='output/final'):
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        os.makedirs(output_dir, exist_ok=True)
    
    def merge_sheets_to_ebook(self, pdf_files, output_filename, add_bookmarks=True, metadata=None):
        \"\"\"Merge multiple sheet PDFs into final ebook\"\"\"
        if not pdf_files:
            self.logger.error("❌ No PDF files to merge")
            return None
        
        existing_files = [f for f in pdf_files if os.path.exists(f)]
        
        if not existing_files:
            self.logger.error("❌ No valid PDF files found")
            return None
        
        output_path = os.path.join(self.output_dir, output_filename)
        self.logger.info(f"📚 Merging {len(existing_files)} PDFs into ebook")
        
        try:
            merger = PdfMerger()
            
            for pdf_file in existing_files:
                chapter_name = self._extract_chapter_name(pdf_file)
                if add_bookmarks:
                    merger.append(pdf_file, bookmark=chapter_name)
                else:
                    merger.append(pdf_file)
                self.logger.info(f"📄 Added: {chapter_name}")
            
            merger.write(output_path)
            merger.close()
            
            self.logger.info(f"✅ Ebook created: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"❌ Failed to merge PDFs: {e}")
            return None
    
    def _extract_chapter_name(self, pdf_file):
        \"\"\"Extract chapter name from PDF filename\"\"\"
        filename = os.path.basename(pdf_file)
        name = os.path.splitext(filename)[0]
        return name.replace('_', ' ')
    
    def validate_ebook(self, ebook_path):
        \"\"\"Validate the final ebook PDF\"\"\"
        return os.path.exists(ebook_path) and os.path.getsize(ebook_path) > 0

if __name__ == '__main__':
    print("🧪 Testing PDF Merger...")
    print("✅ BusinessPDFMerger class available")
"""
    return content

def create_thread_manager():
    content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
Thread Manager
Handle multi-threaded processing of Google Sheets
\"\"\"

from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import time

class ThreadManager:
    \"\"\"Manage parallel processing of multiple sheets\"\"\"
    
    def __init__(self, max_workers=None):
        if max_workers is None:
            import os
            max_workers = min(os.cpu_count() or 4, 6)
        
        self.max_workers = max_workers
        self.logger = logging.getLogger(__name__)
    
    def process_sheets_parallel(self, sheets, processor_func, *args, **kwargs):
        \"\"\"Process multiple sheets in parallel\"\"\"
        if not sheets:
            return {}
        
        results = {}
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_sheet = {
                executor.submit(processor_func, sheet, *args, **kwargs): sheet
                for sheet in sheets
            }
            
            for future in as_completed(future_to_sheet):
                sheet_name = future_to_sheet[future]
                try:
                    result = future.result(timeout=300)
                    if result:
                        results[sheet_name] = result
                        self.logger.info(f"✅ Completed: {sheet_name}")
                    else:
                        self.logger.warning(f"⚠️ No result for: {sheet_name}")
                except Exception as e:
                    self.logger.error(f"❌ Failed {sheet_name}: {str(e)}")
        
        total_time = time.time() - start_time
        self.logger.info(f"🏁 Processing completed in {total_time:.1f} seconds")
        
        return results

def process_single_sheet(sheet_name, spreadsheet_id, sheets_reader, content_processor, pdf_generator):
    \"\"\"Process a single sheet - designed for threading\"\"\"
    logger = logging.getLogger(__name__)
    
    try:
        raw_content = sheets_reader.read_column_d(spreadsheet_id, sheet_name)
        if not raw_content:
            return None
        
        content_blocks = content_processor.process_sheet_content(raw_content)
        if not content_blocks:
            return None
        
        pdf_path = pdf_generator.generate_sheet_pdf(sheet_name, content_blocks)
        return pdf_path
    
    except Exception as e:
        logger.error(f"❌ Error processing {sheet_name}: {str(e)}")
        return None

if __name__ == '__main__':
    print("🧪 Testing Thread Manager...")
    print("✅ ThreadManager class available")
"""
    return content

def main():
    print("🔧 Auto-generating all source files...")
    
    os.makedirs('src', exist_ok=True)
    
    files_to_create = {
        'src/content_processor.py': create_content_processor(),
        'src/style_manager.py': create_style_manager(), 
        'src/pdf_generator.py': create_pdf_generator(),
        'src/pdf_merger.py': create_pdf_merger(),
        'src/thread_manager.py': create_thread_manager(),
    }
    
    for file_path, content in files_to_create.items():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created: {file_path}")
    
    init_content = """# Vietnamese PDF Ebook Generator Source Package
from .sheets_reader import SheetsReader
from .content_processor import ContentProcessor
from .style_manager import BusinessStyleManager
from .pdf_generator import BusinessPDFGenerator
from .pdf_merger import BusinessPDFMerger
from .thread_manager import ThreadManager, process_single_sheet

__all__ = [
    'SheetsReader',
    'ContentProcessor',
    'BusinessStyleManager', 
    'BusinessPDFGenerator',
    'BusinessPDFMerger',
    'ThreadManager',
    'process_single_sheet'
]
"""
    
    with open('src/__init__.py', 'w', encoding='utf-8') as f:
        f.write(init_content)
    print("✅ Created: src/__init__.py")
    
    print("\n🎉 All files generated successfully!")
    print("\n🧪 Testing imports...")
    
    try:
        from src.content_processor import ContentProcessor
        from src.style_manager import BusinessStyleManager
        from src.pdf_generator import BusinessPDFGenerator
        from src.pdf_merger import BusinessPDFMerger
        from src.thread_manager import ThreadManager
        print("✅ All imports successful!")
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")

if __name__ == '__main__':
    main()