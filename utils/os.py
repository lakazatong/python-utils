# source: ChatGPT
def run_import(_import, _from, _as):
	if _as:
		if _from:
			globals()[_as] = __import__(_import, fromlist=[_from])
		else:
			globals()[_as] = __import__(_import)
		return globals()[_as]
	else:
		if _from:
			globals()[_import] = __import__(_import, fromlist=[_from])
		else:
			globals()[_import] = __import__(_import)
		return globals()[_import]

def try_import(_import, _from=None, _as=None, verbose=True, critical=False):
	prefix = f"\033[33mpython_utils: "
	if not _import:
		print(f"{prefix}can't import nothing\033[0m")
		if critical: exit(1)
		return None
	_from_txt = f"from {_from} " if _from else ""
	_as_txt = f" as {_as}" if _as else ""
	_code_txt = f"{_from_txt}import {_import}{_as_txt}"

	try:
		_import_type = type(_import)
		if _import_type is str:
			return run_import(_import, _from, _as)
		# elif _import_type is list:
		# 	if _as:
		# 		print(f"{prefix}`{_code_txt}` is not valid python\033[0m")
		# 		if critical: exit(1)
		# 	# assumes a list of str
		# 	for __import in _import: run_import(__import, _from, _as)
		else:
			print(f"{prefix}unsupported type {_import_type}\033[0m")
			if critical: exit(1)
			return None
	except:
		if verbose: print(f"{prefix}`{_code_txt}` failed\033[0m")
		if critical: exit(1)
		return None

os = try_import("os")
threading = try_import("threading")
platform = try_import("platform")
io = try_import("io")
sys = try_import("sys")
asyncio = try_import("asyncio")
time = try_import("time")

def from_windows():
	return platform.system() == 'Windows'

def split_path(path):
	return os.path.split(path)

def run(func, delay):
	timer = threading.Timer(delay, func)
	timer.start()
	return timer

# source: ChatGPT
# returns what func printed to the console if it did, otherwise its return value
def capture_console_output(func, *args):
	output_buffer = io.StringIO()
	original_stdout = sys.stdout
	try:
		sys.stdout = output_buffer
		return_value = func(*args)
	finally:
		sys.stdout = original_stdout
	captured_output = output_buffer.getvalue()
	output_buffer.close()
	if captured_output:
		return captured_output
	else:
		return return_value

async def check_loop(check_func, timeout, *args):
	wait = 0
	while wait < timeout:
		# consider check_func to run almost instantly
		r = await check_func(*args)
		if r: return True
		await asyncio.sleep(1)
		wait += 1
	return False

class TimeIt:
	_ = 0
	measure_time = 0

	def compute_measure_time(self):
		n = 100000
		for _ in range(n):
			st = time.time()
			tmp = time.time()
			self._ += time.time() - tmp
			self._ += 1
			self.measure_time += time.time() - st
		self.measure_time /= n

	def __init__(self):
		self.time = 0
		self.measured = 0
		self.compute_measure_time()

	def timeit(self, func, *args):
		st = time.time()
		r = func(*args)
		self.time += time.time() - st
		self.measured += 1
		return r

	def time_spent_measuring(self):
		return self.measure_time * self.measured

	def time_spent_waiting(self):
		return self.time - self.time_spent_measuring()
