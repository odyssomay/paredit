
import sublime, sublime_plugin
try:
	from paredit import shared
except:
	import shared

def paredit_forward(view, edit):
	def f(region):
		if region.a == region.b:
			point = region.a
		else:
			return region
		
		c = view.substr(point)
		t = shared.char_type(c)
		if not (t or c == " "):
			for (i, c) in shared.walk_right(view, point):
				if c.isspace():
					return i

			return view.size() - 1

		for (i, c) in shared.walk_right(view, point):
			if not c.isspace():
				t = shared.char_type(c)
				if t == "rbracket":
					return i + 1
				if t == "lbracket":
					(lb, rb) = shared.get_expression(view, i + 1)
					if rb: return rb

	shared.edit_selections(view, f)

def paredit_backward(view, edit):
	def f(region):
		if region.a == region.b:
			point = region.a
		else:
			return region

		c = view.substr(point)
		t = shared.char_type(c)
		if not (t or c.isspace()):
			for (i, c) in shared.walk_left(view, point - 1):
				if c.isspace():
					return i

			return 0

		for (i, c) in shared.walk_left(view, point - 1):
			if not c.isspace():
				t = shared.char_type(c)
				if t == "lbracket":
					return i
				if t == "rbracket":
					(lb, rb) = shared.get_expression(view, i)
					if lb: return lb

		return 0

	shared.edit_selections(view, f)

class Paredit_forwardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if shared.should_paredit(self.view):
			paredit_forward(self.view, edit)

class Paredit_backwardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if shared.should_paredit(self.view):
			paredit_backward(self.view, edit)


