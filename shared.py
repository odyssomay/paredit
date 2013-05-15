
import sublime
import re

def erase_region(view, edit, region):
	view.erase(edit, region)
	return region.begin()

def is_point_inside_regions(point, regions):
	for region in regions:
		if point >= region.begin() and point < region.end():
			return region

def is_inside_string(view, point):
	regions = view.find_by_selector("string")
	return is_point_inside_regions(point, regions)

def is_inside_comment(view, point):
	regions = view.find_by_selector("comment")
	return is_point_inside_regions(point, regions)

whitespace_matcher = re.compile("\s*$")
def is_expression_empty(string):
	return whitespace_matcher.match(string[1:-1])

def find_enclosing_brackets(view, point, left_bracket, right_bracket):
	left_parens = None
	right_parens = None

	i = point - 1
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

	i = point
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

def max_with_none(*args):
	out = args[0]

	for arg in args:
		if arg:
			if not out or (out and arg > out):
				out = arg

	return out

def get_expression(view, point):
	string_region = is_inside_string(view, point)
	if string_region: return (string_region.begin(), string_region.end())

	paren = (lparen, rparen) = find_enclosing_brackets(view, point, "(", ")")
	brack = (lbrack, rbrack) = find_enclosing_brackets(view, point, "[", "]")
	curly = (lcurly, rcurly) = find_enclosing_brackets(view, point, "{", "}")

	m = max_with_none(lparen, lbrack, lcurly)

	if   m == lparen: return paren
	elif m == lbrack: return brack
	elif m == lcurly: return curly
	else: return (None, None)

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

def remove_spaces(view, edit, point):
	i = point - 1

	while i >= 0:
		c = view.substr(i)
		if not c == " ":
			break
		i -= 1

	left_limit = i + 1
	i = point

	while i < view.size():
		c = view.substr(i)
		if not c == " ":
			break
		i += 1

	right_limit = i

	view.erase(edit, sublime.Region(left_limit, right_limit))
	return left_limit

def should_paredit(view):
	return True

def char_type(c):
	if c == "\"": return "string"
	elif c == "(" or c == "[" or c == "{": return "lbracket"
	elif c == ")" or c == "]" or c == "}": return "rbracket"
