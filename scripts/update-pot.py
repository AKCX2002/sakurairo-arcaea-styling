#!/usr/bin/env python3
"""
Regenerate the translation template (.pot) file for the Sakurairo theme.

Scans all PHP files in the theme directory for translatable strings
using __(), _e(), _n(), _x(), _ex() functions and generates a .pot file.

Usage:
    python3 scripts/update-pot.py /path/to/sakurairo-theme
"""

import os
import re
import sys
from datetime import datetime


def find_php_files(theme_dir):
    """Find all PHP files in the theme directory recursively."""
    php_files = []
    exclude_dirs = {'update-checker', 'kirki', 'node_modules'}
    for root, dirs, files in os.walk(theme_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in files:
            if f.endswith('.php'):
                php_files.append(os.path.join(root, f))
    return php_files


def extract_translations(filepath):
    """Extract translatable strings from a PHP file."""
    translations = []
    patterns = [
        # __( 'text', 'domain' )
        r"__\(\s*'((?:[^'\\]|\\.)*)'\s*,\s*'([^']+)'\s*\)",
        # _e( 'text', 'domain' )
        r"_e\(\s*'((?:[^'\\]|\\.)*)'\s*,\s*'([^']+)'\s*\)",
        # _n( 'singular', 'plural', $num, 'domain' )
        r"_n\(\s*'((?:[^'\\]|\\.)*)'\s*,\s*'((?:[^'\\]|\\.)*)'\s*,\s*[^,]+,\s*'([^']+)'\s*\)",
        # _x( 'text', 'context', 'domain' )
        r"_x\(\s*'((?:[^'\\]|\\.)*)'\s*,\s*'((?:[^'\\]|\\.)*)'\s*,\s*'([^']+)'\s*\)",
        # _ex( 'text', 'context', 'domain' )
        r"_ex\(\s*'((?:[^'\\]|\\.)*)'\s*,\s*'((?:[^'\\]|\\.)*)'\s*,\s*'([^']+)'\s*\)",
        # esc_html__(), esc_attr__()
        r"esc_html__\(\s*'((?:[^'\\]|\\.)*)'\s*,\s*'([^']+)'\s*\)",
        r"esc_attr__\(\s*'((?:[^'\\]|\\.)*)'\s*,\s*'([^']+)'\s*\)",
        # esc_html_e(), esc_attr_e()
        r"esc_html_e\(\s*'((?:[^'\\]|\\.)*)'\s*,\s*'([^']+)'\s*\)",
        r"esc_attr_e\(\s*'((?:[^'\\]|\\.)*)'\s*,\s*'([^']+)'\s*\)",
        # _n_noop(), _nx_noop()
        r"_n_noop\(\s*'((?:[^'\\]|\\.)*)'\s*,\s*'((?:[^'\\]|\\.)*)'\s*,\s*'([^']+)'\s*\)",
        r"_nx_noop\(\s*'((?:[^'\\]|\\.)*)'\s*,\s*'((?:[^'\\]|\\.)*)'\s*,\s*'([^']+)'\s*\)",
    ]

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for pattern in patterns:
        for match in re.finditer(pattern, content):
            translations.append({
                'match': match.group(0),
                'groups': match.groups(),
                'line': content[:match.start()].count('\n') + 1
            })

    return translations


def generate_pot(theme_dir, output_path):
    """Generate .pot file from all PHP files."""
    php_files = find_php_files(theme_dir)
    
    # Get theme info from style.css
    theme_name = 'Sakurairo'
    theme_version = '3.0.10'
    style_css = os.path.join(theme_dir, 'style.css')
    if os.path.exists(style_css):
        with open(style_css, 'r', encoding='utf-8') as f:
            content = f.read()
            name_match = re.search(r'Theme Name:\s*(.+)', content)
            ver_match = re.search(r'Version:\s*([\d.]+)', content)
            if name_match:
                theme_name = name_match.group(1).strip()
            if ver_match:
                theme_version = ver_match.group(1).strip()

    lines = [
        f'# Translation template for {theme_name}.',
        f'# Copyright (C) {datetime.now().year} Fuukei',
        '# This file is distributed under the GNU GPL v2 or later.',
        'msgid ""',
        'msgstr ""',
        f'"Project-Id-Version: {theme_name} {theme_version}\\n"',
        f'"Report-Msgid-Bugs-To: \\n"',
        f'"POT-Creation-Date: {datetime.now().strftime("%Y-%m-%d %H:%M%z")}\\n"',
        '"MIME-Version: 1.0\\n"',
        '"Content-Type: text/plain; charset=UTF-8\\n"',
        '"Content-Transfer-Encoding: 8bit\\n"',
        '"Language-Team: \\n"',
        '"X-Generator: update-pot.py\\n"',
        '',
    ]

    all_translations = []
    for php_file in php_files:
        rel_path = os.path.relpath(php_file, theme_dir)
        trans = extract_translations(php_file)
        for t in trans:
            all_translations.append({
                'file': rel_path,
                'line': t['line'],
                'groups': t['groups'],
                'match': t['match'],
            })

    # Group by msgid for deduplication
    seen = {}
    for t in all_translations:
        groups = t['groups']
        if len(groups) == 2:  # __() / _e()
            key = groups[0]
            domain = groups[1] if len(groups) > 1 else 'sakurairo'
        elif len(groups) == 3:  # _n() / _x()
            key = groups[0]
            domain = groups[2] if len(groups) > 2 else 'sakurairo'
        else:
            continue

        if key not in seen:
            seen[key] = {
                'domain': domain,
                'files': [],
                'groups': groups
            }
        seen[key]['files'].append(f'{t["file"]}:{t["line"]}')

    # Write POT entries
    for msgid, info in seen.items():
        for ref in info['files']:
            lines.append(f'#: {ref}')
        lines.append(f'msgid "{msgid}"')
        if len(info['groups']) >= 3 and info['groups'][1]:
            lines.append(f'msgid_plural "{info["groups"][1]}"')
            lines.append('msgstr[0] ""')
            lines.append('msgstr[1] ""')
        else:
            lines.append('msgstr ""')
        lines.append('')

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'✅ Generated POT file: {output_path}')
    print(f'   Found {len(seen)} unique translatable strings in {len(php_files)} files')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        theme_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    else:
        theme_dir = sys.argv[1]

    # Try to find or create languages directory
    languages_dir = os.path.join(theme_dir, 'languages')
    os.makedirs(languages_dir, exist_ok=True)
    output = os.path.join(languages_dir, 'sakurairo.pot')

    generate_pot(theme_dir, output)
