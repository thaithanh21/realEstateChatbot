The source code split the preprocess data with the tree generation to dataconverter.py

go to this link to download fullBDS.json

https://1drv.ms/u/s!An1UosdcVaRLiFUjYAyme71KiZRD

run Data_converter.py to generate pkl file

run FP-Tree.py or IT-Tree.py to generate frequent itemsets change c value in minSupcal() function to change minsup 
	Input of FP-Tree: Convert_data_for_Fp.pkl
	Input of IT-Tree: Convert_data_for_It.pkl + current.pkl + firstnode.pkl

if your machine cant run Data_converter. Use this generated data:

https://1drv.ms/f/s!An1UosdcVaRLiAfS2RKij9I-C2Cq


run api.py (frequentItemsFP.json as default)
