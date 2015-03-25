# sublimetext-epages6

Development tools for epages6.

## Install

Install via Package Manager. To add our repository, have a look (here)[https://github.com/ePages-rnd/sublimetext-plugins].

## Configure

If not already done, create a project for each epages6 virtual machine you want to use with this plugin.

Go to the project settings `Project > Edit Project` and add the `settings` key:
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
            "vm": "jgratz-vm1"
        }
    }
}

```
Change the values to match your configuration. It doesn't matter if you're using Shared Folders, a Windows share or a SFTP mount. You can mix them, too.

## Features

We've got you covered. All epages6 command which are needed frequently are included. Explore all features by clicking on `Tools > epages6` or type in the command palette `Epages:`.

## Settings

You can disable the copy-to-shared feature by clicking on `Preferences > Package Settings > Epages6 > Settings - User` and paste
```
{
    "copy_to_shared": false
}
```

