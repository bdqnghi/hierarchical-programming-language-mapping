import os
import codecs
import numpy as np
from xml_util import parse_tree
from xml_util import get_parent_map
from xml_util import iterate_recursive
from util import process_srcml_source_code
from xml_util import iterate_to_get_node_with_type
from xml_util import iterate_to_get_node_with_types

CURRENT_DIR = os.getcwd()
STUPID_URL = "{http://www.srcML.org/srcML/src}"
projects = ["antlr","cordova","datastax","factual","fpml","log4j","spring","lucene","uap","zeromq","aws","mongodb"]

types_cs= ["if","foreach","while","for","do","break","continue","label","return","switch","case","default","assert","expr_stmt","decl_stmt","function_decl"]
types_java= ["if","while","for","do","break","continue","label","return","switch","case","default","assert","expr_stmt","decl_stmt","function_decl"]
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
				# print cs_file
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

					stmt_temp_1 = list()
					stmt_nodes_cs = iterate_to_get_node_with_types(biggest_block_cs,types_cs,stmt_temp_1)

					stmt_temp_2 = list()
					stmt_nodes_java = iterate_to_get_node_with_types(biggest_block_java,types_java,stmt_temp_2)


					print len(stmt_nodes_cs)
					print len(stmt_nodes_java)
					for cs_node in stmt_nodes_cs:
						processed_cs_code = iterate_recursive(cs_node,cs_tree_str,cs_parent_map)
						processed_cs_code = process_srcml_source_code(processed_cs_code)
						line_cs = project + "," + cs_file + "," + processed_cs_code
						with open("./evaluation_data/statements/statements_cs_" + project + "_1.csv","a") as out:
							out.write(line_cs + "\n")

					for java_node in stmt_nodes_java:
						processed_java_code = iterate_recursive(java_node,java_tree_str,java_parent_map)						
						processed_java_code = process_srcml_source_code(processed_java_code)	
						line_java = project + "," + java_file + "," + processed_java_code
						with open("./evaluation_data/statements/statements_java_" + project + "_1.csv","a") as out:
							out.write(line_java + "\n")
				except Exception as e:
					print e

nodes_origin = list()
cs_root  = cs_tree.getroot()

print cs_root
nodes_return = iterate_to_get_node_with_type(cs_root,"expr",nodes_origin)

