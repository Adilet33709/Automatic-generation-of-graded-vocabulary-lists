## Program that calculates Julian's Dispersion for a word in OSEWB corpora.

### Program that takes all lemmas except for words with specifed POS, punctuation for Onestopenglish and Weebit and stores in one file. Computes count at Texts combined and 
### takes its log and saves word and freq pair in excel. 

import spacy
import string
import pandas as pd
from collections import OrderedDict
import xlsxwriter
from math import log10


nlp = spacy.load("en_core_web_sm")
### Function that takes exam name and file_name in string format, POS=list of POS to exclude words 
# and outputs its lowercased lemmatized form in a form of a list
### Excluding POS
def text_to_list_excl_POS(level, file_name, corpora):
    # opening the file in read mode
    my_file = open("raw_data/" +corpora+ "/" + level + "/" + file_name + ".txt", "r")
    # reading the file
    data = my_file.read()
    doc = nlp(data)
    text_list = []
    ## exclude tokens with specified POS and if it is in punctuation
    for token in doc:
        if token.pos_ in ["NUM", "PROPN", "PUNCT", "SPACE", "SYM", "X"]:
            pass
        elif token.text in string.punctuation:
            pass
        else:
            text_list.append(token.lemma_)
    ## Lowercase all strings
    for i in range(len(text_list)):
        text_list[i] = text_list[i].lower()
    ## For int texts remove first word which shows level name.
    if level == "Int-Txt":
        text_list = text_list[1:]
    my_file.close()
    return text_list


### Function that takes exam name and returns nested list where each element is a list of words of a text exlcuding
### words with specified POS.
def texts_to_lists_excl_POS(level, corpora, folder_size):
    texts_list = []
    for i in range(folder_size):
        file_name = str(i+1) + "file"
        texts_list.append(text_to_list_excl_POS(level, file_name, corpora))
    return texts_list


### Get all lemmas as list
def combine_all_texts(levels, corpora, folder_size):
    all_words = []
    for level in levels:
        ## Get nested list for each exam
        x = texts_to_lists_excl_POS(level, corpora, folder_size)
        ## Open each list element of x and add them to all_words
        for i in range(len(x)):
            all_words += x[i]
    return all_words



## Function given list of percentages, it computes their variation coefficient and then dispersion
def get_dispersion_coefficient(list_of_percentages):
    mean = 0
    for percentage in list_of_percentages:
        mean += percentage / len(list_of_percentages)
    sum_squares = 0
    for percentage in list_of_percentages:
        sum_squares += (mean - percentage) ** 2
    sd = (sum_squares/ len(list_of_percentages)) ** 0.5
    dispersion_value = 1 - sd / mean * 1 / (len(list_of_percentages)-1) ** 0.5
    return dispersion_value



### Function that inputs word and outputs their percentages
def get_list_of_percentages(word):
    list_of_percentages = []
    list_of_percentages.append(OSE_ele.count(word) / len(OSE_ele))
    list_of_percentages.append(OSE_int.count(word) / len(OSE_int))
    list_of_percentages.append(OSE_adv.count(word) / len(OSE_adv))
    list_of_percentages.append(WB_l2.count(word) / len(WB_l2))
    list_of_percentages.append(WB_l3.count(word) / len(WB_l3))
    list_of_percentages.append(WB_l4.count(word) / len(WB_l4))
    list_of_percentages.append(WB_ks3.count(word) / len(WB_ks3))
    list_of_percentages.append(WB_gcse.count(word) / len(WB_gcse))
    assert len(list_of_percentages) == 8

    return list_of_percentages

### Function that inputs list of words and outputs list of dicts where key is word and value is Dispersion
def dispersion_calculator(list_of_words):
    list_of_dicts = []
    for word in list_of_words:
        new_dict = {}
        probability = all_lemmas.count(word) / len(all_lemmas)
        percentages = get_list_of_percentages(word)
        dispersion = get_dispersion_coefficient(percentages)
        new_dict["word"] = word
        new_dict["probability"] = probability
        new_dict["dispersion"] = dispersion
        new_dict["adjusted probability"] = probability * dispersion
        #new_dict["log prob"] = log10(probability * dispersion)
        list_of_dicts.append(new_dict)
    return list_of_dicts







# Upload all lemmas
OSE_ele = combine_all_texts(["Ele-Txt"], "OneStopEnglishCorpus", 189)
OSE_int = combine_all_texts(["Int-Txt"], "OneStopEnglishCorpus", 189)
OSE_adv = combine_all_texts(["Adv-Txt"], "OneStopEnglishCorpus", 189)
WB_l2 = combine_all_texts(["WRLevel2"], "WeeBit", 616)
WB_l3 = combine_all_texts(["WRLevel3"], "WeeBit", 616)
WB_l4 = combine_all_texts(["WRLevel4"], "WeeBit", 616)
WB_ks3 = combine_all_texts(["BitKS3"], "WeeBit", 616)
WB_gcse = combine_all_texts(["BitGCSE"], "WeeBit", 616)
all_lemmas = OSE_ele + OSE_int + OSE_adv + WB_l2 + WB_l3 + WB_l4 + WB_ks3 + WB_gcse



# OSE_ele = combine_all_texts(["Ele-Txt"], "OneStopEnglishCorpus", 2)
# OSE_int = combine_all_texts(["Int-Txt"], "OneStopEnglishCorpus", 2)
# OSE_adv = combine_all_texts(["Adv-Txt"], "OneStopEnglishCorpus", 2)
# WB_l2 = combine_all_texts(["WRLevel2"], "WeeBit", 2)
# WB_l3 = combine_all_texts(["WRLevel3"], "WeeBit", 2)
# WB_l4 = combine_all_texts(["WRLevel4"], "WeeBit", 2)
# WB_ks3 = combine_all_texts(["BitKS3"], "WeeBit", 2)
# WB_gcse = combine_all_texts(["BitGCSE"], "WeeBit", 2)
# all_lemmas = OSE_ele + OSE_int + OSE_adv + WB_l2 + WB_l3 + WB_l4 + WB_ks3 + WB_gcse

all_lemmas_filter = []

for word in all_lemmas:
    if word in all_lemmas_filter:
        pass
    else:
        all_lemmas_filter.append(word)


list_of_dicts = dispersion_calculator(all_lemmas_filter)







## Save to excel
df = pd.DataFrame(list_of_dicts)
with pd.ExcelWriter("OSEWB_freq_adj.xlsx") as writer: 
    df.to_excel(writer, sheet_name= "Adj freq", index = None , header = True)