
import sublime, sublime_plugin
try:
	from paredit import shared
except:
	import shared

def paredit_split_sexp(view, edit):
	pass

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
