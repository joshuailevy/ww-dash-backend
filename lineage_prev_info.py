import pandas as pd 
import os
from freyja.utils import prepLineageDict, prepSummaryDict

agg_df = pd.read_csv('agg_freyja.tsv', skipinitialspace=True, sep='\t',index_col=0) 
agg_df = prepLineageDict(agg_df,thresh=0.0001)

agg_df.index = [ agi.split('.')[0] for agi in agg_df.index]

## now reverse form, so that we can search by lineage and get samples with that lineage, plus estimated freq
dict0 = {}
for agi in agg_df.index:
    dat = agg_df.loc[agi,'linDict']
    for key,val in zip(dat.keys(),dat.values()):
        if key !='Other':
            if key in dict0.keys():
                dict0[key][agi] = val
            else:
                dict0[key] = {agi:val}


import pickle
pickle.dump(dict0,open('lineage_dict.pkl','wb'))
pickle.dump(agg_df.loc[:,'linDict'],open('samples_deconv_dict.pkl','wb'))







