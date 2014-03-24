# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 12:05:41 2014

@author: jake
"""

from __future__ import print_function, division

from mpi4py import MPI
import itertools

import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

n = int(15504/size)

# Overhead
if rank == 0:
    models = np.array(list(itertools.combinations(xrange(20), 5)))
else:
    models = None


if rank < size - 1:
    local_models = np.zeros(n)
else:
    local_models = np.zeros(n + 15504%size)

counts = [n]*size
counts[-1] = n + 15504%size

starts = [n*r for r in xrange(0,size)]

comm.Scatterv([models, tuple(counts), tuple(starts), MPI.DOUBLE],local_models)

print('process ', rank, 'with', len(local_models), 'models')
print(local_models[0], local_models[-1])