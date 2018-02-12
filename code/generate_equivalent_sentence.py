import gensim
import os
import codecs
from sklearn.manifold import TSNE
from gensim.models.keyedvectors import KeyedVectors
import numpy as np


CURRENT_DIR = os.getcwd()

projects = ["antlr","cordova","datastax","factual","fpml","log4j","spring","lucene","uap","zeromq"]

for project in projects:
	cs_paths = list()
	java_paths = list()
	for r,ds,files in os.walk(os.path.join(CURRENT_DIR,"SRCML_PROCESSED_DATA_VER_2",project)):
		for file in files:
			file_path = os.path.join(r,file)
			if file.endswith(".cs"):
				cs_paths.append(file_path)
			if file.endswith(".java"):
				java_paths.append(file_path)


	for cs_path in cs_paths:
		for java_path in java_paths:
			cs_splits = cs_path.split("/")
			java_splits = java_path.split("/")
			cs_file = cs_splits[8]
			java_file = java_splits[8]
			if cs_file.split(".")[0] == java_file.split(".")[0]:
				with open(cs_path,"r") as cs_f:
					cs_data = cs_f.read()
				with open(java_path,"r") as java_f:
					java_data = java_f.read()

				with open(os.path.join(CURRENT_DIR,"sentences","sentences_cs_new.txt"),"a") as f:
					f.write(str(cs_data) + "\n")
				with open(os.path.join(CURRENT_DIR,"sentences","sentences_java_new.txt"),"a") as f:
					f.write(str(java_data) + "\n")
				