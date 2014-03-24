##\section*{How Python interacts with your file system}
##\begin{quote} 
##``I want it now! The meatloaf! 
##I never know what she's doing back there.''
##\end{quote}
##Ok, so how does Python bring you your meatloaf? And where are all of 
##the ingredients in the kitchen? Before integrating Python into your
##workflow you need to know where it gets packages and where it looks
##and writes files, and how to use these packages and files in your code.
##Let's find out where Python is looking on 
##your system for modules and packages. One place it looks is wherever 
##your environment variable, PYTHONPATH, points to. Let's print all the 
##paths in the PYTHONPATH using the os package. 

import os

paths = os.environ['PYTHONPATH'].split(':')

for path in paths:
    print path

##If you experienced a keyerror, have no fear, it just means this variable 
##is not set. There are other places Python looks for packages.   
##It will also look in your current working directory. 

print os.getcwd()

##Let's try to import a module we have made. Saving the following code as `test\_module.py'
##in the directory you are using for this tutorial file:

def crazyWord(string):
    
    return string + ', now that is a crazy word'

##Let's try importing the module first with a different directory and then using the current directory

try:
    current_directory = os.getcwd()
    os.chdir("..\..")
    import test_module as testing

except:
    print "Failed to find module in first directory"
    os.chdir(current_directory)
    import test_module as testing
    print "Succeeded at finding module in " + os.getcwd()

print testing.crazyWord('hippopotamus')

##Ok, so Python could not find the module when you changed the current working directory
##but after changing it back, it found it just fine. Python looks for modules in a certain
##order: first it looks in the current working directory, then it looks 
##in the paths contained in the environment variable PYTHONPATH, and then it looks for 
##them in the location in which your initial installation put packages and modules (where
##the standard library packages are). You can see where this original installation-dependent
##path is with the following:

import sys

for path in sys.path:
    print path
    
##Now what about files? Python looks for files in the current working directory. Let's try
##the following: first we create a file, then we save, and then we open it back up. 

new_file = open('a_text_file.txt', 'w')

important_message = 'John Adams and Thomas Jefferson both died on July 4th, 1826'

new_file.write(important_message)

new_file.close()

print os.getcwd()

##Let's look at the files in the current directory.

for filename in os.listdir(os.getcwd()):
    print filename

##You see the file we just created is in there. Open it. 

old_file = open('a_text_file.txt', 'r')

##Read the text contained in the file

text_from_file = old_file.readlines()

print text_from_file

##Why is all of this important? Because what we want to integrate
##outside scripts and datasets into our projects, we want to 
##be able to tie together modules or scripts from other programming
##languages and we must understand how Python will find and work with these
##files. Thus far, we learned how Python looks for outside files and packages, 
##how to write and read files, and how to create and use a Python module of 
##our own. 
##\section*{Running Code from Other Languages in Python}
##First of all, why do we even continue to use other languages if Python is so great? 
##Several reasons: (i) other languages might have syntactical advantages 
##over Python (STATA for data cleaning as an example), (ii) Python might 
##not have good packages for some types of analyses, and (iii) not everybody
##knows Python, but if you work with people who use STATA primarily you can still
##integrate their code into the project. Let's see how it's done. 
##The first method uses the terminal or command line. Let's create a stata file. 

stata_code = '''

clear all

set obs 5
gen column1 = 3
gen column2 = 4

outsheet using fake_dataset.csv, comma replace
clear all

'''

stata_file = open('fake_statafile.do', 'w')
stata_file.write(stata_code)
stata_file.close()

##And let's run the stata code from Python

import subprocess

#Path to the executable (your path is probably different)
#stata_executable_path = r'/usr/local/stata12/stata-mp'

#Call STATA through command line
#subprocess.call([stata_executable_path, r'/e', 'do', 'fake_statafile.do'])

##If the call worked, you should see a dataset in your current directory
##called fake\_dataset.csv

for filename in os.listdir(os.getcwd()):
    print filename

##\section*{The Power of Python}
##Python is so powerful because of how it fosters community and cooperation. 
##The community serves not only as a potent source of information but a source
##of tried and tested tools. We call these tools third party packages. And no, 
##they aren't the shady dealings of the underworld, they are written by talented
##programmers eager to share the fruits of their labor with the world. Consider 
##two popular packages for data analysis: Numpy and Pandas
##
##\paragraph{Numpy} Numpy or numerical Python works with arrays and is great for
##raw data. It's libraries were written in optimally in C, so it's super fast. 
##
##\paragraph{Pandas} Pandas has all the dataset functionality as R. In fact, it 
##was modeled off of R and uses the dataframe. It provides functionality for 
##SQL-like merges and is great to partner with Numpy. Typically, I work 
##at the higher-level in Pandas and then when I run analyses I convert
##dataframes into arrays. First let's create a dataset to work with

fake_csvtext = '''id,column1,column2,column3
1,10203.0,49495.494,-9999
2,3242.44,4404.405,333304.454
3,22323,454545,454.44
4,-9999,4944959,454.54
5,1123.123,34343.49,454.454
6,49923.3434,99585.454,23230.445
'''

fake_csvfile = open('fake_csvfile.csv', 'w')
fake_csvfile.write(fake_csvtext)
fake_csvfile.close()

##Now we can work with our dataset in Pandas and Numpy

import pandas as pd
import numpy as np


data = pd.read_csv('fake_csvfile.csv', index_col = 0, na_values = -9999)

print data

print data['column1'].mean()

print data[['column1', 'column3']]

##Now let's take the data from pandas and use numpy with statsmodels to quickly run analyses
nonmissing_data = data[~np.isnan(data).any(axis=1)]

numpy_array = nonmissing_data.as_matrix()

print numpy_array

import statsmodels.api as sm

Y = numpy_array[:,0]

X = numpy_array[:,[1,2]]

print np.hstack.__doc__

X = np.hstack((np.ones((len(X),1)), X))

print sm.OLS.__doc__

model = sm.OLS(Y, X)

results = model.fit()

print sm.regression.linear_model.RegressionResults.__doc__

print results.params

print results.resid

print results.rsquared_adj

print results.pvalues

print results.fittedvalues






