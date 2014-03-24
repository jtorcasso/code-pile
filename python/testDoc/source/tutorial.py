#Importing standard libraries
import os
import sys

os.chdir("..")
tablepath = os.getcwd()

#Extending Path to directory of tablemaker module
os.chdir(os.environ['erc']); os.chdir("ercTools"); toolspath = os.getcwd()
sys.path.append(toolspath)

import tablemaker as tm

os.chdir(tablepath)

#First, let's draw in the data
sheetDict = tm.read('testTable.xls')


# Example Table 1
##################################################
table = tm.Table(sheetDict['Sheet1'])

texfile = open('test1.tex', 'w')
texfile.write(table.makeTex())
texfile.close()

# Example Table 2
##################################################

table.setType('sidewaystable')

texfile = open('test2.tex', 'w')
texfile.write(table.makeTex())
texfile.close()

# Example Table 3
##################################################

table.setType('table')

rows = table.rows

rows[0].mergeEmpty()                #merge the row, treat as two columns
rows[0].addhlines(title = True)     #title=True adds lines only under heading
rows[0].align(['c']*2)              #centering the two columns
rows[0].setFormat('textbf')         #formatting the two columns with boldface

rows[1].mergeEmpty()
rows[1].addhlines(title = True)
rows[1].align(['c']*4)
rows[1].setFormat('emph')           #formatting the two columns with italics

rows[2].align(['c']*13)             
rows[2].addhlines()                 #adding full horizontal (default title = False)

rows[3].setTopSpacing('0.25cm')
rows[3].setBottomSpacing('0.25cm')

rows[9].setTopSpacing('2.5mm')
rows[9].setBottomSpacing('2.5mm')

texfile = open('test3.tex', 'w')
texfile.write(table.makeTex())
texfile.close()

# Example Table 4
##################################################

table.setTitle('Parent and Child Measures of Head Start Families, by Group')
table.setLabel('hs_label')
table.setNotes('These statistics were not weighted using HSIS longitudinal weights.')
table.setTableAlignment('lllllllllllll') 

texfile = open('test4.tex', 'w')
texfile.write(table.makeTex())
texfile.close()

# Example Table 5
##################################################

table = tm.Table(sheetDict['Sheet2'])

texfile = open('test5.tex', 'w')
texfile.write(table.makeTex())
texfile.close()

# Example Table 6
##################################################

table.setType('longtable')
table.setTitle('This is a Long Table')
table.setRepeat(0)      #row number(s) to repeat on every page
table.setHlines((0,0))  #eliminating default top and bottom lines

rows = table.rows

rows[0].addhlines()

texfile = open('test6.tex', 'w')
texfile.write(table.makeTex())
texfile.close()

# Example Table 7
##################################################

import pandas as pd
import numpy as np

#generate some random data
data = np.random.randn(1000)
data = data.reshape((100,10))   #100 rows and 10 columns
dataframe = pd.DataFrame(data)

#fake names for variables
dataframe.columns = ['var' + str(i) for i in range(1,11)]

rows = []
rows.append(['Measure', 'Mean', 'Std'])

for i in range(1,11):
    varname = 'var' + str(i)
    series = dataframe[varname]
    mean = series.mean()
    std = series.std()
    rows.append([varname, mean, std])
    

table = tm.Table(rows)

table.setTitle('This table was created without a .xls file')

texfile = open('test7.tex', 'w')
texfile.write(table.makeTex())
texfile.close()

# Example Table 8
##################################################

rowdict = 	{0:['A multiple row column', 'B1', 'C1'], 
			 1:['', 'B2', 'C2'],
			 2:['', 'B3', 'C3']}
table = tm.Table(rowdict)
table.setTitle('A table with multirow functionality')

rows = table.rows
rows[0].setFormat(['multirow{3}{*}', '', ''])

texfile = open('test8.tex', 'w')
texfile.write(table.makeTex())
texfile.close()
