# AC2 Prover

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
		self.numEPR = 4*m
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
			#print("Prover: waiting for sel1 and sel2")

            # 2. receive the id of the EPR pairs
			data = self.node.recvClassical()
			message = list(data)
			sel1 = message[0]
			sel2 = message[1]

			#print("Prover: received sel1 = ", sel1)
			#print("Prover: received sel2 = ", sel2)
			if (sel1 == self.numEPR):
				quit()

            # 3. perform teleportation of the qubit of the EPR pair identified by sel2

			self.reg[sel2].cnot(self.reg[sel1])
			self.reg[sel2].H()
			b1 = self.reg[sel2].measure()
			b2 = self.reg[sel1].measure()
			self.node.sendClassical("node0",[b1,b2])

            # 4. and 5. are performed by the Verifier
			#print("Prover: done")


##############################
#
# main
#
def main():

	#print('AC2 - Prover')
	#print('Number of arguments:', len(sys.argv), 'arguments.')
	#print('Argument List:', str(sys.argv))
	m = int(sys.argv[1])
	prover = Prover(m)


##############################
main()
