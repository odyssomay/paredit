
import sublime
import re

####
#### Removing
def erase_region(view, edit, region):
	view.erase(edit, region)
	return region.begin()

def remove_spaces(view, edit, point, remove_newlines=True, erase_left=True, erase_right=True):
	left_limit = None
	right_limit = None

	def isspace(c):
		if remove_newlines:
			return c.isspace()
		return c == " "

	if not erase_left:
		left_limit = point
	elif (point - 1 >= 0 and
	    is_inside_word(view.substr(point - 1))):
		left_limit = point
	else:
		for (i, c) in walk_left(view, point - 1):
			if not isspace(c):
				left_limit = i + 1
				break

	if not erase_right:
		right_limit = point
	elif is_inside_word(view.substr(point)):
		right_limit = point
	else:
		for (i, c) in walk_right(view, point):
			if not isspace(c):
				right_limit = i
				break

	if left_limit and right_limit and left_limit != right_limit:
		view.erase(edit, sublime.Region(left_limit, right_limit))
	return left_limit

####
#### Context checking
def is_point_inside_regions(point, regions):
	for region in regions:
		if point > region.begin() and point < region.end():
			return region

def is_inside_string(view, point):
	if view.score_selector(point, "string") > 0:
		return view.extract_scope(point)

def is_inside_comment(view, point):
	test_point = point
	if (point == view.size() and point - 1 >= 0 and
	    view.substr(point - 1) != "\n"):
		test_point = point - 1
	if view.score_selector(test_point, "comment") > 0:
		return view.extract_scope(test_point)

whitespace_matcher = re.compile("\s*$")
def is_expression_empty(string):
	return whitespace_matcher.match(string[1:-1])

def is_inside_word(c):
	return not (c.isspace() or char_type(c))

####
#### Get expression
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

def get_next_expression(view, point, skip_endbrackets=False):
	for (i, c) in walk_right(view, point):
		if not c.isspace():
			if is_inside_word(c):
				return get_word(view, i)
			t = char_type(c)
			if t == "lbracket" or t == "string":
				return get_expression(view, i + 1)
			elif (not skip_endbrackets) and t == "rbracket":
				return (None, None)

def get_previous_expression(view, point, skip_endbrackets=False):
	for (i, c) in walk_left(view, point):
		if not c.isspace():
			if is_inside_word(c):
				return get_word(view, i)
			t = char_type(c)
			if t == "rbracket" or t == "string":
				return get_expression(view, i)
			elif (not skip_endbrackets) and t == "lbracket":
				return (None, None)

def get_word(view, point):
	word_left = None
	word_right = None

	if not is_inside_word(view.substr(point)):
		return (None, None)

	for (i, c) in walk_left(view, point):
		if not is_inside_word(c):
			word_left = i + 1
			break

	for (i, c) in walk_right(view, point):
		if not is_inside_word(c):
			word_right = i
			break

	return (word_left, word_right)

def get_next_word(view, point):
	word_start = None

	for (i, c) in walk_right(view, point):
		if is_inside_word(c):
			if not word_start:
				word_start = i
		elif word_start:
			return (word_start, i)

	return (word_start, view.size())

def get_previous_word(view, point):
	word_end = None

	for (i, c) in walk_left(view, point - 1):
		if is_inside_word(c):
			if not word_end:
				word_end = i + 1
		elif word_end:
			return (i + 1, word_end)

	return (0, word_end)

####
#### Get character
def get_next_character(view, point):
	for (i, c) in walk_right(view, point):
		if not c.isspace():
			return (i, c)
	return (None, None)

def get_previous_character(view, point):
	for (i, c) in walk_left(view, point):
		if not c.isspace():
			return (i, c)
	return (None, None)

####
#### Misc
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

def char_type(c):
	if c == "\"": return "string"
	elif c == "(" or c == "[" or c == "{": return "lbracket"
	elif c == ")" or c == "]" or c == "}": return "rbracket"

####
#### Walking
def walk_left(view, point):
	i = point

	while i >= 0:
		c = view.substr(i)
		yield (i, c)
		i -= 1

def walk_right(view, point):
	i = point

	while i < view.size():
		c = view.substr(i)
		yield (i, c)
		i += 1

####
#### Configuration
def should_paredit(view):
	return True
