
import sublime, sublime_plugin
try:
	from paredit import shared
except:
	import shared

def paredit_move(view, edit, direction):
	def f(region):
		if not region.a == region.b:
			return region

		point = region.a

		if shared.is_inside_string(view, point):
			(a, b) = shared.get_expression(view, point, direction)
			target_point = shared.step(b, -1, direction)
			if point == target_point:
				return shared.step(point, 1, direction)
			return shared.step(b, -1, direction)

		if direction == "backward":
			point -= 1

		(word_a, word_b) = shared.get_word(view, point, direction)
		if shared.truthy(word_b):
			return word_b

		(next_a, next_b) = shared.get_next_expression(view, point, False, direction)
		if shared.truthy(next_b):
			return next_b

		expr_point = point
		if direction == "backward":
			expr_point += 1

		(a, b) = shared.get_expression(view, expr_point, direction)
		if shared.truthy(b): return b

		if direction == "forward":
			return shared.step(point, 1, direction)
		else:
			return point

	shared.edit_selections(view, f)

def paredit_forward(view, edit):
	paredit_move(view, edit, "forward")

def paredit_backward(view, edit):
	paredit_move(view, edit, "backward")

class Paredit_forwardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_forward(self.view, edit)

class Paredit_backwardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_backward(self.view, edit)
