## Description ##

The `jump` utility can be used to assign convenient names to frequently used
strings, typically directory paths. The related `j` shell command can then be
used to `cd` to a named path. In combination, these utilities make it very easy
to jump from one place to another on the command line.

A few simple examples:

    # Name a few paths.
    jump --add docs $HOME/my/favorite/docs
    jump --add mp3s $HOME/my/music/from/70s/80s/90s/and/today
    jump --add words /usr/share/dict/words

    # Go to docs directory and do some work. If desired, jump can
    # be used in command-interpolation, as shown in the grep example.
    j docs
    grep ^aa `jump words` > words_starting_with_aa

    # Easily cd somewhere else.
    j mp3s
    
Usage overview:

    jump --add NAME STRING [--literal]   # Add a named path or literal string
    jump --rm NAME                       # Delete a named string
    jump --mv OLD_NAME NEW_NAME          # Change name of a string

    jump NAME                            # Print a named string
    jump                                 # List all named strings

    jump --help                          # Print help and exit

    j NAME                               # cd to a named path

The `jump` utility will add paths in their normalized, absolute form and will
handle common shell conventions (`.`, `..`, and `~`). Use the `--literal`
option to bypass the default path normalization.

Named paths are stored in `.jumprc` in the user's home directory.


## Installation ##

Download the `jump` script to a directory in your `PATH` and make it
executable. For example:

    # Modify the path to the jump script as desired.
    URL='https://raw.githubusercontent.com/hindman/jump/master/jump'
    curl "$URL" -o $HOME/bin/jump
    chmod u+x $HOME/bin/jump

Add commands like the following to your Bash profile:

    # cd to a named path.
    function j {
      [[ $# -eq "1" ]] && cd $($HOME/bin/jump --cd "$1")
    }

The script's only dependency is Python 2.7 or higher.

