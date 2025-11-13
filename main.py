#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vietnamese PDF Ebook Generator - Main CLI
Generate professional business-style ebooks from Google Sheets
"""

import argparse
import logging
import os
import sys
import time
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import our modules with correct paths
from src.sheets_reader import SheetsReader
from src.content_processor import ContentProcessor  
from src.style_manager import BusinessStyleManager
from src.pdf_generator import BusinessPDFGenerator
from src.pdf_merger import BusinessPDFMerger
from src.thread_manager import ThreadManager, process_single_sheet

def setup_logging(verbose=False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Reduce noise from some libraries
    logging.getLogger('googleapiclient').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

def load_config():
    """Load configuration from .env file"""
    load_dotenv()
    
    config = {
        'spreadsheet_id': os.getenv('SPREADSHEET_ID'),
        'credentials_path': os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'config/credentials.json'),
        'output_dir': os.getenv('OUTPUT_DIR', 'output'),
        'max_threads': int(os.getenv('MAX_THREADS', '4'))
    }
    
    return config

def validate_setup(config):
    """Validate that required files and config exist"""
    errors = []
    
    # Check credentials file
    if not os.path.exists(config['credentials_path']):
        errors.append(f"Google credentials not found: {config['credentials_path']}")
    
    # Check spreadsheet ID
    if not config['spreadsheet_id']:
        errors.append("SPREADSHEET_ID not set in .env file")
    
    if errors:
        print("❌ Setup validation failed:")
        for error in errors:
            print(f"   • {error}")
        print("\n🔧 Setup instructions:")
        print("   1. Copy .env.example to .env and configure")
        print("   2. Place Google credentials.json in config/ folder")
        print("   3. Set SPREADSHEET_ID in .env")
        return False
    
    return True

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🇻🇳 Vietnamese PDF Ebook Generator")
    print("📚 Business-style professional ebooks from Google Sheets")
    print("=" * 60)

def main():
    """Main application entry point"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Generate professional Vietnamese PDF ebooks from Google Sheets',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --spreadsheet-id "1BxiMVs..." --output "my-book.pdf"
  %(prog)s --spreadsheet-id "1BxiMVs..." --sheets "Chapter 1" "Chapter 2"
  %(prog)s --spreadsheet-id "1BxiMVs..." --threads 8 --verbose
        """
    )
    
    parser.add_argument(
        '--spreadsheet-id',
        required=True,
        help='Google Sheets spreadsheet ID'
    )
    
    parser.add_argument(
        '--output',
        default='vietnamese-ebook.pdf',
        help='Output ebook filename (default: vietnamese-ebook.pdf)'
    )
    
    parser.add_argument(
        '--sheets',
        nargs='+',
        help='Specific sheets to process (default: all sheets)'
    )
    
    parser.add_argument(
        '--threads',
        type=int,
        default=None,
        help='Number of processing threads (default: auto)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--no-bookmarks',
        action='store_true',
        help='Disable PDF bookmarks'
    )
    
    args = parser.parse_args()
    
    # Setup
    print_banner()
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # Load configuration
    config = load_config()
    
    # Override spreadsheet ID from command line
    config['spreadsheet_id'] = args.spreadsheet_id
    
    # Override thread count if specified
    if args.threads:
        config['max_threads'] = args.threads
    
    # Validate setup
    if not validate_setup(config):
        return 1
    
    try:
        start_time = time.time()
        
        # Initialize components
        logger.info("🔧 Initializing components...")
        
        sheets_reader = SheetsReader(config['credentials_path'])
        content_processor = ContentProcessor()
        style_manager = BusinessStyleManager()
        pdf_generator = BusinessPDFGenerator(style_manager, output_dir=os.path.join(config['output_dir'], 'temp'))
        pdf_merger = BusinessPDFMerger(output_dir=os.path.join(config['output_dir'], 'final'))
        thread_manager = ThreadManager(max_workers=config['max_threads'])
        
        # Get spreadsheet information
        logger.info(f"📊 Reading spreadsheet: {config['spreadsheet_id']}")
        spreadsheet_info = sheets_reader.get_spreadsheet_info(config['spreadsheet_id'])
        
        # Determine which sheets to process
        if args.sheets:
            sheets_to_process = args.sheets
            # Validate that specified sheets exist
            missing_sheets = set(sheets_to_process) - set(spreadsheet_info['sheet_names'])
            if missing_sheets:
                logger.warning(f"⚠️ Sheets not found: {', '.join(missing_sheets)}")
                sheets_to_process = [s for s in sheets_to_process if s in spreadsheet_info['sheet_names']]
        else:
            sheets_to_process = spreadsheet_info['sheet_names']
        
        if not sheets_to_process:
            missing_sheets = set(sheets_to_process) - set(spreadsheet_info['sheet_names'])  # Fix this too
            return 1
        
        sheets_to_process = [s for s in sheets_to_process if s in spreadsheet_info['sheet_names']]  # And this
        
        # Estimate processing time
        if len(sheets_to_process) > 1:
            estimate = thread_manager.estimate_processing_time(len(sheets_to_process), avg_time_per_sheet=8)
            logger.info(f"⏱️ Estimated time: {estimate['estimate_seconds']}s ({estimate['parallel_speedup']}x speedup)")
        
        # Process sheets in parallel
        logger.info("🚀 Starting multi-threaded processing...")
        
        results = thread_manager.process_sheets_parallel(
            sheets_to_process,
            process_single_sheet,
            config['spreadsheet_id'],
            sheets_reader,
            content_processor,
            pdf_generator
        )
        
        # Check results
        if not results:
            logger.error("❌ No PDFs were generated successfully")
            return 1
        
        # Prepare PDF files for merging (maintain sheet order)
        pdf_files = []
        for sheet_name in sheets_to_process:
            if sheet_name in results and results[sheet_name]:
                pdf_files.append(results[sheet_name])
        
        if not pdf_files:
            logger.error("❌ No valid PDFs to merge")
            return 1
        
        # Merge PDFs into final ebook
        logger.info(f"📚 Merging {len(pdf_files)} PDFs into final ebook...")
        
        ebook_metadata = {
            'title': spreadsheet_info['title'],
            'author': 'Vietnamese Translation Team',
            'subject': 'Business Book Translation',
            'creator': 'Vietnamese PDF Ebook Generator'
        }
        
        final_ebook_path = pdf_merger.merge_sheets_to_ebook(
            pdf_files,
            args.output,
            add_bookmarks=not args.no_bookmarks,
            metadata=ebook_metadata
        )
        
        if not final_ebook_path:
            logger.error("❌ Failed to create final ebook")
            return 1
        
        # Validate final ebook
        if not pdf_merger.validate_ebook(final_ebook_path):
            logger.error("❌ Final ebook validation failed")
            return 1
        
        # Get final statistics
        ebook_stats = pdf_merger.get_ebook_stats(final_ebook_path)
        end_time = time.time()
        total_time = end_time - start_time
        
        # Success summary
        print("\n" + "="*50)
        print("🎉 EBOOK GENERATION COMPLETE!")
        print("="*50)
        print(f"📚 Ebook: {final_ebook_path}")
        print(f"📊 Statistics:")
        print(f"   • Pages: {ebook_stats['num_pages']}")
        print(f"   • File size: {ebook_stats['file_size_mb']} MB")
        print(f"   • Chapters: {len(pdf_files)}")
        print(f"   • Processing time: {total_time:.1f}s")
        print(f"   • Success rate: {len(results)}/{len(sheets_to_process)} sheets")
        print(f"📖 Title: {ebook_stats['title']}")
        print("="*50)
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("⚠️ Process interrupted by user")
        return 1
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}", exc_info=args.verbose)
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)