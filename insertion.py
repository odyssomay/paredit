
import sublime, sublime_plugin
try:
	from paredit import shared
except:
	import shared

def paredit_open(view, edit, left_bracket, right_bracket):
	def f(region):
		begin = region.begin()
		end = region.end()

		view.insert(edit, begin, left_bracket)

		if not (begin == end and shared.is_inside_string(view, begin)):
			view.insert(edit, end + 1, right_bracket)

		return begin + 1

	shared.edit_selections(view, f)

def paredit_close_remove_spaces(view, edit, rb):
	i = rb - 2

	while i >= 0:
		c = view.substr(i)
		if not c == " ":
			break
		i -= 1

	spaces_start = i + 1
	spaces_end = rb - 1

	if not spaces_start == spaces_end:
		view.erase(edit, sublime.Region(i + 1, rb - 1))

	return i + 2

def paredit_close(view, edit, left_bracket, right_bracket):
	def f(region):
		if not region.a == region.b:
			return region

		point = region.begin()

		if shared.is_inside_string(view, point):
			view.insert(edit, point, right_bracket)
			return point + 1

		(lb, rb) = shared.find_enclosing_brackets(
			view, region.begin(), left_bracket, right_bracket)

		if rb:
			return paredit_close_remove_spaces(view, edit, rb)
		else:
			return region

	shared.edit_selections(view, f)

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

def paredit_newline(view, edit):
	def f(region):
		s = region.begin()
		e = region.end()

		if not s == e: view.erase(region)
		point = shared.remove_spaces(view, edit, s)
		view.insert(edit, point, "\n")
		return point + 1

	shared.edit_selections(view, f)
	view.run_command("lispindent")

####
#### Commands
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

class Paredit_newlineCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_newline(self.view, edit)
