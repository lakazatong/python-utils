from .os import try_import

from typing import List, Tuple
os = try_import("os")
re = try_import("re")

from .print import cprint

def read_file(path, mode='r'):
	r = None
	if os.path.exists(path):
		try:
			with open(path, mode) as f:
				r = f.read()
		except:
			cprint('read_file: failed tp read '+path, 'red')
	return r

def count_files_in_dir(directory, check_if_file=True):
	count = 0
	if check_if_file:
		for path in os.scandir(directory):
			if os.path.is_file():
				count += 1
	else:
		for path in os.scandir(directory):
			count += 1
	return count

def get_matches(path: str, pattern: re.Pattern, preprocess_function=None, *args) -> List[Tuple[str, str]]:
	content = ''
	with open(path, 'r') as f:
		content = f.read()
	if preprocess_function:
		content = preprocess_function(content, *args)
	return re.findall(pattern, content)

def ask(body_msg: str, continue_msg: str = 'do you want to continue nonetheless? (y or n)\n',
		accept_inputs: List[str] = ['y'], refuse_input: List[str] = ['n'], exit_code: int = 0):
	print(body_msg, end='')
	tmp = input(continue_msg)
	while not tmp in accept_inputs:
		if tmp in refuse_input:
			exit(exit_code)
		tmp = input(continue_msg)
