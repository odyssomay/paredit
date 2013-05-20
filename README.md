# paredit

This is an implementation of [paredit](http://www.emacswiki.org/emacs/ParEdit)
for [sublime text](http://www.sublimetext.com/).

The plugin is under development, but intended to be finished before 2013-05-25.


## Usage

See [the cheatsheet](http://pub.gajendra.net/src/paredit-refcard.pdf).

## Implementation Status

Below is a list of all currently **not** implemented paredit commands
from the cheatsheet.

* paredit-close-round-and-newline
* paredit-meta-doublequote
* paredit-backslash
* paredit-comment-dwim

* paredit-splice-sexp-killing-backward
* paredit-splice-sexp-killing-forward
* paredit-raise-sexp

* paredit-recentre-on-sexp
* paredit-reindent-defun

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
