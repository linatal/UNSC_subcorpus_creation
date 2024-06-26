# Subcorpus Creation for UNSC Corpus
The project helps to select debates in the UNSC Debates Corpus (covering debates 1995-2020 (v5), see Schönfeld et al. 2019) based on different factors for further analysis.


## Prerequisites
Download requirements via pip: 
```pip install requirements.txt```

## Prepare Corpus
1. Download the original "UN Security Council Debates" corpus from https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/KGVSYH
(Schoenfeld et al. 2019) containing all debates. 
2. Unzip directory ``dataverse_files.zip`` and extract subdirectiory ``speeches.tar``. 
3. Copy ``dataverse_files`` into ``/data`` project folder . The projectstructure should look like the following:
```
- /UNSC_subcorpus_creation
-- /data
---- /dataverse_files <--original UNSC corpus
------ speaker.tsv
------ meta.tsv
------ /speaker
------ ...
-- /output
-- create_subcorpus.py
-- config.ini
```

## Setting Flags for Filtering   
``$python create_subcorpus.py  [-h] [-t] [-y] [-o] [-c]``

### Output
The default output is a list of debates that meet the requirements on the console. To create a new folder containing a subcorpus with debates 
and speeches and metadata based on filters (see below), please use the ``--create`` flag.

**--create**  
If set, the script will create a subcorpus in ``/outcome``.  
``$python create_subcorpus.py --create``

### Filter Topics:
It is possible to filter the debates by topic. The Corpus includes over 5,000 topics, therefore we cannot provide a list
of all possible topics. It is possible to specify a substring (default) or search for an exact match (--exact_match).
The corpus includes several subtopics, which can also be included in the search to broaden the search  (--subtopics) (TODO).

**--topic + str**  
defines one or more topics that the subcorpus should cover. The input is one or more strings.  
``$python create_subcorpus.py --topic "Ukraine"``  
``$python create_subcorpus.py --topic "Ukraine" "Iraq"``  
**--exact_match**   
If set, substring search is changed to exact match search.
``$python create_subcorpus.py --topic "Iraq-Kuwait" --exact_match``    
(TODO) **--subtopics**  
If set, the script searches in topics and subtopics for the topic-query.  
``$python create_subcorpus.py --topic "Iraq-Kuweit" --subtopics`` 

### Other Filters
**--year + int int**  
defines start and end year according to which the debates should be filtered. Accepts two integers as input in format yyyy.  
``$python create_subcorpus.py --year 2014 2018``

**--outcome + str**:  
Some debates either have a Press Statement (```"PRST"```), Resolution (```"RES"```) or no outcome (```"None"```). 
The flag defines one or more outcomes according to which the debates should be filtered.  
``$python create_subcorpus.py --outcome "PRST"``  
``$python create_subcorpus.py --outcome "PRST" "None"``

It is possible to define several filters. The next command is creating a subcorpus and metadata with debates on Iraq from 2024.  
``$python create_subcorpus.py --topic "Iraq" --year 2024 2024 --create``


--------------

potential TODO on subcorpus:
- voting behaviour:
    - extract resolution info S/RES/\d\d\d\d from meta[outcome] 
    - use UN library API, and search for voting behaviour
- new github project: sentiment analysis with lexicoder --> add filter



