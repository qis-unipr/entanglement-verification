# AC2 Verifier

from cqc.pythonLib import *
from time import sleep
import random

##############################
#
# Verifier class derived from CQCConnection, with reg* attributes
#

class Verifier():

	def __init__(self, m):
		self.myid = 0
		self.myself = 'node0'
		self.m = m
		self.numEPR = 4*m
		self.reg = []
		self.checked = []

        # Initialize the CQC connection
		with CQCConnection(self.myself) as self.node:
			self.init()
			time.sleep(2) # meanwhile the Prover may do something bad
			self.run_protocol()


	###################################
	#
	#  Create the EPR pairs
	#
	def init(self):
		self.reg.clear()
		for i in range(0,self.numEPR):
			# Create an EPR pair Beta00
			self.reg.append(self.node.createEPR("node1"))
			self.checked.append(0)
			# turn to Beta01
			#self.reg[i].Z()
			self.reg[i].X()
		#print(self.checked)


	###################################
	#
	#  Run the verification protocol
	#
	def run_protocol(self):
		v = 0
		k = 0
		while ((k < self.m) and (v == 0)):
            # 1.
			k = k + 1

            # 2. select two previously unchecked EPR pairs
			sel1 = 0 # this is for the teleportation
			while True:
				sel1 = random.randint(0,self.numEPR-1)
				if (self.checked[sel1] == 0):
					self.checked[sel1] = 1
					break
			#print("Verifier: sel1 = ", sel1)
			sel2 = 0 # this is the EPR that will be checked
			while True:
				sel2 = random.randint(0,self.numEPR-1)
				if (self.checked[sel2] == 0):
					self.checked[sel2] = 1
					break
			#print("Verifier: sel2 = ", sel2)

			# send a classical message to the Prover: [sel1,sel2]
			self.node.sendClassical("node1",[sel1,sel2])

            # 3. receive 2 classical bits from the prover
			data = self.node.recvClassical()
			message = list(data)
			b1 = message[0]
			b2 = message[1]

            # 4. apply U = X^b2 Z^b1 to the owned half of Beta_00
			if (b2 == 1):
				self.reg[sel1].X()
			if (b1 == 1):
				self.reg[sel1].Z()

            # 5. apply the quantum circuit that turns the Bell basis into the computational one; then measure
			self.reg[sel2].cnot(self.reg[sel1])
			self.reg[sel2].H()
			self.reg[sel2].cnot(self.reg[sel1])
			v1 = self.reg[sel1].measure()
			v2 = self.reg[sel2].measure()
			#print("Verifier: v1 = ", v1, " v2 = ", v2)

			if ( not ( (v1 == 0) and (v2 == 0) ) ):
				v = 1
			#print("Verifier: v = ", v)

		if (v == 1):
			print("compromised")
		else:
			print("abort")
		kill = self.numEPR
		self.node.sendClassical("node1", [kill,kill])
		quit()

##############################
#
# main
#
def main():

	#print('AC2 - Verifier')
	#print('Number of arguments:', len(sys.argv), 'arguments.')
	#print('Argument List:', str(sys.argv))
	m = int(sys.argv[1])
	verifier = Verifier(m)


##############################
main()
