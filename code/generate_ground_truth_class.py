import os
import codecs
import numpy as np
from xml_util import parse_tree
from xml_util import get_parent_map
from xml_util import iterate_recursive
# from xml_util import get_package_name_of_node
from util import process_srcml_source_code
from xml_util import transform_source_code
from xml_util import get_necessary_information_to_process_source_code
from xml_util import iterate_function_node_to_get_text
from xml_util import iterate_to_get_node_with_type
from xml_util import find_biggest_block
from xml_util import get_information_of_decl_stmts
from util import remove_empty_intext
from xml_util import get_global_part_of_root

CURRENT_DIR = os.getcwd()
STUPID_URL = "{http://www.srcML.org/srcML/src}"
# projects = ["antlr","cordova","datastax","factual","fpml","log4j","spring","lucene","uap","zeromq","aws","mongodb"]

projects = ["antlr","cordova","datastax","factual","fpml","log4j","spring","lucene","uap","zeromq","itext","jgit","poi","jts","db4o","mongodb"]
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
			if len(cs_file.split(".")) == 2 and len(java_file.split(".")) == 2:
				if cs_file.split(".")[0] == java_file.split(".")[0]:
				
					try: 
						_, _, cs_package_object_mapping, _, cs_third_party_package_object_mapping_list, _ = get_necessary_information_to_process_source_code(cs_path, "cs", project)

						_, _, java_package_object_mapping, _, java_third_party_package_object_mapping_list, _ = get_necessary_information_to_process_source_code(java_path, "java", project)
						
						cs_tree = parse_tree(cs_path)
						cs_parent_map = get_parent_map(cs_tree)
						cs_tree_str = ""
						cs_root  = cs_tree.getroot()

						java_tree = parse_tree(java_path)
						java_parent_map = get_parent_map(java_tree)
						java_tree_str = ""
						java_root  = java_tree.getroot()
						
						processed_cs_code = get_global_part_of_root(cs_root, "cs", cs_package_object_mapping, cs_third_party_package_object_mapping_list)
						processed_cs_code = processed_cs_code.replace("@","").replace("{","").replace("}","")
						processed_cs_code = remove_empty_intext(processed_cs_code)
						
						processed_java_code = get_global_part_of_root(java_root, "java", java_package_object_mapping, java_third_party_package_object_mapping_list)
						processed_java_code = processed_java_code.replace("@","").replace("{","").replace("}","")
						processed_java_code = remove_empty_intext(processed_java_code)

						divide_1 = float(len(processed_cs_code))/float(len(processed_java_code))
						divide_2 = float(len(processed_java_code))/float(len(processed_cs_code))

						
						if (divide_1 > 0.6 and divide_1 < 1) or (divide_2 > 0.6 and divide_2 < 1):
							print "Because cs/java = " + str(divide_1) + " and java/cs = " + str(divide_2)
							# line = project + "," + cs_file.split(".")[0] + "," + package_name_cs + "," + processed_cs_code + "," + package_name_java + "," + processed_java_code
							# with open("./evaluation_data/functions/functions_" + project + "_new" + ".csv","a") as out:
							# 	out.write(line + "\n")

							with open("./sentences/sentences_global_cs_new.csv","a") as out:
								out.write(processed_cs_code + "\n")
							with open("./sentences/sentences_global_java_new.csv","a") as out:
								out.write(processed_java_code + "\n")
					except Exception as e:
						print e

