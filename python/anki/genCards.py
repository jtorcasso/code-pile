#!/usr/bin/env python

import sys
import csv 

filename = sys.argv[1]

if len(sys.argv) == 3:
    outname = sys.argv[2]
else:
    outname = filename.split('.')[0]+'.tex'
    
def process_term(term):
    
    field = '\n\\begin{{field}}\n{}\n\\end{{field}}\n'.format(term)
    
    return field

def process_definition(definition):
    
    field = '\n\\begin{{field}}\n{}\n\\end{{field}}\n'.format(definition)
    
    return field

def process_image(image):
    
    field = '\n\\xplain{{{}}}\n'.format(image)
    
    return field

def process_note(term, definition, image):
    
    content = process_term(term) + process_definition(definition) + process_image(image)
    
    note = '\n\\begin{{note}}\n{}\n\\end{{note}}\n'.format(content)
    
    return note

newlines = []
with open(filename, 'rb') as f:
  
    for row in csv.reader(f, delimiter=';'):
        term, definition, image = row
        newlines.append(process_note(term, definition, image))

tex = r'''
% -*- coding: utf-8 -*-
\documentclass[12pt]{article}
\special{papersize=3in,5in}
\usepackage{amssymb,amsmath}
\pagestyle{empty}
\setlength{\parindent}{0in}
\newenvironment{note}{\paragraph{NOTE:}}{}
\newenvironment{field}{\paragraph{field:}}{}

\begin{document}
''' + '\n'.join(newlines) + '\\end{document}'

with open(outname, 'wb') as outfile:
    outfile.write(tex)