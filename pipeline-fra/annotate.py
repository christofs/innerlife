"""
Script to annotate plain text with spacy for annotation. 

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

# Local data
workdir = join("/", "media", "christof", "Data", "Drive", "03_Academic", "03_Aktionen", "1-Aktuell", "2023_innerlife")
textfolder = join(workdir, "data", "plain", "19b", "*.txt") 
annotatedfolder = join(workdir, "data", "annotated", "19b", "")


# === Functions === 


def read_textfile(file): 
    """
    Reads a plain text file from the text repository. 
    Returns: string (containing the complete plain text). 
    """
    with open(file, "r", encoding="utf8") as infile: 
        text = infile.read()
    text = re.sub("\t", "", text)
    #text = text[0:2000] # for testing
    return text


def annotate_text(text, nlp): 
    """
    Annotates the text using the spacy NLP model activated initially.
    Returns: list (list of tokens with annotation according to spacy data model)
    """
    nlp.max_length = len(text) + 1000
    annotated = nlp(text)
    #print([(w.text, w.pos_, w.lemma_, w.tag_, w.dep_, w.morph) for w in annotated[0:25]])
    return annotated


def save_annotated(basename, annotated): 
    serialized = [t.text + "\t" + t.pos_ + "\t" + t.lemma_ + "\t" + t.dep_ + "\t" + str(t.morph) for t in annotated if t.pos_ != "SPACE" and t.text != " "]
    serialized = "\n".join(serialized)
    serialized = "wordform\tpos\tlemma\tdep\tmorph\n" + serialized
    annotatedfile = join(annotatedfolder, basename + ".csv")
    with open(annotatedfile, "w", encoding="utf8") as outfile: 
        outfile.write(serialized)


# === Coordination function === 

def main():
    """
    Coordinates the process. 
    Loads nlp model from spacy. 
    Then loops over each text to annotate, and saves annotation to disk. 
    """
    nlp = spacy.load("fr_dep_news_trf", disable=["ner"])
    spacy.prefer_gpu()
    progress = 0
    plain_files = [os.path.basename(file).split(".")[0] for file in glob.glob(join(textfolder))]
    already_annotated = [os.path.basename(file).split(".")[0] for file in glob.glob(join(annotatedfolder, "*.csv"))]
    print("Total plain files:", len(plain_files), "| already annotated:", len(already_annotated))
    for file in glob.glob(textfolder): 
        basename, ext = os.path.basename(file).split(".")
        if basename not in already_annotated: 
            text = read_textfile(file)
            annotated = annotate_text(text, nlp)
            save_annotated(basename, annotated)
            print(progress, basename, str(len(re.split("\W+", text))) + ": done.")
        else: 
            print(progress, basename, ": already annotated.")
        progress +=1

main()



