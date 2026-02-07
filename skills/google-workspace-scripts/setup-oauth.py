#!/usr/bin/env python3
"""
OAuth Setup for Google Workspace (Sheets, Docs, Slides)
Run this on your LOCAL machine (not VM) - requires browser
"""

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

# All scopes needed for Sheets, Docs, Slides
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/presentations'
]

def main():
    print("=" * 60)
    print("Google Workspace OAuth Setup")
    print("=" * 60)
    print("\nThis will generate tokens for:")
    print("  - Google Sheets")
    print("  - Google Docs")
    print("  - Google Slides")
    print("\nA browser window will open for authentication.")
    print("=" * 60)
    input("\nPress Enter to continue...")
    
    # Check for credentials file
    creds_file = 'oauth-credentials.json'
    if not os.path.exists(creds_file):
        print(f"\n❌ ERROR: {creds_file} not found!")
        print("\nGet it from:")
        print("1. Go to: https://console.cloud.google.com/apis/credentials")
        print("2. Create OAuth 2.0 Client ID (Desktop app)")
        print("3. Download JSON as 'oauth-credentials.json'")
        print("4. Place in same directory as this script")
        return
    
    # Run OAuth flow
    print("\n🔐 Starting OAuth flow...")
    flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
    creds = flow.run_local_server(port=0)
    
    # Save tokens (same token works for all 3 services)
    print("\n✅ Authentication successful!")
    print("\n📝 Saving tokens...")
    
    with open('sheets-token.pickle', 'wb') as f:
        pickle.dump(creds, f)
    print("  ✓ sheets-token.pickle")
    
    with open('docs-token.pickle', 'wb') as f:
        pickle.dump(creds, f)
    print("  ✓ docs-token.pickle")
    
    with open('slides-token.pickle', 'wb') as f:
        pickle.dump(creds, f)
    print("  ✓ slides-token.pickle")
    
    print("\n" + "=" * 60)
    print("✅ OAuth setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Upload tokens to VM:")
    print("   gcloud compute scp *-token.pickle openclaw-desktop:~/.openclaw/keys/ \\")
    print("     --zone=us-central1-a --project=linkhealth-care-2024 --tunnel-through-iap")
    print("\n2. Test on VM:")
    print("   ssh openclaw-desktop")
    print("   python3 ~/.openclaw/scripts/sheets-cli.py create 'Test Sheet'")
    print("=" * 60)

if __name__ == '__main__':
    main()
