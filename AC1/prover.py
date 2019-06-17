# AC1 Prover

from cqc.pythonLib import *
from time import sleep
import random

##############################
#
# Prover class derived from CQCConnection, with reg* attributes
#

class Prover():

	def __init__(self, m):
		self.myid = 1
		self.myself = 'node1'
		self.m = m
		self.numEPR = 2*m
		self.reg = []
		self.checked = []

        # Initialize the CQC connection
		with CQCConnection(self.myself) as self.node:
			self.init()
			# do something bad
			self.perform_attack()
			self.run_protocol()


	###################################
	#
	#  Create the EPR pairs
	#
	def init(self):
		self.reg.clear()
		for i in range(0,self.numEPR):
			# Create an EPR pair Beta00
			self.reg.append(self.node.recvEPR())
			self.checked.append(0)
		#print(self.checked)


	###################################
	#
	#  Create the EPR pairs
	#
	def perform_attack(self):
		for i in range(0,self.numEPR):
			# Measure in the computational or diagonal basis leaving the qubit in post-measurement state.
			x = random.randint(0,1)
			if (x == 1):
				self.reg[i].H() # measure in the diagonal basis
			self.reg[i].measure(inplace=True)
			if (x == 1):
				self.reg[i].H()


	###################################
	#
	#  Run the verification protocol
	#
	def run_protocol(self):
		while True:
			# 1. is performed by the Verifier

			#print("Prover: waiting for sel")
            # 2. receive the id of the EPR pair being checked, and s
			data = self.node.recvClassical()
			message = list(data)
			sel = message[0]
			s = message[1]
			if (sel == self.numEPR):
				quit()

			#print("Prover: received sel = ", sel)
			#print("Prover: received s = ", s)

            # 3. prepare state psi and perform teleportation
			psi = qubit(self.node)
			if (s == 1):
				psi.H()

			psi.cnot(self.reg[sel])
			psi.H()
			b1 = psi.measure()
			b2 = self.reg[sel].measure()
			self.node.sendClassical("node0",[b1,b2])

            # 4. and 5. are performed by the Verifier
			#print("Prover: done")


##############################
#
# main
#
def main():

	#print('AC1 - Prover')
	#print('Number of arguments:', len(sys.argv), 'arguments.')
	#print('Argument List:', str(sys.argv))
	m = int(sys.argv[1])
	prover = Prover(m)


##############################
main()
