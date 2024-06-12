# Preparing Subcorpus Selection for UNSCon (based on Debates)

### Prerequesites
Download requirements via pip: 
```pip install requirements.txt```

### Prepare Corpus
1. Download the original "UN Security Council Debates" corpus from https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/KGVSYH
(Schoenfeld et. al 2019) containing all debates. 
2. Unzip directory ``dataverse_files.zip`` and extract subdirectiory ``speeches.tar``. 
3. Copy ``dataverse_files`` into ``/data`` project folder . The pr
```
- /UNSC_subcorpus_creation
-- /data
---- /dataverse_files
------ speaker.tsv
------ meta.tsv
------ /speaker
------ ...
-- /output
-- topics.py
-- config.ini
```

### Flags 
``python topic.py  [-h] [--topic] [-y] [-o] [-c]``

#### Output
The default output is a list of debates on the console. To create a new folder containing a subcorpus with debates 
and speeches and metadata based on filters (see below), please use the ``--create`` flag.

**--create**: If set, the script will create a subcorpus in ``/outcome``.
``python topic.py --topic [-t] True``

#### Filter
**--topic**: defines one or more topics that the subcorpus should cover. The input is one or more strings.
``python topic.py --topic [-t] "Ukraine"``  
``python topic.py --topic [-t] "Ukraine" "Iraq"``

**--year**: defines start and end year according to which the debates should be filtered. Accepts two integers as input in format yyyy.  
``python topic.py --year [-y] 2014 2018``

**--outcome**: Some debates have either a Press Statement (```"PRST"```), Resolution (```"RES"```) or no outcome (```"None"```). 
Flag defines one or more outcomes according to which the debates should be filtered.  
``python topic.py --outcome [-o] "PRST"``  
``python topic.py --outcome [-o] "PRST" "None"``

It is possible to define several filters. The next command is creating a subcorpus and metadata with debates on Iraq from 2024.  
``python topic.py --topic "Iraq" --year 2024 2024 --create``


TODO: 
- input path: Preprocessed UNSCcorpus speeches, metadata debates
- input flags: start_year--> meta[topics], end_year --> meta[year], topics --> meta[topics]
- output: len debates, list of debates (print), len speeches (from meta)

TODO: 
- additional input flag --create True (default: False)
- use list of debates to:
    - create subcorpus_dir
    - create subcorpus_meta and subcorpus_speeches
    - create subcorpus_speeches, copy subcorpus_speeches.txt to it 

potential TODO on subcorpus:
- voting behaviour:
    - extract resolution info S/RES/\d\d\d\d from meta[outcome] 
    - use UN library API, and search for voting behaviour
- sentiment analysis with lexicoder



