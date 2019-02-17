Explaination of submitted files:

The following files are cProfile comparisons as I made changes to the original code and tested new ideas:

cprofileresultpoor.txt
cprofileresultgoodfirst.txt
cprofileresultgoodsecond.txt
cprofileresultgoodthird.txt
cprofileresultgoodfourth.txt

I had missed that 2018 was suppose to peg the 2017 count from the original poor file so I had to adjust my design and implemented a lambda to handle this specific case. 

The file codecomparison.txt is a test of one code snippet change using just time stampstamps to compare the old code with the new code. The improvement was minimal between the two snippets.

I tried pstat to get a more formatted comparison of the cprofiles between the poor and the latest version. These are in the files pstatspoor.txt and pstatsgoodrefact.txt.

I used timeit to compare poor_perf with good_perf_refact and showed the result in the file timeitComparison.txt.