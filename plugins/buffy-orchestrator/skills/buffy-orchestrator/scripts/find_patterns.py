#!/usr/bin/env python3
"""
Code pattern search script.
Finds function definitions, class definitions, imports, and usages.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from collections import defaultdict

IGNORE_DIRS = {'node_modules', '.git', '__pycache__', '.next', 'dist', 'build', 
               '.venv', 'venv', 'coverage', 'target'}

@dataclass
class Match:
    file: str
    line_num: int
    line: str
    match_type: str  # 'definition', 'usage', 'import'


def should_ignore(path: Path) -> bool:
    for part in path.parts:
        if part in IGNORE_DIRS or part.startswith('.'):
            return True
    return False


def search_file(file_path: Path, pattern: str, extensions: Optional[List[str]] = None) -> List[Match]:
    """Search a single file for pattern matches."""
    if extensions and file_path.suffix.lower() not in extensions:
        return []
    
    matches = []
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')
        
        # Patterns to identify match type
        def_patterns = [
            rf'function\s+{re.escape(pattern)}\s*\(',
            rf'(const|let|var)\s+{re.escape(pattern)}\s*=',
            rf'class\s+{re.escape(pattern)}',
            rf'interface\s+{re.escape(pattern)}',
            rf'type\s+{re.escape(pattern)}\s*=',
            rf'def\s+{re.escape(pattern)}\s*\(',
            rf'async\s+def\s+{re.escape(pattern)}\s*\(',
        ]
        
        import_patterns = [
            rf'import.*{re.escape(pattern)}.*from',
            rf'from\s+\S+\s+import.*{re.escape(pattern)}',
            rf'require\([\'"].*{re.escape(pattern)}',
        ]
        
        for i, line in enumerate(lines, 1):
            if pattern.lower() not in line.lower():
                continue
            
            # Determine match type
            match_type = 'usage'
            
            for dp in def_patterns:
                if re.search(dp, line, re.IGNORECASE):
                    match_type = 'definition'
                    break
            
            if match_type == 'usage':
                for ip in import_patterns:
                    if re.search(ip, line, re.IGNORECASE):
                        match_type = 'import'
                        break
            
            matches.append(Match(
                file=str(file_path),
                line_num=i,
                line=line.strip()[:200],  # Truncate long lines
                match_type=match_type
            ))
    
    except Exception as e:
        pass
    
    return matches


def search_directory(root: str, pattern: str, extensions: Optional[List[str]] = None) -> Dict[str, List[Match]]:
    """Search entire directory for pattern."""
    root_path = Path(root).resolve()
    
    results = defaultdict(list)
    
    for file_path in root_path.rglob('*'):
        if not file_path.is_file():
            continue
        if should_ignore(file_path):
            continue
        
        matches = search_file(file_path, pattern, extensions)
        for match in matches:
            # Use relative path
            match.file = str(file_path.relative_to(root_path))
            results[match.match_type].append(match)
    
    return results


def format_results(results: Dict[str, List[Match]], pattern: str) -> str:
    """Format results for display."""
    lines = [f"## Search Results: \"{pattern}\"", ""]
    
    total = sum(len(matches) for matches in results.values())
    
    if total == 0:
        return f"No matches found for \"{pattern}\""
    
    # Definitions first
    if results['definition']:
        lines.append(f"### Definitions ({len(results['definition'])} found)")
        for match in sorted(results['definition'], key=lambda m: m.file)[:15]:
            lines.append(f"- `{match.file}:{match.line_num}` - `{match.line[:100]}`")
        if len(results['definition']) > 15:
            lines.append(f"- ... and {len(results['definition']) - 15} more")
        lines.append("")
    
    # Imports
    if results['import']:
        lines.append(f"### Imports ({len(results['import'])} found)")
        for match in sorted(results['import'], key=lambda m: m.file)[:10]:
            lines.append(f"- `{match.file}:{match.line_num}` - `{match.line[:100]}`")
        if len(results['import']) > 10:
            lines.append(f"- ... and {len(results['import']) - 10} more")
        lines.append("")
    
    # Usages
    if results['usage']:
        lines.append(f"### Usages ({len(results['usage'])} found)")
        for match in sorted(results['usage'], key=lambda m: m.file)[:20]:
            lines.append(f"- `{match.file}:{match.line_num}` - `{match.line[:100]}`")
        if len(results['usage']) > 20:
            lines.append(f"- ... and {len(results['usage']) - 20} more")
        lines.append("")
    
    lines.append(f"**Total:** {total} matches")
    
    return "\n".join(lines)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: find_patterns.py <pattern> [--type ext1,ext2] [--path /dir]")
        sys.exit(1)
    
    pattern = sys.argv[1]
    extensions = None
    search_path = '.'
    
    # Parse args
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--type' and i + 1 < len(sys.argv):
            extensions = ['.' + e.lstrip('.') for e in sys.argv[i + 1].split(',')]
            i += 2
        elif sys.argv[i] == '--path' and i + 1 < len(sys.argv):
            search_path = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    results = search_directory(search_path, pattern, extensions)
    print(format_results(results, pattern))
