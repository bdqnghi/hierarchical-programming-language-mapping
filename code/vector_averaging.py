import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cosine
from util import process_diff
import csv
from util import split_source_to_sequences
import sys
import codecs
import gensim
csv.field_size_limit(sys.maxsize)

doc2vec_model = gensim.models.Doc2Vec.load("doc2vec")

def normalize(word_vec):
	norm = np.linalg.norm(word_vec)
	if norm == 0:
		return word_vec
	return word_vec/norm

with open("java2vec.txt", "rb") as lines:
	next(lines)
	java2vec = {line.split()[0]: np.array(map(float, line.split()[1:]))
		for line in lines}

with open("cs2vec.txt", "rb") as lines:
	next(lines)
	cs2vec = {line.split()[0]: np.array(map(float, line.split()[1:]))
		for line in lines}

with open("code2vec.txt", "rb") as lines:
	next(lines)
	code2vec = {line.split()[0]: np.array(map(float, line.split()[1:]))
		for line in lines}

with open("antlr_code2vec.txt", "rb") as lines:
	next(lines)
	antlr_code2vec = {line.split()[0]: np.array(map(float, line.split()[1:]))
		for line in lines}

def vector_averaging(sentence):
	mean = np.mean([normalize(code2vec[w]) for w in sentence if w in code2vec] or [np.zeros(100)],axis=0)
	return mean.reshape(1,-1)

def vector_averaging_java(sentence):
	mean = np.mean([normalize(java2vec[w]) for w in sentence if w in java2vec] or [np.zeros(100)],axis=0)
	return mean.reshape(1,-1)

def vector_averaging_cs(sentence):
	mean = np.mean([normalize(cs2vec[w]) for w in sentence if w in cs2vec] or [np.zeros(100)],axis=0)
	return mean.reshape(1,-1)
cs_sentence = "class"
java_temp_sent = "class"
java_sentence = "package org antlr analysis import org antlr tool Grammar import org antlr tool GrammarAST public class Action Label extends Label public GrammarAST actionAST public Action Label GrammarAST actionAST super ACTION this actionAST actionAST Override public boolean is Epsilon return true Override public boolean is Action return true Override public String to String return actionAST Override public String to String Grammar return to String"

vec_1 = vector_averaging_cs(cs_sentence.split(" "))
vec_2 = vector_averaging_java(java_temp_sent.split(" "))

# print vec_1
# print vec_2
cos = cosine_similarity(vec_1,vec_2)

# print cos

diff_cs_list = list()
def get_java_class_of_diff(data):
	for i,row in enumerate(data.splitlines()):
		if i == 0:
	
			split = row.split(" ")
			
			class_pos = 0
			for j,s in enumerate(split):
				if s == "class":
					class_pos = j
					break
		
			if class_pos != 0:
			
				for j,s2 in enumerate(split):
					if j == (class_pos + 1):
						
						return s2
			return None		

def get_cs_class_of_diff(data):
	for i,row in enumerate(data.splitlines()):
		if i == 0:
	
			split = row.split(" ")
			print split
			class_pos = 0
			for j,s in enumerate(split):
				if s == "class":
					class_pos = j
					break
		
			if class_pos != 0:
			
				for j,s2 in enumerate(split):
					if j == (class_pos + 1):
						
						return s2
			return None		


with codecs.open("codelabel_factual.csv","rb") as f_csv:
	reader = csv.reader(f_csv)

	y_true = list()
	y_predicted = list()
	for i,row in enumerate(reader):
		print "###############################"
		# if i == 40:
		print "id : " + row[1]
		diff_1 = process_diff(row[3])
		diff_2 = process_diff(row[5])

		print "diff 1 : " + diff_1
		print "diff 2 : " + diff_2
		# if i > 0 and i != 40:
		# 	diff_cs_list.append(process_source_code(row[5]))
		
		predict = cosine_similarity(vector_averaging(diff_1.split(" ")),vector_averaging(diff_2.split(" ")))[0][0]
		# predict = doc2vec_model.docvecs.similarity_unseen_docs(doc2vec_model,diff_1.split(" "),diff_2.split(" "))
		print predict
		print row[7]
		new_row = list()
		new_row.append(row[0])
		new_row.append(row[1])
		new_row.append(row[7])
		new_row.append(row[8])
		new_row.append(row[9])
		new_row.append(str(predict))
		with open("new_factual.csv","a") as f:
			f.write(",".join(new_row) + "\n")
		y_predicted.append(predict)
		y_true.append(row[7])
		
		# print get_java_class_of_diff(row[3])
		# print get_cs_class_of_diff(row[5])

# print y_true
# print y_predicted
# print diff_1

# print diff_2

# for diff in diff_cs_list:
# 	print cosine_similarity(vector_averaging(diff_1.split(" ")),vector_averaging(diff.split(" ")))
# print cosine_similarity(vector_averaging(diff_1.split(" ")),vector_averaging(diff_2.split(" ")))
exit()

with open("./PROCESSED_DATA_BACKUP/lucene/java/ASCIIFoldingFilter.java","r") as f_java:
	java_data = f_java.read()

with open("./PROCESSED_DATA_BACKUP/lucene/cs/ASCIIFoldingFilter.cs","r") as f_cs:
	cs_data = f_cs.read()

java_seqs = split_source_to_sequences(java_data)
cs_seqs = split_source_to_sequences(cs_data)

print "java seq : " + str(len(java_seqs))
print "cs seq :" + str(len(cs_seqs))


for java_seq in java_seqs:
	print java_seq
	
	java_join = " ".join(java_seq)
	java_processed = process_source_code(java_join)
	for cs_seq in cs_seqs:
		
		cs_join = " ".join(cs_seq)
		cs_processed = process_source_code(cs_join)
		print cosine_similarity(vector_averaging_java(java_processed.split(" ")),vector_averaging_cs(cs_processed.split(" ")))


