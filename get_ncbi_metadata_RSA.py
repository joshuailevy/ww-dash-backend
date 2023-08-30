import pandas as pd
def pull_sample_bed(accID):
    df = pd.read_csv('wastewater_ncbi_RSA.csv',index_col=0)
    scheme = df.loc[accID,'amplicon_PCR_primer_scheme']
    if 'QIAseq' in scheme or 'v3' in scheme:
        print('ARTICv3')
    elif 'V5.3' in scheme:
        print('ARTICv5.3.2')
    elif 'V4.1' in scheme:
        print('ARTICv4.1')
    elif 'SNAP' in scheme:
        print('snap_primers')
    else:
        print('unknown_scheme')


if __name__=="__main__":
    from Bio import Entrez
    from Bio import SeqIO
    Entrez.email = "jolevy@scripps.edu"
    # handle = Entrez.esearch(db="sra", idtype='acc', retmax=10000, term="((wastewater metagenome[Organism] OR (wastewater metagenome[Organism] OR wastewater metagenome[All Fields])) AND (Severe acute respiratory syndrome coronavirus 2[Organism] OR (Severe acute respiratory syndrome coronavirus 2[Organism] OR sars-cov-2[All Fields]))) AND strategy wgs[Properties]")#, idtype="acc")
    handle = Entrez.esearch(db="sra", idtype='acc', retmax=1000,
                            sort='recently_added',
                            term="SARS-CoV-2[All Fields] AND wastewater[All Fields] AND south africa[All Fields]") 
    record = Entrez.read(handle)
    handle.close()

    handle = Entrez.efetch(db="sra", id=record['IdList'], rettype="gb",retmode='text')
    string= handle.read()
    handle.close()

    returned_meta=str(string,'UTF-8')

    with open("NCBI_metadata_RSA.xml", "w") as f:
        f.write(returned_meta)
    # #parse xml
    import xml.etree.ElementTree as ET
    root = ET.fromstring(returned_meta)
    allDictVals = {}

    for root0 in root:
        ### pull all sample attributes
        vals = [r.text for r in root0.findall('.//SAMPLE_ATTRIBUTE/')]
        print(vals)
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
    df['collection_date'] = pd.to_datetime(df['collection_date'])
    df = df.sort_values(by='collection_date',ascending=False)
    ## add last 
    # df = df[df['collection_date'] >='2023-07-20']
    df.to_csv('wastewater_ncbi_RSA.csv')



