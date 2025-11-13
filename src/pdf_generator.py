#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Business PDF Generator
Generate professional business-style PDFs from processed content
"""

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
    """Generate professional business-style PDFs"""
    
    def __init__(self, style_manager, output_dir='output/temp'):
        self.style_manager = style_manager
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_sheet_pdf(self, sheet_name, content_blocks, metadata=None):
        """Generate PDF for a single sheet"""
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
        """Build ReportLab story from content blocks"""
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
        """Check if text looks like a chapter title"""
        if not text:
            return False
        return any(keyword in text.lower() for keyword in ['chương', 'chapter', 'phần'])
    
    def _sanitize_filename(self, filename):
        """Sanitize filename for filesystem"""
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
        return safe_name[:50] if len(safe_name) > 50 else safe_name

if __name__ == '__main__':
    print("🧪 Testing PDF Generator...")
    print("✅ BusinessPDFGenerator class available")
