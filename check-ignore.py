#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys
import os
import platform
from pathlib import Path

HELP_FOOTER = r"""
Note:
  This script is used to check which files in the specified directory are ignored based on the rules defined in the .gitignore file.
  Requires the 'pathspec' module.
  You can install it using:

      pip install pathspec

  Example for Windows:
    > check_ignore.py --allow D:\Users\staff\Example\Source
    > check_ignore.py --ignore D:\temp\ignotefile.txt --allow D:\Users\staff\Example\Source

  Example for Mac/Linux:
    > check_ignore.py --allow /home/staff/Example/Source
    > check_ignore.py --ignore /usr/tmp/ignotefile.txt --allow /home/staff/Example/Source

"""

def load_gitignore_rules(gitignore_path):
    import pathspec
    try:
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error: Cannot open .gitignore file at {gitignore_path}\n{e}")
        sys.exit(1)

    if not lines:
        print(f"Error: .gitignore file at {gitignore_path} is empty.")
        sys.exit(1)

    return pathspec.PathSpec.from_lines("gitwildmatch", lines)


def collect_files_recursively(base_path):
    return [str(p.relative_to(base_path).as_posix()) for p in Path(base_path).rglob('*') if p.is_file()]


def map_to_full_paths(base_path, relative_paths):
    system = platform.system()
    results = []
    for rel in relative_paths:
        full_path = (Path(base_path) / Path(rel)).resolve()
        if system == 'Windows':
            results.append(str(full_path))
        else:
            results.append(full_path.as_posix())
    return results


def filter_paths(filelist, spec, mode):
    matched = set(spec.match_files(filelist))
    if mode == 'deny':
        return sorted(matched)
    else:  # allow
        return sorted(set(filelist) - matched)


def main():
    parser = argparse.ArgumentParser(
        description='Check .gitignore impact on directory tree',
        epilog=HELP_FOOTER,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--ignore', metavar='GITIGNORE',
                        help='Path to .gitignore file to use (default: ./.gitignore from current directory)')
    parser.add_argument('--allow', metavar='DIR',
                        help='Show files allowed (not ignored) under the directory')
    parser.add_argument('--deny', metavar='DIR',
                        help='Show files denied (ignored) under the directory')
    args = parser.parse_args()

    if not args.allow and not args.deny:
        parser.print_help()
        sys.exit(0)

    try:
        import pathspec
    except ModuleNotFoundError:
        print("Error: This script requires the 'pathspec' module.")
        print("Install it using:\n\n    pip install pathspec\n")
        sys.exit(1)

    mode = 'allow' if args.allow else 'deny'
    target_dir = args.allow if args.allow else args.deny
    target_dir_path = Path(target_dir).resolve()

    filelist_rel = collect_files_recursively(target_dir_path)
    filelist_abs = map_to_full_paths(target_dir_path, filelist_rel)

    if args.ignore:
        gitignore_path = Path(args.ignore)
    else:
        gitignore_path = Path.cwd() / '.gitignore'

    if not gitignore_path.exists():
        print(f"Error: .gitignore not found at {gitignore_path}")
        sys.exit(1)

    spec = load_gitignore_rules(gitignore_path)
    filtered_rel = filter_paths(filelist_rel, spec, mode)
    filtered_abs = map_to_full_paths(target_dir_path, filtered_rel)

    for f in filtered_abs:
        print(f)


if __name__ == '__main__':
    main()
