
import sublime, sublime_plugin
try:
	from paredit import shared
except:
	import shared

def paredit_forward_delete(view, edit):
	def f(region):
		if not region.begin() == region.end():
			return shared.erase_region(view, edit, region)

		next_char = view.substr(region.begin())
		if next_char == "\"" or next_char == "(" or next_char == "[" or next_char == "{":
			return region.begin() + 1
		elif next_char == ")" or next_char == "]" or next_char == "}":
			(lb, rb) = shared.get_expression(view, region.begin())
			if not (lb == None or rb == None):
				expr_region = sublime.Region(lb, rb)
				expression = view.substr(expr_region)
				if shared.is_expression_empty(expression):
					return shared.erase_region(view, edit, expr_region)
				else:
					return sublime.Region(region.begin() + 1, region.begin() + 1)
			else:
				return region
		else:
			view.erase(edit, sublime.Region(region.begin(), region.begin() + 1))
			return region

	shared.edit_selections(view, f)

def paredit_backward_delete(view, edit):
	def f(region):
		if not region.begin() == region.end():
			return shared.erase_region(view, edit, region)

		next_char = view.substr(region.begin() - 1)
		if next_char == "\"" or next_char == ")" or next_char == "]" or next_char == "}":
			return region.begin() - 1
		elif next_char == "(" or next_char == "[" or next_char == "{":
			(lb, rb) = shared.get_expression(view, region.begin())
			if not (lb == None or rb == None):
				expr_region = sublime.Region(lb, rb)
				expression = view.substr(expr_region)
				if shared.is_expression_empty(expression):
					return shared.erase_region(view, edit, expr_region)
				else:
					return sublime.Region(region.begin() - 1, region.begin() - 1)
			else:
				return region
		else:
			view.erase(edit, sublime.Region(region.begin(), region.begin() - 1))
			return region.begin() - 1

	shared.edit_selections(view, f)

def paredit_kill_abstract(view, edit, expression):
	def f(region):
		point = region.begin()
		if region.end() == point:
			(lb, rb) = shared.get_expression(view, point)
			if lb and rb:
				if expression:
					view.erase(edit, sublime.Region(lb + 1, rb - 1))
					return lb + 1
				else:
					view.erase(edit, sublime.Region(point, rb - 1))
					return point
			else:
				return point
		else:
			return region

	shared.edit_selections(view, f)

def paredit_kill(view, edit):
	paredit_kill_abstract(view, edit, False)

def paredit_kill_expression(view, edit):
	paredit_kill_abstract(view, edit, True)

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

class Paredit_kill_expressionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_kill_expression(self.view, edit)
