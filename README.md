# useful_scripts
These are the tools that I use to be more efficient behind the wheel.

These scripts should run equivalently on MacOS and all linux distros.

<br>

## Setup
After cloning the repositories, simply run:

```
make setup
```

To get the most recent version of the scripts on this machine, run:

```
make sync
```

<br>

## Commands

### add-to-gitignore (Alias: ignore)

Adds all arguments as patterns in ./.gitignore. Ignores rules that already exist in the file.

---

### add-to-path
Adds the first argument to the `$PATH` variable, if it is not already a part of the path.

You may want to run `sp` (source-profile) after this change.

---

### add-to-profile
Adds a variable to all of the system bash profiles, if it is not already defined in each file.

You may want to run `sp` (source-profile) after this change.

Examples:
```
add-to-profile PYTHON_PATH /path/to/python
```

Additional behaviors:
```
add-to-profile --alias <alias_name> "<alias_content>"    # Adds an alias to your bash profiles.
add-to-profile --source <thing_to_source>                # Adds a source to your bash profiles.
```

---

### copy-my-command (Alias: cmc)
Copies the contents of one of the commands to the clipboard.

---

### copy-to-clipboard (Alias: c)

Copy the result of subsequent args (like the sudo syntax) to the clipboard. examples:

```
c cat my_file.txt
c echo "hey there, fella"
```

---

### define-server
Some of these tools let you operate on "server" "objects" (i.e. push, goto). This script starts a cli to configure a server connection object.

---

### gittree (Alias: gree)
It's like the native `tree` command, but it skips files that match patterns in the `.gitignore` files.

---

### goto
Opens an ssh connection to a server object defined with `define-server`. Supports these flags:

Additional behaviors:
```
goto <server> -t / --tunnel <that_port>:<this_port>    # opens a tunnel from that_port on that machine to this_port on this machine (incomplete)
goto <server> -c / --code "<code>"                     # executes arbitrary code on the target
```

---

### install-\*
These scripts install the package after the hyphen. Version numbers, if applicable, can be specified as the first arg.

---

### list-my-commands (Alias: lmc)
Lists all commands available in the `commands` folder.

---

### make-alias (Alias: ma)

Adds an alias to the `aliasses` folder and to the bash profiles.

---

### make-command (Alias: mc)

Opens a vim session to define a new command.

---

### paste-from-clipboard (Alias: p)

Pastes the contents of the clipboard to a file.

Example:
```
p my_file.txt
```

---

### paste-my-command (Alias: pmc)

Pastes the contents of the clipboard to a new or existing command. Existing commands will ask the user for confirmation.

Example:
```
pmc new-command       # does not ask for confirmation
pmc old-command       # asks for confirmation
pmc -y old-command    # does not ask for confirmation
```

---

### pip
Works hand-in-hand with the python command.

Runs any version of python -m pip.

If poetry is found in the current directory lineage, then it will use poetry.

Both `add` and `install` do the same behavior.

If simple "pip freeze" is called, then it will generate `./requirements.txt`.

The `--quiet` or `-q` flags will suppress output made by this script.

Examples:
```
# Base cases
pip install my_package       
    Executing command: python3.10 -m pip install my_package
    Collecting my_package
    ...
pip add my_package       
    Executing command: python3.10 -m pip install my_package
    Collecting my_package
    ...
pip freeze
    Executing command: python3.10 -m pip freeze > requirements.txt

# Specific version cases
pip --version 3.11 install my_package   
    Do you want to set Python 3.11 as the default version? (y/n) y
    ...

# Poetry cases (pyproject.toml is found)
pip install my_package    
    Executing command: poetry add my_package
pip add my_package    
    Executing command: poetry add my_package
pip freeze
    Executing command: poetry export --format=requirements.txt --without-hashes > requirements.txt
```

---

### push
Pushes files around (with rsync). Handles any of the following:

- local to local
- local to remote
- remote to local

To specify a remote target, use a `#` followed by the name of the target.

Examples:
```
push /path/to/foo /path/to/bar                 # local to local
push /path/to/foo #my-instance:/path/to/bar    # local to remote
push #my-instance:/path/to/foo /path/to/bar    # remote to local
```

---

### python
Runs any version of python.

If poetry is found in the current directory lineage, then it will use poetry.

The `--quiet` or `-q` flags will suppress output made by this script.

Note that when you normally call `--version` you get the version of python being
used, but in this script it actually instructs which version to use.

Examples:
```
# Base case
python my_script.py                     
    Which version of Python do you want to run? 3.10
    Do you want to set Python 3.10 as the default version? (y/n) y

# Specific version case
python --version 3.11 my_script.py      
    Do you want to set Python 3.11 as the default version? (y/n) y
    Python 3.11 is not installed. Do you want to install it? (y/n) y
    Installing Python 3.11 on macOS...

# Poetry case (pyproject.toml is found)
python my_script.py    
    Executing command: poetry run python my_script
```

---

### rm-pycache
Removes `__pycache__/` from this directory and all subdirectories.

---

### source-profile (Alias: sp)

Sources the bash profile into the current context.

(Note: This one is actually itself an alias)

---

### sync-useful-scripts

Runs this project's "make sync" command.

Useful if you use this repo as a dependency in another project and want to make
sure the most recent version is being used.
