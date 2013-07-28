
import sublime, sublime_plugin
try:
	from paredit import shared
except:
	import shared

def insert_brackets(view, edit, lbracket, rbracket, region):
	view.insert(edit, region.begin(), lbracket)
	view.insert(edit, region.end() + 1, rbracket)
	return region.begin() + 1

def paredit_wrap(view, edit, lbracket, rbracket):
	def f(region):
		if not region.a == region.b:
			return insert_brackets(view, edit, lbracket, rbracket, region)

		point = region.a

		(lb, rb) = shared.get_next_expression(view, point)
		if shared.truthy(lb, rb):
			return insert_brackets(view, edit, lbracket, rbracket,
				sublime.Region(lb, rb))

		return point

	shared.edit_selections(view, f)

def paredit_wrap_round(view, edit):
	paredit_wrap(view, edit, "(", ")")

def paredit_wrap_square(view, edit):
	paredit_wrap(view, edit, "[", "]")

def paredit_wrap_curly(view, edit):
	paredit_wrap(view, edit, "{", "}")

def paredit_meta_doublequote(view, edit):
	paredit_wrap(view, edit, "\"", "\"")

def paredit_splice_sexp(view, edit):
	def f(region):
		if not region.a == region.b:
			return region

		point = region.a

		(lb, rb) = shared.get_expression(view, point)
		if shared.truthy(lb, rb):
			view.erase(edit, sublime.Region(rb - 1, rb))
			view.erase(edit, sublime.Region(lb, lb + 1))
			return point - 1
		else:
			return point

	shared.edit_selections(view, f)

def paredit_splice_sexp_killing_backward(view, edit):
	def f(region):
		if not region.a == region.b:
			return region

		point = region.a

		(lb, rb) = shared.get_expression(view, point)
		if shared.truthy(lb, rb):
			view.erase(edit, sublime.Region(rb - 1, rb))
			view.erase(edit, sublime.Region(lb, point))
			return lb
		else:
			return point

	shared.edit_selections(view, f)

####
#### Commands
class Paredit_wrap_roundCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_wrap_round(self.view, edit)

class Paredit_wrap_squareCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_wrap_square(self.view, edit)

class Paredit_wrap_curlyCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_wrap_curly(self.view, edit)

class Paredit_meta_doublequoteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_meta_doublequote(self.view, edit)

class Paredit_splice_sexpCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_splice_sexp(self.view, edit)

class Paredit_splice_sexp_killing_backwardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_splice_sexp_killing_backward(self.view, edit)
