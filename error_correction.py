from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import networkx as nx
import dwave_networkx as dnx
import numpy as np

# Set up our connection to the D-Wave Computer
solver = EmbeddingComposite(DWaveSampler())
print("\nConnected to", solver.properties['child_properties']['chip_id'])

# Find good cell indices, i.e. cells without missing qubits/couplers, in the online D-Wave chip
G = nx.Graph()
G.add_edges_from(DWaveSampler().edgelist)
goodcellindices = []
for q in range(0, 2048, 8):
    if all((i, j) in G.edges for i in range(q, q+4) for j in range(q+4, q+8)):
        goodcellindices.append(q)
print("\nNumber of complete unit cells on chip:", len(goodcellindices))

fullword = 'Hydroelectricity accentuates conceivable possibilities expeditiously, whereas circumlocutions fail'

wordlength = min(100, len(fullword))   #number of characters in word to be transmitted
bitsperchar = 8
numbits = wordlength*bitsperchar # there are eight qubits in each unit cell; each qubit maps each bit of the ASCII code

wordstring = fullword[0:wordlength]
print("\nOriginal string:", wordstring)

crossoverprob = 0.02  # this is a measure of how noisy the channel is: it is the probability that any bit transmitted on the channel gets flipped during transmission
# print("\nCrossover Probability:", crossoverprob)

# get the connectivity map which defines which qubits are coupled to which other qubits
connectivity = np.triu(nx.to_numpy_matrix(dnx.chimera_graph(1,1,4)))

# convert the word to be transmitted into a binary string:    
bitsarray= np.array([[ord(i)] for i in wordstring],  dtype=np.uint8)
bitsword = np.unpackbits(bitsarray, axis=1).reshape((1,-1))
print("\nOriginal string in binary:\n", bitsword)
# bitsword now contains an array of zeros and ones encoding the error-free word to be transmitted

# now flip some fraction of the information bits, corresponding to the received set of corrupted data bits
randomarray1D = np.random.rand(numbits)
flippedbitindex = np.array(randomarray1D<crossoverprob).astype(int)

rxbits = np.bitwise_xor(bitsword, flippedbitindex)
print("\nCorrupted string:\n", rxbits)
# rxbits now contains the received set of corrupted data bits in {0,1}

# now we need to make a 2-D array whose elements correspond to the couplers between each qubit; the value of the coupler is set so that the qubits are in their ground state
rowbits = np.repeat(bitsword[0].reshape(1,-1), numbits, axis=0)
columnbits = np.repeat(bitsword[0].reshape(-1,1), numbits, axis=1)

jtxbits = (~(np.bitwise_xor(rowbits,columnbits).astype(bool))).astype(int)
# this is the transmitted error-free set of couplers with 1 being ferromagnetic and 0 being antiferromagnetic.
# note that it is upper triangular; note that couplers which don't exist are assigned zero. 

# now flip some fraction of the couplers
randomarray2D = np.triu(np.random.rand(numbits), 1)
flippedcouplerindex = np.array(randomarray2D < crossoverprob).astype(int)
jrxbits = np.bitwise_xor(jtxbits, flippedcouplerindex)
# jrxbits now contains the received set of couplers in {0,1}, with 1 being ferromagnetic

# decode the received word without any error correction            
rxword = rxbits.reshape((-1,bitsperchar))
rxword = rxword.dot(1 << np.arange(rxword.shape[-1] - 1, -1, -1))

corruptedword = ''.join([str(chr(i)) for i in rxword])
print("\nCorrupted message received:", corruptedword)
# corruptedword is what would be received if there were no error correction            

# now let's do the error correction!
hshift = np.zeros(2048)
jshift = np.zeros((2048,2048))
rxcharbits = rxbits.reshape((-1, 8))
for charindex in range(wordlength):
    
    # loop through each character in turn
    lowestbitindex = charindex*bitsperchar
    highestbitindex = (charindex+1)*bitsperchar-1
    
    rxchar = rxcharbits[charindex]
    
    # first map the received corrupted information bits onto the local fields for each qubit
    h = -1 + 2*rxchar
    # h contains the local fields for each character in {-1,1}

    lowestshiftedindex = goodcellindices[charindex]
    highestshiftedindex = lowestshiftedindex+bitsperchar-1
    
    hshift[lowestshiftedindex:highestshiftedindex+1] = h
    # hshift contains the local fields for the whole word in {-1,1}

    # now map the received corrupted coupler bits onto the couplers for each qubit
    j = np.multiply(connectivity,(1-2*jrxbits[lowestbitindex:highestbitindex+1,lowestbitindex:highestbitindex+1]))    
    # j contains the received set of couplers for the current character in {-1,1} where -1 is ferro and 1 is antiferro unused couplers are set to 0

    # now shift the couplers by a number of bits in the Chimera graph:
    jshift[lowestshiftedindex:highestshiftedindex+1,lowestshiftedindex:highestshiftedindex+1] = j[0:bitsperchar,0:bitsperchar]

# now find the ground-state spin configuration corresponding to the received corrupted set of local fields (h) and couplers (j)
h = dict(enumerate(hshift.flatten(), 0))
h = {x:y for x,y in h.items() if y!=0}

J = {(row,col): jshift[row,col] for row in range(2048) for col in range(2048)}
J = {x:y for x,y in J.items() if y!=0}

answer = solver.sample_ising(h, J, num_reads=10)
print("\nD-Wave System Response:\n",answer)

spins = answer.record.sample[0]

# now read off each character in turn from the ground state spin configuration
decodedword = []
for charindex in range(wordlength):
      
    lowestshiftedindex = charindex*bitsperchar
    highestshiftedindex = lowestshiftedindex+bitsperchar-1
        
    decodedbits = (0.5 - 0.5*spins[lowestshiftedindex:highestshiftedindex+1]).astype(int)
    # this now contains the decoded bit string in (0,1)

    # finally decode the received binary into ascii
    decodedbits = decodedbits.reshape((-1,bitsperchar))
    decodedint = np.packbits(decodedbits)
    decodedword.append(chr(decodedint))

decodedword = ''.join([str(i) for i in decodedword])
print("\nDecoded word:", decodedword)

transmiterrors = sum([corruptedword[i]!=wordstring[i] for i in range(wordlength)])
print("\nErrors in transmission:", transmiterrors)

errors = sum([decodedword[i]!=wordstring[i] for i in range(wordlength)])
print("\nErrors in decoding:", errors)
