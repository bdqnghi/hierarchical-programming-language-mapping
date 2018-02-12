import os
import codecs
import numpy as np
from xml_util import parse_tree
from xml_util import get_parent_map
from xml_util import iterate_recursive
from xml_util import get_package_name_of_node
from util import process_srcml_source_code
CURRENT_DIR = os.getcwd()
STUPID_URL = "{http://www.srcML.org/srcML/src}"
projects = ["antlr","cordova","datastax","factual","fpml","log4j","spring","lucene","uap","zeromq","aws","mongodb"]


def get_class_node_cs(root):
	class_node = None
	for elem in root.getchildren():
		tag = elem.tag.replace(STUPID_URL,"")
		if tag == "namespace":
			for elem2 in elem.getchildren():
				tag2 = elem2.tag.replace(STUPID_URL,"")
				if tag2 == "block":
					for elem3 in elem2.getchildren():
						tag3 = elem3.tag.replace(STUPID_URL,"")
						if tag3 == "class":
							class_node = elem3
	return class_node


def get_class_node_java(root):
	class_node = None
	for elem in root.getchildren():
		tag = elem.tag.replace(STUPID_URL,"")
		if tag == "class":
			class_node = elem
	return class_node


for project in projects:
	cs_paths = list()
	java_paths = list()
	for r,ds,files in os.walk(os.path.join(CURRENT_DIR,"SRCML_DATA",project)):
		for file in files:
			file_path = os.path.join(r,file)
			split = file_path.split("/")
			if split[7] == "cs":
				cs_paths.append(file_path)
			if split[7] == "java":
				java_paths.append(file_path)


	for cs_path in cs_paths:
	
		for java_path in java_paths:

			cs_splits = cs_path.split("/")
			java_splits = java_path.split("/")
			cs_file = cs_splits[8]
			java_file = java_splits[8]
			if cs_file.split(".")[0] == java_file.split(".")[0]:
				print "###################"
				print cs_file
				try: 
					cs_tree = parse_tree(cs_path)
					cs_parent_map = get_parent_map(cs_tree)
					cs_tree_str = ""
					cs_root  = cs_tree.getroot()

					java_tree = parse_tree(java_path)
					java_parent_map = get_parent_map(java_tree)
					java_tree_str = ""
					java_root  = java_tree.getroot()

					cs_class_node = get_class_node_cs(cs_root)
					java_class_node = get_class_node_java(java_root)
					
					biggest_block_cs = None
					biggest_block_java = None

					for c in cs_class_node.getchildren():
						tag = c.tag.replace(STUPID_URL,"")
						if tag == "block":
							biggest_block_cs = c
					for j in java_class_node.getchildren():
						tag = j.tag.replace(STUPID_URL,"")
						if tag == "block":
							biggest_block_java = j

					for block_cs_node in biggest_block_cs.getchildren():
						tag = block_cs_node.tag.replace(STUPID_URL,"")
						if tag == "function":
							for node in block_cs_node:
								cs_tree_str = ""
								tag1 = node.tag.replace(STUPID_URL,"")
								if tag1 == "name":
									cs_function_name_origin = node.text
									cs_function_name = node.text.lower()
								
									for block_java_node in biggest_block_java.getchildren():
										tag2 = block_java_node.tag.replace(STUPID_URL,"")
										if tag2 == "function":
											for node2 in block_java_node:
												java_tree_str = ""
												tag3 = node2.tag.replace(STUPID_URL,"")
												if tag3 == "name":
													java_function_name_origin = node2.text
													java_function_name = node2.text.lower()
													
													if cs_function_name == java_function_name:
														print "&&&&&&&&"
														print "cs name : " + cs_function_name
														print "java name : " + java_function_name

														package_name_cs = get_package_name_of_node(cs_root,"cs",cs_tree_str) + "." + cs_function_name_origin
														processed_cs_code = iterate_recursive(block_cs_node,cs_tree_str,cs_parent_map)
														processed_cs_code = process_srcml_source_code(processed_cs_code)
														print processed_cs_code
														print "--"
														package_name_java = get_package_name_of_node(java_root,"java",java_tree_str) + "." + java_function_name_origin
														processed_java_code = iterate_recursive(block_java_node,java_tree_str,java_parent_map)
														processed_java_code = process_srcml_source_code(processed_java_code)
														print processed_java_code


														divide_1 = float(len(processed_cs_code))/float(len(processed_java_code))
														divide_2 = float(len(processed_java_code))/float(len(processed_cs_code))

														
														if (divide_1 > 0.8 and divide_1 < 1) or (divide_2 > 0.8 and divide_2 < 1):
															print "Because cs/java = " + str(divide_1) + " and java/cs = " + str(divide_2)
															line = project + "," + cs_file.split(".")[0] + "," + package_name_cs + "," + processed_cs_code + "," + package_name_java + "," + processed_java_code
															with open("./evaluation_data/functions/functions_" + project + "_4" + ".csv","a") as out:
																out.write(line + "\n")

															# with open("./sentences/sentences_function_cs_2.csv","a") as out:
															# 	out.write(processed_cs_code + "\n")
															# with open("./sentences/sentences_function_java_2.csv","a") as out:
															# 	out.write(processed_java_code + "\n")
				except Exception as e:
					print e

