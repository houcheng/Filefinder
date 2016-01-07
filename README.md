# Sublime Filefinder plugin

![Demo](demo.gif "Demo of file finder plugin")

## Installation

Via the [Sublime Package Manager](http://wbond.net/sublime_packages/package_control):

* `Ctrl+Shift+P` or `Cmd+Shift+P` in Linux / Windows / OS X
* Type `install`, select `Package Control: Install Package`
* Select `Filefinder`

## Usage

A prompt file finder utility for sublime. You should:

1. Set the "include_dirs" in menu of /Preference/Packages/File finders/User setting.
2. Restart sublime, then use "ctrl+t" to do the file search.

## Default

- Default hot key

```
  { "command": "filefinder", "keys": ["ctrl+t"] },
```

- Default settings

```
// search path
"include_dirs": ["~/Documents", "~/Desktop"],
// files open by system applications
"binary_files": ["ppt", "doc", "xls", "pdf", "docx", "pptx", "odp"],
```

- In windows environment, your search path may looks like this:

```
"include_dirs": ["C:\\Users\\YOUR-USER-NAME-HERE\\Documents"],
```

## Note

Please do not set include_dirs to contains too many files, this may takes a while to walk the file-list and sublime
would freeze during file walking.

