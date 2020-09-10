from dwave.system import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import dwave.inspector as dwi
import numpy as np

inner_qubits = [0, 1, 2, 3]
outer_qubits = [4, 5, 6, 7]
inner_qubits_qpu = [7, 3, 4, 0]
outer_qubits_qpu = [15, 131, 12, 128]

logical_qubits = inner_qubits + outer_qubits
logical_couplers = [(i, (i + 1) % 4) for i in inner_qubits] + list(zip(inner_qubits, outer_qubits))
physical_qubits = inner_qubits_qpu + outer_qubits_qpu
physical_couplers = [(physical_qubits[i], physical_qubits[j]) for (i, j) in logical_couplers]

# thermal control parameter, 0 < alpha <= 1 
alpha = 1

h_list = np.array([1] * len(inner_qubits) + [-1] * len(outer_qubits)).astype(np.float64)
h_list *= alpha

h = {q: h_list[i] for i, q in enumerate(physical_qubits)}
J = {couple: -alpha for couple in physical_couplers}


sampler = DWaveSampler(solver=dict(qpu=True))

response = sampler.sample_ising(h, J, num_reads=1000, num_spin_reversal_transforms=0)
print(response.aggregate())
dwi.show(response)
