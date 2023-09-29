import pandas as pd
from Codesss.List_generation.functions import get_auto_list




## This function outputs automatically generated vocabulary list in a form of list
## The function have following parameters:
## disp: Specifies whether to get list evaluated with dispersion or without. Possible values "Yes", "No".
## auto_list: Specifies which auto MWEs list should be choosen to generate vocabulary list. Possible values "Pickard", "EFLlex"
## comp: If Pickard list is choosen, this parameter specifies which percentage of Pickard list based on Compositionality 
## should be choosen to generate vocabulary list. Possible values ranges from 0 to 100.


auto_list = get_auto_list(disp="Yes", auto_list="Pickard", comp=80)
print(len(auto_list))


pd.DataFrame(auto_list).to_excel("auto.xlsx", sheet_name="Auto list", index=None, header=None)
