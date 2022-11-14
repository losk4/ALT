@echo off
echo python3 src/SAR_Indexer.py corpora/2015 indexes/index2015.bin

FOR %%x IN (levenshtein damerau_r damerau_i) DO (
    FOR %%y in (1 2 3) DO (
        python src/SAR_Searcher.py indexes/index2015.bin -L resources/queries.txt -C -t %%y -d %%x > results/resul_%%x_%%y.txt
    )
) 
