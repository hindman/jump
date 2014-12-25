#! /usr/bin/env perl

use warnings;
use strict;

my (@arg, $godata, $pwd, %dir, $cddir, $t, $confirm);

# Help message.
sub Help {
    print STDERR shift(), "\n" if @_;
    print STDERR "
    Usage summary:
        go add KEY PATH        # Add (or replace) a path.
        go del KEY             # Delete a path.
        go ren OLDKEY NEWKEY   # Change a key for a path.
        go KEY                 # Go to a path.
        go clear               # Clear all paths.
        go                     # Show the paths.
        go help                # Show this help message.

    Details:
        This script is an improved version of the Unix pushd(), popd(), and dirs() commands.
        It creates a data file in the user's home directory to store paths as key-value
        pairs:

            KEY     /some/path
            KEY     /some/other/path
            etc.

        The user can then `cd` to those paths, using the assigned KEY.

            go KEY

        The script is designed to be run within the context of a Unix `cd` command.
        In other words, whatever go.pl prints to STDOUT becomes the argument
        supplied to `cd`.

        To get starting using this utility, you need to modify your shell configuration file:

            # If your shell is bash.
            function go {
                cd `/pkg/ipums/programming/perl_ipums/go.pl $@`
            }

            # If your shell is tcsh, add this line to .chsrc.user.
            alias go 'cd  `/pkg/ipums/programming/perl_ipums/go.pl \!:*`'

        The script supplies limited support for the special Unix directory conventions.
        The following simple items work when supplying a PATH to the script, but more
        complex specifications do not:

                .
                ..
                ~
";
}

# Get the arguments passed to the script, the user name, and the current working directory.
@arg = @ARGV;
$pwd = `pwd`;
chomp $pwd;

# If the user doesn't have a .gorc file already, create one.
$godata = "$ENV{HOME}/.gorc";
system "touch $godata" unless -f $godata;

# Read the go.pl data file.
open(GODATA, $godata) or die "Failed to open file for reading: $godata.\n";
while (<GODATA>){
    next unless /\S/;
    die "Bad line in go.pl data file:\n    $_\n" unless /^\s*(\S+)\s+(.+)\s+$/;
    $dir{$1} = $2;
}
close GODATA;

# The first argument to the script determines what action will be taken.
# The default action is 'show'.
@arg = ('show') unless @arg;

# This is the effective return value to the Unix cd() command that invokes go.pl.
# The default value is to cd to the current directory.
$cddir = '.';

# Take the action requested by the user.
if ($arg[0] eq 'show' and @arg == 1){
    ShowGoPaths();
} elsif ($arg[0] eq 'clear' and @arg == 1){
    print STDERR "Enter 'yes' to clear all paths: ";
    $confirm = <STDIN>;
    chomp $confirm;
    if ($confirm eq 'yes'){
        %dir = ();
        WriteGoPaths();
    }
} elsif ($arg[0] eq 'help' and @arg == 1){
    Help();
} elsif ($arg[0] eq 'add' and @arg == 3){
    $t = PathNorm($arg[2]);
    if (-d $t){
        $dir{$arg[1]} = $t;
        WriteGoPaths();
    } else {
        Help('Invalid path.');
    }
} elsif ($arg[0] eq 'ren' and @arg == 3 and defined $dir{$arg[1]}){
    $dir{$arg[2]} = $dir{$arg[1]};
    delete $dir{$arg[1]};
    WriteGoPaths();
} elsif ($arg[0] eq 'del' and @arg == 2 and defined $dir{$arg[1]}){
    delete $dir{$arg[1]};
    WriteGoPaths();
} elsif (defined $dir{$arg[0]} and @arg == 1){
    # Go.
    $cddir = $dir{$arg[0]};
} else {
    Help();
}

# Print the script's return value, which becomes the argument for a Unix cd() command.
print $cddir;


# Subroutine to display the go paths.
sub ShowGoPaths {
    my $fmt = "        %-16s%s\n";
    printf STDERR $fmt, $_, $dir{$_} for sort { $dir{$a} cmp $dir{$b} } keys %dir;
}

# Subroutine to write the go data.
sub WriteGoPaths {
    open(GODATA, "> $godata") or die "Failed to open file for writing: $godata.\n";
    print GODATA "$_\t$dir{$_}\n" for sort keys %dir;
    close GODATA;
}

# Subroutine to normalize paths.
sub PathNorm {
    my ($d, $nopwd);
    $d = shift;
    $d = '' if $d eq '.';
    if ($d eq '..'){
        # Support for '..'
        $d = `dirname $pwd`;
        chomp $d;
        $nopwd = 1;
    } elsif ( substr($d, 0, 1) eq '/' ){
        # If the user supplied a full path, we don't want to prepend $pwd to it.
        $nopwd = 1;
    }
    # Prepend $pwd to the path, unless the path is already full.
    $d = "$pwd/$d" unless $nopwd or substr($d, 0, length($pwd)) eq $pwd;
    # Remove any trailing forward slash.
    substr($d, -1, 1) = '' if substr($d, -1, 1) eq '/';
    return $d;
}
