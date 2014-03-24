'''
Created on Jul 7, 2013

@author: jtorcasso
'''

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import LatexFormatter
import os

os.chdir("..")
os.chdir('code')

code_path = os.getcwd()
os.chdir("../tex")
tex_path = os.getcwd()

def snippetize(code_path):
    
    code_file = open(code_path, 'r')
    
    snippet_dict = {}
    
    comment = ''
    
    code = ''
    
    new_snippet = True
    
    index = 0
    
    for line in code_file.readlines():
        
        if line == '\n': continue
        
        if line[:2] == '##':
            
            if not new_snippet:
                
                snippet_dict[index] = (comment, code)
                comment = ''
                index+=1
            
            new_snippet = True
            comment += line[2:]
            code = ''
            
        else:
            
            new_snippet = False
            code += line
        
    snippet_dict[index] = (comment, code)
    
    return snippet_dict
            
def pack_code(code_snippet):     
      
    tex = '\n' + r'\begin{framed}' + '\n'
    
    tex += highlight(code_snippet, PythonLexer(), LatexFormatter())
    
    tex += r'''\end{framed}
    
'''
    
    return tex
       
def codeToTex(code_path):
    
    snippet_dict = snippetize(code_path)
    
    snippets = snippet_dict.keys(); snippets.sort()
    
    tex_string = ''
    
    for key in snippets:
        
        snippet = snippet_dict[key]
        
        comment = snippet[0]
        
        code = pack_code(snippet[1])
        
        if comment != '':
            
            comment = r'\noindent ' + comment

        tex_string += comment + code
    
    return tex_string


tutorial_tex = r'''
\documentclass{article}

\usepackage[margin=0.5in]{geometry}
\usepackage{fancyvrb}
\usepackage{color}
\usepackage{framed}

''' + LatexFormatter().get_style_defs() + r'''

\begin{document}

\section*{Motivation}

The research process is a collection of tasks, sometimes performed by multiple 
people, which combine, in the end, into a carefully structured, defensible 
argument. Each task might require a different tool or person, and the 
order in which the tasks take place often matters. Hence, a more formal 
and well-planned research project combines the disparate tasks efficiently. 
Part of this efficiency means the project's results are also reproducible, 
and, as a result, more defensible. 

Typical Tasks of the Empirical Researcher:

\begin{itemize}
\item retrieve/convert data
\item clean/organize data
\item run analyses
\item generate figures and tables
\item cater discussion and results to the empirical evidence
\end{itemize}

We should all be familiar to at least some of these tasks. Often different
tools and people work optimally at different links in the chain. For instance, 
you might use STATA to clean data, MATLAB to run analyses, Python to 
generate figures and tables, and LateX to compile the containing paper. 
Often you have research assistants cleaning the data, and PhDs running analyses and 
discussing the results. You might be passing data back and forth, funneling 
everything through different machines with different configurations, operating 
systems, and installed software. The advantage of doing it this way is that each 
program or person has a functional advantage at each leg of the project's journey. 
However, all of this movement can increase the chances of error and slow your project
down.

In this tutorial, I plan on showing how you can use Python to manage your workflow
efficiently. The concepts we will cover include:

\begin{enumerate}
\item Understanding how Python works with your file system
\item Integrating Python with STATA, R, and LateX
\item How to design your own modules for projects
\item How to organize your project to use Python effectively
\item Getting to know some of Python's useful packages for research
\item Version Control
\item waf and wscript
\end{enumerate}
'''

tutorial_tex += codeToTex(code_path + '/' + 'project_management.py')



tutorial_tex += r'\end{document}'



export_file = open(tex_path + '/' + "project_management.tex", 'w')
export_file.write(tutorial_tex)
export_file.close()



