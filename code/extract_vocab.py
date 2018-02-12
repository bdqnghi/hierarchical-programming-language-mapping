

with open("cs2vec.txt","r") as f:
	data = f.readlines()

	for line in data:
		
		split = line.split(" ")
		with open("vocab_cs.txt","a") as f2:
			f2.write(split[0] + "\n")