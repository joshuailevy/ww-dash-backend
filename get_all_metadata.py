import pandas as pd
import os
import numpy as np
import shortuuid

if __name__=="__main__":
    accIDs = [id0.split('.tsv')[0] for id0 in os.listdir('vars/')]

    from Bio import Entrez
    from Bio import SeqIO
    Entrez.email = "jolevy@scripps.edu"

    handle = Entrez.efetch(db="sra", id=accIDs, rettype="gb",retmode='text')
    string= handle.read()
    handle.close()

    returned_meta=str(string,'UTF-8')

    with open("NCBI_metadata_ALL.xml", "w") as f:
        f.write(returned_meta)
    # #parse xml
    import xml.etree.ElementTree as ET
    root = ET.fromstring(returned_meta)
    allDictVals = {}

    for root0 in root:
        ### pull all sample attributes
        vals = [r.text for r in root0.findall('.//SAMPLE_ATTRIBUTE/')]
        sampExp = [r.text for r in root0.findall('.//EXPERIMENT/IDENTIFIERS/PRIMARY_ID')]
        seq_meta = [r.text for r in root0.findall('.//RUN_SET/RUN/RUN_ATTRIBUTES/RUN_ATTRIBUTE/')]
        sampID =  [r.text for r in root0.findall('.//RUN_SET/RUN/IDENTIFIERS/PRIMARY_ID')]
        if len(sampID)>1:
            print('more than one experiment... add funcs')
            asdfa
        else:
            sampID = sampID[0]
        ## write to dictionary form
        dictVals = {vals[i].replace(' ','_'):vals[i+1] for i in range(0,len(vals),2)}
        for i in range(0,len(seq_meta),2):
            dictVals[seq_meta[i].replace(' ','')] = seq_meta[i+1]
        dictVals['experiment_id'] = sampID
        dictVals['SRA_id'] = root0[0].attrib['accession']
        allDictVals[sampID] =dictVals

    df = pd.DataFrame(allDictVals).T

    df.columns = df.columns.str.replace(' ','_')
    # df = df[df['collection_date'].str.startswith('20')]
    df['collection_date'] = pd.to_datetime(df['collection_date'].apply(lambda x: x.split('/')[0] if '/' in x and len(x.split('/')[0])>2 else x))
    df = df.sort_values(by='collection_date',ascending=False)
    df['geo_loc_ENA'] = df[["geographic_location_(country_and/or_sea)",'geographic_location_(region_and_locality)']].apply(lambda row:': '.join(row.values.astype(str)), axis=1)
    df['geo_loc_name'] = df['geo_loc_name'].combine_first(df['geo_loc_ENA'])
    merged = df['geo_loc_name']+df['ww_population'].fillna('').astype(str)
    merged = merged.apply(lambda x:shortuuid.uuid(x)[0:12])
    df['site id'] = df['collection_site_id'].combine_first(merged)
    ## add last 
    # df = df[df['collection_date'] >='2023-07-20']
    df.to_csv('wastewater_ncbi_ALL.csv')



