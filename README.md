# check-ignore.py
<br>

```
usage: check_ignore.py [-h] [--ignore GITIGNORE] [--allow DIR] [--deny DIR]

Check .gitignore impact on directory tree

options:
  -h, --help          show this help message and exit
  --ignore GITIGNORE  Path to .gitignore file to use (default: ./.gitignore from current directory)
  --allow DIR         Show files allowed (not ignored) under the directory
  --deny DIR          Show files denied (ignored) under the directory

Note:
  This script is used to check which files in the specified directory are ignored based on the rules defined in the .gitignore file.

  Requires the 'pathspec' module.
  You can install it using:

      pip install pathspec

  Example for Windows:
    > check_ignore.py --allow D:\Users\staff\Example\Source
    > check_ignore.py --ignore D:\\temp\\ignotefile.txt --allow D:\\Users\\staff\\Example\\Source

  Example for Mac/Linux:
    > check_ignore.py --allow /home/staff/Example/Source
    > check_ignore.py --ignore /usr/tmp/ignotefile.txt --allow /home/staff/Example/Source
```
