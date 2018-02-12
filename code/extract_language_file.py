
import os
import codecs
import shutil
import numpy as np



CURRENT_DIR = os.getcwd()

projects = ["itext","jgit","poi","jts","db4o"]
# projects = ["google-api"]
# projects = ["antlr"]

NEW_FOLDER = "PROCESSED_DATA_BACKUP_ORIGINAL"
for project in projects:
	new_project_path = os.path.join(CURRENT_DIR,NEW_FOLDER,project)
	for r,ds,files in os.walk(os.path.join(CURRENT_DIR,"PROJECT_DATA_RAW",project)):
		for file in files:
			file_path = os.path.join(r,file)

			if file.endswith(".cs"):
				new_path_directory = os.path.join(new_project_path,"cs")
				if not os.path.exists(new_path_directory):
					os.makedirs(new_path_directory)
				new_file_path = os.path.join(new_path_directory,file)
				shutil.copy2(file_path,new_file_path)

			if file.endswith(".java"):
				new_path_directory = os.path.join(new_project_path,"java")
				if not os.path.exists(new_path_directory):
					os.makedirs(new_path_directory)
				new_file_path = os.path.join(new_path_directory,file)
				shutil.copy2(file_path,new_file_path)
			# if file.endswith(".java"):
			# 	java_paths.append(file_path)
			# 	num_java +=1