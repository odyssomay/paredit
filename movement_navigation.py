
import sublime, sublime_plugin
try:
	from paredit import shared
except:
	import shared

def paredit_forward(view, edit):
	def f(region):
		if not region.a == region.b:
			return region

		point = region.a

		if shared.is_inside_string(view, point):
			(lb, rb) = shared.get_expression(view, point)
			target_point = rb - 1
			if point == target_point:
				return point + 1
			return rb - 1

		(word_start, word_end) = shared.get_word(view, point)
		if word_start and word_end:
			return word_end

		(next_left, next_right) = shared.get_next_expression(view, point)
		if next_right:
			return next_right
		else:
			(lb, rb) = shared.get_expression(view, point)
			if rb: return rb
			return point + 1

	shared.edit_selections(view, f)

def paredit_backward(view, edit):
	def f(region):
		if not region.a == region.b:
			return region

		point = region.a

		if shared.is_inside_string(view, point):
			(lb, rb) = shared.get_expression(view, point)
			target_point = lb + 1
			if point == target_point:
				point - 1
			return lb + 1

		(word_start, word_end) = shared.get_word(view, point - 1)

		if word_start and word_end:
			return word_start

		(prev_left, prev_right) = shared.get_previous_expression(view, point - 1)
		if prev_left:
			return prev_left
		else:
			(lb, rb) = shared.get_expression(view, point)
			if lb: return lb
			return point - 1

	shared.edit_selections(view, f)

class Paredit_forwardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_forward(self.view, edit)

class Paredit_backwardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_backward(self.view, edit)


