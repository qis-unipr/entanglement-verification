# Entanglement Verification

Implementation and testing of the NA2010, AC1 and AC2 protocols with [SimulaQron](http://www.simulaqron.org/) v.3.0.10

### Prerequisites

* [SimulaQron](http://www.simulaqron.org/)

  Please refer to the [Getting started](https://softwarequtech.github.io/SimulaQron/html/GettingStarted.html) page of the SimulaQron guide for installation instructions.

### Setup

    1. To change the setup of the network, edit the .simulaqron.json file in each folder NA2010/, AC1/ and AC2/.
    See: https://softwarequtech.github.io/SimulaQron/html/ConfNodes.html
    The default configuration is:
    ```
    {
        "backend": "projectq",
        "log-level": 10
        "max-qubits": 40
        "max-registers":100
        "recv-timeout":2.0
    }

    ```

## Running

    1. To start SimulaQron, open a first shell and execute:
       ```
       simulaqron start --nodes node0,node1

       ```

    2. Open a second shell, enter for example the NA2010/ folder and execute:
       ```
       ./run.sh > NA2010-m5.txt &
       ```

### Logging

Once the simulation has completed, to enumerate the "compromised" and "abort" labels, type:

* cat NA2010-m5.txt | sed 's|[,.]||g' | tr ' ' '\n' | sort | uniq -c
