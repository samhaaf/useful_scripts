# useful_scripts
The intent of this library is to centralize the tools that I use to be more efficient behind the wheel.

## Setup
After cloning the repositories, simply run:

```
make setup
```

To get the most recent version of the scripts on this machine, run:

```
make sync
```

and that's it.

## Commands

These are the bash scripts that become available on the system. Most have been written to run on MacOS and all linux distros.

---

### add-to-path
Adds the first given argument to the `$PATH` variable, if it is not already a part of the path. You may to run source-profile after this change.

---

### c
Copy the result of the following arguments to the clipboard. examples:

```
c cat my_file.txt
c echo "hey there, fella"
```

---

### cmc
Stands for "Copy Make Command". Copies the contents of one of these scripts to the clipboard.

---

### define-server 
Some of these tools let you operate on "server" "objects" (i.e. push, goto). This script starts a cli to configure a server connection object.

---

### gitignore
Adds all arguments as patterns in ./.gitignore. Ignores rules that already exist in the file.

---
  
### gittree
Prints to stdout in the same format as the native `tree` command, but it skips files that match patterns in the `.gitignore` files.

---

### goto
Opens an ssh connection to a server object defined with `define-server`. Supports these flags:

```
-t / --tunnel <that_port>:<this_port> : opens a tunnel from that_port on that machine to this_port on this machine (incomplete)
-c / --code "<code>" : executes arbitrary code on the target
```

---

### install-\*
These scripts install the package after the hyphen. Version numbers, if applicable, can be specified as the first arg.

---

### lmc
Stands for "List Make Command". Lists all commands available in `scripts`.\

---
