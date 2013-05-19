# paredit

This is an implementation of [paredit](http://www.emacswiki.org/emacs/ParEdit)
for [sublime text](http://www.sublimetext.com/).

The plugin is under development, but intended to be finished before 2013-05-25.

## Implementation Status

Below is a list of all currently implemented paredit commands.

Note: The actual name of the commands inside sublime text use 
underscores instead of hyphens. E.g. *paredit-open-round* is
called *paredit_open_round*.

### Basic Insertion Commands

* paredit-open-round
* paredit-close-round
* paredit-open-square
* paredit-close-square
* paredit-doublequote
* paredit-newline

### Deleting & killing

* paredit-forward-delete
* paredit-backward-delete
* paredit-kill
* paredit-forward-kill-word
* paredit-backward-kill-word

### Movement & Navigation

* paredit-forward
* paredit-backward

### Depth-Changing Commands

* paredit-wrap-round
* paredit-splice-sexp

### Miscellaneous Commands

* paredit-split-sexp

### Extra commands

These are not part of emacs paredit.

* paredit-open-curly, same as *paredit-open-round* but with *{*.
* paredit-close-curly, same as *paredit-close-round* but with *}*.
* paredit-kill-expression, same as *paredit-kill*, but removes the
whole expression.

## Installation

To try the current implementation, clone the repository and place the resulting
directory in `Installed Packages` inside your
[data directory](http://docs.sublimetext.info/en/latest/basic_concepts.html#the-data-directory).

## Testing

Press *ctrl+shift+p* to open the command palette. Type *test*
and run *Paredit: Run Tests*.
