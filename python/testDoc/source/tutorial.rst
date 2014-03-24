Detailed Tutorial
=================

First let's save the current directory because our example .xls table file
is located here. If you have downloaded this material on your local machine
ensure the directory you save to tablepath contains testTable.xls.

.. testsetup:: *
	
	import tutorial

.. testcode:: *

	#Importing standard libraries
	import os
	import sys

	tablepath = os.getcwd()

Let's start by importing tablemaker.py. If you have the environment variables
'erc' setup with 'ercTools' as a subdirectory and tablemaker.py in that 
directory, then use the following code:

.. testcode:: *

	#Extending Path to directory of tablemaker module
	os.chdir(os.environ['erc']); os.chdir("ercTools"); toolspath = os.getcwd()
	sys.path.append(toolspath)

We have added the path to ercTools temporarily to the system path. The system 
path contains directories Python will use to search for modules. Thus, by adding
ercTools to this path, Python will be able to find tablemaker.py. So let's 
import the module.

.. testcode:: *

	import tablemaker as tm

To create a latex table using tablemaker we can use two methods: 

	1. use existing xls file and create tables from this file
	2. create a dictionary of lists which contain the elements of a row

We will demonstrate the first method here

.. testcode:: *
	
	#change directory to tablepath
	os.chdir(tablepath)

	#First, let's draw in the data
	sheetDict = tm.read('testTable.xls')

When we instantiate a table object from tablemaker we need to tell it
which sheet of data to use. 'testTable.xls' contains 'Sheet1' and 'Sheet2'. 
We will begin with 'Sheet1'

.. testcode:: *

	table = tm.Table(sheetDict['Sheet1'])

We gave the basic arguments to create a table, but we could have specified
more arguments in the call. For example:

::

	tm.Table(result_dict, type_ = 'table', fillempty = None, merge = False)


Now we can write the tex of the table without further modifications. And we 
can see how it looks. We call the makeTex() of the table object to produce
a string to insert into the tex file.

.. testcode:: *


	texfile = open('test1.tex', 'w')
	texfile.write(table.makeTex())
	texfile.close()

Here is a first look at the table.

.. raw:: latex

	\input{../../test1}

It does not appear the table even fits on the page. We can either turn the table
sideways or merge some cells. First, let's try turning sideways.

.. testcode:: *

	table.setType('sidewaystable')

	texfile = open('test2.tex', 'w')
	texfile.write(table.makeTex())
	texfile.close()

Here is what the sidewaystable looks like.

.. raw:: latex

	\clearpage
	\input{../../test2}
	\clearpage

We probably do not need the table sideways here, if we merge the right cells
all the data should fit.

.. testcode:: *

	table.setType('table')

In order to merge the appropriate rows, we will use the row by row 
functionality of tablemaker. First we get a list of row objects from
the current table. The first row is indexed with 0. Then we can configure
the rows, one by one.

.. testcode:: *

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

Now let's see what we have.

.. testcode:: *

	texfile = open('test3.tex', 'w')
	texfile.write(table.makeTex())
	texfile.close()

.. raw:: latex

	\input{../../test3}

And now what about adding footnotes, labels, and a title? We can also provide different
default parameters for LateX's tabular environment.

.. testcode:: *

	table.setTitle('Parent and Child Measures of Head Start Families, by Group')
	table.setLabel('hs_label')
	table.setNotes('These statistics were not weighted using HSIS longitudinal weights.')
	table.setTableAlignment('lllllllllllll') 			#left justifying table by default

	texfile = open('test4.tex', 'w')
	texfile.write(table.makeTex())
	texfile.close()

.. raw:: latex

	\input{../../test4}

Now what if we have a longer table?
Sheet2 is a long table that doesn't fit on one page

.. testcode:: *

	table = tm.Table(sheetDict['Sheet2'])

	texfile = open('test5.tex', 'w')
	texfile.write(table.makeTex())
	texfile.close()

.. raw:: latex

	\input{../../test5}
	\clearpage

If we specify the type as longtable, the table will flow onto 
multiple pages.

.. testcode:: *

	table.setType('longtable')
	table.setTitle('This is a Long Table')
	table.setRepeat(0)      #row number(s) to repeat on every page
	table.setHlines((0,0))  #eliminating default top and bottom lines

	rows = table.rows

	rows[0].addhlines()

	texfile = open('test6.tex', 'w')
	texfile.write(table.makeTex())
	texfile.close()

.. raw:: latex

	\clearpage
	\input{../../test6}
	\clearpage

We can also construct a table without an .xls file. 
Let's assume we have some data. 

.. testcode:: *

	import pandas as pd
	import numpy as np

	#generate some random data
	data = np.random.randn(1000)
	data = data.reshape((100,10))   #100 rows and 10 columns
	dataframe = pd.DataFrame(data)

	#fake names for variables
	dataframe.columns = ['var' + str(i) for i in range(1,11)]

	print dataframe[['var1', 'var2', 'var3']].head(10)  #take a look at data

Let's create a table of means and standard deviations of these variables.

.. testcode:: *

	rowdict = {}
	rowdict[0] = ['Measure', 'Mean', 'Std']
	row = 1

	for i in range(1,11):
	    varname = 'var' + str(i)
	    series = dataframe[varname]
	    mean = series.mean()
	    std = series.std()
	    rowdict[row] = [varname, mean, std]
	    
	    row += 1

Now the data for the table is stored in a dictionary similar to the one
produced from the tm.read() method. So we can instantiate a table object.

.. testcode:: *

	table = tm.Table(rowdict)

	table.setTitle('This table was created without a .xls file')

	texfile = open('test7.tex', 'w')
	texfile.write(table.makeTex())
	texfile.close()

You can use the methods we have discussed previously to modify the 
table to your liking, but present here the basic table to prove
our test worked. 

.. raw:: latex

	\input{../../test7}
	\clearpage

Does tablemaker support multirow functionality? Yes! Let's try it out!

.. testcode:: *

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

.. raw:: latex

	\input{../../test8}
	\clearpage

