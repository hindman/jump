## namit ##

    nameit - Associate a frequently used string with a short name
    j      - Jump to a named path (cd to it)
    e      - Echo a named string

## Synopsis ##

    nameit --add NAME STRING [--literal] # Add a named path or literal string
    nameit --rm NAME                     # Delete a named string
    nameit --mv OLD_NAME NEW_NAME        # Change name of a string

    nameit NAME                          # Print a named string
    nameit                               # List all named strings

    nameit --help                        # Print help and exit

    j NAME
    e NAME

## Description ##

The `nameit` utility can be used to assign convenient names to frequently used
strings, typically paths.

The related `j` and `e` shell commands can then be used to cd to a named path
or to echo a named string (the latter when constructing larger shell commands
via command interpolation).

A simple example:

    nameit docs $HOME/my/favorite/docs
    nameit words /usr/share/dict/words

    j docs
    grep ^aa `e words` > words_starting_with_aa

The `nameit` utility will add paths in their normalized, absolute form and will
handle common shell conventions (., .., and ~). Use the --literal option to
bypass the default path normalization.

Named paths are stored in `.nameitrc` in the user's home directory.

## Installation ##

Download the `nameit` script to a directory in your PATH and make it
executable. The script's only dependency is Python 2.7 or higher.

Add the following commands to your Bash profile (adjust the value assigned to
`NAME_SCRIPT` as needed):

    NAME_SCRIPT="$HOME/bin/nameit"

    function j { cd $("$NAME_SCRIPT" "$1") }
    function e { "$NAME_SCRIPT" "$1" }

