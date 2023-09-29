import pandas as pd
from iteration_utilities import unique_everseen


## Function that returns list of dictionaries of single lemmas with prob with or without dispersion
def get_single_lemmas(disp):
    df_single = pd.read_excel("Resources/List generation/OSEWB_single_lemmas.xlsx")
    list_single = []
    for i in range(len(df_single.axes[0])):
        new_dict = {}
        new_dict["word"] = df_single.iat[i,0]
        if disp == "Yes":
            new_dict["score"] = df_single.iat[i,3]
            list_single.append(new_dict)
        elif disp == "No":
            new_dict["score"] = df_single.iat[i,1]
            list_single.append(new_dict)
        else:
            raise Exception("Enter valid disp value")
    return list_single


## Upload auto list/EFLlex frequencies in OSEWB
def get_dictionary(name, disp):
    ### Upload Norvig.com file as dataframe
    df = pd.read_excel("Resources/List generation/" + name +  '.xlsx', header=None)
    ##Convert dataframe into dictionary
    norvig_dict = {}
    for i in range(len(df.axes[0])):
        if disp == "Yes":
            norvig_dict[str(df.iat[i,0]).lower()] = df.iat[i,3]
        elif disp == "No":
            norvig_dict[str(df.iat[i,0]).lower()] = df.iat[i,1]
        else:
            raise Exception("Enter valid disp value")
    return norvig_dict


## Function that returns list of dictionaries of MWEs of Pickard list with or without dispersion
def get_Pickard(disp, comp):
    pickard_df = pd.read_excel("Resources/Pickard.xlsx", header=None)
    pickard = {}
    for i in range(len(pickard_df.axes[0])):
        pickard[pickard_df.iat[i,0]] = (1-pickard_df.iat[i,1]) / 2
    auto_list_full = pickard_df.iloc[:,0].tolist()
    perc = round(comp/100 * len(auto_list_full))
    auto_list = auto_list_full[: int(perc)]
    auto_list = list(unique_everseen(auto_list))
    bigrams = get_dictionary("Auto_list_bigram_freqs_OSEWB", disp)
    trigrams = get_dictionary("Auto_list_trigram_freqs_OSEWB", disp)
    auto_dicts = []
    for word in auto_list:
        new_dict = {}
        new_dict["word"] = str(word)
        word = str(word)
        if word in bigrams.keys():
            ## Weight with compositionality score
            new_dict["score"] = float(bigrams[word]) * float(pickard[word])
        elif word in trigrams.keys():
            new_dict["score"] = float(trigrams[word]) * float(pickard[word])
        else:
            new_dict["score"] = 0
        auto_dicts.append(new_dict)
    return auto_dicts



## Function that inputs disp, auto list, comp and returns automatically generated list
def get_auto_list(disp, auto_list = "Pickard",comp = 100):
    list_single = get_single_lemmas(disp)
    if auto_list == "Pickard":
        auto_dicts = get_Pickard(disp, comp)
    else:
        raise Exception("Enter valid auto_list value")
    auto_full = auto_dicts + list_single
    auto_full = sorted(auto_full, key=lambda i: i['score'], reverse=True)
    final_list = []
    for dictionary in auto_full:
        if dictionary["score"] > 0:
            final_list.append(dictionary)
    return final_list
