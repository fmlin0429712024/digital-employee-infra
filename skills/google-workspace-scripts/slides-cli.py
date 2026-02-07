#!/usr/bin/env python3
"""Google Slides CLI for OpenClaw"""

import argparse
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/presentations']
TOKEN_PATH = os.path.expanduser('~/.openclaw/keys/slides-token.pickle')

def get_service():
    """Get authenticated Slides service"""
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
    
    return build('slides', 'v1', credentials=creds)

def create_presentation(title):
    """Create new presentation"""
    service = get_service()
    presentation = service.presentations().create(body={'title': title}).execute()
    print(f"Created: {presentation['title']}")
    print(f"ID: {presentation['presentationId']}")
    print(f"URL: https://docs.google.com/presentation/d/{presentation['presentationId']}")

def read_presentation(presentation_id):
    """Read presentation info"""
    service = get_service()
    presentation = service.presentations().get(presentationId=presentation_id).execute()
    
    print(f"Title: {presentation['title']}")
    print(f"Slides: {len(presentation.get('slides', []))}")
    print("\nSlide titles:")
    for i, slide in enumerate(presentation.get('slides', []), 1):
        print(f"  {i}. Slide {slide['objectId']}")

def add_slide(presentation_id, title_text, body_text=None):
    """Add slide with title and optional body"""
    service = get_service()

    import uuid
    slide_id = f"slide_{uuid.uuid4().hex[:8]}"

    # Create slide with specific ID
    requests = [
        {
            'createSlide': {
                'objectId': slide_id,
                'slideLayoutReference': {
                    'predefinedLayout': 'TITLE_AND_BODY'
                }
            }
        }
    ]

    response = service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': requests}
    ).execute()

    # Get the slide to find placeholder IDs
    presentation = service.presentations().get(presentationId=presentation_id).execute()

    title_id = None
    body_id = None

    for slide in presentation.get('slides', []):
        if slide['objectId'] == slide_id:
            for element in slide.get('pageElements', []):
                shape = element.get('shape', {})
                placeholder = shape.get('placeholder', {})
                if placeholder.get('type') == 'TITLE':
                    title_id = element['objectId']
                elif placeholder.get('type') == 'BODY':
                    body_id = element['objectId']

    # Insert text into placeholders
    text_requests = []

    if title_id and title_text:
        text_requests.append({
            'insertText': {
                'objectId': title_id,
                'text': title_text
            }
        })

    if body_id and body_text:
        text_requests.append({
            'insertText': {
                'objectId': body_id,
                'text': body_text
            }
        })

    if text_requests:
        service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': text_requests}
        ).execute()

    print(f"Added slide: {slide_id}")
    print(f"Title: {title_text}")
    if body_text:
        print(f"Body: {body_text[:50]}...")

def main():
    parser = argparse.ArgumentParser(description='Google Slides CLI')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Create
    create_parser = subparsers.add_parser('create', help='Create presentation')
    create_parser.add_argument('title', help='Presentation title')
    
    # Read
    read_parser = subparsers.add_parser('read', help='Read presentation')
    read_parser.add_argument('id', help='Presentation ID')
    
    # Add slide
    add_parser = subparsers.add_parser('add-slide', help='Add slide')
    add_parser.add_argument('id', help='Presentation ID')
    add_parser.add_argument('title', help='Slide title')
    add_parser.add_argument('--body', help='Slide body text', default=None)

    args = parser.parse_args()

    if args.command == 'create':
        create_presentation(args.title)
    elif args.command == 'read':
        read_presentation(args.id)
    elif args.command == 'add-slide':
        add_slide(args.id, args.title, args.body)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
