# Overview

This repository contains the data and implementation for the paper <a href="https://bdqnghi.github.io/files/icse-18-nier.pdf">Hierarchical Learning of Cross-Language Mappings through Distributed Vector Representations for Code </a>, in Proceedings of the <a href="https://www.icse2018.org/"> IEEE/ACM 40th International Conference on Software Engineering: New Ideas and Emerging Technologies Results Track (ICSE-NIER), Gothenburg, Sweden, 2018 </a>.

Since we found that the implementation of BiSkip2Vec from <a href="https://github.com/eske/multivec">Multivec</a> has better performance than our implementation, we recommend the researchers that want to reproduce our result use Multivec for training the token embeddings.

# Data

- DATA/DATA_RAW.tar.gz: contains the raw data of these open source projects: antlr, cordova, datastax, factual, fpml, log4j, lucene, spring, uap, zeromq
- DATA/TRAINING_SENTENCES: contains the processed data of aligned sentences between C# and Java, which will use as the input for Multivec.
- DATA/SIGNATURE: all of the method signatures for each of the project

# Result
- The mapping that we found can be access at <a href="https://github.com/bdqnghi/hierarchical-programming-language-mapping/blob/master/evaluation/method_mappings.csv">mapping results</a> 

- We also use the mappings mined from our work in the configuration file of Java2Csharp: https://github.com/bdqnghi/sharpen-java2csharp.
