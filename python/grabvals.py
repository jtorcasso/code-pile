import csv
import os


def getLabels(dset_root, label_directory):
    """
    Returns a dictionary with variable names of the dataset as keys
    and values of the form [variable label, dict of value labels]
    
    dset_root is the root of the dataset name.
    
    label_directory is the location of the dataset variable labels, variable-value label
    crosswalk, and value label-value files
    
    Ex:
    
    dset_root = 'hsis_data'
    
    label_directory = '~/Klmshare/Data_Central/HSIS/Data/Refined'
    """
    
    os.chdir(label_directory)
    
    #Drawing in variable labels (file created in STATA)
    labels = dict(csv.reader(open(dset_root + 'Labels.txt', 'rb'), delimiter='\t'))
    
    #Drawing in a crosswalk between variables and value labels (file created in STATA)
    crosswalk = dict(csv.reader(open(dset_root + 'Vars2Values.txt', 'rb'), delimiter='\t'))
    
    #Drawing in log file of 'label list' command in STATA
    valuelabels_raw = open(dset_root + 'Values.txt', 'rb').readlines()
    
    #Creating a dict with value label names as keys and dicts of value-label pairs as values
    valuelabels = {}
    begin = False
    currentvl = ''
    for line in valuelabels_raw:
        if line == '. log close\n':
            break
        if begin:
            if line[0] == ' ':
                content = line.strip().split(' ')
                value = content[0]
                label = ' '.join(content[1:])
                valuelabels[currentvl].update({value:label})
            elif line != '\n':
                currentvl = line[:-2]
                valuelabels[currentvl] = {}
        elif line == '. label list\n':
            begin = True
    
    #Storing in a dictionary the varname as key and a list [variable label, value labels] as 
    #values
    varLabels = {}
    for var in labels:
        label = labels[var]
        try:
            valdict = valuelabels[crosswalk[var]]
        except:
            valdict = {}
        
        varLabels[var] = [label, crosswalk[var], valdict]
    
    return varLabels

labels = getLabels('temp', os.getcwd())

ofile = open('relabelValues.do', 'w')
string = ''

sortedvars = labels.keys(); sortedvars.sort()

for var in sortedvars:
	valdict = labels[var][2] 
	values = valdict.keys(); values.sort()
	values = ' '.join([' '.join([v,'"' + valdict[v] + '"']) for v in values])
	if values.strip() != '':
		string += 'label define ' + labels[var][1] + ' ' + values + ', replace' + '\n'

ofile.write(string)
ofile.close()	


















