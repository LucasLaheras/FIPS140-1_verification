import numpy as np
from itertools import groupby


class FIPS1401(object):
	def __init__(self, binary_key):
		self.binary_key = binary_key
		self.hex_length = int(len(self.binary_key)/4)
		mono = self.monobit_test()
		poker = self.poker_test()
		runs = self.runs_test()
		long_run = self.long_run_test()

		if mono and poker and runs and long_run:
			print("APROVED")
		else:
			print("REPROVED")
			print("Monobit Test", mono)
			print("Poker Test", poker)
			print("Runs Test", runs)
			print("Long Run Test", long_run)

	def monobit_test(self):
		x = self.binary_key.count('1')
		if 9654 < x < 10346:
			return True
		return False

	def poker_test(self):
		count_vector = np.zeros(16)
		for x in range(self.hex_length):
			num_int = int(self.binary_key[x*4: (x+1)*4], 2)
			count_vector[num_int] += 1

		x = 16.0/float(self.hex_length) * sum(count_vector**2) - self.hex_length

		if 1.03 < x < 57.4:
			return True
		return False

	def runs_test(self):
		count_one = np.zeros(6)
		count_zero = np.zeros(6)
		for i, j in groupby(self.binary_key):
			length_of_run = len(list(j))-1
			if length_of_run > 5:
				length_of_run = 5
			if i == '0':
				count_zero[length_of_run] += 1
			else:
				count_one[length_of_run] += 1

		count_vector = count_one
		if (2267 < count_vector[0] < 2733 and 1079 < count_vector[1] < 1421 and 502 < count_vector[2] < 748
				and 402 > count_vector[3] > 223 > count_vector[4] > 90 and 90 < count_vector[5] < 223):

			count_vector = count_zero
			if (2267 < count_vector[0] < 2733 and 1079 < count_vector[1] < 1421 and 502 < count_vector[2] < 748
					and 402 > count_vector[3] > 223 > count_vector[4] > 90 and 90 < count_vector[5] < 223):

				return True
		return False

	def long_run_test(self):
		for _, j in groupby(self.binary_key):
			if len(list(j))-1 >= 34:
				return False
		return True


if __name__ == '__main__':
	f = open("Chaves de Criptografia.txt", "r")

	for i in range(20):
		key = f.readline()
		key = key[1:-2]

		binary_key = str('')
		for caracter in key:
			binary_key += "{0:04b}".format(int(caracter, 16))

		print("key line", i+1)
		testes = FIPS1401(binary_key)
		print("")

	f.close()
