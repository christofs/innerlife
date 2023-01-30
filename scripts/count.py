"""
Script to count verbs of "inner life" in collections of unannotated files. 
Uses spacy for annotation. (Optimization: use TreeTagger with PRESTO model for 18th century.)
Outputs verb count information in the same style as Lou's and/or Diana's scripts, for compatibility. 

Script written by Christof Schöch (Trier), January 2023. 
"""


# === Imports ===

#== Basics
import os
import random
import re
from os.path import join
import numpy as np
import glob

#== Data
import pandas as pd
import seaborn as sns

# Linguistic annotation
import spacy
import fr_dep_news_trf


# === Global variables ===

# Files outside the innerlife repository
metadatafile = join("/", "media", "christof", "Data", "Github", "mimotext", "roman18", "XML-TEI", "xml-tei_metadata.tsv")

# Local data
workdir = join(os.path.realpath(os.path.dirname(__file__)), "..")
annotatedfolder = join(workdir, "data", "fra18", "annotated", "*.csv")
verbsfile = join(workdir, "data", "fra18", "verbs.csv")
resultsfile = join(workdir, "data", "fra18", "manualCounts.dat")


# === Functions === 


def read_metadatafile(): 
    """
    Reads the metadatafile from the romsn18 repository. 
    Returns: DataFrame. 
    """
    with open(metadatafile, "r", encoding="utf8") as infile: 
        metadata = pd.read_csv(infile, sep="\t", index_col="filename")
    return metadata


def get_pubyear(metadata, basename): 
    """
    Extracts the year of first publication for the current text from the metadata table.
    Returns: int (year)
    """
    pubyear = int(metadata.loc[basename, "reference-year"])
    return pubyear


def read_verbsfile(): 
    """
    Reads the file with the list of verbs of inner life, 
    along with the different categories of verbs. 
    Returns: Three lists (lemmas, categories, combined labels)
    """
    with open(verbsfile, "r", encoding="utf8") as infile: 
        data = pd.read_csv(infile, sep=";")
    verblemmas = list(data["lemma"])
    verbcats = list(data["category"])
    verblabels = []
    for i in range(0, len(verblemmas)): 
        verblabels.append(verblemmas[i] + ":" + verbcats[i])
    #print(verblabels)
    return verblemmas, verbcats, verblabels


def read_annotated(file): 
    """
    Reads an annotated text file from the folder. 
    Returns: list (each item containing one line / token). 
    """
    with open(file, "r", encoding="utf8") as infile: 
        annotated = pd.read_csv(infile, sep="\t")
    annotated.columns = ["wordform", "pos", "lemma"]
    return annotated


def count_verbs(annotated, verblemmas): 
    """
    Establishes the number of tokens marked as a verb in the annotated text (=allverbcounts). 
    Establishes the count of each individual verb from the list of verbs of inner life (=indverbcounts). 
    Calculates the sum of counts of verbs of inner life (=innerverbcounts). 
    Returns: int, int, dict
    """
    verbs = annotated[annotated["pos"] == "VERB"]
    #print(verbs.head(10))
    allverbscount = len(verbs)
    innerverbs = verbs[verbs["lemma"].isin(verblemmas)]
    innerverbscount = len(innerverbs)
    indverbcounts = {}
    for lemma in verblemmas: 
        indverbcounts[lemma] = len([verb for verb in list(verbs["lemma"]) if lemma in verb])
    #print(indverbcounts)
    return allverbscount, innerverbscount, indverbcounts


def save_verbcounts(data, verblabels): 
    """
    Saves the combined data from each text to disc. 
    Renames the columns to include the verb category for each individual verb. 
    Returns: nothing (but saves CSV to disk)
    """
    labels = ["0TextId", "year", "verbs", "innerVerbs"]
    labels.extend(verblabels)
    data_df = pd.DataFrame.from_dict(data, orient="columns").T
    data_df.columns = labels
    with open(resultsfile, "w", encoding="utf8") as outfile: 
        data_df.to_csv(outfile, sep=" ", index=None)


# === Coordination function === 

def main():
    """
    Coordindates the entire process. 
    Some things need to be done only once (get metadata, get verbs). 
    Then loops over each text to get year of publication and establish verb counts.
    Verb count information is collected and saved to disk in the end. 
    """
    metadata = read_metadatafile()
    verblemmas, verbcats, verblabels = read_verbsfile()
    progress = 0
    data = {}
    for file in glob.glob(annotatedfolder): 
        basename, ext = os.path.basename(file).split(".")
        #print("Next:", basename)
        pubyear = get_pubyear(metadata, basename)
        annotated = read_annotated(file)
        allverbcounts, innerverbcounts, indverbcounts = count_verbs(annotated, verblemmas)
        verbdata = {"0TextId" : basename, "pubyear" : pubyear, "verbs" : allverbcounts, "innerVerbs" : innerverbcounts} 
        verbdata.update(indverbcounts)
        #TESTDATA#verbdata = {'0TextId': 'Pertusier_Premiere', 'pubyear': 1800, 'verbs': 13310, 'innerVerbs' : 9999, 'voir': 1008, 'regarder': 15, 'sentir': 29, 'apercevoir': 27, 'vouloir': 132, 'oser': 62, 'compter': 20, 'essayer': 0, 'savoir': 104, 'trouver': 73, 'croire': 84, 'entendre': 65, 'attendre': 94, 'connaître': 66, 'devoir': 65, 'falloir': 121, 'espérer': 17, 'valoir': 6, 'refuser': 9, 'accepter': 6, 'engager': 19, 'aimer': 50, 'manquer': 9, 'souffrir': 10, 'craindre': 32}
        data[basename] = verbdata
        progress +=1
        print("Done:", progress, basename, pubyear)
    save_verbcounts(data, verblabels)

main()



