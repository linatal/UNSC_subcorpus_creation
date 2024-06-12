import os
import argparse
from pathlib import Path
import configparser
import pandas as pd
import numpy as np



def get_topic_debates(df_meta, topics_list):
    # get only rows with one of topics
    df_metasub = df_meta[df_meta['topic'].str.contains('|'.join(topics_list))]
    # count occurence 
    df_count_debates = df_metasub["year"].value_counts()
    df_count_debates = df_count_debates.sort_index()
    # all basenames containing topic
    #debates_list = df_metasub["basename"].tolist()
    return df_count_debates#, debates_list


def filter_debates_outcome(df_meta, outcome_list):
    #standardize outcome column
    df_meta = df_meta.replace({np.nan: "None"})
    # standardize labels for outcome column
    #df_meta = df_meta.rename(columns={'outcome':'outcome_url'})
    values = ['PRST', 'RES', 'None']
    df_values = pd.DataFrame(values, columns=['values'])
    df_meta['outcome_label'] = list(map(lambda x: next((y for y in df_values['values'] if y in x), 'None'), df_meta['outcome']))
    # filter dataframe based on outcome
    df_meta_outcome = df_meta[df_meta['outcome_label'].isin(outcome_list)]
    return df_meta_outcome


def filter_debates_year(df, year_list):


def open_speeches(data_dir, df_count_debates):
    df_spch = pd.read_csv(data_dir + "speaker.tsv", sep="\t")
    # print(df_spch.columns)
    df_spchsub_topic = df_spch[df_spch['topic'].str.contains("Ukraine")]
    df_count_spch = df_spchsub_topic["year"].value_counts()
    df_count_spch = df_count_spch.sort_index()

    df_concat = pd.concat([df_count_spch.rename('num_speeches'), df_count_debates.rename('num_debates')], axis=1,
                          join="inner")
    # plt.figure()
    # df_concat.plot.bar()
    # plt.show()
    # list_spchsub = df_spch["topic"].tolist()

"""
def create_topic_table(undata_dir, data_dir):
    # merge undata table with Ukraine topics (=subjets) with meta.tsv, create new table
    df_undata = pd.read_csv(undata_dir+"results_UKRAINE.csv", sep=",")
    df_meta = pd.read_csv("output/meta_v2.tsv", sep="\t")
    print(df_undata.head())
    #prepare df_meta
    df_meta['basename_num'] = df_meta['basename'].str.extract('UNSC_\d{4}_SPV\.(\d{4})')
    print(df_meta['basename_num'][1])

    # prepare df_undata
    df_undata= df_undata.drop('001', axis=1)
    df_undata= df_undata.rename(columns={'191__a':'basename_short', '650__a':'Subject_1', '651__a':'Subject_2', '992__a':'datetime', '993':'presid_statement'})
    df_undata['basename_num'] = df_undata['basename_short'].str.extract('S\/PV\.(\d{4})')
    df_merged = pd.merge(df_meta, df_undata, on='basename_num')
    df_merged.to_csv('./output/meta_UKRAINE.tsv', index=False, sep='\t')

    print(df_merged)
"""
# ---check flags
def check_topic_flag(flag_topic, df):
    if flag_topic is not None:
        topics_list = flag_topic
        print(f"Debates are filtered by topic(s): {topics_list}")
        df_topic = get_topic_debates(df, topics_list)
        return df_topic
    else:
        print('No topic selected.')
        return df

def check_outcome_flag(flag_outcome, df):
    # filters debates based on outcome (Press Release vs. Resolution vs. None)
    outcome_list = flag_outcome
    if outcome_list is not None:
        print(f"Debates are filtered by outcome type(s): {outcome_list}")
        df_outcome = filter_debates_outcome(df, outcome_list)
    else:
        print('No outcome selected.')
        return df

def check_year_flag(flag_year, df):
    # filters debates based on year (input: flag_year[list with two int])
    year_list = flag_year
    if year_list is not None:
        print(f"Debates are selected by years between: {year_list}")
        df_year = filter_debates_year(df, year_list)
    else:
        print('No years selected.')
        return df



if __name__ == '__main__':
    # manage flags
    parser = argparse.ArgumentParser(prog="create_subcorpus.py", description="Creates subcorpus based on agenda topic and "
                                    "optionally based on start and end year. For subcorpus creation use flag -c. ")
    #parser.add_argument("-t", "--topic", nargs="+", default=["Iraq"]) # creates list of topic entries
    parser.add_argument("-t", "--topic", nargs="+")  # creates list of topic entries
    parser.add_argument('-y', "--year", nargs=2, type=int) # creates list of start and end year "-y 2024 2025"
    parser.add_argument("-o", "--outcome", nargs="+") # creates list of outcomes: 'PRST', 'RES', 'None'
    parser.add_argument("-c", "--create", action="store_true")     # boolean value, default True
    args = parser.parse_args()

    # manage paths in config file
    config = configparser.ConfigParser()
    #config.read("config.ini") #CHANGE
    config.read("config_temp.ini")

    meta_path = config['DATA_INPUT']['meta_table']
    df_meta = pd.read_csv(meta_path, sep="\t")

    df_topic_debates = check_topic_flag(args.topic, df_meta)
    df_outcome_debates = check_outcome_flag(args.outcome, df_topic_debates)
    df_year_debates = check_year_flag(args.year, df_outcome_debates)

    # filter debates based on start-end year
    if args.outcome is not None and args.year is not None:
        year = args.year

    if args.create == True:
        output_speeches = config['DATA_OUTPUT']['output_dir'] + "/speeches_subcorpus"
        print(f"Create subcorpus in {output_speeches}")



    '''
    spch_dir = ROOT_DIR + "/data/speeches_spv7658/preprocessed_spch/"
    data_dir = ROOT_DIR + "/data/"
    undata_dir = ROOT_DIR + "/data/digitallibrary_query/"
    '''

    #open_speeches(data_dir, count_debates)
    #df_meta_v2 = filter_debates_outcome(df_meta)
    #create_topic_table(undata_dir, data_dir)



