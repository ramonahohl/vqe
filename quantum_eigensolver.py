from projectq import MainEngine
from projectq.ops import QubitOperator, H, X, Measure, TimeEvolution
from scipy.optimize import minimize_scalar, minimize
import math
import numpy as np
import matplotlib.pyplot as plt
import csv

# load coefficient g
g=[]
with open('./coeffs.csv', 'r') as csvfile:
	coeffreader = csv.reader(csvfile, delimiter=' ')
	for row in coeffreader:
		g.append(row[:8])

#energy function
def E(theta, i):
	#build second quantized hamiltonian (devided for clearer arrangement)
	hamiltonian2quant = QubitOperator('', float(g[i][1])) + QubitOperator('Z0', float(g[i][2])) 
	hamiltonian2quant += QubitOperator('Z1', float(g[i][3])) + QubitOperator('Z0 Z1', float(g[i][4]))
	hamiltonian2quant += QubitOperator('X0 X1', float(g[i][5])) + QubitOperator('Y0 Y1', float(g[i][6]))
	
	#allocate two qubits in |00> state
	wavefunction = eng.allocate_qureg(2)
	#set to "HF basis" |01>
	X | wavefunction[0]
	#build operator op1
	op1 = QubitOperator('X0 Y1') 
	#create time evolution operator e^{-i*op1*t}
	TimeEvolution(time=theta, hamiltonian=op1) | wavefunction
	eng.flush()
	#calculate energy=expectation value
	energy = eng.backend.get_expectation_value(hamiltonian2quant, wavefunction)
	Measure | wavefunction
	return energy


#main part
eng = MainEngine()
energy_r = []
r= []
thetas = []

#find E for all the bond lenghts r
for ir in range(0, len(g)):
	r.append(float(g[ir][0]))

	#lamda energy function for current bond lenght/coefficients 
	efun = lambda thetax: E(thetax, ir)
	theta0 = 1.0 
	e0 = efun(theta0)
	
	#find minimal energy
	emin= minimize_scalar(efun)
	thetas.append(emin.x)
	energy_r.append(emin.fun)	

	#print information of current bond length	
	print("The coefficient for R= ",r[ir], " are: g= ", g[ir][1:7]," and t0 is t0= ", g[ir][7])
	print("Results of scalar optimzer (bond length =",r[ir], ") is: ",emin.x)
	print("The initial energy (bond length = ",r[ir], ") is: ", e0)


#plot
sizescatter=4
fig = plt.figure()
plt.scatter(r, energy_r, color='seagreen', s=sizescatter, marker='D')

plt.title('Energy Plot VQE')
plt.xlabel('Bond lenght R [A°]')
plt.ylabel('Energy')
plt.grid(True)
plt.savefig('energyVQE.png')
#plt.show()
