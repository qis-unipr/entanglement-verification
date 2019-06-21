# entanglement-verification

We implemented a few protocols for entanglement verification. To run the protocols, you need SimulaQron:

* pip3 install simulaqron

Then checkout this repository and enter it from your (bash) shell.

To setup the network, type:

* simulaqron set backend projectq
* simulaqron set nodes-file ./config/Nodes.cfg
* simulaqron set app-file ./config/appNodes.cfg
* simulaqron set cqc-file ./config/cqcNodes.cfg
* simulaqron set vnode-file ./config/virtualNodes.cfg
* simulaqron set topology-file ./config/topology.json
* simulaqron set max-qubits 40
* simulaqron set max-registers 100
* simulaqron set recv-timeout 2.0
* simulaqron set log-level debug

To start SimulaQron, type:

* simulaqron start

To start the tests, for example with NA2010 and m=5, enter the corresponding folder and type:

* ./run.sh > NA2010-m5.txt &

Once the simulation has completed, to enumerate the "compromised" and "abort" labels, type:

* cat NA2010-m5.txt | sed 's|[,.]||g' | tr ' ' '\n' | sort | uniq -c
