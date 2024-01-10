from .os import try_import

# List = try_import("List", _from="typing")
# Union = try_import("Union", _from="typing")
# from typing import List
# from typing import Union

def is_power_of_two(number):
	return number & (number - 1) == 0 and number != 0

# def divide(n:int, nb:int) -> List[Union[int, int]]:
def divide(n:int, nb:int):
	quotient = n // nb
	remainder = n % nb
	start_indices = [i * quotient + min(i, remainder) for i in range(nb)]
	end_indices = [(i + 1) * quotient + min(i + 1, remainder) - 1 for i in range(nb)]
	return [(start_indices[i], end_indices[i]+1) for i in range(nb)]
