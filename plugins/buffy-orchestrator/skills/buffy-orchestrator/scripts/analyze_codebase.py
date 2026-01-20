#!/usr/bin/env python3
"""
Fast codebase analysis script for context gathering.
Equivalent to Codebuff's fast codebase indexing.
"""

import os
import sys
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set

# Common ignore patterns
IGNORE_DIRS = {
    'node_modules', '.git', '__pycache__', '.next', 'dist', 'build',
    '.venv', 'venv', 'env', '.env', 'coverage', '.nyc_output',
    '.pytest_cache', '.mypy_cache', 'vendor', 'target'
}

IGNORE_FILES = {
    '.DS_Store', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
    'Cargo.lock', 'poetry.lock', 'composer.lock'
}

# File type categories
FILE_CATEGORIES = {
    'source': {'.ts', '.tsx', '.js', '.jsx', '.py', '.go', '.rs', '.java', '.rb', '.php'},
    'config': {'.json', '.yaml', '.yml', '.toml', '.ini', '.env'},
    'style': {'.css', '.scss', '.sass', '.less'},
    'markup': {'.html', '.htm', '.xml', '.svg'},
    'docs': {'.md', '.mdx', '.rst', '.txt'},
    'test': set(),  # Determined by path
}


def should_ignore(path: Path) -> bool:
    """Check if path should be ignored."""
    for part in path.parts:
        if part in IGNORE_DIRS or part.startswith('.'):
            return True
    if path.name in IGNORE_FILES:
        return True
    return False


def categorize_file(path: Path) -> str:
    """Categorize a file by its type and location."""
    suffix = path.suffix.lower()
    name = path.name.lower()
    path_str = str(path).lower()
    
    # Test files
    if 'test' in name or 'spec' in name or '/test/' in path_str or '/tests/' in path_str:
        return 'test'
    
    # Check by extension
    for category, extensions in FILE_CATEGORIES.items():
        if suffix in extensions:
            return category
    
    return 'other'


def analyze_directory(root_path: str) -> Dict:
    """Analyze a directory and return structured information."""
    root = Path(root_path).resolve()
    
    if not root.exists():
        return {'error': f'Path does not exist: {root_path}'}
    
    result = {
        'root': str(root),
        'stats': {
            'total_files': 0,
            'total_dirs': 0,
            'by_category': defaultdict(int),
            'by_extension': defaultdict(int),
        },
        'structure': {},
        'key_files': [],
        'package_info': None,
    }
    
    # Look for package/project files
    package_files = ['package.json', 'Cargo.toml', 'pyproject.toml', 
                     'requirements.txt', 'go.mod', 'composer.json']
    
    for pf in package_files:
        pf_path = root / pf
        if pf_path.exists():
            result['package_info'] = {
                'type': pf,
                'path': str(pf_path.relative_to(root))
            }
            result['key_files'].append(str(pf_path.relative_to(root)))
            break
    
    # Walk the directory
    dirs_by_depth = defaultdict(list)
    
    for item in root.rglob('*'):
        if should_ignore(item):
            continue
        
        rel_path = item.relative_to(root)
        depth = len(rel_path.parts) - 1
        
        if item.is_dir():
            result['stats']['total_dirs'] += 1
            if depth <= 2:
                dirs_by_depth[depth].append(str(rel_path))
        elif item.is_file():
            result['stats']['total_files'] += 1
            category = categorize_file(rel_path)
            result['stats']['by_category'][category] += 1
            result['stats']['by_extension'][item.suffix.lower()] += 1
            
            # Key files at root or one level deep
            if depth <= 1:
                name = item.name.lower()
                if name in ['readme.md', 'readme.txt', 'readme']:
                    result['key_files'].append(str(rel_path))
                elif name in ['claude.md', '.claude.md']:
                    result['key_files'].append(str(rel_path))
                elif name.startswith('config') or name.endswith('config.ts') or name.endswith('config.js'):
                    result['key_files'].append(str(rel_path))
    
    # Build structure (top 2 levels)
    result['structure'] = {
        'root_dirs': sorted(dirs_by_depth[0])[:20],
        'second_level': {d: [] for d in dirs_by_depth[0][:10]}
    }
    
    for d in dirs_by_depth[1]:
        parent = Path(d).parts[0]
        if parent in result['structure']['second_level']:
            result['structure']['second_level'][parent].append(Path(d).name)
    
    # Trim second level
    for parent in result['structure']['second_level']:
        result['structure']['second_level'][parent] = \
            sorted(result['structure']['second_level'][parent])[:15]
    
    return result


def format_output(analysis: Dict) -> str:
    """Format analysis for human-readable output."""
    if 'error' in analysis:
        return f"Error: {analysis['error']}"
    
    lines = [
        f"# Codebase Analysis: {analysis['root']}",
        "",
        "## Overview",
        f"- **Files:** {analysis['stats']['total_files']}",
        f"- **Directories:** {analysis['stats']['total_dirs']}",
    ]
    
    if analysis['package_info']:
        lines.append(f"- **Project Type:** {analysis['package_info']['type']}")
    
    lines.extend(["", "## File Distribution"])
    for cat, count in sorted(analysis['stats']['by_category'].items(), key=lambda x: -x[1]):
        lines.append(f"- {cat}: {count}")
    
    lines.extend(["", "## Top Extensions"])
    top_ext = sorted(analysis['stats']['by_extension'].items(), key=lambda x: -x[1])[:10]
    for ext, count in top_ext:
        lines.append(f"- {ext or '(no ext)'}: {count}")
    
    lines.extend(["", "## Directory Structure"])
    for d in analysis['structure']['root_dirs']:
        subdirs = analysis['structure']['second_level'].get(d, [])
        if subdirs:
            lines.append(f"- **{d}/** ({len(subdirs)} subdirs)")
            for sd in subdirs[:5]:
                lines.append(f"  - {sd}/")
            if len(subdirs) > 5:
                lines.append(f"  - ... and {len(subdirs) - 5} more")
        else:
            lines.append(f"- {d}/")
    
    if analysis['key_files']:
        lines.extend(["", "## Key Files"])
        for f in analysis['key_files']:
            lines.append(f"- {f}")
    
    return "\n".join(lines)


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    output_format = sys.argv[2] if len(sys.argv) > 2 else 'text'
    
    analysis = analyze_directory(path)
    
    if output_format == 'json':
        # Convert defaultdicts to regular dicts for JSON
        analysis['stats']['by_category'] = dict(analysis['stats']['by_category'])
        analysis['stats']['by_extension'] = dict(analysis['stats']['by_extension'])
        print(json.dumps(analysis, indent=2))
    else:
        print(format_output(analysis))
