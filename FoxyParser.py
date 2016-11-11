    # Python 3.5
import xml.etree.ElementTree as ET
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def xml_checker(file_name):
    '''Runs a check to confirm a .xml file has been entered'''
    assert file_name.endswith('.xml'), ' wrong file type entered'
    return(check_file(file_name))
    
def check_file(file_name):
    ''' check the input file is an LRG and return root '''    
    tree = ET.parse(file_name)
    root = tree.getroot()
    assert root.tag == 'lrg', 'Input file must be an LRG'
    return(check_public(root))

def check_public(root):
    ''' Checks that the LRG file is a public file. for pending files issues a warning regarding completeness'''
    if root.findall("./fixed_annotation/*")[4].tag == 'source':
        print('done checks')
        return(root)
    else:
        print ('Warning! this is a pending LRG file and may be subject to modification')
        return(root)

def get_data(root):
    ''' extract data from xml and store in a pandas dataframe (and other variables) '''
    # define an empty dataframe to accept parsed exon data relative to lrg coordinate from xml file
    df_exon_rel = pd.DataFrame(columns=['exon_no','start','end'])
    # get LRG id and genomic sequence
    lrg_id = root.findall('./fixed_annotation/id')[0].text
    genomic_sequence = root.findall('./fixed_annotation/sequence')[0].text
    # define empty lists to hold parsed exon data
    ex_label = []
    ex_start = []
    ex_end = []
    ex_strand = []
    
    # loop through exons pulling out exon number, start and stop position
    for item in root.findall('./fixed_annotation/transcript/exon'):
        ex_label.append(item.attrib['label'])
        ex_start.append(int(item[0].attrib['start'])-1)
        ex_end.append(int(item[0].attrib['end']))
        #ex_strand.append(item[0].attrib['strand'])
    
    # enter data from lists into pandas dataframe
    for i in range(len(ex_label)):
        df_exon_rel.loc[df_exon_rel.shape[0]] = [ex_label[i],ex_start[i],ex_end[i]]

    #df_exon_rel['seq'] = genomic_sequence[df_exon_rel.start:df_exon_rel.end]
    # check that coordinates are in correct spatial orientation
    for j in range(len(df_exon_rel['start'])):
        assert int(df_exon_rel['end'].loc[j]) > int(df_exon_rel['start'].loc[j]), 'the exon coordinate order may be wrong'
    
    # return dataframe for further analysis
    print('done get data')

    return(df_exon_rel)

def add_sequence(df_exon_rel,root):
    ''' find genomic sequence for each exon '''
    # find genomic sequence by LRG coordinates
    genomic_sequence = root.findall('./fixed_annotation/sequence')[0].text.upper()
    # check that the genomic sequence conforms to standard DNA bases
    assert set(genomic_sequence) == set(['A', 'C', 'T', 'G']), 'Unexpected characters found in genomic sequence.'
    # add temporary indexing columns to df for sequence slice
    df_exon_rel['int_start'] = df_exon_rel.start.astype(int)
    df_exon_rel['int_end'] = df_exon_rel.end.astype(int)
    # calulate exon length and add to dataframe
    df_exon_rel['exon_length'] = df_exon_rel['int_end'] - df_exon_rel['int_start']
    df_exon_rel['seq'] = [(genomic_sequence[
        (df_exon_rel.int_start.loc[i]):(df_exon_rel.int_end.loc[i])]) for i in range(len(df_exon_rel.start))]
    # remove intermediary indexing columns
    df_exon_rel = df_exon_rel[['exon_no','start','end','exon_length','seq']]
    # check that sequence legth matches the exon length
    for i in range(len(df_exon_rel.start)):
        len(df_exon_rel.seq.loc[i]) == df_exon_rel.exon_length.loc[i],
        "Sequence length doesn't match exon length"
    return df_exon_rel

def genome_loc(df_exon_rel, root):
    ''' Extract exome genome cordinates for build GRC37'''
    # Generate list to extract inofrmation of genome build, chromosome, genomic start and stop possition and build assembly type
    GRCh_build = []
    GRCh_chr = []
    GRCh_start = []
    GRCh_end = []
    GRCh_strand = []
    GRCh_type = []
    
    # define an empty dataframe to accept genome build informtion from xml file
    df_gen_build = pd.DataFrame(columns=['Build','Chr', 'g_start','g_end', 'strand', 'type'])
    
    # loop through LRG file to pull out genomic information
    for item in root.findall('updatable_annotation/annotation_set[@type="lrg"]/mapping'):
        GRCh_build.append(item.attrib['coord_system'])
        GRCh_chr.append(item.attrib['other_name'])
        GRCh_start.append(item.attrib['other_start'])
        GRCh_end.append(item.attrib['other_end'])
        GRCh_type.append(item.attrib['type'])
    # pull in stand from next layer down mapping_span
    for item in root.findall('updatable_annotation/annotation_set[@type="lrg"]/mapping/mapping_span'):   
        GRCh_strand.append(item.attrib['strand'])
       
    # enter genome build data from lists into pandas dataframe
    for i in range(len(GRCh_build)):
        df_gen_build.loc[df_gen_build.shape[0]] = [GRCh_build[i], GRCh_chr[i], GRCh_start[i], GRCh_end[i],GRCh_strand[i], GRCh_type[i]]
    
    print('done genome build')

    return df_gen_build

def leg (df_gen_build, df_exon_rel):
    '''Location of Exome in Genome'''
    
    for i in range(len(df_gen_build.Build)):
        # checks that the genome build is canonical
        if 'assembly' in str(df_gen_build.type.loc[i]):
            # check the stand orientation
            
            if str(df_gen_build.strand.loc[i]) == "-1":
                print('on reverse strand')
                # generate a list of lrg star positions and a ver for genomic end possition
                g_loc = df_gen_build.at[i,'g_end']
                lrg_loc_s = []
                lrg_loc_e = []
                #g_loc_e = df_gen_build.at[i,'g_start']
                
                # populate list of lrg possitions
                for l in range(len(df_exon_rel.exon_no)):
                    lrg_loc_s.append(df_exon_rel.start.loc[l])    
                    lrg_loc_e.append(df_exon_rel.end.loc[l])
                # loop through calculate genomic start pos for rev strand
                exon_pos_s = [int(g_loc) - int(lrg_loc_s[x]) for x in range(len(lrg_loc_s))]
                df_exon_rel[(df_gen_build.Build.loc[i])+'_start'] = exon_pos_s
                
                # loop through calculate genomic pos for rev strand
                exon_pos_e = [int(g_loc) - int(lrg_loc_e[x]) + 1 for x in range(len(lrg_loc_s))]
                df_exon_rel[(df_gen_build.Build.loc[i])+'_end'] = exon_pos_e
            
            elif str(df_gen_build.strand.loc[i]) == "1":
                print('on Forward strand')
                
                # generate a list of lrg star positions and a ver for genomic end possition 
                g_loc = df_gen_build.at[i,'g_start']
                lrg_loc_s = []
                lrg_loc_e = []
                
                # populate list of lrg possitions
                for l in range(len(df_exon_rel.exon_no)):
                    lrg_loc_s.append(df_exon_rel.start.loc[l])  
                    lrg_loc_e.append(df_exon_rel.end.loc[l])
                    
                # loop through calculate genomic start pos for rev strand
                exon_pos_s = [int(g_loc) + int(lrg_loc_s[x]) for x in range(len(lrg_loc_s))]
                df_exon_rel[(df_gen_build.Build.loc[i])+'_start'] = exon_pos_s
                                # loop through calculate genomic pos for rev strand
                exon_pos_e = [int(g_loc) + int(lrg_loc_e[x]) - 1 for x in range(len(lrg_loc_s))]
                df_exon_rel[(df_gen_build.Build.loc[i])+'_end'] = exon_pos_e
                
                print('genLoc:', df_gen_build.Build.loc[i])
               
            else:
                print("Problem! DNA should only have two strands, this has more, so cant be DNA")
    return df_exon_rel

def main(infile):
    '''launches main workflow for parsing LRG dtat from xml'''
    # run checks on file type
    checked = (xml_checker(infile)) 
    # checked = root
    # find LRG id for gene
    lrg_id = checked.findall('./fixed_annotation/id')[0].text
    # find gene symbol
    symbol = checked.findall('./updatable_annotation/annotation_set/features/gene/symbol')[0].attrib['name']
    # retive relative exon data from LRG
    exon_data = get_data(checked)
    # exon_data is the df_exon_rel dataframe
    # calculate exon lengths and get exon sequences
    exon_data_with_seq = add_sequence(exon_data,checked)
    genome_build = genome_loc(exon_data, checked)
    # genome_build is the df_gen_build dataframe
    exon_gen_pos = leg(genome_build, exon_data_with_seq)
    #print(exon_data)
    print('LRG id :',lrg_id)
    print('Gene symbol :',symbol)
    print(exon_data_with_seq)
    print()
    #print(genome_build)

    return exon_data

main('LRG_517.xml') # NEED TO CHANGE SO NOT HARD CODED
    

