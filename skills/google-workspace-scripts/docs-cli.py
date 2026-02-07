#!/usr/bin/env python3
"""Google Docs CLI for OpenClaw"""

import argparse
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/documents']
TOKEN_PATH = os.path.expanduser('~/.openclaw/keys/docs-token.pickle')

def get_service():
    """Get authenticated Docs service"""
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
    
    return build('docs', 'v1', credentials=creds)

def create_doc(title):
    """Create new document"""
    service = get_service()
    doc = service.documents().create(body={'title': title}).execute()
    print(f"Created: {doc['title']}")
    print(f"ID: {doc['documentId']}")
    print(f"URL: https://docs.google.com/document/d/{doc['documentId']}")

def read_doc(doc_id):
    """Read document content"""
    service = get_service()
    doc = service.documents().get(documentId=doc_id).execute()
    
    print(f"Title: {doc['title']}")
    print("\nContent:")
    content = doc.get('body', {}).get('content', [])
    for element in content:
        if 'paragraph' in element:
            for text_run in element['paragraph'].get('elements', []):
                if 'textRun' in text_run:
                    print(text_run['textRun']['content'], end='')

def append_text(doc_id, text):
    """Append text to document"""
    service = get_service()
    requests = [{
        'insertText': {
            'location': {'index': 1},
            'text': text + '\n'
        }
    }]
    result = service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': requests}
    ).execute()
    print(f"Appended text to document")

def main():
    parser = argparse.ArgumentParser(description='Google Docs CLI')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Create
    create_parser = subparsers.add_parser('create', help='Create document')
    create_parser.add_argument('title', help='Document title')
    
    # Read
    read_parser = subparsers.add_parser('read', help='Read document')
    read_parser.add_argument('id', help='Document ID')
    
    # Append
    append_parser = subparsers.add_parser('append', help='Append text')
    append_parser.add_argument('id', help='Document ID')
    append_parser.add_argument('text', help='Text to append')
    
    args = parser.parse_args()
    
    if args.command == 'create':
        create_doc(args.title)
    elif args.command == 'read':
        read_doc(args.id)
    elif args.command == 'append':
        append_text(args.id, args.text)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
