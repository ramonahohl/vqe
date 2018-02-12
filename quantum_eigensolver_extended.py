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
def E(thetas, i):
	#the conjugate gradient minimizer uses np arrays and not scalars
	if(not isinstance(thetas, float)):
		theta = thetas[0]
	else: 
		theta = thetas
	hamiltonian2quant = QubitOperator('', float(g[i][1])) + QubitOperator('Z0', float(g[i][2])) + QubitOperator('Z1', float(g[i][3])) + QubitOperator('Z0 Z1', float(g[i][4])) + QubitOperator('X0 X1', float(g[i][5])) + QubitOperator('Y0 Y1', float(g[i][6]))
	wavefunction = eng.allocate_qureg(2)
	X | wavefunction[0]
	op1 = QubitOperator('X0 Y1') 
	TimeEvolution(time=theta, hamiltonian=op1) | wavefunction
	eng.flush()
	energy = eng.backend.get_expectation_value(hamiltonian2quant, wavefunction)
	Measure | wavefunction
	eng.flush()
	return energy


# returns energy for a given time t
# used to plot the time reults from the paper, which are in the same table as the g coefficients
def E2(t0, i):
	hamiltonian2quant = QubitOperator('', float(g[i][1])) + QubitOperator('Z0', float(g[i][2])) + QubitOperator('Z1', float(g[i][3])) + QubitOperator('Z0 Z1', float(g[i][4])) + QubitOperator('X0 X1', float(g[i][5])) + QubitOperator('Y0 Y1', float(g[i][6]))
	wavefunction = eng.allocate_qureg(2)
	X | wavefunction[0]
	TimeEvolution(time=t0, hamiltonian=hamiltonian2quant) | wavefunction
	eng.flush()
	energy = eng.backend.get_expectation_value(hamiltonian2quant, wavefunction)	
	Measure | wavefunction
	eng.flush()
	return energy

eng = MainEngine()
energy_r = [[],[],[],[]]
r= []
thetas = [[],[],[],[]]

minimizer = input('Choose minimizer  [1]=normal, [2]=ConjugateGradient, [3]=bounded [0, 2pi]')

for ir in range(0, len(g)):
	r.append(float(g[ir][0]))
	print("The coefficient for R= ",r[ir], " are: g= ", g[ir][1:7]," and t0 is t0= ", g[ir][7])
	efun = lambda thetax: E(thetax, ir)
	theta0 = np.array([1.0, 1.0]) 
	e0 = efun(theta0)
	print("The initial energy (bond length = ",r[ir], ") is: ", e0)
		
	if (minimizer== '3'):
		eminbd= minimize_scalar(efun, method='bounded', bounds=(0,math.pi+math.pi))
		print("Results of bounded scalar optimzer (bond length =",r[ir], ") is: ",eminbd.x)
		thetas[3].append(eminbd.x)
		energy_r[3].append(eminbd.fun)
	elif (minimizer== '2'):
		emincg = minimize(efun, theta0, method='CG')
		print("Results of CG optimzer (bond length =",r[ir], ") is: ",emincg.x[0])
		thetas[2].append(emincg.x[0])
		energy_r[2].append(emincg.fun)
	elif (minimizer== '1'):
		emin= minimize_scalar(efun)
		print("Results of scalar optimzer (bond length =",r[ir], ") is: ",emin.x)
		thetas[1].append(emin.x)
		energy_r[1].append(emin.fun)
	
	thetas[0].append(float(g[ir][7]))
	energy_r[0].append(E2(float(g[ir][7]), ir))
	
sizescatter=4
fig = plt.figure()
plt.scatter(r, energy_r[0],color='orange', s=sizescatter+sizescatter)
plt.scatter(r, energy_r[int(minimizer)], color='seagreen', s=sizescatter, marker='D')
plt.legend(['paper','results'])
plt.title('Energy Plot VQE')
plt.xlabel('Bond lenght R [A°]')
plt.ylabel('Energy')
plt.grid(True)
plt.savefig('energyX2.png')
plt.show()
