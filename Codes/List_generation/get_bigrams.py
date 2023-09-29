## Program that extracts ngrams up to fourgrams from OSE/WB and calculates their frequencies
## Program that calculates Julian's Dispersion for a word in OSEWB corpora.

### Program that takes all lemmas except for words with specifed POS, punctuation for Onestopenglish and Weebit and stores in one file. Computes count at Texts combined and 
### takes its log and saves word and freq pair in excel. 

import spacy
import pandas as pd
from collections import OrderedDict
from math import log10
from iteration_utilities import unique_everseen
import time


## Function inputs list of dicts. Outputs cleander list of dicts by 
## POS, punctuation, removing "ve" or "s"
def clean_list_of_dicts(list_of_dicts):
    cleaned_list_of_dicts = []
    for dictionary in list_of_dicts:
        ## Remove words with specified POS
        POS_exclude = ["NUM", "PROPN", "PUNCT", "SPACE", "SYM", "X"]
        if dictionary["tag"] in POS_exclude:
            pass
        ## Remove if word len = 1 and it is in punctuation list
        elif any(c.isalpha() for c in dictionary["word"]) == False:
            pass
        ## Remove if word is either "'ve" or "'s"
        elif dictionary["word"] == "'ve" or dictionary["word"] == "'s":
            pass
        else:
            cleaned_list_of_dicts.append(dictionary)
    return cleaned_list_of_dicts

### Function that converts list of single words into pairs of two-word MWEs
def get_MWE(list_of_dicts):
    output_list = []
     ## Get two-word MWEs
    for i in range(len(list_of_dicts)-1):
        ## For lemmas
        MWE = list_of_dicts[i]["lemma"] + " " + list_of_dicts[i+1]["lemma"]
        output_list.append(MWE)
    return output_list


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
    output_list = []
    for token in doc:
        output_dict = {}
        output_dict["lemma"] = token.lemma_
        output_dict["word"] = token.text
        output_dict["tag"] = token.pos_
        output_list.append(output_dict)
    my_file.close()
    output_list = clean_list_of_dicts(output_list)
    output_list = get_MWE(output_list)
    text_list = output_list
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
        list_of_dicts.append(new_dict)
    return list_of_dicts







## Upload all lemmas
OSE_ele = combine_all_texts(["Ele-Txt"], "OneStopEnglishCorpus", 189)
OSE_int = combine_all_texts(["Int-Txt"], "OneStopEnglishCorpus", 189)
OSE_adv = combine_all_texts(["Adv-Txt"], "OneStopEnglishCorpus", 189)
WB_l2 = combine_all_texts(["WRLevel2"], "WeeBit", 616)
WB_l3 = combine_all_texts(["WRLevel3"], "WeeBit", 616)
WB_l4 = combine_all_texts(["WRLevel4"], "WeeBit", 616)
WB_ks3 = combine_all_texts(["BitKS3"], "WeeBit", 616)
WB_gcse = combine_all_texts(["BitGCSE"], "WeeBit", 616)
all_lemmas = OSE_ele + OSE_int + OSE_adv + WB_l2 + WB_l3 + WB_l4 + WB_ks3 + WB_gcse

# print(len(all_lemmas))
# print(len(OSE_ele))
# print(len(OSE_int))
# print(len(OSE_adv))
# print(len(WB_l2))
# print(len(WB_l3))
# print(len(WB_l4))
# print(len(WB_ks3))
# print(len(WB_gcse))
# print(len(list(unique_everseen(OSE_ele))))
# print(len(list(unique_everseen(OSE_int))))
# print(len(list(unique_everseen(OSE_adv))))
# print(len(list(unique_everseen(WB_l2))))
# print(len(list(unique_everseen(WB_l3))))
# print(len(list(unique_everseen(WB_l4))))
# print(len(list(unique_everseen(WB_ks3))))
# print(len(list(unique_everseen(WB_gcse))))



# OSE_ele = combine_all_texts(["Ele-Txt"], "OneStopEnglishCorpus", 1)
# OSE_int = combine_all_texts(["Int-Txt"], "OneStopEnglishCorpus", 1)
# OSE_adv = combine_all_texts(["Adv-Txt"], "OneStopEnglishCorpus", 1)
# WB_l2 = combine_all_texts(["WRLevel2"], "WeeBit", 1)
# WB_l3 = combine_all_texts(["WRLevel3"], "WeeBit", 1)
# WB_l4 = combine_all_texts(["WRLevel4"], "WeeBit", 1)
# WB_ks3 = combine_all_texts(["BitKS3"], "WeeBit", 1)
# WB_gcse = combine_all_texts(["BitGCSE"], "WeeBit", 1)
# all_lemmas = OSE_ele + OSE_int + OSE_adv + WB_l2 + WB_l3 + WB_l4 + WB_ks3 + WB_gcse




## Uplaod Pickard
auto = pd.read_excel("Resources/Pickard.xlsx", header=None).iloc[:,0].tolist()
auto_filtered = list(set(auto) & set(all_lemmas))


## Upload EFLlex
# EFLlex = pd.read_excel("Resources/MWEs/EFLlex.xlsx", header=None).iloc[:,0].tolist()
# EFLlex_filtered = list(set(EFLlex) & set(all_lemmas))




list_of_dicts_auto_list = dispersion_calculator(auto_filtered)
# list_of_dicts_EFLlex = dispersion_calculator(EFLlex_filtered)




## Save to excel
pd.DataFrame(list_of_dicts_auto_list).to_excel("Resources/Auto_list_bigram_freqs_OSEWB.xlsx", index=None)
# pd.DataFrame(list_of_dicts_EFLlex).to_excel("Resources/EFLlex_bigram_freqs_OSEWB.xlsx", index=None)