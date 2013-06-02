
import sublime, sublime_plugin
try:
	from paredit import shared
except:
	import shared

####
#### Slurping
def paredit_slurp_sexp(view, edit, direction):
	def f(region):
		if not region.a == region.b:
			return region
		point = region.a

		(a_exp, b_exp) = shared.get_expression(view, point, direction)

		if a_exp and b_exp:
			(anext_exp, bnext_exp) = shared.get_next_expression(view, b_exp, True, direction)
			if anext_exp and bnext_exp:
				end_bracket = shared.get_char(view, shared.step(b_exp, -1, direction), direction)
				view.erase(edit, sublime.Region(shared.step(b_exp, -1, direction), b_exp))
				shared.insert(view, edit, shared.step(bnext_exp, -1, direction), end_bracket, direction)

		return point

	shared.edit_selections(view, f)

def paredit_forward_slurp_sexp(view, edit):
	paredit_slurp_sexp(view, edit, "forward")

def paredit_backward_slurp_sexp(view, edit):
	paredit_slurp_sexp(view, edit, "backward")

####
#### Barfing
def paredit_barf_sexp(view, edit, direction):
	def f(region):
		if not region.a == region.b:
			return region
		point = region.a

		(a_exp, b_exp) = shared.get_expression(view, point, direction)

		if a_exp and b_exp:
			(anext_exp, bnext_exp) = reversed(shared.get_next_expression(
				view, shared.step(b_exp, -1 if direction == "backward" else -2, direction), True, shared.opposite_direction(direction)))
			if anext_exp and bnext_exp:
				end_bracket = shared.get_char(view, shared.step(b_exp, -1, direction), direction)

				view.erase(edit, sublime.Region(shared.step(b_exp, -1, direction), b_exp))
				target_point = anext_exp
				for (i, c) in shared.walk(view, shared.step(anext_exp, -1 if direction == "forward" else -2, direction), shared.opposite_direction(direction)):
					if not c.isspace():
						target_point = shared.step(i, 1, direction)
						break

				shared.insert(view, edit, target_point, end_bracket, direction)

		return point

	shared.edit_selections(view, f)

def paredit_forward_barf_sexp(view, edit):
	paredit_barf_sexp(view, edit, "forward")

def paredit_backward_barf_sexp(view, edit):
	paredit_barf_sexp(view, edit, "backward")

####
#### Commands
class Paredit_forward_slurp_sexpCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_forward_slurp_sexp(self.view, edit)

class Paredit_forward_barf_sexpCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_forward_barf_sexp(self.view, edit)

class Paredit_backward_slurp_sexpCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_backward_slurp_sexp(self.view, edit)

class Paredit_backward_barf_sexpCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_backward_barf_sexp(self.view, edit)
