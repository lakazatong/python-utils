from .os import try_import

BeautifulSoup = try_import("BeautifulSoup", _from="bs4")
json = try_import("json")
inspect = try_import("inspect")
pprint = try_import("pprint")
re = try_import("re")
time = try_import("time")
sys = try_import("sys")
colorsys = try_import("colorsys")
#try_import("zlib")

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

with "many lines" rainbow'ing for 2s, after what some other
bullshit will be printed
'''
default_rainbow_keyword = "rainbow"
default_rainbow_pattern = re.compile(rf'{default_rainbow_keyword}\((.*?)\)')
def print_rainbow(buffer, t, keyword=default_rainbow_keyword, smoothness=0.005, speed=0.01):
	r, g, b = 0, 0, 0
	pattern = re.compile(rf'{keyword}\((.*?)\)') if keyword != default_rainbow_keyword else default_rainbow_pattern
	last_line_len = len(buffer.split("\n")[-1])
	nb_newlines = buffer.count('\n') + 1
	st = time.time()
	hue = 0.0
	while True:
		modified_buffer = re.sub(pattern, rf'\033[38;2;{r};{g};{b}m\1\033[0m', buffer)
		if time.time() - st > t:
			break
		modified_buffer += f"\033[{last_line_len}D\033[{nb_newlines}A"
		sys.stdout.write(modified_buffer + "\n")
		sys.stdout.flush()
		r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
		hue +=smoothness
		time.sleep(speed)
		if hue >= 1.0: hue = 0.0
	print(modified_buffer)

# somewhat merge cprint and print_rainbow? im not sure

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
