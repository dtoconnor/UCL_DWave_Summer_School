from dwave.system import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import dwave.inspector as dwi
import numpy as np

inner_qubits = [0, 1, 2, 3]
outer_qubits = [4, 5, 6, 7]
# 2000Q only
# inner_qubits_qpu = [7, 3, 4, 0]
# outer_qubits_qpu = [15, 131, 12, 128]

logical_qubits = inner_qubits + outer_qubits
logical_couplers = [(i, (i + 1) % 4) for i in inner_qubits] + list(zip(inner_qubits, outer_qubits))
# 2000Q only
# physical_qubits = inner_qubits_qpu + outer_qubits_qpu
# physical_couplers = [(physical_qubits[i], physical_qubits[j]) for (i, j) in logical_couplers]

# thermal control parameter, 0 < alpha <= 1 
alpha = 1

h_list = np.array([alpha] * len(inner_qubits) + [-alpha] * len(outer_qubits)).astype(np.float64)

h = {q: h_list[i] for i, q in enumerate(logical_qubits)}
J = {couple: -alpha for couple in logical_couplers}


sampler = EmbeddingComposite(DWaveSampler(solver=dict(qpu=True)))   # use if function below fails, will call any available quantum processor
# sampler = EmbeddingComposite(DWaveSampler(solver=dict(name="DW_2000Q_6")))

response = sampler.sample_ising(h, J, num_reads=1000, num_spin_reversal_transforms=0)
print(response.aggregate())
dwi.show(response)
