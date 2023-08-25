import pandas as pd 
import os
varsDir = 'vars'
ct_thresh = 20
j=0
for var in os.listdir(varsDir):
    df = pd.read_csv(varsDir+'/'+var,sep='\t')
    df = df[df['ALT_DP']>=ct_thresh]
    #drop frame shifts
    sname=var.split('.')[0]
    df = df[df['ALT'].apply(lambda x: True if (('+' not in x and '-' not in x) or ((len(x)-1)%3==0)) else False)]
    if len(df)==0:
        print('hi')
        continue
    df['mutName'] = df['REF'] + df['POS'].astype(str) + df['ALT']
    df['sample'] = sname
    df = df[['mutName','sample','ALT_FREQ','ALT_DP']]
    if j==0:
        dfAll = df.copy()
    else:
        dfAll = pd.concat((dfAll,df), axis=0)
    j+=1

# dfAll =dfAll[dfAll['sample']=='SRR25665869']
dfAll = dfAll.set_index(['mutName','sample'])
dfAll.to_csv('testData.csv')
    
muts=['G21608+TCATGCCGCTGT','C897A','G3431T','A7842G','C8293T','G8393A','T9866C','G11042T','C12789T','T13339C','T15756A','A18492G','C21711T','G21941T','T22032C','C22033A','A22034G','C22208T','C22353A','G22577C','G22770A','G22895C','T22896A','G22898A','A22910G','C22916T','T22942A','T23005A','G23012A','C23013A','T23018C','T23019C','C23271T','C23423T','A23604G','C24378T','C24990T','C25207T','G26529C','A26610G','C26681T','C26833T','C28958A']
from collections import Counter

h0 = Counter()
for mut in muts:
    try:
        for jj in list(dfAll.loc[pd.IndexSlice[mut,:]].index):
            h0[jj]+=1
        print(f"Samples with {mut}:")
        print(dfAll.loc[pd.IndexSlice[mut,:]])
    except:
        print(f"{mut} not found")

print(h0.most_common())

