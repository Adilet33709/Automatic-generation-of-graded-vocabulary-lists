### Program that for a given ranked list calculates how many first n words user needs to know
### to understand at least Y% of documents in Cambridge texts. 
import pandas as pd
import spacy
import string
from collections import OrderedDict
import time

### Import American to british table and create dictionary where key is american word and value is british and vice versa
df_converter = pd.read_excel('Resources/American_to_british.xlsx')
americ_to_brit = {}
brit_to_americ = {}
for i in range(len(df_converter.axes[0])):
    americ_to_brit[df_converter.iat[i,1]] = df_converter.iat[i,0]
    brit_to_americ[df_converter.iat[i,0]] = df_converter.iat[i,1]


gold_list = pd.read_excel("Resources/GOLD_list.xlsx", sheet_name="Total wth GSE", header=None).iloc[:, 0].tolist()
numbers = pd.read_excel("Resources/0_to_1000.xlsx", header=None).iloc[:,0].tolist()
excl_propn = pd.read_excel("Resources/propn_ignore.xlsx", header=None).iloc[:,0].tolist()

# Inputs filename and sheet_name and outputs list of words in a given ranked list.
def ranked_vocab_to_list(file_name, sheet_name):
    dataframe = pd.read_excel('Resources/' + file_name + ".xlsx", sheet_name = sheet_name, header = None)
    vocab_list = dataframe.iloc[:, 0].tolist()
    return vocab_list


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
        elif dictionary["word"] == "'ve" or dictionary["word"] == "'s" or dictionary["word"] == "’s":
            pass
        elif dictionary["word"].count("\ufeff") > 0 or dictionary["lemma"].count("\ufeff") > 0:
            pass
        ## Remove numbers and exclued PROPN
        elif (dictionary["lemma"].lower() in numbers) or (dictionary["lemma"].lower()) in excl_propn:
            pass
        else:
            cleaned_list_of_dicts.append(dictionary)
    return cleaned_list_of_dicts

### Function that finds MWE's from the list of dicts and adds new key/value pair MWE and its value
### Gold list is list of MWE from EVP/GSE
def get_MWE(list_of_dicts, gold_list):
    output_list = list_of_dicts
    for i in range(len(list_of_dicts)-1):
        MWE = list_of_dicts[i]["lemma"] + " " + list_of_dicts[i+1]["lemma"]
        if MWE in gold_list:
            if (output_list[i]["MWE"] == None) and (output_list[i+1]["MWE"] == None):
                output_list[i]["MWE"] = MWE
                output_list[i+1]["MWE"] = MWE
        else:
            MWE = list_of_dicts[i]["word"] + " " + list_of_dicts[i+1]["word"]
            if MWE in gold_list:
                if (output_list[i]["MWE"] == None) and (output_list[i+1]["MWE"] == None):
                    output_list[i]["MWE"] = MWE
                    output_list[i+1]["MWE"] = MWE
    return output_list


### Function that finds trigram MWE's from the list of dicts and adds new key/value pair MWE and its value
### Gold list is list of MWE from EVP/GSE
def get_trigram_MWE(list_of_dicts, gold_list):
    output_list = list_of_dicts
    for i in range(len(list_of_dicts)-2):
        MWE = list_of_dicts[i]["lemma"] + " " + list_of_dicts[i+1]["lemma"] + " " + list_of_dicts[i+2]["lemma"]
        if MWE in gold_list:
            if (output_list[i]["MWE"] == None) and (output_list[i+1]["MWE"] == None) and (output_list[i+2]["MWE"] == None):
                output_list[i]["MWE"] = MWE
                output_list[i+1]["MWE"] = MWE
                output_list[i+2]["MWE"] = MWE
        else:
            MWE = list_of_dicts[i]["word"] + " " + list_of_dicts[i+1]["word"] + " " + list_of_dicts[i+2]["word"]
            if MWE in gold_list:
                if (output_list[i]["MWE"] == None) and (output_list[i+1]["MWE"] == None) and (output_list[i+2]["MWE"] == None):
                    output_list[i]["MWE"] = MWE
                    output_list[i+1]["MWE"] = MWE
                    output_list[i+2]["MWE"] = MWE
    ##Include wildcard
    for i in range(len(list_of_dicts)-2):
        MWE = list_of_dicts[i]["lemma"] + " " + "wildcard" + " " + list_of_dicts[i+2]["lemma"]
        if MWE in gold_list:
            if (output_list[i]["MWE"] == None) and (output_list[i+1]["MWE"] == None) and (output_list[i+2]["MWE"] == None):
                output_list[i]["MWE"] = MWE
                output_list[i+1]["MWE"] = MWE
                output_list[i+2]["MWE"] = MWE
        else:
            MWE = list_of_dicts[i]["word"] + " " + "wildcard" + " " + list_of_dicts[i+2]["word"]
            if MWE in gold_list:
                if (output_list[i]["MWE"] == None) and (output_list[i+1]["MWE"] == None) and (output_list[i+2]["MWE"] == None):
                    output_list[i]["MWE"] = MWE
                    output_list[i+1]["MWE"] = MWE
                    output_list[i+2]["MWE"] = MWE
    return output_list




### Function that finds fourgram MWE's from the list of dicts and adds new key/value pair MWE and its value
### Gold list is list of MWE from EVP/GSE
def get_fourgram_MWE(list_of_dicts, gold_list):
    output_list = list_of_dicts
    for i in range(len(list_of_dicts)-3):
        MWE = list_of_dicts[i]["lemma"] + " " + list_of_dicts[i+1]["lemma"] + " " + list_of_dicts[i+2]["lemma"] +  " " + list_of_dicts[i+3]["lemma"]
        if MWE in gold_list:
            if (output_list[i]["MWE"] == None) and (output_list[i+1]["MWE"] == None) and (output_list[i+2]["MWE"] == None) and (output_list[i+3]["MWE"] == None):
                output_list[i]["MWE"] = MWE
                output_list[i+1]["MWE"] = MWE
                output_list[i+2]["MWE"] = MWE
                output_list[i+3]["MWE"] = MWE
        else:
            MWE = list_of_dicts[i]["word"] + " " + list_of_dicts[i+1]["word"] + " " + list_of_dicts[i+2]["word"] + " " + list_of_dicts[i+3]["word"]
            if MWE in gold_list:
                if (output_list[i]["MWE"] == None) and (output_list[i+1]["MWE"] == None) and (output_list[i+2]["MWE"] == None) and (output_list[i+3]["MWE"] == None):
                    output_list[i]["MWE"] = MWE
                    output_list[i+1]["MWE"] = MWE
                    output_list[i+2]["MWE"] = MWE
                    output_list[i+3]["MWE"] = MWE
    ## Include wildcard
    for i in range(len(list_of_dicts)-3):
        MWE = list_of_dicts[i]["lemma"] + " " + "wildcard" + " " + list_of_dicts[i+2]["lemma"] +  " " + list_of_dicts[i+3]["lemma"]
        if MWE in gold_list:
            if (output_list[i]["MWE"] == None) and (output_list[i+1]["MWE"] == None) and (output_list[i+2]["MWE"] == None) and (output_list[i+3]["MWE"] == None):
                output_list[i]["MWE"] = MWE
                output_list[i+1]["MWE"] = MWE
                output_list[i+2]["MWE"] = MWE
                output_list[i+3]["MWE"] = MWE
        else:
            MWE = list_of_dicts[i]["word"] + " " + "wildcard" + " " + list_of_dicts[i+2]["word"] + " " + list_of_dicts[i+3]["word"]
            if MWE in gold_list:
                if (output_list[i]["MWE"] == None) and (output_list[i+1]["MWE"] == None) and (output_list[i+2]["MWE"] == None) and (output_list[i+3]["MWE"] == None):
                    output_list[i]["MWE"] = MWE
                    output_list[i+1]["MWE"] = MWE
                    output_list[i+2]["MWE"] = MWE
                    output_list[i+3]["MWE"] = MWE
    for i in range(len(list_of_dicts)-3):
        MWE = list_of_dicts[i]["lemma"] + " " + list_of_dicts[i+1]["lemma"] + " " + "wildcard" +  " " + list_of_dicts[i+3]["lemma"]
        if MWE in gold_list:
            if (output_list[i]["MWE"] == None) and (output_list[i+1]["MWE"] == None) and (output_list[i+2]["MWE"] == None) and (output_list[i+3]["MWE"] == None):
                output_list[i]["MWE"] = MWE
                output_list[i+1]["MWE"] = MWE
                output_list[i+2]["MWE"] = MWE
                output_list[i+3]["MWE"] = MWE
        else:
            MWE = list_of_dicts[i]["word"] + " " + list_of_dicts[i+1]["word"] + " " + "wildcard" + " " + list_of_dicts[i+3]["word"]
            if MWE in gold_list:
                if (output_list[i]["MWE"] == None) and (output_list[i+1]["MWE"] == None) and (output_list[i+2]["MWE"] == None) and (output_list[i+3]["MWE"] == None):
                    output_list[i]["MWE"] = MWE
                    output_list[i+1]["MWE"] = MWE
                    output_list[i+2]["MWE"] = MWE
                    output_list[i+3]["MWE"] = MWE
    return output_list



# ### Function that finds fourgram MWE's from the list of dicts and adds new key/value pair MWE and its value
# ### Gold list is list of MWE from EVP/GSE
def get_allgram_MWE(list_of_dicts, gold, gram):
    output_list = list_of_dicts
    Gold = gold.copy()
    ## Turn stings into list
    for p in range(len(Gold)):
        Gold[p] = Gold[p].split(" ")
    ## For each possible ngram check
    for i in range(len(list_of_dicts)-(gram-1)):
        MWE = []
        for r in range(gram):
            MWE.append(list_of_dicts[i+r]["lemma"])
        MWE_words = []
        for w in range(gram):
            MWE_words.append(list_of_dicts[i+w]["word"])
        for gold in Gold:
            ## check if gold and MWE are the same elementwise except for wildcard
            if len(gold) == len(MWE):
                count = 0
                for j in range(len(gold)):
                    if gold[j] == "wildcard":
                        count += 1
                    elif gold[j] == MWE[j]:
                        count += 1
                count_words = 0
                for m in range(len(gold)):
                    if gold[m] == "wildcard":
                        count_words += 1
                    elif gold[m] == MWE_words[m]:
                        count_words += 1
                if count == len(gold):
                    MWEs = []
                    for n in range(gram):
                        MWEs.append(list_of_dicts[i+n]["MWE"])
                    ## Check if all elements of MWE isn't MWE already
                    if all([v == None for v in MWEs]) == True:
                        for q in range(gram):
                            MWE_string = MWE[0]
                            for j in range(len(MWE)-1):
                                MWE_string += (" " + MWE[j+1])
                            output_list[i+q]["MWE"] = MWE_string
                        break
                elif count_words == len(gold):
                    MWEs = []
                    for n in range(gram):
                        MWEs.append(list_of_dicts[i+n]["MWE"])
                    ## Check if all elements of MWE isn't MWE already
                    if all([b == None for b in MWEs]) == True:
                        for c in range(gram):
                            MWE_string = MWE[0]
                            for j in range(len(MWE)-1):
                                MWE_string += (" " + MWE[j+1])
                            output_list[i+c]["MWE"] = MWE_string
                        break
    return output_list

nlp = spacy.load("en_core_web_sm")
## Function that takes exam name and file_name in string format and outputs Cleaned list of dictionaries.
## Where each dictionary contains word, lemma, tag.
def text_to_list_of_dict(exam, file_name):
    # opening the file in read mode
    my_file = open("Resources/ICNALE/" + exam + "/" + file_name + ".txt", "r")
    # reading the file
    data = my_file.read()
    doc = nlp(data)
    output_list = []
    for token in doc:
        output_dict = {}
        output_dict["word"] = token.text
        output_dict["lemma"] = token.lemma_
        output_dict["tag"] = token.pos_
        output_dict["MWE"] = None
        output_list.append(output_dict)
    my_file.close()
    output_list = clean_list_of_dicts(output_list)
    output_list = get_allgram_MWE(output_list, gold_list, 9)
    output_list = get_allgram_MWE(output_list, gold_list, 8)
    output_list = get_allgram_MWE(output_list, gold_list, 7)
    output_list = get_allgram_MWE(output_list, gold_list, 6)
    output_list = get_allgram_MWE(output_list, gold_list, 5)
    output_list = get_fourgram_MWE(output_list, gold_list)
    output_list = get_trigram_MWE(output_list, gold_list)
    output_list = get_MWE(output_list, gold_list)
    return output_list

### Function that takes exam name and returns nested list where each element is a list of dictionary.
def texts_to_nested_list(exam):
    texts_list = []
    for i in range(250):
        try:
            file_name = str(i+1) + "text"
            texts_list.append(text_to_list_of_dict(exam, file_name))
        except:
            pass
    return texts_list


# Inputs list of words and list of dictionaries of text. 
# Returns percentage of text words user can understand 
# given he knows all vocabulary
## !!! Everything is lowercased.
def percentage_calculator_new(vocabulary, list_of_dicts):
    ### Lowercase all strings of vocabulary
    vocabulary = vocabulary
    for i in range(len(vocabulary)):
        vocabulary[i] = str(vocabulary[i]).lower()
    # Count known words
    count_known = 0
    ### Calculate how many of words in list_of_dicts are known. 
    for dictionary in list_of_dicts:
        if dictionary["MWE"] == None:
            if dictionary["lemma"].lower() in vocabulary:
                count_known += 1
            elif dictionary["word"].lower() in vocabulary:
                count_known += 1
            ## Account for American British difference
            elif dictionary["word"].lower() in americ_to_brit.keys():
                if americ_to_brit[dictionary["word"].lower()] in vocabulary:
                    count_known += 1
            elif dictionary["lemma"].lower() in americ_to_brit.keys():
                if americ_to_brit[dictionary["lemma"].lower()] in vocabulary:
                    count_known += 1
            elif dictionary["word"].lower() in brit_to_americ.keys():
                if brit_to_americ[dictionary["word"].lower()] in vocabulary:
                    count_known += 1
            elif dictionary["lemma"].lower() in brit_to_americ.keys():
                if brit_to_americ[dictionary["lemma"].lower()] in vocabulary:
                    count_known += 1
        ### If word part of MWE
        else:
            if dictionary["MWE"].lower() in vocabulary:
                count_known += 1
    percentage = count_known / len(list_of_dicts)
    assert percentage <= 1
    return percentage




# Inputs value from 0 to 1 and threshold value. Converts them to discrete 0 or 1 values
# if x >= X, then 1. otherwise 0.
def thresholder(input, X):
    assert input <= 1
    assert X <= 100
    if input >= X / 100:
        return 1
    else:
        return 0

def number_of_words_calculator(vocabulary_list, list_of_dicts, X):
    max_val = 40
    if percentage_calculator_new(vocabulary_list, list_of_dicts) * 100 < X:
        return None
    if percentage_calculator_new(vocabulary_list[:max_val * 500], list_of_dicts) * 100 < X:
        return None
    ## Every 500 check initial guessing parameter.
    number_of_words = 0
    for i in range(max_val):
        x = (max_val-i) * 500
        if percentage_calculator_new(vocabulary_list[:x],list_of_dicts) * 100 < X:
            number_of_words = x - 200
            break
    changer = 0
    output = 0
    while output <  X:
        if (X - output) > 60:
            changer = 60
            number_of_words += 200
        elif (X - output) > 50:
            changer = 50
            number_of_words += 100
        elif (X - output) > 40:
            changer = 40
            number_of_words += 50
        elif (X - output) > 20:
            number_of_words += 20
            changer = 20
        elif (X - output) > 10:
            number_of_words += 10
            changer = 10
        elif (X - output) > 6:
            number_of_words += 4
            changer = 6
        else:
            number_of_words += 1
            changer = 1
        vocab_list = vocabulary_list[0 : number_of_words]
        output = percentage_calculator_new(vocab_list, list_of_dicts) * 100
    number_of_words_new = number_of_words - changer
    while output <  X:
        if X != output:
            number_of_words_new += 1
        vocab_list = vocabulary_list[0 : number_of_words_new]
        output = percentage_calculator_new(vocab_list, list_of_dicts) * 100
    number_of_words_new += 1
    return number_of_words_new






A2_0 = texts_to_nested_list("A2_0")
B1_1 = texts_to_nested_list("B1_1")
B1_2 = texts_to_nested_list("B1_2")
B2_0 = texts_to_nested_list("B2_0")
texts_to_nested_list_dict = {"A2_0" : A2_0, "B1_1" : B1_1, "B1_2" : B1_2, "B2_0" : B2_0}
#texts_to_nested_list_dict = {"KET" : texts_to_nested_list("KET")}
### Function that for an given vocabulary list computes text comprehension and 
### number of words needed to have Y docs understood for a given level
def comprehen_and_number_of_words(vocabulary, ranked_list, Levels, Y, X=90, k = 14000):
    # k = 14000
    output_dictionary = {}
    output_dictionary["Method"] = str(vocabulary) + " " + str(ranked_list)
    vocabulary_list = ranked_vocab_to_list(vocabulary, ranked_list)
    text_comprehension_sum = 0
    for Level in Levels:
        nested_list = texts_to_nested_list_dict[Level]
        threshold_values = []
        for list_of_dicts in nested_list:
            threshold_values.append(number_of_words_calculator(vocabulary_list, list_of_dicts, X=X))
        threshold_values_length = len(threshold_values)
        while None in threshold_values:
            threshold_values.remove(None)
        text_comprehension = 0
        number_of_words = 1
        percentage_of_docs = 0
        if sum(i <= len(vocabulary_list) for i in threshold_values) / threshold_values_length * 100 < Y:
            output_dictionary[str(Level)] = "/"
        else:
            while percentage_of_docs < Y:
                percentage_of_docs = sum(i <= number_of_words for i in threshold_values) / threshold_values_length * 100
                number_of_words += 1
            number_of_words -= 1
            output_dictionary[str(Level)] = number_of_words
        count = 0
        while count < k:
            count += 1
            text_comprehension += sum(i <= count for i in threshold_values) / k
        text_comprehension_sum += text_comprehension
        print("Number of words for " + str(vocabulary) + " " + str(ranked_list) + " "  + str(number_of_words) + " Y= " + str(Y)) 
        print("Text comprehension for " + str(vocabulary) + " " + str(ranked_list) + " "  + str(text_comprehension))   
    text_comprehension_sum = round(text_comprehension_sum / 656,3)
    output_dictionary["TC"] = text_comprehension_sum
    return output_dictionary

### Inputs vocabulary list. and nested list of dicts and threshold (in %) for understanding a document
### Outputs how much percentage of docs user can understand. 
def percentage_of_docs_calculator(vocabulary_list, nested_list, X):
    count = 0
    for i in range(len(nested_list)):
        ## Get percentages for each list of dicts
        x = percentage_calculator_new(vocabulary_list, nested_list[i])
        x = thresholder(x, X)
        count += x
    percentage = count / len(nested_list) * 100
    return percentage



def changer(dictionary):
    new_dict = dictionary
    lis = []
    for item in new_dict.keys():
        if item == "Method":
            pass
        elif item == "TC":
            pass
        else:
            lis.append(float(str(new_dict[item]).replace("/", "1000000")))
    ## If value of previous level is higher then equalize the value of next to previous one
    for i in range(len(lis)-1):
        if lis[i] > lis[i+1]:
            lis[i+1] = lis[i]
    ## Convert to dictionary 
    count = 0
    for item in new_dict.keys():
        if item == "Method":
            pass
        elif item == "TC":
            pass
        else:
            value = str(lis[count]).replace("1000000.0","/")
            ## If value is number then do rounding
            if value == "/":
                new_dict[item] = value
            else:   
                new_dict[item] = round(float(value))
            count += 1
    return new_dict

def evaluate(vocabulary, ranked_list, Levels, Y, X=90, k = 14000):
    # k = 14000
    output_dictionary = {}
    output_dictionary["Method"] = str(vocabulary) + " " + str(ranked_list)
    vocabulary_list = ranked_vocab_to_list(vocabulary, ranked_list)
    text_comprehension_sum = 0
    for Level in Levels:
        nested_list = texts_to_nested_list_dict[Level]
        threshold_values = []
        for list_of_dicts in nested_list:
            threshold_values.append(number_of_words_calculator(vocabulary_list, list_of_dicts, X=X))
        threshold_values_length = len(threshold_values)
        while None in threshold_values:
            threshold_values.remove(None)
        text_comprehension = 0
        number_of_words = 1
        percentage_of_docs = 0
        if sum(i <= len(vocabulary_list) for i in threshold_values) / threshold_values_length * 100 < Y:
            output_dictionary[str(Level)] = "/"
        else:
            while percentage_of_docs < Y:
                percentage_of_docs = sum(i <= number_of_words for i in threshold_values) / threshold_values_length * 100
                number_of_words += 1
            number_of_words -= 1
            output_dictionary[str(Level)] = number_of_words
        count = 0
        while count < k:
            count += 1
            text_comprehension += sum(i <= count for i in threshold_values) / k
        text_comprehension_sum += text_comprehension
        print("Number of words for " + str(vocabulary) + " " + str(ranked_list) + " "  + str(number_of_words) + " Y= " + str(Y)) 
        print("Text comprehension for " + str(vocabulary) + " " + str(ranked_list) + " "  + str(text_comprehension))  
    text_comprehension_sum = round(text_comprehension_sum / 656 , 3) 
    output_dictionary["TC"] = text_comprehension_sum
    output_dictionary = changer(output_dictionary)
    return output_dictionary
