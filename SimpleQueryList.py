true, false, null, none = True, False, None, None
STORAGE = {"root": {}}
CDICT = "root"
VERSIONCHECK = "sqlt:ver(1)"
import os

RUNNING = true
def command(c):
    global RUNNING, STORAGE, CDICT;
    DICT = STORAGE[CDICT]
    c = c.strip();
    c = c.split();
    if c[0] in ["termin", "terminate", "endprogram", "shutdown"]: RUNNING = false;
    
    if c[0] in ["view", "show", "print"]:
        if len(c) != 2: print("Error! This command takes exactly 1 parameter!")
        else:
            if c[1] in DICT.keys():
                print(DICT[c[1]])
            else:
                print("Error!", c[1], "doesn't exist!")
                
    if c[0] == "create":
        if len(c) != 2: print("Error! This command takes exactly 1 parameter!")
        else:
            if c[1] not in DICT.keys():
                DICT[c[1]] = []
            else:
                print("This array already exists. Override it with an empty one? Y/N")
                a = input()
                if a.upper() == "Y":
                    DICT[c[1]] = []
                else:
                    print("Cancelled.")
                    
    if c[0] == "add":
        if len(c) < 4: print("Error! This command must follow this syntax:\nadd <value> to <array>")
        else:
            if c[-2] != "to": print("Error! This command must follow this syntax:\nadd <value> to <array>")
            else:
        	    if c[-1] not in DICT.keys(): print("Error! This array doesn't exist!")
        	    else: DICT[c[-1]].append(" ".join(c[1:-2]))
		    
    if c[0] in ["del", "delete"]:
        if len(c) != 2: print("Error! This command takes exactly 1 parameter!")
        else:
            if c[1] in DICT.keys():
              print("Really delete? Type the array name to confirm.")
              if input().strip() == c[1]:
                del DICT[c[1]]
              else: print("Cancelled")
            else:
              print("Error! There is no such array!")
              
    if c[0] == "remove":
      if len(c) < 4: print("Error! This command must follow this syntax:\nremove <value> from <array>")
      else:
          if c[-2] != "from": print("Error! This command must follow this syntax:\nremove <value> from <array>")
          else:
            if c[-1] not in DICT.keys(): print("Error! This array doesn't exist!")
            else: DICT[c[-1]].pop(DICT[c[-1]].index(" ".join(c[1:-2])))

    if c[0] == "pop":
      if len(c) != 3: print("Error! This command must follow this syntax:\npop <array> <index>")
      else:
        if c[1] not in DICT.keys(): print("Error! This array doesn't exist!")
        else:
            try:
                DICT[c[1]].pop(int(c[2]))
            except:
                print("Index must be a number. Make sure it's lower than\nyour array's total length.")

    if c[0] == "index":
        if len(c) < 3: print("Error! This command must follow this syntax:\nindex <value> <array>")
        else:
            if c[-1] not in DICT.keys(): print("Error! This array doesn't exist!")
            else: print(DICT[c[-1]].index(" ".join(c[1:-1])))
            

    if c[0] in ["len", "length"]:
        if len(c) != 2: print("Error! This command takes exactly 1 parameter!")
        else:
            if c[1] not in DICT.keys(): print("Error! This array doesn't exist!")
            else:
                print(c[1]+":LENGTH =", len(DICT[c[1]]))
        
    if c[0] in ["ws", "workspace", "cw", "changews", "changeworkpace"]:
        if len(c) != 2: print("Error! This command takes exactly 1 parameter!")
        else:
            if c[1] in STORAGE.keys():
                CDICT = c[1]
            else:
                STORAGE[c[1]] = {}
                CDICT = c[1]
            print("Changed workspace to", c[1] + ".")
            
    if c[0] == "save":
        if len(c) != 4 or c[2] != "as":
            print("Error! This command must follow this syntax:\nsave <workspace> as <file>")
        else:
            if c[1] in STORAGE.keys():
                try:
                    with open(c[3]+".sqlt", "w") as f:
                        if f.writable():
                            f.write(VERSIONCHECK)
                            for i in STORAGE[c[1]].keys():
                                if len(STORAGE[c[1]][i])==0:
                                    f.write("\n"+i)
                                else:
                                    f.write("\n"+i+"|"+("|".join(STORAGE[c[1]][i])))
                            print("Saved succesfully.")
                        else: print("Error. You do not have permissions to write to this file.")
                except:
                    print("Folder, that you are trying to save your file to doesn't exist.")
            else: print("Workspace", c[1], "doesn't exist.")

    if c[0] == "load":
        if len(c) != 4 or c[2] != "as":
            print("Error! This command must follow this syntax:\nload <file> as <workspace>")
        else:
            if os.path.exists(c[1]+".sqlt"):
                if c[3] in STORAGE.keys():
                    askert = input("This workspace already exists. Please choose a command to execute:\n\
o/ow/over/overwrite - Overwrite the workspace's contents.\n\
m/mg/merge - Merge the workspace's contents with the file contents.\n\
<anything else> - Cancel.\n\
Input your command: ").strip().lower()
                    if askert not in ["o", "ow", "overwrite", "over", "m", "mg", "merge"]:print("Operation cancelled.")
                    else:
                        if askert in ["o", "ow", "overwrite", "over"]:
                            STORAGE[c[3]] = {}
                        with open(c[1]+".sqlt", "r") as f:
                            if f.readable():
                                r = f.readlines()
                                if r[0].strip() != VERSIONCHECK:
                                    print("Warning. The version of your file does not correspond with your SQLt language version.\n\
Do you wish to procceed? Y/N")
                                    lt = input().upper().strip()
                                    if lt=="Y": braket = true
                                    else: braket = false
                                else: braket = true
                                if braket == true:
                                    for i in r[1:]:
                                        i = i.split("|")
                                        STORAGE[c[3]][i[0]] = [x.strip() for x in i[1:]]
                                    print("Workspace loaded. Do you wish to change your workspace to it? Y/N")
                                    ltr = input().upper().strip()
                                    if ltr == "Y":
                                        CDICT = c[3]
                                        print("Changed workspace to", c[3] + ".")
                                else:
                                    print("Cancelled.")
                            else: print("Error. You do not have permissions to read this file.")
                else:
                    STORAGE[c[3]] = {}
                    with open(c[1]+".sqlt", "r") as f:
                            if f.readable():
                                r = f.readlines()
                                if r[0].strip() != VERSIONCHECK:
                                    print("Warning. The version of your file does not correspond with your SQLt language version.\n\
Do you wish to procceed? Y/N")
                                    lt = input().upper().strip()
                                    if lt=="Y": braket = true
                                    else: braket = false
                                else: braket = true
                                if braket == true:
                                    for i in r[1:]:
                                        i = i.split("|")
                                        STORAGE[c[3]][i[0]] = [x.strip() for x in i[1:]]
                                    print("Workspace loaded. Do you wish to change your workspace to it? Y/N")
                                    ltr = input().upper().strip()
                                    if ltr == "Y":
                                        CDICT = c[3]
                                        print("Changed workspace to", c[3] + ".")
                                else:
                                    print("Cancelled.")
                            else: print("Error. You do not have permissions to read this file.")
            else: print("Error! This file doesn't exist.")     
            
    if c[0] == "info":
        if len(c) > 2: print("Error! This comand takes 1 parameter at most!")
        else:
            if len(c) == 1:
                print(CDICT,DICT)
            else:
                if c[1] in STORAGE.keys():
                    print(c[1], STORAGE[c[1]])
                else:
                    print("Workspace", c[1], "doesn't exist.")
                    
    if c[0] == "list": print("; ".join(list(STORAGE.keys())))


    '''
    ONLY HELP UNDER THIS LINE!!!
    '''
    if c[0] == "help":
        if len(c) != 2: print("Error! This command takes exactly 1 parameter!")
        else:
            if c[1] in ["termin", "terminate", "endprogram", "shutdown"]: print("This command terminates the terminal. Possible aliases: termin, terminate, endprogram, shutdown.")
            elif c[1] == "save" : print("This command saves a workspace to a file. Syntax: save <workspace> as <file>\n\
File must be either full path (C:\\Users\\User\\myworkspace), partial path (\\myfolder\\myorkspace)\n\
or just the file name (myworkspace). It will be saved as a .sqlt file.")
            elif c[1] == "load" : print("This command loads a workspace from a file. Syntax: load <file> as <workspace>\n\
File must be either full path (C:\\Users\\User\\myworkspace), partial path (\\myfolder\\myorkspace)\n\
or just the file name (myworkspace). You can only load .sqlt files.")
            elif c[1] in ["view", "show", "print"]: print("This command prints an array to the screen. Possible aliases: view, show, print.\n\
Syntax: print <array>")
            elif c[1] == "create": print("This command creates a new array. Syntax: create <array>")
            elif c[1] == "add": print("This command adds a value to an array.\n\
Syntax: add <value> to <array>")
            elif c[1] in ["del", "delete"]: print("This command deletes an array. Possible aliases: del, delete.\n\
Syntax: del <array>")
            elif c[1] in ["len", "length"]: print("This command returns the amount of items in an array.\n\
Possible aliases: len, length. Syntax: len <array>")
            elif c[1] == "remove": print("This command removes a value from array.\n\
Syntax: remove <value> from <array>")
            elif c[1] == "pop": print("This command removes a value from array.\n\
Syntax: pop <array> <index>")
            elif c[1] in ["ws", "workspace", "cw", "changews", "changeworkpace"]: print("This command changes the current/creates a new workspace. The default workspace is root.\n\
Possible aliases: ws, workspace, cw, changews, changeworkspace. Syntax: cw <workspace>")
            elif c[1] == "info": print("This command shows information about a workspace. If we do not include the workspace name,\n\
it will show information about our current workspace. Syntax: info <optional:workspace>\n\
Output syntax: <workspace> {<array>: <list of values>, <array>: <list of values>, ...}")
            elif c[1] == "list": print("This command lists all existing workspaces.")
            elif c[1] == "me": print("Use the 'help <command>' syntax to view help about any command.\n\
If you wish to learn the commands, use 'help tutorial'.")
            elif c[1] == "tutorial": print("""WELCOME TO SimpleQueryList ARRAY MANAGEMENT LANGUAGE!
This is a quick tutorial to help you get started.

--- WORKSPACES ---
Defaultly, you work in the root workspace.
Feel free to create a new workspace, or change to any
other workspace at any time! You can use the workspace
command for that. Use 'help workspace' for more ways
to use the workspace command, as well as a full
explanation of how to use it!

Now, let's switch to a workspace we will be using
throughout this tutorial, fun!

```COMMAND
workspace fun
```

Now we are working in the workspace fun. All workspaces
are completely independent from each other, so do not
worry about them interfering with each other.



--- SAVING WORKSPACES AND LOADING THEM ---
You can use the save and load commands to save your
workspace as a file and then load a workspace from
a file. Let's say, we have done a ton of work to our
fun workspace. Now it's time to save it, so we don't
lose any progress. We can do it like this:

```COMMAND
save fun as myfile
```

Now, we can see the myfile.sqlt in the same directory
where we have StyleQueryList app saved at. Let's say,
a day has passed. Now it's time to resume our work!
Let's open SimpleQueryList and open our workspace!

```COMMAND
load myfile as fun
```

We can now switch to our workspace fun and continue
our work! Great stuff!



--- END TUTORIAL ---
There is a lot more to learn, type the following
command to get more information!

help t1
""")
            elif c[1] == "t1":
                print("""TUTORIAL: MANAGING ARRAYS
To access the previous tutorial, use ```help tutorial```.

--- WHAT ARE ARRAYS ---
lol
""")
            else: print("This is a help message!")
            


#DEF:MAIN
while RUNNING:
    CMD = input("> ")
    if CMD == "":
        print("Please provide a command first.");
    else: command(CMD)


input()
