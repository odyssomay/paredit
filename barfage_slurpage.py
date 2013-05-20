
import sublime, sublime_plugin
try:
	from paredit import shared
except:
	import shared

def paredit_forward_slurp_sexp(view, edit):
	pass

def paredit_forward_barf_sexp(view, edit):
	pass

def paredit_backward_slurp_sexp(view, edit):
	pass

def paredit_backward_barf_sexp(view, edit):
	pass

class Paredit_forward_slurp_sexpCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if shared.should_paredit(self.view):
			paredit_forward_slurp_sexp(self.view, edit)

class Paredit_forward_barf_sexpCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if shared.should_paredit(self.view):
			paredit_forward_barf_sexp(self.view, edit)

class Paredit_backward_slurp_sexpCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if shared.should_paredit(self.view):
			paredit_backward_slurp_sexp(self.view, edit)

class Paredit_backward_barf_sexpCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if shared.should_paredit(self.view):
			paredit_backward_barf_sexp(self.view, edit)
