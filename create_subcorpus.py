import os
import argparse
from pathlib import Path
import configparser
import pandas as pd
import numpy as np
import shutil


def get_topic_debates(topics_list, exact_match, df_meta):
    topics_list_lw = [x.lower() for x in topics_list] #lowercase input
    df_meta['topic_lc'] = df_meta['topic'].map(lambda x: x.lower() if isinstance(x,str) else x) # create lw topics column
    # check len topics input
    if len(topics_list_lw) == 1:
        new_str_topic = topics_list_lw[0]
        print("topic regex:", new_str_topic)
    elif len(topics_list_lw) > 1:
        new_str_topic = "|".join(topics_list_lw) # transpose list for regex
        print("topic regex:", new_str_topic)
    else:
        print("something went wrong, check topics input list")
    # check exact match
    if exact_match:
        df_metasub = df_meta[df_meta['topic_lc'].str.fullmatch(new_str_topic)] # if row is eq input_topic string
    elif not exact_match:
        df_metasub = df_meta[df_meta['topic_lc'].str.contains(new_str_topic)] # if row is eq or contains input_topic string

    topics = set(df_metasub['topic'].tolist())
    print(f"The following topics were found: {topics}")
    print(f"Extracted {df_metasub.shape[0]} debates based on chosen topics.")

    return df_metasub.drop(columns=['topic_lc'])


def get_debates_outcome(outcome_list, df_meta):
    #standardize outcome column
    df_meta = df_meta.replace({np.nan: "None"})
    # standardize labels for outcome column
    values = ['PRST', 'RES', 'None']
    df_values = pd.DataFrame(values, columns=['values'])
    df_meta['outcome_label'] = list(map(lambda x: next((y for y in df_values['values'] if y in x), 'None'), df_meta['outcome']))
    # filter dataframe based on outcome
    df_meta_outcome = df_meta[df_meta['outcome_label'].isin(outcome_list)]
    print(f"Extracted {df_meta_outcome.shape[0]} debates based on chosen topics and outcomes.")
    return df_meta_outcome


def get_debates_year(year_list, df):
    x = range(year_list[0], year_list[1]+1)
    listi = [xi for xi in x]
    df_year = df[df['year'].isin(listi)]
    print(f"Extracted {df_year.shape[0]} debates based on chosen topics, outcomes and years.")
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
    return df, df_spchs_filtered


# ---check flags
def check_topic_flag(flag_topic, flag_exact, df):
    if flag_topic is not None:
        topics_list = flag_topic
        print(f"Debates are filtered by topic(s): {topics_list}")
        df_topic = get_topic_debates(topics_list, flag_exact,  df)
        return df_topic
    else:
        print('No topic selected.')
        return df


def check_outcome_flag(flag_outcome, df):
    # filters debates based on outcome (Press Release vs. Resolution vs. None)
    outcome_list = flag_outcome
    if outcome_list is not None:
        print(f"Debates are filtered by outcome type(s): {outcome_list}")
        df_outcome = get_debates_outcome(outcome_list, df)
    else:
        print('No outcome selected.')
        return df


def check_year_flag(flag_year, df):
    # filters debates based on year (input: flag_year[list with two int])
    year_list = flag_year
    if year_list is not None:
        print(f"Debates are selected by years between: {year_list}")
        df_year = get_debates_year(year_list, df)
        return df_year
    else:
        print('No years selected.')
        return df


if __name__ == '__main__':
    # manage flags

    parser = argparse.ArgumentParser(prog="create_subcorpus.py", description="Creates subcorpus based on agenda topic, "
                                    "outcome, start and end year. For subcorpus creation use flag --create. ")
    parser.add_argument("-t", "--topic", nargs="+")  # creates list of topic entries
    parser.add_argument("--exact_match", action="store_true") # boolean value, default False
    #parser.add_argument("--subtopics", action="store_true") # boolean value, default False

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

    exmat = args.exact_match
    df_topic_debates = check_topic_flag(args.topic, exmat, df_meta)
    df_outcome_debates = check_outcome_flag(args.outcome, df_topic_debates)
    df_year_debates = check_year_flag(args.year, df_outcome_debates)

    if args.create is True:
        print(f"Will create subcorpus with {len(df_year_debates)} debates.")
        a = input("Continue? [y(es)/n(o)] ")
        if a.lower() == "yes" or a.lower() == "y":
            output_dir = Path(config['DATA_OUTPUT']['output_dir'])

            orig_speeches = Path(config['DATA_INPUT']['corpus_raw_dir'])

            print(f"Create subcorpus in directory: ./{output_dir}")
            df_meta_filtered, df_speaker_filtered = create_corpus(df_year_debates, df_speech, orig_speeches, output_dir)

            # create speeches-metadata table
            df_meta_filtered.to_csv(output_dir / "meta_subcorpus.csv", index=True)
            df_speaker_filtered.to_csv(output_dir / "speeches_subcorpus.csv", index=True)
        elif a.lower() == "no" or a.lower() == "n":
            print("User input is 'NO'. Corpus creation aborted.")
        else:
            print("User input is invalid. Corpus creation aborted.")
    else:
        output_list = df_year_debates['basename'].tolist()
        print(f"{len(output_list)} debates meet the criteria:")
        print(output_list)






