# tfidf

A Web Application to find the most similar ChIP-seq datasets according to the TF-IDF score of gene regulation.

The input data is the peak file of MACS2 (https://github.com/taoliu/MACS).

The output is public ChIP-seq datasets ranked by similarity.


The TF (term frequency) is the strength of peaks at a specific site (e.g. 10k bin) in one dataset.

The IDF (inverse document frequency) is the logarithmically scaled inverse fraction of the datasets that contain the peak at a specific site (e.g. 10k bin).

