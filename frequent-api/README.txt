The source code split the preprocess data with the tree generation to dataconverter.py

go to this link to download fullBDS.json

https://1drv.ms/u/s!An1UosdcVaRLiFUjYAyme71KiZRD

run Data_converter.py to generate pkl file

run FP-Tree.py or IT-Tree.py to generate frequent itemsets change c value in minSupcal() function to change minsup 
	Input of FP-Tree + MIS: Convert_data_for_Fp.pkl
	Input of IT-Tree: Convert_data_for_It.pkl + tag_aspect.pkl

if your machine cant run Data_converter. Use this generated data:

https://1drv.ms/f/s!An1UosdcVaRLikHfr5rrKtzHM-XD

move frequentItemsetFP.json or frequentItemsetIT.json to recommend-app folder

run Api.py in local or deploy to gcloud 
