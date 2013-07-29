# paredit

This is an implementation of [paredit](http://www.emacswiki.org/emacs/ParEdit)
for [sublime text](http://www.sublimetext.com/).

## Installation

### With package control (recommended)

Use [Sublime Package Control](http://wbond.net/sublime_packages/package_control),
the package is called `paredit`.

### Manually

1. Clone the repository or download the [zipfile](https://github.com/odyssomay/paredit/archive/master.zip).
2. The resulting folder - either from cloning or unzipping - should be moved to
`Installed Packages` inside your [data directory](http://docs.sublimetext.info/en/latest/basic_concepts.html#the-data-directory).

## Usage

See [the cheatsheet](http://pub.gajendra.net/src/paredit-refcard.pdf).

## Implementation Status

Below is a list of all currently **not** implemented paredit commands
from the cheatsheet.

* paredit-backslash
* paredit-recentre-on-sexp
* paredit-reindent-defun

## Testing

Press *ctrl+shift+p* to open the command palette. Type *test*
and run *Paredit: Run Tests*.
