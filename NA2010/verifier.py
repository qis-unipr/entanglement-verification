# NA2010 Verifier

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
			x = random.randint(0,1)

            # 3.
			a = 0
			if (x == 0):
				# measure in the comp. basis the qubit of the selected pair
				a = self.reg[sel].measure()
			else:
				# apply H then measure in the comp. basis the qubit of the selected pair
				self.reg[sel].H()
				a = self.reg[sel].measure()

            # 4. send the id of the EPR pair to the Prover
			self.node.sendClassical("node1",sel)

            # 5. and 6. are performed by the Prover
			#print("Verifier: waiting for b and y")
            # 7. wait for b and y sent by the Prover
			data = self.node.recvClassical()
			message = list(data)
			b = message[0]
			y = message[1]

            # 8. check conditions, and produce v
			v = 0
			if ((x == y) and (a != b)):
				v = 1
			else:
				v = 0
			#print("Verifier: v = ", v)

		if (v == 1):
			print("compromised")
		else:
			print("abort")
		kill = self.numEPR
		self.node.sendClassical("node1", kill)
		quit()

##############################
#
# main
#
def main():

	#print('NA2010 - Verifier')
	#print('Number of arguments:', len(sys.argv), 'arguments.')
	#print('Argument List:', str(sys.argv))
	m = int(sys.argv[1])
	n = 0
	verifier = Verifier(m)


##############################
main()
