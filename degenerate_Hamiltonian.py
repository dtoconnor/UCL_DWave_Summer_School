from dwave.system import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import dwave.inspector as dwi
import numpy as np

inner_qubits = [0, 1, 2, 3]
outer_qubits = [4, 5, 6, 7]
couplers = [(i, (i + 1) % 4) for i in inner_qubits] + list(zip(inner_qubits, outer_qubits))

# thermal control parameter, 0 < alpha <= 1 
alpha = 1

h_list = np.array([1] * len(inner_qubits) + [-1] * len(outer_qubits))
h_list *= alpha

h = dict(enumerate(h_list))
J = {couple: -1 * alpha for couple in couplers}

sampler = EmbeddingComposite(DWaveSampler(solver=dict(qpu=True)))

response = sampler.sample_ising(h, J, num_reads=1000, num_spin_reversal_transforms=0)

dwi.show(response)
