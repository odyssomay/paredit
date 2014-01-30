
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
	view.erase(edit, sublime.Region(start_index, view.size()))
	if not (actual_result == result and result_carets == actual_carets):
		actual_result = add_carets(actual_result, actual_carets)
		view.insert(edit, view.size(),
			"FAILED! Input: \"" + init_with_carets +
			"\", Expected: \"" + result_with_carets +
			"\", Result: \"" + actual_result + "\"\n")

def run_tests(view, edit, command, tests):
	write(view, edit, "========================================")
	write(view, edit, "Testing " + command + "\n")
	for test in tests:
		run_test(view, edit, command, test)
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
		"paredit_close_round_and_newline",
		[
			["(defn f (x|   ))", "(defn f (x)\n  |)"]
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
		,	["(def a \"|\")", "(def a \"\"|)"]
		,	["(def a \"| \")", "(def a \"\\\"| \")"]
		,	["|hello world|", "\"|hello world|\""]
		])
	run_tests(view, edit,
		"paredit_comment_dwim",
		[
			["(foo |bar) ; baz", "(foo bar) ; |baz"]
		,	["(foo |bar)", "(foo bar) ;|"]
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
		,	["(quux \"z|(ot\")", "(quux \"z|ot\")"]
		,	["(quux \"|\")", "(quux |)"]
		,	["(quux \"|\\\"\")", "(quux \"|\")"]
		,	["(foo (|) bar)", "(foo | bar)"]
		,	["(foo [|] bar)", "(foo | bar)"]
		,	["|(foo bar)", "(|foo bar)"]
		,	["|[hello world]", "[|hello world]"]
		,	["|{:a 3 :b 4}", "{|:a 3 :b 4}"]
		,	["(hello|)", "(hello)|"]
		,	["; |(", "; |"]

		,	["|()|", "|"]
		,	["|[][]|", "|"]
		,	["(fo|o (bar)| baz)", "(fo| baz)"]
		,	["(fo|o (bar|) baz)", "(fo| (bar) baz)"]
		,	["(defn f1 [coll f |x]| (conj (map f coll) x))",
			 "(defn f1 [coll f |] (conj (map f coll) x))"]
		,	["|(def a 3) ; (|", "|"]
		])
	run_tests(view, edit,
		"paredit_backward_delete",
		[
			["(\"zot\" q|uux)", "(\"zot\" |uux)"]
		,	["(\"zot\"| quux)", "(\"zot|\" quux)"]
		,	["(\"zot|\" quux)", "(\"zo|\" quux)"]
		,	["(quux \"z(|ot\")", "(quux \"z|ot\")"]
		,	["(quux \"|\")", "(quux |)"]
		,	["(quux \"\\\"|\")", "(quux \"|\")"]

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
		,	["(|)", "|"]
		,	["(  | )", "|"]
		,	["(foo |bar)", "(foo |)"]
		,	["(foo \"|bar baz\" quux)", "(foo \"|\" quux)"]
		,	["(foo \"bar |baz\" quux)", "(foo \"bar |\" quux)"]
		,	["[1 2| 3]", "[1 2|]"]
		,	["{:a |3 :b 4}", "{:a |}"]
		,	["(foo)| ; Bar", "(foo)|"]
		])
	run_tests(view, edit,
		"paredit_kill_expression",
		[
			["(foo| bar)", "(|)"]
		,	["(foo \"|bar baz\" quux)", "(foo \"|\" quux)"]
		,	["(foo \"bar |baz\" quux)", "(foo \"|\" quux)"]
		,	["[1 2| 3]", "[|]"]
		,	["{:a |3 :b 4}", "{|}"]
		,	["(foo)| ; Bar", "|"]
		])
	run_tests(view, edit,
		"paredit_forward_kill_word",
		[
			["|(foo bar)", "(| bar)"]
		,	["(| bar)", "(|)"]
		])
	run_tests(view, edit,
		"paredit_backward_kill_word",
		[
			["(quux)|", "(|)"]
		,	["(foo |)", "(|)"]
		])

def paredit_test_movement_navigation(view, edit):
	run_tests(view, edit,
		"paredit_forward",
		[
			["(foo |(bar baz) quux)", "(foo (bar baz)| quux)"]
		,	["(foo (bar baz)|)", "(foo (bar baz))|"]
		,	["(f|oo (bar baz))", "(foo| (bar baz))"]
		,	["(foo)| (bar)", "(foo) (bar)|"]
		,	["(foo)|\n(bar)", "(foo)\n(bar)|"]
		])
	run_tests(view, edit,
		"paredit_backward",
		[
			["(foo (bar baz)| quux)", "(foo |(bar baz) quux)"]
		,	["(|(foo) bar)", "|((foo) bar)"]
		,	["(foo) (bar)|", "(foo) |(bar)"]
		,	["(foo) |(bar)", "|(foo) (bar)"]
		,	["(foo)\n|(bar)", "|(foo)\n(bar)"]
		])
	run_tests(view, edit,
		"paredit_forward_up",
		[
			["(foo (bar baz|))", "(foo (bar baz)|)"]
		,	["(foo (bar| baz))", "(foo (bar baz)|)"]
		])
	run_tests(view, edit,
		"paredit_forward_down",
		[
			["(foo |(bar baz))", "(foo (|bar baz))"]
		,	["(|foo (bar baz))", "(foo (|bar baz))"]
		])
	run_tests(view, edit,
		"paredit_backward_up",
		[
			["(foo (|bar baz))", "(foo |(bar baz))"]
		,	["(foo (bar baz|))", "(foo |(bar baz))"]
		])
	run_tests(view, edit,
		"paredit_backward_down",
		[
			["(foo (bar baz)|)", "(foo (bar baz|))"]
		,	["(foo (bar baz) baz|)", "(foo (bar baz|) baz)"]
		])

def paredit_test_depth_changing(view, edit):
	run_tests(view, edit,
		"paredit_wrap_round",
		[
			["(foo |bar baz)", "(foo (|bar) baz)"]
		,	["(foo| (bar) (baz))", "(foo (|(bar)) (baz))"]
		,	["(foo| \"bar\")", "(foo (|\"bar\"))"]
		,	["(foo |bar| baz)", "(foo (|bar) baz)"]
		])
	run_tests(view, edit,
		"paredit_wrap_square",
		[
			["(foo |bar baz)", "(foo [|bar] baz)"]
		])
	run_tests(view, edit,
		"paredit_wrap_curly",
		[
			["(foo |bar baz)", "(foo {|bar} baz)"]
		])
	run_tests(view, edit,
		"paredit_splice_sexp",
		[
			["(foo (bar| baz) quux)", "(foo bar| baz quux)"]
		,	["(def a \"hello| world\")", "(def a hello| world)"]
		,	["(def a \"hello world\"|)", "def a \"hello world\"|"]
		,	["(def a {|:a 3 :b 4})", "(def a |:a 3 :b 4)"]
		,	["(def a {:a 3 :b 4|})", "(def a :a 3 :b 4|)"]
		])
	run_tests(view, edit,
		"paredit_splice_sexp_killing_backward",
		[
			["[1 2 |3 4]", "|3 4"]
		,	["(def a |[1 2 3 4])", "|[1 2 3 4]"]
		,	["(def a \"hell|o world!\")", "(def a |o world!)"]
		])
	run_tests(view, edit,
		"paredit_splice_sexp_killing_forward",
		[
			["[1 2 |3 4]", "1 2 |"]
		,	["(def a |[1 2 3 4])", "def a |"]
		,	["(def a \"hell|o world!\")", "(def a hell|)"]
		])
	run_tests(view, edit,
		"paredit_raise_sexp",
		[
			["[1 2 |3 4]", "|3"]
		,	["(def a |[1 2 3 4])", "|[1 2 3 4]"]
		,	["(def a |:bla)", "|:bla"]
		,	["(def a [1 2 |:hello :world])", "(def a |:hello)"]
		,	["(def a [1 2 3|])", "(def a |)"]
		])

def paredit_test_barfage_slurpage(view, edit):
	run_tests(view, edit,
		"paredit_forward_slurp_sexp",
		[
			["(foo (bar |baz) quux zot)", "(foo (bar |baz quux) zot)"]
		,	["(a b ((c| d)) e f)", "(a b ((c| d) e) f)"]
		,	["(a b ((c| d) e) f)", "(a b ((c| d e)) f)"]
		])
	run_tests(view, edit,
		"paredit_forward_barf_sexp",
		[
			["(foo (bar |baz quux) zot)", "(foo (bar |baz) quux zot)"]
		,	["(f (b |z q) t)", "(f (b |z) q t)"]
		,	["(defn f1 [coll f x] (conj (m|ap f coll x)))",
			 "(defn f1 [coll f x] (conj (m|ap f coll) x))"]
		,	["(defn f1 [coll f x] (conj (m|ap f coll) x))",
			 "(defn f1 [coll f x] (conj (m|ap f) coll x))"]
		,	["(defn f1 [coll f x] (conj (m|ap f) coll x))",
			 "(defn f1 [coll f x] (conj (m|ap) f coll x))"]
		])
	run_tests(view, edit,
		"paredit_backward_slurp_sexp",
		[
			["(foo bar (baz| quux) zot)", "(foo (bar baz| quux) zot)"]
		])
	run_tests(view, edit,
		"paredit_backward_barf_sexp",
		[
			["(foo (bar baz| quux) zot)", "(foo bar (baz| quux) zot)"]
		,	["(f (b |z q) t)", "(f b (|z q) t)"]
		])

def paredit_test_miscellaneous(view, edit):
	run_tests(view, edit,
		"paredit_split_sexp",
		[
			["(hello| world)", "(hello)| (world)"]
		,	["(hello |world)", "(hello)| (world)"]
		,	["(foo \"hello, |world!\")", "(foo \"hello, \"| \"world!\")"]
		])
	run_tests(view, edit,
		"paredit_join_sexp",
		[
			["(hello)| (world)", "(hello| world)"]
		,	["(foo \"Hello, \"| \"world!\")", "(foo \"Hello, |world!\")"]
		,	["hello-\n|  world", "hello-|world"]
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

class Paredit_test_depth_changingCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_test_depth_changing(self.view, edit)

class Paredit_test_barfage_slurpageCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_test_barfage_slurpage(self.view, edit)

class Paredit_test_miscellaneousCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		paredit_test_miscellaneous(self.view, edit)

class Paredit_run_testsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		window = sublime.active_window()
		view = window.new_file()

		commands = [
			"paredit_test_insertion"
		,	"paredit_test_deleting_killing"
		,	"paredit_test_movement_navigation"
		,	"paredit_test_depth_changing"
		,	"paredit_test_barfage_slurpage"
		,	"paredit_test_miscellaneous"
		]

		view.run_command("set_file_type", {"syntax": "Packages/Clojure/Clojure.tmLanguage"})
		write(view, edit, "Running tests\n")

		for command in commands:
			view.run_command(command)
