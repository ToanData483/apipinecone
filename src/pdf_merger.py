#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Merger - FIXED VERSION
Combine multiple sheet PDFs into final ebook
"""

from PyPDF2 import PdfMerger
import os
import logging

class BusinessPDFMerger:
    """Merge multiple PDFs into final business ebook"""
    
    def __init__(self, output_dir='output/final'):
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        os.makedirs(output_dir, exist_ok=True)
    
    def merge_sheets_to_ebook(self, pdf_files, output_filename, add_bookmarks=True, metadata=None):
        """Merge multiple sheet PDFs into final ebook"""
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
                    # FIXED: Use outline_item instead of deprecated bookmark
                    try:
                        merger.append(pdf_file, outline_item=chapter_name)
                    except TypeError:
                        # Fallback for older PyPDF2 versions
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
        """Extract chapter name from PDF filename"""
        filename = os.path.basename(pdf_file)
        name = os.path.splitext(filename)[0]
        return name.replace('_', ' ')
    
    def validate_ebook(self, ebook_path):
        """Validate the final ebook PDF"""
        return os.path.exists(ebook_path) and os.path.getsize(ebook_path) > 0
    
    def get_ebook_stats(self, ebook_path):
        """Get ebook statistics"""
        if not self.validate_ebook(ebook_path):
            return None
        
        try:
            from PyPDF2 import PdfReader
            
            reader = PdfReader(ebook_path)
            file_size = os.path.getsize(ebook_path)
            
            return {
                'file_path': ebook_path,
                'file_size_kb': round(file_size / 1024, 2),
                'file_size_mb': round(file_size / (1024 * 1024), 2),
                'num_pages': len(reader.pages),
                'title': 'Vietnamese Business Ebook'
            }
        except Exception:
            return {
                'file_path': ebook_path,
                'file_size_kb': round(os.path.getsize(ebook_path) / 1024, 2),
                'num_pages': 'Unknown'
            }

if __name__ == '__main__':
    print("🧪 Testing PDF Merger...")
    print("✅ BusinessPDFMerger class available")
