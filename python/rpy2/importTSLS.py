'''an exercise for import robjects'''

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
sem = importr("sem")

def IV_Contamination(Y, exog, endog, Z):
    '''iv regression with control contamination
    
    Parameters
    ----------
    Y : array-like
        2-d matrix of an outcome (Nx1)
    exog : array-like
        2-d matrix of exogenous variables (Nxk)
    endog: array-like
        2-d matrix of endogenous variables (Nxj)
    Z : array-like
        2-d matrix of instruments (Nxj)
    '''
    
    rY = robjects.r['matrix'](robjects.FloatVector(Y.as_matrix().flatten().tolist()), \
                                 nrow=Y.shape[0], ncol=Y.shape[1])
    rendog = robjects.r['matrix'](robjects.FloatVector(endog.as_matrix().flatten().tolist()), \
                                 nrow=endog.shape[0], ncol=endog.shape[1])
    rexog = robjects.r['matrix'](robjects.FloatVector(exog.as_matrix().flatten().tolist()), \
                                 nrow=exog.shape[0], ncol=exog.shape[1])
    rZ = robjects.r['matrix'](robjects.FloatVector(Z.as_matrix().flatten().tolist()), \
                                 nrow=Z.shape[0], ncol=Z.shape[1])
    rfmlaY = robjects.Formula('rY ~ rendog + rexog')
    rfmlaZ = robjects.Formula('~ rexog + rZ')
    env = rfmlaY.environment
    rfmlaZ.setenvironment(env)
    env['rY'] = rY
    env['rendog'] = rendog
    env['rexog'] = rexog
    env['rZ'] = rZ
    
    tsls = sem.tsls(formula=rfmlaY, instruments=rfmlaZ)
    
    sem.print_tsls(tsls)