#!/usr/bin/python
# -*- coding: utf8 -*-
#
# FormR Likert-Scale Survey Generator
# For rapid preparation of norming surveys using formr.org
#
# Borys Jastrzębski @ Prague, 09.11.2021
# borys.jastrzebski [at] psych.uw.edu.pl

import xlsxwriter
import sys

##### FUNCTIONS #####

# List splitter into n lists
def split(a, n):
    n = min(n, len(a)) # don't create empty buckets
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))
def flatten(t):
    return [item for sublist in t for item in sublist]

# A function to replace a non-standard latin character
# Used for the purpose of creating variable names
# Contains diacritics from Polish, Czech and German
#
# If you need to add more, just put the diacritic in the subs_from
# and its equivalent at subs_to, at the same indices.
def unpolish(char):
    subs_from = "ąćęłńóśźżáčďéěíňřšťúůýžäöüß"
    subs_to = "acelnoszzacdeeinrstuuyzaous"
    if char in subs_from:
        return subs_to[subs_from.index(char)]
    else:
        return char

def clean_diacr(b):
    return "".join([unpolish(char) for char in b])

##### END OF FUNCTIONS #####

##### PROCESSING THE CONFIG FILE #####
# Picking out the variable lines and cleaning them up
with open(sys.argv[1], 'r') as conf:
    config = list(filter(None, [x.rstrip() for x in conf.readlines() if not x.startswith("#")]))

# Splitting, tupling and putting the variables into a dictionary
config = dict([tuple(x.split(": ")) for x in config])

# turning the config dictionary into a namespace, so the variables can be called
try:
    from types import SimpleNamespace
    config = SimpleNamespace(**config)
except:
    # Pre-SimpleNamespace compatible solution for the purpose of Platypus Mac App generator
    from collections import namedtuple
    vars = list(config.keys())
    ConfClass = namedtuple('ConfClass', vars)
    config = ConfClass(*[config[x] for x in vars])
    
##### END OF PROCESSING THE CONFIG FILE #####

# Reading in the input file
with open(config.inpath, 'r') as wordf:
    words = [x.rstrip() for x in wordf.readlines()]

# Dividing the words into pages
words_divided = list(split(words, int(config.dpages)))

columns = []

# Generating columns

# type column
columns.append([x + ["submit"] for x in split(["rating_button 1,{},1 ".format(int(config.likertsize)) + x for x in words], int(config.dpages))])
columns[-1].insert(0, "type")

# name column
columns.append([[clean_diacr(word.lower()) for word in x] + ["page{}".format(ind+1)] for ind, x in enumerate(words_divided)])
columns[-1].insert(0,"name")

# label column
columns.append([["###" + i for i in x] + [str(config.nextpage)] for x in words_divided])
columns[-1].insert(0,"label")

# Choice1 column (left label of the Likert scale)
columns.append([[config.llabel for i in x] + [""] for x in words_divided])
columns[-1].insert(0,"choice1")

# Choice2 column (right label of the Likert scale)
columns.append([[config.rlabel for i in x] + [""] for x in words_divided])
columns[-1].insert(0,"choice2")

# Flattening all the columns
columns_flat = [[columns[ind][0]] + x for ind, x in enumerate([flatten(x[1:]) for x in columns])]

# Generating an excel file
workbook = xlsxwriter.Workbook(config.outpath)
worksheet = workbook.add_worksheet()

for ind, column in enumerate(columns_flat):
    # Rows and columns are zero indexed.
    row = 0
    # iterating through content list
    for item in column:
        # write operation perform
        worksheet.write(row, ind, item)
    
        # incrementing the value of row by one
        # with each iterations.
        row += 1
     
workbook.close()