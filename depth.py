
import sublime, sublime_plugin
try:
	from paredit import shared
except:
	import shared

def paredit_wrap(view, edit, lbracket, rbracket):
	pass

def paredit_wrap_round(view, edit):
	paredit_wrap(view, edit, "(", ")")

def paredit_wrap_square(view, edit):
	paredit_wrap(view, edit, "[", "]")

def paredit_wrap_curly(view, edit):
	paredit_wrap(view, edit, "{", "}")

def paredit_splice_sexp(view, edit):
	pass

####
#### Commands
class Paredit_wrap_roundCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if shared.should_paredit(self.view):
			paredit_wrap_round(self.view, edit)

class Paredit_wrap_squareCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if shared.should_paredit(self.view):
			paredit_wrap_square(self.view, edit)

class Paredit_wrap_curlyCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if shared.should_paredit(self.view):
			paredit_wrap_curly(self.view, edit)

class Paredit_splice_sexpCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if shared.should_paredit(self.view):
			paredit_splice_sexp(self.view, edit)
