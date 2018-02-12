import gensim
import os
import codecs
from sklearn.manifold import TSNE
from gensim.models.keyedvectors import KeyedVectors
import numpy as np
import csv
from sklearn.metrics.pairwise import cosine_similarity
from util import vector_averaging
from util import vector_averaging_with_tfidf
from util import process_source_code
from util import process_diff_srcml

from util import process_diff_srcml2
from util import word2weight
import sys

csv.field_size_limit(sys.maxsize)
cs_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/cs_vectors_3.txt",binary=False)
java_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/java_vectors_3.txt",binary=False)

with open("sentences_cs.txt","r") as cs_f:
	cs_data = cs_f.readlines()
with open("sentences_java.txt","r") as java_f:
	java_data = java_f.readlines()

cs_sentences = [x for x in cs_data]
java_sentences = [x for x in java_data]

cs_word2weight = word2weight(cs_sentences)
java_word2weight = word2weight(java_sentences)
# print cs_word2weight
# Predicting part ----------------------------------------------
# print(cosine_similarity(cs_vectors["while"].reshape(1,-1),java_vectors["class"].reshape(1,-1))

with codecs.open("./codelabel/codelabel_lucene.csv","r") as f_csv:
	reader = csv.reader(f_csv)

	for i,row in enumerate(reader):
		print("###############################")
		# if i == 40:
		print("id : " + row[1])

		# C#
		# diff_1 = process_diff_srcml(row[3],0)
		# diff_1 = process_source_code(row[3],0)
		diff_1 = process_diff_srcml2(row[3])
		# Java
		# diff_2 = process_diff_srcml(row[5],1)
		# diff_2 = process_source_code(row[5],0)
		diff_2 = process_diff_srcml2(row[5])
		print("diff 1 : " + diff_1)
		print("diff 2 : " + diff_2)
		# if i > 0 and i != 40:
		# 	diff_cs_list.append(process_source_code(row[5]))
		
		predict_average = cosine_similarity(vector_averaging(diff_1.split(" "),cs_vectors),vector_averaging(diff_2.split(" "),java_vectors))[0][0]
		predict_average_tfidf = cosine_similarity(vector_averaging_with_tfidf(diff_1.split(" "),cs_vectors,cs_word2weight),vector_averaging_with_tfidf(diff_2.split(" "),java_vectors,java_word2weight))[0][0]
		# predict = doc2vec_model.docvecs.similarity_unseen_docs(doc2vec_model,diff_1.split(" "),diff_2.split(" "))
		print(predict_average)
		print(predict_average_tfidf)
		print(row[7])
		new_row = list()
		new_row.append(row[0])
		new_row.append(row[1])
		new_row.append(row[7])
		new_row.append(row[8])
		new_row.append(row[9])
		new_row.append(str(predict_average))
		new_row.append(str(predict_average_tfidf))
		with open("./codelabel_result/bi2vec_lucene_3.csv","a") as f:
			f.write(",".join(new_row) + "\n")

