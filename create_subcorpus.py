import os
import argparse
from pathlib import Path
import configparser
import pandas as pd
import numpy as np
import shutil


def get_topic_debates(topics_list, df_meta):
    # get only rows with one of topics
    df_metasub = df_meta[df_meta['topic'].str.contains('|'.join(topics_list))]
    # count occurence 
    df_count_debates = df_metasub["year"].value_counts()
    df_count_debates = df_count_debates.sort_index()
    # all basenames containing topic
    return df_count_debates


def filter_debates_outcome(outcome_list, df_meta):
    #standardize outcome column
    df_meta = df_meta.replace({np.nan: "None"})
    # standardize labels for outcome column
    values = ['PRST', 'RES', 'None']
    df_values = pd.DataFrame(values, columns=['values'])
    df_meta['outcome_label'] = list(map(lambda x: next((y for y in df_values['values'] if y in x), 'None'), df_meta['outcome']))
    # filter dataframe based on outcome
    df_meta_outcome = df_meta[df_meta['outcome_label'].isin(outcome_list)]
    return df_meta_outcome


def filter_debates_year(year_list, df):
    x = range(year_list[0], year_list[1]+1)
    listi = [xi for xi in x]
    df_year = df[df['year'].isin(listi)]
    return df_year


def create_corpus(df, df_speech_meta, dir_path, output_dir_path):
    # copies filtered speech-txt-files from orig corpus into subcorpus
    # get basenames(=debates) from subcorpus meta table, filter speech-meta table based on basenames
    output_dir_path = output_dir / "speeches_subcorpus"
    basename_list = df['basename'].tolist()
    df_spchs_filtered = df_speech_meta[df_speech_meta['basename'].isin(basename_list)]

    speeches_list = df_spchs_filtered['filename'].tolist()
    # create output folder if not exists, if exists delete and create a new folder
    if not output_dir_path.exists():
        os.makedirs(output_dir_path)
    elif output_dir_path.exists() and output_dir_path.is_dir():
        shutil.rmtree(output_dir_path)
        os.makedirs(output_dir_path)

    for sp in speeches_list:
        speech_path = Path.joinpath(dir_path, sp)
        copy_speech_path = Path.joinpath(output_dir_path, sp)
        if not speech_path.exists():
            print(f"Warning {speech_path} does not exist.")
        else:
            shutil.copy(speech_path, copy_speech_path)
    return df, df_speech


# ---check flags
def check_topic_flag(flag_topic, df):
    if flag_topic is not None:
        topics_list = flag_topic
        print(f"Debates are filtered by topic(s): {topics_list}")
        df_topic = get_topic_debates(topics_list, df)
        return df_topic
    else:
        print('No topic selected.')
        return df


def check_outcome_flag(flag_outcome, df):
    # filters debates based on outcome (Press Release vs. Resolution vs. None)
    outcome_list = flag_outcome
    if outcome_list is not None:
        print(f"Debates are filtered by outcome type(s): {outcome_list}")
        df_outcome = filter_debates_outcome(outcome_list, df)
    else:
        print('No outcome selected.')
        return df


def check_year_flag(flag_year, df):
    # filters debates based on year (input: flag_year[list with two int])
    year_list = flag_year
    print(year_list)
    if year_list is not None:
        print(f"Debates are selected by years between: {year_list}")
        df_year = filter_debates_year(year_list, df)
        return df_year
    else:
        print('No years selected.')
        return df


if __name__ == '__main__':
    # manage flags
    # TODO keyerror when using more than one flag
    parser = argparse.ArgumentParser(prog="create_subcorpus.py", description="Creates subcorpus based on agenda topic and "
                                    "optionally based on start and end year. For subcorpus creation use flag -c. ")
    parser.add_argument("-t", "--topic", nargs="+")  # creates list of topic entries
    parser.add_argument("-y", "--year", nargs=2, type=int) # creates list of start and end year '-y 2024 2025'
    parser.add_argument("-o", "--outcome", nargs="+") # creates list of outcomes: 'PRST', 'RES', 'None'
    parser.add_argument("-c", "--create", action="store_true")     # boolean value, default True
    args = parser.parse_args()

    # manage paths in config file
    config = configparser.ConfigParser()
    #config.read("config.ini") #CHANGE
    config.read("config_temp.ini")

    meta_path = config['DATA_INPUT']['meta_table']
    speaker_path = config['DATA_INPUT']['speaker_table']
    df_meta = pd.read_csv(meta_path, sep="\t")
    df_speech = pd.read_csv(speaker_path, sep="\t")

    df_topic_debates = check_topic_flag(args.topic, df_meta)
    df_outcome_debates = check_outcome_flag(args.outcome, df_topic_debates)
    df_year_debates = check_year_flag(args.year, df_outcome_debates)

    if args.create is True:
        output_dir = Path(config['DATA_OUTPUT']['output_dir'])

        orig_speeches = Path(config['DATA_INPUT']['corpus_raw_dir'])

        print(f"Create subcorpus in {output_dir}")
        df_meta_filtered, df_speaker_filtered = create_corpus(df_year_debates, df_speech, orig_speeches, output_dir)

        # create speeches-metadata table
        df_meta_filtered.to_csv(output_dir / "meta_subcorpus.csv", index=False)
        df_speaker_filtered.to_csv(output_dir / "speeches_subcorpus.csv", index=False)






