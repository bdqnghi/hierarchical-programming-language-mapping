import os
import re
import string
import codecs
import concurrent.futures
from util import process_source_code
from util import process_srcml_source_code
from util import process_source_code_with_remove_line_break
from util import stripcomments
CURRENT_DIR = os.getcwd()


def pre_process(file_path):
	with codecs.open(file_path,"r",encoding="utf-8", errors="ignore") as f:
		data = f.read()
	try:
		data = str(data)
		data = process_source_code_with_remove_line_break(data)
	
	except Exception as e:
		print("error : " + str(e))

	# print(data)

	
	os.remove(file_path)
	with codecs.open(file_path,"a",encoding="utf-8", errors="ignore") as f2:
		f2.write(data)

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
	for r,ds,files in os.walk(os.path.join(CURRENT_DIR,"DATA_NO_PROCESSED")):
		for file in files:
			file_path = os.path.join(r,file)
			print(file_path)
			# with codecs.open(file_path,"r",encoding="utf-8", errors="ignore") as f:
			# 	data = f.read()
			# data = str(data)
			
			future = executor.submit(pre_process,file_path)
			

