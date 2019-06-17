# AC1 Verifier

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
		self.numEPR = 2*m
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

            # 2. select a previously uncheked EPR
			sel = 0
			while True:
				sel = random.randint(0,self.numEPR-1)
				#print("Verifier: sel = ", sel)
				if (self.checked[sel] == 0):
					self.checked[sel] = 1
					break
			s = random.randint(0,1)
			# send a classical message to the Prover: [sel,s]
			self.node.sendClassical("node1",[sel,s])

            # 3. receive 2 classical bits from the prover
			data = self.node.recvClassical()
			message = list(data)
			b1 = message[0]
			b2 = message[1]

            # 4. apply U = X^b2 Z^b1 to the owned half of Beta_00
			if (b1 == 1):
				self.reg[sel].Z()
			if (b2 == 1):
				self.reg[sel].X()

            # 5. apply H^s, then measure the state of the resulting qubit in the comp. basis
			if (s == 1):
				self.reg[sel].H()
			v = self.reg[sel].measure()
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

	#print('AC1 - Verifier')
	#print('Number of arguments:', len(sys.argv), 'arguments.')
	#print('Argument List:', str(sys.argv))
	m = int(sys.argv[1])
	verifier = Verifier(m)


##############################
main()
