import os
import codecs
import numpy as np
from xml_util import parse_tree
from xml_util import get_parent_map
from xml_util import iterate_to_get_node_with_type
from xml_util import get_package_name_of_file
from xml_util import get_class_node_cs
from xml_util import get_parameter_type_of_method

CURRENT_DIR = os.getcwd()

STUPID_URL = "{http://www.srcML.org/srcML/src}"

# lang = "cs"
projects = ["antlr","aws","cordova","datastax","factual","fpml","log4j","spring","lucene","uap","zeromq","itext","jgit","poi","jts","db4o"]
# projects = ["itext","jgit","poi","jts","db4o"]
# projects = ["mongodb"]
# projects = ["aws"]
for project in projects:
	cs_signatures = list()
	java_signatures = list()
	for r,ds,files in os.walk(os.path.join(CURRENT_DIR,"PROJECT_DATA_RAW",project)):
		for file in files:
		
			file_path = os.path.join(r, file)
			print "Parsing file : " + file_path + " --------------------------"
			if file.endswith(".cs") and file != "Stylesheet.cs":
				
				command = "srcml " + file_path + " > Temp.xml"
				os.system(command)
				try: 
					try:
						tree = parse_tree("Temp.xml")
						root  = tree.getroot()
						parent_map = get_parent_map(tree)
						
					except Exception as e:
						print "Error in this block : " + str(e)
					decorations = ["class","interface"]
					for decoration in decorations:
						cs_class_nodes = list()
						cs_class_nodes = iterate_to_get_node_with_type(root,decoration,cs_class_nodes)

						biggest_block_cs = None
						class_name = None
					
						if len(cs_class_nodes) != 0:
							for c in cs_class_nodes[0].getchildren():
								tag = c.tag.replace(STUPID_URL,"")
								if tag == "block":
									biggest_block_cs = c
								if tag == "name":
									if c.text != None:
										class_name = c.text
									else:
										for c2 in c.getchildren():
											tag2 = c2.tag.replace(STUPID_URL,"")
											if tag2 == "name":
												class_name = c2.text


							package_nodes = list()
							package_nodes = iterate_to_get_node_with_type(root,"namespace",package_nodes)
							package_name = ""
							package_name = get_package_name_of_file(root,"cs",package_name)
							functions = list()

							if decoration == "class":
								tag_type = "function"
							if decoration == "interface":
								tag_type = "function_decl"

							functions = iterate_to_get_node_with_type(biggest_block_cs,tag_type,functions)

							for function in functions:
								for elem in function.getchildren():
									child_tag = elem.tag.replace(STUPID_URL,"")
									if child_tag == "name":
										parameters = get_parameter_type_of_method(function)

										parameter_tostr = ""
										if len(parameters) != 0:
											parameters = [x for x in parameters if x != None]
											parameter_tostr = ",".join(parameters)
										if package_name != None and package_name != "" and class_name != None and elem.text != None:	
											full_signature = package_name + "." + class_name + "." + elem.text + "(" + parameter_tostr + ")"
											print full_signature
											cs_signatures.append(full_signature)

				except Exception as e:
					print "Error " + str(e) + "on file : " + file_path

			if file.endswith(".java"):

				
				command = "srcml " + file_path + " > Temp.xml"
				os.system(command)
				try:
					tree = parse_tree("Temp.xml")
					root  = tree.getroot()
					parent_map = get_parent_map(tree)

					decorations = ["class","interface"]
					for decoration in decorations:
						java_class_nodes = list()
						java_class_nodes = iterate_to_get_node_with_type(root,decoration,java_class_nodes)

						biggest_block_java = None
						class_name = None
						if len(java_class_nodes) != 0:
							# print java_class_nodes[0].text
							for c in java_class_nodes[0].getchildren():
								tag = c.tag.replace(STUPID_URL,"")
								if tag == "block":
									biggest_block_java = c
								if tag == "name":
									if c.text != None:
										class_name = c.text
									else:
										for c2 in c.getchildren():
											tag2 = c2.tag.replace(STUPID_URL,"")
											if tag2 == "name":
												class_name = c2.text

							package_nodes = list()
							package_nodes = iterate_to_get_node_with_type(root,"package",package_nodes)
							package_name = ""
							package_name = get_package_name_of_file(root,"java",package_name)
							functions = list()
							if decoration == "class":
								tag_type = "function"
							if decoration == "interface":
								tag_type = "function_decl"
							functions = iterate_to_get_node_with_type(biggest_block_java,tag_type,functions)
							for function in functions:
								for elem in function.getchildren():
									child_tag = elem.tag.replace(STUPID_URL,"")
									if child_tag == "name":
										parameters = get_parameter_type_of_method(function)

										parameter_tostr = ""
										if len(parameters) != 0:
											parameters = [x for x in parameters if x != None]
											parameter_tostr = ",".join(parameters)
										if package_name != None and package_name != "" and class_name != None and elem.text != None:	
											full_signature = package_name + "." + class_name + "." + elem.text + "(" + parameter_tostr + ")"
											print full_signature
											java_signatures.append(full_signature)
						
				except Exception as e:
					print "Error " + str(e) + " on file : " + file_path

	signature_path = "./SIGNATURE_DATA/" + project
	print cs_signatures
	if not os.path.exists(signature_path):
		os.makedirs(signature_path)

	for cs_signature in set(cs_signatures):
		with open(signature_path + "/signature_cs.txt","a") as f:
			f.write(cs_signature + "\n")

	for java_signature in set(java_signatures):
		with open(signature_path + "/signature_java.txt","a") as f:
			f.write(java_signature + "\n")

