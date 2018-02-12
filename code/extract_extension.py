import os
import shutil

CURRENT_DIR = os.getcwd()

dir_list = os.walk("./IEICE-projects").next()[1]

for dir in dir_list:
	dir_path = os.path.join(CURRENT_DIR,"IEICE-projects",dir)

	processed_dir_path = os.path.join(CURRENT_DIR,"PROCESSED_DATA",dir)
	if not os.path.exists(processed_dir_path):
		os.makedirs(processed_dir_path)

	processed_cs_path = os.path.join(processed_dir_path,"cs")
	if not os.path.exists(processed_cs_path):
		os.makedirs(processed_cs_path)

	processed_java_path = os.path.join(processed_dir_path,"java")
	if not os.path.exists(processed_java_path):
		os.makedirs(processed_java_path)

	for r,ds,files in os.walk(dir_path):
		for file in files:
			file_path = os.path.join(r,file)
			if file.endswith(".cs"):
				shutil.copy(os.path.realpath(file_path),processed_cs_path)
			if file.endswith(".java"):
				shutil.copy(os.path.realpath(file_path),processed_java_path)

