
import sublime, sublime_plugin
try:
	from paredit import shared
except:
	import shared

def paredit_forward_slurp_sexp(view, edit):
	def f(region):
		if not region.a == region.b:
			return region
		point = region.a

		(l_exp, r_exp) = shared.get_expression(view, point)

		if l_exp and r_exp:
			(lnext_exp, rnext_exp) = shared.get_next_expression(view, r_exp, True)
			if lnext_exp and rnext_exp:
				rbracket = view.substr(r_exp - 1)
				view.erase(edit, sublime.Region(r_exp - 1, r_exp))
				view.insert(edit, rnext_exp - 1, rbracket)

		return point

	shared.edit_selections(view, f)

def paredit_forward_barf_sexp(view, edit):
	def f(region):
		if not region.a == region.b:
			return region
		point = region.a

		(l_exp, r_exp) = shared.get_expression(view, point)

		if l_exp and r_exp:
			(lnext_exp, rnext_exp) = shared.get_next_expression(view, point, True)
			if lnext_exp and rnext_exp:
				rbracket = view.substr(r_exp - 1)
				view.erase(edit, sublime.Region(r_exp - 1, r_exp))
				view.insert(edit, rnext_exp, rbracket)

		return point

	shared.edit_selections(view, f)

def paredit_backward_slurp_sexp(view, edit):
	def f(region):
		if not region.a == region.b:
			return region
		point = region.a

		(l_exp, r_exp) = shared.get_expression(view, point)

		if l_exp and r_exp:
			(lnext_exp, rnext_exp) = shared.get_previous_expression(view, l_exp, True)
			if lnext_exp and rnext_exp:
				rbracket = view.substr(l_exp)
				view.erase(edit, sublime.Region(l_exp, l_exp + 1))
				view.insert(edit, lnext_exp, rbracket)

		return point

	shared.edit_selections(view, f)

def paredit_backward_barf_sexp(view, edit):
	def f(region):
		if not region.a == region.b:
			return region
		point = region.a

		(l_exp, r_exp) = shared.get_expression(view, point)

		if l_exp and r_exp:
			(lnext_exp, rnext_exp) = shared.get_previous_expression(view, point, True)
			if lnext_exp and rnext_exp:
				rbracket = view.substr(l_exp)
				view.erase(edit, sublime.Region(l_exp, l_exp + 1))
				view.insert(edit, lnext_exp - 1, rbracket)

		return point

	shared.edit_selections(view, f)

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
