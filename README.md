# UCL_DWave_Summer_School
Quantum Annealer can be used to solve a host of optimization problems when framed within the context of the Ising model. Using Python and the D-Wave 2000Q quantum annealer, this repository looks at error correction of ASCII messages sent over a noisy channel.

## Setup
To use complete all tasks in this repo, copy and paste the following links into your browser, logging into to each of the services:
- Leap Account: ```https://cloud.dwavesys.com/leap/```
- D-Wave GUI: ```https://cloud.dwavesys.com/qubist/```
- D-Wave IDE with this repo: ```https://ide.dwavesys.io/#https://github.com/dtoconnor/UCL_DWave_Summer_School```

## Task 1: GUI
Go to *solver visualizer - submit problems*, and select a view setting before viewing graph data. From here you will select a part of the graph to then experimentally analyse how a two spin system behaves on the D-Wave 2000Q. You will look at four scenarios of the four spin system:
- Two spins coupled by a ferromagnetic interaction (J = -1) with no local fields
- Two spins coupled by an anti-ferromagnetic interaction (J = 1) with no local fields
- Two spins coupled by a ferromagnetic interaction (J = -1) with a small local field (say h = 0.2) on one of the spins
- Two spins coupled by a ferromagnetic interaction (J = -1) with local fields of magnitude 1 pointing in opposite directions on the two spins. This is known as a *frustrated system* since it’s not possible for all three constraints (the ferromagnetic interaction and the two local fields) to be simultaneously satisfied. Such systems typically have many lowest energy solutions – what a physicist would call a multiply-degenerate ground state

## Task 2: Error correction
You will firstly look at the code used in ``error_correction.py``. Using the top right play button in the IDE, you can run the code straight away to then retrieve a result from a D-Wave sampler. Your task is to first understand the code and its functions, and to then improve the results you recieve.

## Task 3: Degenerate Hamiltonian 
TBC

