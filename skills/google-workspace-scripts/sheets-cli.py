#!/usr/bin/env python3
"""Google Sheets CLI for OpenClaw"""

import argparse
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
TOKEN_PATH = os.path.expanduser('~/.openclaw/keys/sheets-token.pickle')

def get_service():
    """Get authenticated Sheets service"""
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)
        else:
            print("ERROR: Token not found or invalid. Run OAuth setup first.")
            exit(1)
    
    return build('sheets', 'v4', credentials=creds)

def create_spreadsheet(title):
    """Create new spreadsheet"""
    service = get_service()
    spreadsheet = {
        'properties': {'title': title}
    }
    result = service.spreadsheets().create(body=spreadsheet).execute()
    print(f"Created: {result['properties']['title']}")
    print(f"ID: {result['spreadsheetId']}")
    print(f"URL: https://docs.google.com/spreadsheets/d/{result['spreadsheetId']}")

def read_sheet(spreadsheet_id, range_name='Sheet1'):
    """Read data from spreadsheet"""
    service = get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()
    
    values = result.get('values', [])
    if not values:
        print("No data found")
    else:
        for row in values:
            print('\t'.join(str(cell) for cell in row))

def write_sheet(spreadsheet_id, range_name, values):
    """Write data to spreadsheet"""
    service = get_service()
    body = {'values': values}
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()
    print(f"Updated {result.get('updatedCells')} cells")

def append_sheet(spreadsheet_id, range_name, values):
    """Append data to spreadsheet"""
    service = get_service()
    body = {'values': values}
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()
    print(f"Appended {result.get('updates', {}).get('updatedCells')} cells")

def main():
    parser = argparse.ArgumentParser(description='Google Sheets CLI')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Create
    create_parser = subparsers.add_parser('create', help='Create spreadsheet')
    create_parser.add_argument('title', help='Spreadsheet title')
    
    # Read
    read_parser = subparsers.add_parser('read', help='Read spreadsheet')
    read_parser.add_argument('id', help='Spreadsheet ID')
    read_parser.add_argument('--range', default='Sheet1', help='Range (default: Sheet1)')
    
    # Write
    write_parser = subparsers.add_parser('write', help='Write to spreadsheet')
    write_parser.add_argument('id', help='Spreadsheet ID')
    write_parser.add_argument('range', help='Range (e.g., A1:B2)')
    write_parser.add_argument('values', help='Values (comma-separated rows, semicolon-separated cells)')
    
    # Append
    append_parser = subparsers.add_parser('append', help='Append to spreadsheet')
    append_parser.add_argument('id', help='Spreadsheet ID')
    append_parser.add_argument('range', help='Range (e.g., A:A)')
    append_parser.add_argument('values', help='Values (comma-separated rows, semicolon-separated cells)')
    
    args = parser.parse_args()
    
    if args.command == 'create':
        create_spreadsheet(args.title)
    elif args.command == 'read':
        read_sheet(args.id, args.range)
    elif args.command == 'write':
        rows = [row.split(';') for row in args.values.split(',')]
        write_sheet(args.id, args.range, rows)
    elif args.command == 'append':
        rows = [row.split(';') for row in args.values.split(',')]
        append_sheet(args.id, args.range, rows)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
