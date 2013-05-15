
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

		i = point

		c = view.substr(point)
		t = shared.char_type(c)
		if not (t or c == " "):
			while i < view.size():
				c = view.substr(i)
				if c.isspace():
					return i
				i += 1

			return i

		while i < view.size():
			c = view.substr(i)
			if not c.isspace():
				t = shared.char_type(c)
				if t == "rbracket":
					return i + 1
				if t == "lbracket":
					(lb, rb) = shared.get_expression(view, i + 1)
					if rb: return rb

			i += 1

	shared.edit_selections(view, f)

def paredit_backward(view, edit):
	def f(region):
		if region.a == region.b:
			point = region.a
		else:
			return region

		i = point - 1

		c = view.substr(point)
		t = shared.char_type(c)
		if not (t or c.isspace()):
			while i >= 0:
				c = view.substr(i)
				if c.isspace():
					return i
				i -= 1

			return i

		while i >= 0:
			c = view.substr(i)
			if not c.isspace():
				t = shared.char_type(c)
				if t == "lbracket":
					return i
				if t == "rbracket":
					(lb, rb) = shared.get_expression(view, i)
					if lb: return lb

			i -= 1

	shared.edit_selections(view, f)

class Paredit_forwardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if shared.should_paredit(self.view):
			paredit_forward(self.view, edit)

class Paredit_backwardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if shared.should_paredit(self.view):
			paredit_backward(self.view, edit)


