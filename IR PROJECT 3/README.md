# Evaluating IR models

This project aims at implementing different IR models. 

Given Twitter data (training_tweet.json), sample queries (queries.txt), and the corresponding relevance judgement score (qrel.txt) for each query,the following tasks were implemented:

 * Implement and evaluate :
    * Language Model
    * BM25
    * Divergence from Randomness (DFR) Model
  * Based on evaluation results, improve performance of these 3 models in terms of MAP (Mean Average Precision).
  * Use TREC evaluation program to evaluate Solr search functionality.


File                  | Information
--------------        |--------------
training_tweet.json   |Twitter Data
queries.txt           |Sample queries
qrel.txt              |Relevance judgement score
BM25                  |Output scores for BM25 model
DFR                   |Output scores for DFR model
LM                    |Output scores for LM model
schema                |Schema files for models
json_to_trec.py       |Python code for model evaluation
report.pdf            |Result summarization
