from .os import try_import

BeautifulSoup = try_import("BeautifulSoup", _from="bs4")
json = try_import("json")
inspect = try_import("inspect")
pprint = try_import("pprint")
re = try_import("re")
time = try_import("time")
sys = try_import("sys")
colorsys = try_import("colorsys")
signal = try_import("signal")
math = try_import("math")
shutil = try_import("shutil")
threading = try_import("threading")
# zlib = try_import("zlib")

BLACK, RED, GREEN, YELLOW, BLUE, PURPLE, CYAN, WHITE = 30, 31, 32, 33, 34, 35, 36, 37
color_codes = {
	'black': BLACK,
	'red': RED,
	'green': GREEN,
	'yellow': YELLOW,
	'blue': BLUE,
	'purple': PURPLE,
	'cyan': CYAN,
	'white': WHITE
}
available_color_codes = list(color_codes.keys())
# make it work for windows?
def cprint(string, color=37, end='\n', bold=False, italic=False):
	if type(color) is str: color = color_codes.get(color.lower())
	bold_txt = '\033[1m' if bold else ''
	italic_txt = '\033[3m' if italic else ''
	if color in color_codes.values():
		print(f"{bold_txt}{italic_txt}\033[{color}m{string}\033[0m", end=end)
	else:
		print(f'cprint: Unknown color ({color}), available colors are: {available_color_codes}\n')

# example use :
'''
buffer = """a very long tet
with arainbow(many lines)a
yolo"""

print("bulls\nshit")
print_rainbow(buffer, 2)
print("some other\nbullshit")

will print:
bulls
shit
a very long tet
with amany linesa
yolo
some other
bullshit

with 'many lines' rainbow'ing for 2s, after which 'some other
bullshit' will be printed
'''

default_rainbow_keyword = "rainbow"
default_rainbow_pattern = re.compile(rf'{default_rainbow_keyword}\(((?:[^a]|a)*?)\)')
def rainbow_print(	buffer, rainbow_time,
					keyword = default_rainbow_keyword,
					smoothness = 0.005, speed = 0.01,
					static = True, wooble = None, scrolling = None):
	r, g, b = 0, 0, 0
	pattern = re.compile(rf'{keyword}\((.*?)\)') if keyword != default_rainbow_keyword else default_rainbow_pattern
	last_line_len = len(buffer.split("\n")[-1])
	nb_newlines = buffer.count('\n') + 1
	st = time.time()
	hue = 0.0

	addon = '\n' if static else '\n\n'
	
	wooble_start, wooble_delta, wooble_max = 0, 0.5, 8
	if wooble != None:
		try:
			if 'wooble_start' in wooble: wooble_start = float(wooble['wooble_start'])
			if 'wooble_delta' in wooble: wooble_delta = float(wooble['wooble_delta'])
			if 'wooble_max' in wooble: wooble_max = float(wooble['wooble_max'])
		except Exception as e:
			cprint('rainbow_print: all wooble parameters must be numbers', RED)
			return
	wooble_count = wooble_start

	wooble_lines = []
	for _ in range(len(buffer)):
		wooble_lines.append([])
	
	columns, lines = shutil.get_terminal_size()
	scrolling_start, scrolling_delta, scrolling_max, scrolling_wait = 0, 1, lines, 2
	scrolling_top_padding, scrolling_bottom_padding = 2, 2
	if scrolling != None:
		try:
			if 'scrolling_start' in scrolling: scrolling_start = float(scrolling['scrolling_start'])
			if 'scrolling_delta' in scrolling: scrolling_delta = float(scrolling['scrolling_delta'])
			if 'scrolling_max' in scrolling: scrolling_max = float(scrolling['scrolling_max'])
			if 'scrolling_wait' in scrolling: scrolling_wait = float(scrolling['scrolling_wait'])
			if 'scrolling_top_padding' in scrolling: scrolling_wait = float(scrolling['scrolling_top_padding'])
			if 'scrolling_bottom_padding' in scrolling: scrolling_wait = float(scrolling['scrolling_bottom_padding'])
		except Exception as e:
			cprint('rainbow_print: all scrolling parameters must be numbers', RED)
			return
		scrolling_max = scrolling_max - scrolling_top_padding - scrolling_bottom_padding
		nb_newlines = lines 
		last_line_len = columns

	scrolling_count = scrolling_start
	scrolling_time_remaining = 0

	def decrement_time_remaining():
		nonlocal scrolling_time_remaining
		while scrolling_time_remaining > 0:
			time.sleep(0.1)
			scrolling_time_remaining -= 0.1

	try:
		while True:
			modified_buffer = re.sub(pattern, rf'\033[38;2;{r};{g};{b}m\1\033[0m', buffer)
			if time.time() - st > rainbow_time:
				break

			cur_last_line_len = last_line_len

			if wooble:
				buffer_lines = modified_buffer.split('\n')
				for i in range(len(wooble_lines)):
					wooble_lines[i] = ' ' * math.floor(wooble_count)
					wooble_count += wooble_delta
					if wooble_count < 0:
						wooble_delta = - wooble_delta
						wooble_count = 0
					elif wooble_count >= wooble_max:
						wooble_delta = - wooble_delta
						wooble_count = wooble_max
				for i in range(len(buffer_lines)):
					buffer_lines[i] = wooble_lines[i] + buffer_lines[i]
				cur_last_line_len = len(buffer_lines[-1])
				modified_buffer = '\n'.join(buffer_lines)

			pos_c = 0
			neg_c = 0
			for _ in range(10000000):
				if scrolling:
					buffer_lines = modified_buffer.split('\n')
					n = len(buffer_lines) - scrolling_max
					if n > 0:
						if scrolling_time_remaining <= 0:
							scrolling_count += scrolling_delta
							if scrolling_delta > 0:
								pos_c += 1
								pos_c %= lines
							else:
								neg_c += 1
								neg_c %= lines
							if scrolling_count <= 0 or pos_c == neg_c:
								scrolling_delta = - scrolling_delta
								scrolling_count = 0
								# scrolling_time_remaining = scrolling_wait
								# threading.Thread(target=decrement_time_remaining, daemon=True).start()
							elif scrolling_count >= n:
								scrolling_delta = - scrolling_delta
								scrolling_count = n
								# scrolling_time_remaining = scrolling_wait
								# threading.Thread(target=decrement_time_remaining, daemon=True).start()
						tmp = math.floor(scrolling_count)
						buffer_lines = buffer_lines[0:0 + scrolling_max - 1]
						for _ in range(scrolling_bottom_padding):
							buffer_lines.insert(0, "")
						for _ in range(scrolling_top_padding):
							buffer_lines.append("")
						for i in range(len(buffer_lines) - 1):
							if len(buffer_lines[i]) < columns:
								buffer_lines[i] += ' ' * (columns - len(buffer_lines[i]) - 1) + '\n'
						buffer_lines[-1] += ' ' * (columns - len(buffer_lines[-1]))
						# modified_buffer = ''.join(buffer_lines)
						modified_buffer = ""
						for line in buffer_lines:
							modified_buffer += line
				print(modified_buffer + f"\033[{cur_last_line_len}D\033[{nb_newlines}A" + addon, end='')
				print(pos_c, neg_c)
				sys.stdout.flush()
				time.sleep(speed)
				input()
			exit(2)

			sys.stdout.write(modified_buffer + f"\033[{cur_last_line_len}D\033[{nb_newlines}A" + addon)

			sys.stdout.flush()
			r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
			hue += smoothness
			time.sleep(speed)
			if hue >= 1.0: hue = 0.0
	except KeyboardInterrupt:
		print(re.sub(pattern, rf'\033[38;2;{r};{g};{b}m\1\033[0m', buffer) + f"\033[{last_line_len}D\033[{nb_newlines}A")
	print(re.sub(pattern, rf'\033[38;2;{r};{g};{b}m\1\033[0m', buffer) + f"\033[{last_line_len}D\033[{nb_newlines}A")
	if nb_newlines > 1:
		print('\n' * nb_newlines)

# somewhat merge cprint and print_rainbow? im not sure

# v bullshit v

def report(message, color=WHITE, module=None):
	function_name = report.calling_function
	cprint(f"{module}: {function_name}: {message}" if module else f"{function_name}: {message}", color=color)

def ereport(message, module=None):
	report(message, RED, module)

def reportd(func):
	def wrapper(*args, **kwargs):
		report.calling_function = func.__name__
		return func(report=report, ereport=ereport, *args, **kwargs)
	return wrapper

# ^ bullshit ^

def print_var(var, indent=3, color=37):
	callers_local_vars = inspect.currentframe().f_back.f_locals.items()
	cprint(pprint.pformat(str([k for k, v in callers_local_vars if v is var][0])+' = '+str(var), indent=indent), color=color)
	print()

def _print_json(obj, indent, color):
	if type(obj) is str or type(obj) is bytes:
		try:
			obj = json.loads(obj)
		except:
			obj = str(obj)
			cprint(f'print_json: json.loads() failed loading the provided string or bytes ({obj})')
			return
	cprint(json.dumps(obj, indent=indent), color)

# accepts bytes, str, dict or list of them
def print_json(obj, indent=3, color=37):
	if type(obj) is list:
		if obj != []:
			for o in obj: _print_json(o, indent, color)
		else:
			cprint('[]', color=color)
	else:
		_print_json(obj, indent, color)

def print_all_attributes(obj, builtin=False, color=37):
	if builtin:
		for attr in dir(obj):
			value = getattr(obj, attr)
			cprint(f'{attr} = {value}\n\n', color)
	else:
		for attr in dir(obj):
			if not attr.startswith("__"):
				value = getattr(obj, attr)
				cprint(f'{attr} = {value}\n\n', color)

def print_all_items(obj, color=37):
	for key, value in obj.items():
		cprint(f'{key} = {value}\n\n', color)

def print_response(r, indent=3, color=37, content_color=37):
	if color != 37 and content_color == 37: content_color = color
	
	headers = {}
	for key, value in r.headers.items():
		headers[key] = value
	saved_response = {
		# "_content": r._content.decode('utf-8'),
		"_content_consumed": str(r._content_consumed),
		"_next": str(r._next),
		"status_code": str(r.status_code),
		"headers": headers,
		"url": str(r.url),
		"encoding": str(r.encoding),
		"history": str(r.history),
		"reason": str(r.reason),
		"elapsed": str(r.elapsed)
	}

	cprint(json.dumps(saved_response, indent=indent), color=color)
	if r._content != b'':
		# decode

		content_encoding = None
		content_encoding_in_headers = True
		if 'Content-Encoding' in headers: content_encoding = 'Content-Encoding'
		elif 'content-encoding' in headers: content_encoding = 'content-encoding'
		else: content_encoding_in_headers = False

		if content_encoding in headers:
			if 'gzip' in headers[content_encoding] or 'compress' in headers[content_encoding] or 'deflate' in headers[content_encoding]:
				# content = zlib.decompress(r._content) fails :c
				content = r._content.decode('utf-8', 'ignore')
			elif 'br' in headers[content_encoding]:
				# content = brotli.decompress(r._content) fails :c
				content = r._content.decode('utf-8', 'ignore')
		else:
			content = r._content.decode('utf-8', 'ignore')

		# format and print
		
		content_type = None
		content_type_in_headers = True
		if 'Content-Type' in headers: content_type = 'Content-Type'
		elif 'content-type' in headers: content_type = 'content-type'
		else: content_type_in_headers = False

		if content_type_in_headers:
			if 'text/plain' in headers[content_type]:
				cprint(content, color=content_color)
			elif 'text/html' in headers[content_type]:
				cprint(BeautifulSoup(content, 'html.parser').prettify(indent_width=indent), color=content_color)
			elif 'application/json' in headers[content_type]:
				cprint(json.dumps(json.loads(content), indent=indent), color=content_color)
			elif 'application/x-www-form-urlencoded' in headers[content_type]:
				cprint(decode_url(content), color=content_color)
		else:
			cprint(content, color=content_color)
