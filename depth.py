
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
	def f(region):
		if not region.a == region.b:
			return region

		point = region.a

		(lb, rb) = shared.get_expression(view, point)
		if lb and rb:
			print(view.substr(sublime.Region(lb, rb)))
			view.erase(edit, sublime.Region(rb - 1, rb))
			view.erase(edit, sublime.Region(lb, lb + 1))
			return point - 1
		else:
			return point

	shared.edit_selections(view, f)

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
