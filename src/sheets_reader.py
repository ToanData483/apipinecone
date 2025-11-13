#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Sheets Reader - WITH RETRY LOGIC
"""

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from google_auth_httplib2 import AuthorizedHttp
import logging
import time
import random
import ssl
import httplib2

class SheetsReader:
    """Google Sheets API reader với retry logic"""

    def __init__(self, credentials_path):
        self.credentials_path = credentials_path
        self.service = None
        self.logger = logging.getLogger(__name__)
        self._initialize_service()

    def _initialize_service(self):
        """Initialize Google Sheets service"""
        try:
            credentials = Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
            )

            # Disable SSL verification for development/testing environment
            http_base = httplib2.Http(disable_ssl_certificate_validation=True)
            http = AuthorizedHttp(credentials, http=http_base)
            self.service = build('sheets', 'v4', http=http)

            # Get service account email for logging
            service_account_email = credentials.service_account_email
            self.logger.info(f"🔑 Using service account: {service_account_email}")
            self.logger.info("✅ Google Sheets API initialized successfully")

        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Google Sheets API: {e}")
            raise

    def get_spreadsheet_info(self, spreadsheet_id):
        """Get spreadsheet metadata"""
        try:
            self.logger.info(f"📊 Accessing spreadsheet: {spreadsheet_id}")

            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=spreadsheet_id
            ).execute()

            title = spreadsheet.get('properties', {}).get('title', 'Unknown')
            sheets = spreadsheet.get('sheets', [])
            sheet_names = [sheet['properties']['title'] for sheet in sheets]

            self.logger.info(f"📚 Spreadsheet: '{title}'")

            if len(sheet_names) > 3:
                visible_sheets = sheet_names[:3]
                hidden_count = len(sheet_names) - 3
                self.logger.info(f"📄 Available sheets ({len(sheet_names)}): {', '.join(visible_sheets)}")
                self.logger.info(f"     ... and {hidden_count} more sheets")
            else:
                self.logger.info(f"📄 Available sheets ({len(sheet_names)}): {', '.join(sheet_names)}")

            return {
                'title': title,
                'sheet_names': sheet_names
            }

        except Exception as e:
            self.logger.error(f"❌ Failed to get spreadsheet info: {e}")
            raise

    def read_column_d(self, spreadsheet_id, sheet_name):
        """Read column D với retry logic"""
        max_retries = 3

        for attempt in range(max_retries):
            try:
                self.logger.info(f"📖 Reading '{sheet_name}' Column D...")

                # Add random delay to avoid rate limiting
                if attempt > 0:
                    delay = random.uniform(1, 3) + (attempt * 2)
                    self.logger.info(f"⏳ Retry {attempt}, waiting {delay:.1f}s...")
                    time.sleep(delay)

                range_name = f"'{sheet_name}'!D:D"
                result = self.service.spreadsheets().values().get(
                    spreadsheetId=spreadsheet_id,
                    range=range_name
                ).execute()

                values = result.get('values', [])
                content_blocks = [row[0] for row in values if row and len(row) > 0 and row[0].strip()]

                if content_blocks:
                    self.logger.info(f"✅ Retrieved {len(content_blocks)} content blocks from '{sheet_name}'")
                    return content_blocks
                else:
                    self.logger.warning(f"⚠️ No content found in '{sheet_name}' Column D")
                    return []

            except Exception as e:
                if attempt == max_retries - 1:
                    self.logger.error(f"❌ Failed to read '{sheet_name}': {str(e)}")
                    return []
                else:
                    self.logger.warning(f"⚠️ Attempt {attempt + 1} failed for '{sheet_name}': {str(e)}")
                    continue

        return []

if __name__ == '__main__':
    print("🧪 Testing Sheets Reader with retry logic...")
    print("✅ SheetsReader class available")
