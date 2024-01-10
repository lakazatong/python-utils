from .os import try_import

tempfile = try_import("tempfile")

tmp_folder_path = tempfile.gettempdir()
python_utils_tmp_folder_path = tmp_folder_path+'/python_utils'	