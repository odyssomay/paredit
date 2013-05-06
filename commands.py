import sublime
import sublime_plugin
import re

whitespace_matcher = re.compile("\s*$")
def is_expression_empty(string):
	return whitespace_matcher.match(string[1:-1])

def find_enclosing_brackets(view, region, left_bracket, right_bracket):
	left_parens = None
	right_parens = None

	i = region.a
	parens_count = 0
	while i >= 0:
		c = view.substr(i)
		if c == left_bracket:
			parens_count += 1
		elif c == right_bracket:
			parens_count -= 1

		if parens_count == 1:
			left_parens = i
			break
		i -= 1

	i = region.b
	parens_count = 0
	end = view.size()
	while i < end:
		c = view.substr(i)
		if c == left_bracket:
			parens_count += 1
		elif c == right_bracket:
			parens_count -= 1

		if parens_count == -1:
			right_parens = i + 1
			break
		i += 1

	return (left_parens, right_parens)

def get_context():
	pass

def edit_selections(view, f):
	new_regions = []

 	for i in range(len(view.sel())):
		region = view.sel()[i]
		new_region = f(region)
		new_regions += [new_region]

	view.sel().clear()
	for region in new_regions:
		if not region == None:
			view.sel().add(region)

def paredit_open(view, edit, left_bracket, right_bracket):
	def f(region):
		begin = region.begin()
		end = region.end()
		view.insert(edit, begin, left_bracket)
		view.insert(edit, end + 1, right_bracket)
		if begin == end:
			new_begin = begin + 1
			new_end = new_begin
		else:
			new_begin = begin
			new_end = end + 2
		return sublime.Region(new_begin, new_end)

	edit_selections(view, f)

def paredit_close(view, edit, left_bracket, right_bracket):
	def f(region):
		(lb, rb) = find_enclosing_brackets(view, region,
		                                   left_bracket, right_bracket)

		if rb:
			return rb
		else:
			return region

	edit_selections(view, f)

def paredit_open_round(view, edit):
	paredit_open(view, edit, "(", ")")

def paredit_close_round(view, edit):
	paredit_close(view, edit, "(", ")")

def paredit_open_square(view, edit):
	paredit_open(view, edit, "[", "]")

def paredit_close_square(view, edit):
	paredit_close(view, edit, "[", "]")

def paredit_open_curly(view, edit):
	paredit_open(view, edit, "{", "}")

def paredit_close_curly(view, edit):
	paredit_close(view, edit, "{", "}")

####
#### Deleting & Killing
def paredit_forward_delete(view, edit):
	def f(region):
		skip = False
		next_char = view.substr(region.begin())
		if next_char == "\"" or next_char == "(":
			return region.begin() + 1
		elif next_char == ")":
			enclosing_region = sublime.Region(region.begin(), region.begin())
			(lb, rb) = find_enclosing_brackets(view, enclosing_region, "(", ")")
			if not (lb == None or rb == None):
				expr_region = sublime.Region(lb, rb + 1)
				expression = view.substr(expr_region)
				print(expression)
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

	edit_selections(view, f)

def paredit_backward_delete(view, edit):
	pass

def paredit_kill(view, edit):
	def f(region):
		(lb, rb) = find_enclosing_brackets

####
#### Basic insertion
class Paredit_open_roundCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_open_round(self.view, edit)

class Paredit_close_roundCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_close_round(self.view, edit)

class Paredit_open_squareCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_open_square(self.view, edit)

class Paredit_close_squareCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_close_square(self.view, edit)

class Paredit_open_curlyCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_open_curly(self.view, edit)

class Paredit_close_curlyCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_close_curly(self.view, edit)

####
#### Deleting & Killing
class Paredit_forward_deleteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_forward_delete(self.view, edit)

class Paredit_backward_deleteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_backward_delete(self.view, edit)

class Paredit_killCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		pass
