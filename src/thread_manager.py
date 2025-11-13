#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thread Manager
Handle multi-threaded processing of Google Sheets
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import time

class ThreadManager:
    """Manage parallel processing of multiple sheets"""
    
    def __init__(self, max_workers=None):
        if max_workers is None:
            import os
            max_workers = min(os.cpu_count() or 4, 6)
        
        self.max_workers = max_workers
        self.logger = logging.getLogger(__name__)
    
    def process_sheets_parallel(self, sheets, processor_func, *args, **kwargs):
        """Process multiple sheets in parallel"""
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
    """Process a single sheet - designed for threading"""
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
