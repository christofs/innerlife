"""
Script to extract the inner life categories for verbs in different languages. 
"""

# === Imports ===

import os
from os.path import join
import pandas as pd
import numpy as np
import re


# === Global variables ===

workdir = join(os.path.realpath(os.path.dirname(__file__)))
categoryfile = join(workdir, "data", "innerVerbs_clean.xml")


# === Functions === 

def get_categories(): 
    with open(categoryfile, "r", encoding="utf8") as infile: 
        data = infile.read()
    categorydata = {}
    lemmas = re.findall("<lemma (.*?)/>", data)
    for item in lemmas: 
        form = re.findall("form=\"(.*?)\"", item)[0]
        cat = re.findall("cat=\"(.*?)\"", item)[0]
        categorydata[form] = cat
    #print(categorydata)
    return categorydata

def create_categorytable(categorydata): 
    print("Done")


# === Main ===

def main(): 
    categorydata = get_categories()
    create_categorytable(categorydata)
main()