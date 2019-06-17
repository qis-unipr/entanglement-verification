# NA2010 Prover

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
			# 1., 2., 3. are performed by the Verifier

			#print("Prover: waiting for sel")
            # 4. receive the id of the EPR pair being checked
			data = self.node.recvClassical()
			message = list(data)
			sel = message[0]

			#print("Prover: received sel = ", sel)
			if (sel == self.numEPR):
				quit()

            # 5. select a random binary value y
			y = random.randint(0,1)

            # 6.
			b = 0
			if (y == 0):
				# measure in the comp. basis the qubit of the selected pair
				b = self.reg[sel].measure()
			else:
				# apply H then measure in the comp. basis the qubit of the selected pair
				self.reg[sel].H()
				b = self.reg[sel].measure()

			#time.sleep(1)

            # 7.
			self.node.sendClassical("node0",[b,y])

            # 8. is performed by the Verifier
			#print("Prover: done")


##############################
#
# main
#
def main():

	#print('NA2010 - Prover')
	#print('Number of arguments:', len(sys.argv), 'arguments.')
	#print('Argument List:', str(sys.argv))
	m = int(sys.argv[1])
	prover = Prover(m)


##############################
main()
