# entanglement-verification

To run the IBM Q version of the protocols, you need Qiskit:

* pip3 install qiskit

Full installation instructions are here: https://github.com/Qiskit/qiskit-terra

To run AC1 on a real device, type:

* python3 AC1.py real

To run AC2 on a real device, type:

* python3 AC2.py real

In both cases, the presence of the attacker is implemented by using either |00>
or |++> in place of |Beta00>, at random. Also s is randomly chosen.

To run the protocols on a locally simulated device, just replace "real" with "sim".
