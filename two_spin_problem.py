from dwave.system import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import dwave.inspector as dwi

"""
Follow the four scenarios listed in task 1 by changing the variables in this file

qubit_1   qubit_2

  O -------- O 
        
h_1, J_val, h_2
 
"""

qubit_1 = 0
qubit_2 = 1

h_1 = 0
h_2 = 0

J_val = -1

h = {qubit_1: h_1, qubit_2: h_2}
J = {(qubit_1, qubit_2): J_val}

# sampler = EmbeddingComposite(DWaveSampler(solver=dict(qpu=True)))   # use if function below fails, will call any available quantum processor
sampler = EmbeddingComposite(DWaveSampler(solver=dict(name="DW_2000Q_6")))

response = sampler.sample_ising(h, J, num_reads=1000, num_spin_reversal_transforms=0)
print(response.aggregate())
dwi.show(response)
