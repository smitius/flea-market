#!/usr/bin/env python3
"""
Script to clean flag-emoji related styles from CSS file
"""

import re

def clean_css():
    # Read the CSS file
    with open('app/static/css/style.css', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Original file size: {len(content)} characters")
    print(f"Original flag-emoji count: {content.count('flag-emoji')}")
    
    # Remove flag-emoji related CSS rules and comments
    patterns_to_remove = [
        # Remove .flag-emoji rules
        r'\.flag-emoji\s*\{[^}]*\}',
        # Remove nested flag-emoji rules
        r'\.language-toggle\s+\.flag-emoji\s*\{[^}]*\}',
        r'\.language-option\s+\.flag-emoji\s*\{[^}]*\}', 
        r'\.mobile-language-option\s+\.flag-emoji\s*\{[^}]*\}',
        # Remove comments about emoji flags
        r'/\*[^*]*emoji flag[^*]*\*/',
        r'/\*[^*]*Enhanced emoji flag support[^*]*\*/',
        # Remove @supports rules for emoji
        r'@supports not \([^)]*Apple Color Emoji[^)]*\)\s*\{[^}]*\.flag-emoji[^}]*\}',
        # Remove media queries for emoji
        r'@media \([^)]*prefers-contrast[^)]*\)\s*\{[^}]*\.flag-emoji[^}]*\}',
    ]
    
    for pattern in patterns_to_remove:
        old_content = content
        content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
        if old_content != content:
            print(f"Removed pattern: {pattern[:50]}...")
    
    # Clean up multiple empty lines
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Write back the cleaned content
    with open('app/static/css/style.css', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Cleaned file size: {len(content)} characters")
    print(f"Remaining flag-emoji count: {content.count('flag-emoji')}")
    print("CSS file cleaned successfully!")

if __name__ == '__main__':
    clean_css()