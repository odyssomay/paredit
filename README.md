# paredit

This is an implementation of [paredit](http://www.emacswiki.org/emacs/ParEdit)
for [sublime text](http://www.sublimetext.com/).

## Installation

To try the current implementation, clone the repository and place the resulting
directory in `Installed Packages` inside your
[data directory](http://docs.sublimetext.info/en/latest/basic_concepts.html#the-data-directory).

## Usage

See [the cheatsheet](http://pub.gajendra.net/src/paredit-refcard.pdf).

## Implementation Status

Below is a list of all currently **not** implemented paredit commands
from the cheatsheet.

* paredit-backslash
* paredit-splice-sexp-killing-backward
* paredit-splice-sexp-killing-forward
* paredit-raise-sexp
* paredit-recentre-on-sexp
* paredit-reindent-defun

## Testing

Press *ctrl+shift+p* to open the command palette. Type *test*
and run *Paredit: Run Tests*.
