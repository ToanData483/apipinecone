#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Content Processor
Xử lý nội dung từ Google Sheets - CHỈ format, KHÔNG thêm content
"""

import re
import unicodedata
import logging

class ContentProcessor:
    """Process raw content from Google Sheets Column D"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.paragraph_min_length = 10
    
    def clean_vietnamese_text(self, text):
        """Clean and normalize Vietnamese text ONLY - no content changes"""
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
        """Detect content type WITHOUT changing content"""
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
        """Process raw content from Google Sheets Column D"""
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
