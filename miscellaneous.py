
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

		if shared.truthy(lb, rb):
			lc = view.substr(lb)
			rc = view.substr(rb - 1)
			if lc == "\"":
				spaces_start = point
			else:
				spaces_start = shared.remove_spaces(view, edit, point)
			return insert_split_brackets(view, edit, lc, rc, spaces_start)

		return point

	shared.edit_selections(view, f)

def join_sexp(view, edit, prev_i, next_i, should_insert_space=True):
	view.erase(edit, sublime.Region(prev_i, next_i + 1))
	if should_insert_space:
		view.insert(edit, prev_i, " ")
	return prev_i

def paredit_join_sexp(view, edit):
	def f(region):
		if not region.a == region.b:
			return region
		point = region.a

		(prev_i, prev_char) = shared.get_previous_character(view, point)
		(next_i, next_char) = shared.get_next_character(view, point)

		if (prev_char == ")" and next_char == "(" or
		    prev_char == "]" and next_char == "[" or
		    prev_char == "}" and next_char == "{"):
			return join_sexp(view, edit, prev_i, next_i)
		elif prev_char == "\"" and next_char == "\"":
			return join_sexp(view, edit, prev_i, next_i, False)
		else:
			return shared.remove_spaces(view, edit, point)

	shared.edit_selections(view, f)

class Paredit_split_sexpCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_split_sexp(self.view, edit)

class Paredit_join_sexpCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_join_sexp(self.view, edit)
