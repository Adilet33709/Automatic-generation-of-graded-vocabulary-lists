## Automatic Generation of Vocabulary Lists
This repository contains codes for our upcoming paper "Automatic Generation of Vocabulary Lists"
The Code folder has two parts. The Evaluation part contains codes to evaluate a vocabulary list in terms of study time and text comprehension metrics introduced in our paper. The evaluate.py contains a function that outputs the results based on graduation level and text comprehension parameters for different vocabulary levels (See evaluate.py for detailed instructions). The second part contains codes to automatically generate various vocabulary lists with MWEs based on the dispersion, and compositionality (See generate_list.py for detailed instructions).  
## Before your start
1. Put Cambridge graded texts, OneStopEnglish, and WeeBit folders into the Resources folder containing Cambridge, OneStopEnglishCorpus, and WeeBit graded texts. Graded texts within each folder should be separated according to their levels into different folders. Each file should be named as "i+text.txt" where i ranges from 1 to a number of files in a given level.
2. To evaluate a vocabulary list, put an Excel file with the name of a vocabulary list into the Resource folder. Place each word per line. 
3. If you want to use your own Gold MWEs list, place your Gold MWEs list in the Gold.xlsx file located in the Resources folder.
4. get_single_lemmas.py, get_bigrams.py, and get_trigrams.py in Codes/List_generation are used to generate files in Resouces/List generation. These files are used to generate a vocabulary list.

