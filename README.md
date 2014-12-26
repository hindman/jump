## Description ##

The `nameit` utility can be used to assign convenient names to frequently used
strings, typically paths.

The related `j` shell command can then be used to cd to a named path (`j` for
jump). The `ni` shell command can be used to echo a named string -- for
example, when constructing larger shell commands via command interpolation. The
`ni` command is nothing more than a shortcut for the main script, so you can
also use it to execute any `nameit` functionality.

A couple of simple example:

    nameit --add docs $HOME/my/favorite/docs
    nameit --add words /usr/share/dict/words

    j docs
    grep ^aa `e words` > words_starting_with_aa

Usage overview:

    nameit --add NAME STRING [--literal] # Add a named path or literal string
    nameit --rm NAME                     # Delete a named string
    nameit --mv OLD_NAME NEW_NAME        # Change name of a string

    nameit NAME                          # Print a named string
    nameit                               # List all named strings

    nameit --help                        # Print help and exit

    j NAME                               # cd to a named path
    ni NAME                              # echo a named string

The `nameit` utility will add paths in their normalized, absolute form and will
handle common shell conventions (., .., and ~). Use the --literal option to
bypass the default path normalization.

Named paths are stored in `.nameitrc` in the user's home directory.

## Installation ##

Download the `nameit` script to a directory in your `PATH` and make it
executable. The script's only dependency is Python 2.7 or higher.

Add commands like the following to your Bash profile, adjusting the path to the
`nameit` script as needed:

    # cd to a named path.
    function j {
      [[ $# -eq "1" ]] && cd $($HOME/bin/nameit "$1")
    }

    # echo a named string, or run any other nameit operations.
    function ni {
      $HOME/bin/nameit "$@"
    }

