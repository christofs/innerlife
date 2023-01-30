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
textfolder = join("/", "media", "christof", "Data", "Github", "mimotext", "roman18", "plain", "files", "*.txt")

# Local data
workdir = join(os.path.realpath(os.path.dirname(__file__)), "..")
annotatedfolder = join(workdir, "data", "fra18", "annotated", "")


# === Functions === 


def read_textfile(file): 
    """
    Reads a plain text file from the text repository. 
    Returns: string (containing the complete plain text). 
    """
    with open(file, "r", encoding="utf8") as infile: 
        text = infile.read()
    if len(text) > 50000: 
        text = text[0:(int(len(text)/10))]
    elif len(text) > 20000: 
        text = text[0:(int(len(text)/5))]
    return text


def annotate_text(text, nlp): 
    """
    Annotates the text using the spacy NLP model activated initially.
    Returns: list (list of tokens with annotation according to spacy data model)
    """
    nlp.max_length = len(text) + 1000
    annotated = nlp(text, disable = ['ner', 'parser'])
    #print([(w.text, w.pos_) for w in annotated[0:5]])
    return annotated


def save_annotated(basename, annotated): 
    serialized = [t.text + "\t" + t.pos_ + "\t" + t.lemma_ for t in annotated]
    serialized = "\n".join(serialized)
    annotatedfile = join(annotatedfolder, basename + ".csv")
    with open(annotatedfile, "w", encoding="utf8") as outfile: 
        outfile.write(serialized)


# === Coordination function === 

def main():
    """
    Coordindates the entire process. 
    Then loops over each text to annotate, and saves annotation to disk. 
    """
    nlp = spacy.load("fr_dep_news_trf")
    progress = 0
    for file in glob.glob(textfolder)[40:]: 
        basename, ext = os.path.basename(file).split(".")
        text = read_textfile(file)
        annotated = annotate_text(text, nlp)
        save_annotated(basename, annotated)
        print(progress, basename, str(len(text)) + ": done.")
        progress +=1

main()



