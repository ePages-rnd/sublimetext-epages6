# sublimetext-epages6

Development tools for epages6.

## Install

### Install the plugin

Install via Package Manager. To add our repository, have a look [here](https://github.com/ePages-rnd/sublimetext-plugins).

Search for `Epages6` and install it.

### Install local python

Install ActivePython version 3.4 [from here](http://www.activestate.com/activepython/downloads).

Add the folder with the binary to your path:
- Windows: `C:\Python34`
- OS X: `/Library/Frameworks/Python.framework/Versions/Current/bin`

### Install paramiko

Open your local terminal and type
```
pypm install paramiko
```
for Windows and
```
sudo pypm install paramiko
```
for OS X.

### Windows only: patch paramiko

Unfortunately there are two major upstream bugs, so you have to fix them manually:

- Change `%APPDATA%\Python\Python34\site-packages\Crypto\Random\OSRNG\nt.py` as described [here](https://github.com/dlitz/pycrypto/commit/10abfc8633bac653eda4d346fc051b2f07554dcd#diff-f14623ba167ec6ff27cbf0e005d732a7)
- Change `%APPDATA%\Python\Python34\site-packages\paramiko\_winapi.py` as described [here](https://github.com/paramiko/paramiko/issues/461)

## Configure

If not already done, create a project for each epages6 virtual machine you want to use with this plugin.

Go to the project settings `Project > Edit Project` and add the `settings` key like (OS X):
```
{
    "folders":
    [
        ...
    ],
    "settings":
    {
        "ep6vm":
        {
            "cartridges": "/Users/jgratz/Developer/epages6/Cartridges",
            "log": "/Volumes/epages/Shared/Log",
            "password": "qwert6",
            "storetypes": "/Volumes/WebRoot/StoreTypes",
            "user": "root",
            "vm": "jgratz-vm1",
            "copy_to_shared": true
        }
    }
}
```
or (Windows):
```
{
    "folders":
    [
        ...
    ],
    "settings":
    {
        "ep6vm":
        {
            "cartridges": "C:\\SharedFolders\\vm1\\Cartridges",
            "log": "C:\\SharedFolders\\vm1\\Log",
            "password": "qwert6",
            "storetypes": "C:\\SharedFolders\\vm1\\StoreTypes",
            "user": "root",
            "vm": "ahartmann-vm1",
            "copy_to_shared": true
        }
    }
}
```

Change the values to match your configuration. It doesn't matter if you're using Shared Folders, a Windows share or a SFTP mount. You can mix them, too.

## Features

We've got you covered. All epages6 command which are needed frequently are included. Explore all features by clicking on `Tools > epages6` or type in the command palette `Epages:`.
