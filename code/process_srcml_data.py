from xml_util import iterate_recursive
import xml.etree.ElementTree as ET

from xml_util import get_parent_map
from xml_util import find_name_space
from xml_util import parse_tree
from xml_util import find_block
from util import process_srcml_source_code
import os
import re
import string
import codecs
import concurrent.futures


CURRENT_DIR = os.getcwd()
STUPID_URL = "{http://www.srcML.org/srcML/src}"


def pre_process(file_path):

	

	split = file_path.split("/")
	try:
		tree = parse_tree(file_path)
		file_type = 0
		if split[7] == "cs":
			file_type = 1

		parent_map = get_parent_map(tree)
		tree_str = ""
		root  = tree.getroot()
		# C#
		# if file_type == 1:

			
		# 	namespace = find_name_space(root)
		# 	biggest_block = find_block(namespace)
		# 	processed_code =  iterate_recursive(biggest_block,tree_str,parent_map)

		# # Java
		# else:
		processed_code = iterate_recursive(root,tree_str,parent_map)
		processed_code = process_srcml_source_code(processed_code)
		# print(processed_code)
		srcml_data_path = os.path.join(CURRENT_DIR,"SRCML_PROCESSED_DATA_SPLIT_CAMEL_ALL_V3",split[6],split[7])
		if not os.path.exists(srcml_data_path):
			os.makedirs(srcml_data_path)
		
		new_path = os.path.join(CURRENT_DIR,"SRCML_PROCESSED_DATA_SPLIT_CAMEL_ALL_V3",split[6],split[7],split[8])

		with codecs.open(new_path,"a",encoding="utf-8", errors="ignore") as f2:
			f2.write(processed_code)

	except Exception as e:
		print(e)
	

with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
	for r,ds,files in os.walk(os.path.join(CURRENT_DIR,"SRCML_DATA")):
		for file in files:
			if file.endswith(".xml"):
				file_path = os.path.join(r,file)
				print(file_path)
				# with codecs.open(file_path,"r",encoding="utf-8", errors="ignore") as f:
				# 	data = f.read()
				# data = str(data)
				pre_process(file_path)
				# future = executor.submit(pre_process,file_path)
