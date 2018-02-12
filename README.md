# Variational quantum eigensolver

In the paper "Scalable quantum simulation of molecular energies" [1] they report that their VQE experiment achieves chemical accuracy and is the first scalable quantum simulation of molecular energies performed on universal quantum hardware.

This is the basic code to simulate molecular hydrogen implemented as described in paper [1] using ProjectQ [2], a framework for quantum computing. The code can be adapted (using a different main engine and changing some gates) such that it can be run on the IBM-q. It can also be adapted with more qubits and other coefficients of the (transformed) second quantization such that further molecules can be simulated.

The resulting plot does not look like a pretty potential curve, because most likely the coefficients from the paper used for the vqe are wrong:

![vqe plot](https://github.com/ramonahohl/vqe/blob/master/energyVQE.png)


## Prerequisits
install following libraries: scipy, (matplotlib), projectq


## References

[1]
P. J. J. O'Malley, R. Babbush, I. D. Kivlichan, J. Romero, J. R. McClean, R. Barends, J. Kelly,
P. Roushan, A. Tranter, N. Ding, B. Campbell, Y. Chen, Z. Chen, B. Chiaro, A. Dunsworth, A. G.
Fowler, E. Jerey, E. Lucero, A. Megrant, J. Y. Mutus, M. Neeley, C. Neill, C. Quintana, D. Sank,
A. Vainsencher, J. Wenner, T. C. White, P. V. Coveney, P. J. Love, H. Neven, A. Aspuru-Guzik, and
J. M. Martinis. Scalable quantum simulation of molecular energies. Phys. Rev. X, 6:031007, Jul 2016

[2]
Thomas Haner, Damian S. Steiger, Krysta M. Svore, and Matthias Troyer. Projectq: An open source
software framework for quantum computing. 2016.
http://projectq.ch/


## TODO
- correct coefficients
- adapt code to run on IBM-q
- make scalable and add further molecules coefficients
