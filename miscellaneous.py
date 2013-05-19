
import sublime, sublime_plugin
try:
	from paredit import shared
except:
	import shared

def insert_split_brackets(view, edit, lbracket, rbracket, point):
	view.insert(edit, point, rbracket + " " + lbracket)
	return point + 1

def paredit_split_sexp(view, edit):
	def f(region):
		if not region.a == region.b:
			return region

		point = region.a

		(lb, rb) = shared.get_expression(view, point)

		if lb and rb:
			lc = view.substr(lb)
			rc = view.substr(rb - 1)
			spaces_start = shared.remove_spaces(view, edit, point)
			return insert_split_brackets(view, edit, lc, rc, spaces_start)

		return point

	shared.edit_selections(view, f)

def paredit_join_sexp(view, edit):
	pass

class Paredit_split_sexpCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if shared.should_paredit(self.view):
			paredit_split_sexp(self.view, edit)

class Paredit_join_sexpCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if shared.should_paredit(self.view):
			paredit_join_sexp(self.view, edit)
