
import sublime, sublime_plugin
try:
	from paredit import shared
except:
	import shared

def paredit_forward_delete(view, edit):
	def f(region):
		skip = False
		next_char = view.substr(region.begin())
		if next_char == "\"" or next_char == "(":
			return region.begin() + 1
		elif next_char == ")":
			enclosing_region = sublime.Region(region.begin(), region.begin())
			(lb, rb) = shared.find_enclosing_brackets(view, enclosing_region, "(", ")")
			if not (lb == None or rb == None):
				expr_region = sublime.Region(lb, rb + 1)
				expression = view.substr(expr_region)
				if is_expression_empty(expression):
					view.erase(edit, expr_region)
					return sublime.Region(lb, lb)
				else:
					return sublime.Region(region.begin() + 1, region.begin() + 1)
			else:
				return region
		else:
			view.erase(edit, sublime.Region(region.begin(), region.begin() + 1))
			return region

	shared.edit_selections(view, f)

def paredit_backward_delete(view, edit):
	pass

def paredit_kill(view, edit):
	def f(region):
		pass

####
#### Commands
class Paredit_forward_deleteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_forward_delete(self.view, edit)

class Paredit_backward_deleteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_backward_delete(self.view, edit)

class Paredit_killCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_kill(self.view, edit)