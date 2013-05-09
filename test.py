
import sublime, sublime_plugin
import re

def write(view, edit, text):
	view.insert(edit, view.size(), text + "\n")

find_carets = re.compile("\\|")
def process_carets(text):
	carets = []
	for match in find_carets.finditer(text):
		i = match.start() - len(carets)
		carets += [i]

	if len(carets) == 1:
		carets += [carets[0]]

	return (text.replace("|", ""), carets)

def set_carets(view, offset, carets):
	(start, end) = carets
	sel = view.sel()
	sel.clear()
	sel.add(sublime.Region(start + offset, end + offset))

def get_carets(view, offset):
	region = view.sel()[0]
	return [region.begin() - offset, region.end() - offset]

def add_carets(text, carets):
	out = text
	(start, end) = carets
	out = out[:start] + "|" + out[start:]
	if not start == end:
		end += 1
		out = out[:end] + "|" + out[end:]
	return out

def run_test(view, edit, command, test):
	(init_with_carets, result_with_carets) = test
	(init, init_carets) = process_carets(init_with_carets)
	(result, result_carets) = process_carets(result_with_carets)

	start_index = view.size()
	view.insert(edit, start_index, init)
	set_carets(view, start_index, init_carets)
	view.run_command(command)
	actual_result = view.substr(sublime.Region(start_index, view.size()))
	actual_carets = get_carets(view, start_index)
	if not (actual_result == result and result_carets == actual_carets):
		actual_result = add_carets(actual_result, actual_carets)
		view.insert(edit, view.size(),
			"\nFAILED! Input: \"" + init_with_carets +
			"\", Expected: \"" + result_with_carets +
			"\", Result: \"" + actual_result + "\"")

def run_tests(view, edit, command, tests):
	write(view, edit, "========================================")
	write(view, edit, "Testing " + command)
	for test in tests:
		run_test(view, edit, command, test)
		write(view, edit, "")
	write(view, edit, "")

def paredit_test_insertion(view, edit):
	run_tests(view, edit,
		"paredit_open_round",
		[
			["|", "(|)"]
		,	["(|)", "((|))"]
		,	["|hel|lo", "(|hel)lo"]
		,	["(def s \"hel|lo\")", "(def s \"hel(|lo\")"]
		,	["; |", "; (|"]
		])
	run_tests(view, edit,
		"paredit_close_round",
		[
			["|", "|"]
		,	["(|)", "()|"]
		,	["(|  )", "()|"]
		,	["(def s \"hel|lo\")", "(def s \"hel)|lo\")"]
		,	["; |", "; )|"]
		,	["(def |a 3)", "(def a 3)|"]
		,	["(def |a 3    )", "(def a 3)|"]
		])
	run_tests(view, edit,
		"paredit_open_square",
		[
			["|", "[|]"]
		,	["[|]", "[[|]]"]
		,	["hell|o w|orld", "hell[|o w]orld"]
		])
	run_tests(view, edit,
		"paredit_doublequote",
		[
			["|", "\"|\""]
		,	["(def a \"|\")", "(def a \"\\\"|\")"]
		,	["|hello world|", "\"|hello world|\""]
		])
	run_tests(view, edit,
		"paredit_newline",
		[
			["|", "\n|"]
		,	["(defn add1 [x] | (+ x 1))", "(defn add1 [x]\n  |(+ x 1))"]
		])

def paredit_test_deleting_killing(view, edit):
	run_tests(view, edit,
		"paredit_forward_delete",
		[
			["(quu|x \"zot\")", "(quu| \"zot\")"]
		,	["(quux |\"zot\")", "(quux \"|zot\")"]
		,	["(quux \"|zot\")", "(quux \"|ot\")"]
		,	["(quux \"|\")", "(quux |)"]
		,	["(foo (|) bar)", "(foo | bar)"]
		,	["(foo [|] bar)", "(foo | bar)"]
		,	["|(foo bar)", "(|foo bar)"]
		,	["|[hello world]", "[|hello world]"]
		,	["|{:a 3 :b 4}", "{|:a 3 :b 4}"]
		,	["(hello|)", "(hello)|"]

		,	["; |(", "; |"]
		])
	run_tests(view, edit,
		"paredit_backward_delete",
		[
			["(\"zot\" q|uux)", "(\"zot\" |uux)"]
		,	["(\"zot\"| quux)", "(\"zot|\" quux)"]
		,	["(\"zot|\" quux)", "(\"zo|\" quux)"]
		,	["(quux \"|\")", "(quux |)"]

		,	["(foo (|) bar)", "(foo | bar)"]
		,	["(foo [|] bar)", "(foo | bar)"]
		,	["(foo {|} bar)", "(foo | bar)"]

		,	["(foo bar)|", "(foo bar|)"]
		,	["[foo bar]|", "[foo bar|]"]
		,	["{:a 3 :b 4}|", "{:a 3 :b 4|}"]

		,	["(|foo bar)", "|(foo bar)"]
		,	["[|foo bar]", "|[foo bar]"]
		,	["{|:a 3 :b 4}", "|{:a 3 :b 4}"]

		,	["; (|", "; |"]
		])
	run_tests(view, edit,
		"paredit_kill",
		[
			["(|foo bar)", "(|)"]
		,	["(foo |bar)", "(foo |)"]
		,	["(foo \"|bar baz\" quux)", "(foo \"|\" quux)"]
		,	["(foo \"bar |baz\" quux)", "(foo \"bar |\" quux)"]
		,	["[1 2| 3]", "[1 2|]"]
		,	["{:a |3 :b 4}", "{:a |}"]
		])
	run_tests(view, edit,
		"paredit_kill_expression",
		[
			["(foo| bar)", "(|)"]
		,	["(foo \"|bar baz\" quux)", "(foo \"|\" quux)"]
		,	["(foo \"bar |baz\" quux)", "(foo \"|\" quux)"]
		,	["[1 2| 3]", "[|]"]
		,	["{:a |3 :b 4}", "{|}"]
		])

def paredit_test_movement_navigation(view, edit):
	run_tests(view, edit,
		"paredit_forward",
		[
			["(foo |(bar baz) quux)", "(foo (bar baz)| quux)"]
		,	["(foo (bar baz)|)", "(foo (bar baz))|"]
		,	["(f|oo (bar baz))", "(foo| (bar baz))"]
		,	["(fo|o bar)", "(foo  bar|)"]
		])
	run_tests(view, edit,
		"paredit_backward",
		[
			["(foo (bar baz)| quux)", "(foo |(bar baz) quux)"]
		,	["(|(foo) bar)", "|((foo) bar)"]
		])

####
#### Commands
class Paredit_test_insertionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_test_insertion(self.view, edit)

class Paredit_test_deleting_killingCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_test_deleting_killing(self.view, edit)

class Paredit_test_movement_navigationCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_test_movement_navigation(self.view, edit)

class Paredit_run_testsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		window = sublime.active_window()
		view = window.new_file()

		commands = [
			"paredit_test_insertion"
		,	"paredit_test_deleting_killing"
		,	"paredit_test_movement_navigation"
		]

		view.run_command("set_file_type", {"syntax": "Packages/Clojure/Clojure.tmLanguage"})
		write(view, edit, "Running tests\n")

		for command in commands:
			view.run_command(command)
