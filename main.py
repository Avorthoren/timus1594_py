from time import time
from random import randint
from typing import Union, List

from scipy.sparse.linalg import splu
from scipy.sparse import csc_matrix

from complex_modulo import ComplexMod
from rat_complex import RatComplex

ElementT = Union[type(ComplexMod), type(RatComplex)]
MatrixT = Union[List[List[ComplexMod]], List[List[RatComplex]]]


def showMatrix(matrix: MatrixT) -> None:
	for row in matrix:
		print(" ".join(str(i) for i in row))
	print()


def createMatrix(m: int, n: int, type_: ElementT) -> MatrixT:
	"""
	Mark all cells and construct neighbours matrix.

	For even m:
	00112233
	44556677
	...
	For odd m:
	0011223
	3445566
	...
	"""
	mn = m * n
	if mn & 1:
		raise ValueError("Either m or n must be even")

	matrixWidth = mn // 2

	matrix = [[type_() for _ in range(matrixWidth)] for __ in range(matrixWidth)]

	for y in range(n-1):
		for x in range(m-1):
			isBlack = (x & 1) ^ (y & 1)
			curNumber = (x + y * m) // 2
			rightNumber = (x+1 + y * m) // 2
			downNumber = (x + (y+1) * m) // 2
			if isBlack:
				matrix[rightNumber][curNumber].r = 1
				matrix[downNumber][curNumber].im = 1
			else:
				matrix[curNumber][rightNumber].r = 1
				matrix[curNumber][downNumber].im = 1

		x = m-1
		isBlack = (x & 1) ^ (y & 1)
		curNumber = (x + y * m) // 2
		downNumber = (x + (y + 1) * m) // 2
		if isBlack:
			matrix[downNumber][curNumber].im = 1
		else:
			matrix[curNumber][downNumber].im = 1

	y = n-1
	for x in range(m-1):
		isBlack = (x & 1) ^ (y & 1)
		curNumber = (x + y * m) // 2
		rightNumber = (x + 1 + y * m) // 2
		if isBlack:
			matrix[rightNumber][curNumber].r = 1
		else:
			matrix[curNumber][rightNumber].r = 1

	return matrix


def det(matrix: MatrixT) -> ElementT:
	n = len(matrix)
	res = 1

	for i in range(n):
		# print(res, end="")

		k = i
		for j in range(i+1, n):
			if matrix[j][i].abs2() > matrix[k][i].abs2():
				k = j
		if not matrix[k][i]:
			res = 0
			break

		matrix[i], matrix[k] = matrix[k], matrix[i]
		if i != k:
			res = -res

		# print(f" * {matrix[i][i]}")

		res *= matrix[i][i]

		for j in range(i+1, n):
			matrix[i][j] /= matrix[i][i]

		for j in range(n):
			if j != i and matrix[j][i]:
				for k in range(i+1, n):
					matrix[j][k] -= matrix[i][k] * matrix[j][i]

		# showMatrix(matrix)

	return res


def solve(m: int, n: int, type_: ElementT) -> ElementT:
	try:
		matrix = createMatrix(m, n, type_)
	except ValueError:
		return 0

	showMatrix(matrix)

	return det(matrix)


def test(n, m, type_):
	matrix = createMatrix(m, n, type_)
	# matrix = [
	# 	[1, 1j, 0, 0, 0, 0],
	# 	[1j, 1, 1j, 0, 0, 0],
	# 	[0, 1j, 1, 1j, 0, 0],
	# 	[0, 0, 1j, 1, -1j, 0],
	# 	[0, 0, 0, 1j, 1, 1j],
	# 	[0, 0, 0, 0, 1j, 1],
	# ]
	# nn = 1000
	# matrix = []
	# for i in range(nn):
	# 	matrix.append([(1 if (randint(0, nn-1) < 2 or j == i) else 0) for j in range(nn)])
	# matrix = csc_matrix(matrix)

	for col in matrix:
		print(" ".join(str(i) for i in col))
	print()

	# lu = splu(matrix)
	# diagL = lu.L.diagonal()
	# diagU = lu.U.diagonal()
	# det_ = diagL.prod()*diagU.prod()
	# print(det_)

	return det(matrix)


if __name__ == "__main__":
	"""
	1  0  i  0  0  0  0  0  0  0  0  0  0  0  0
	1  1  0  i  0  0  0  0  0  0  0  0  0  0  0
	0  1  0  0  i  0  0  0  0  0  0  0  0  0  0
	i  0  1  1  0  i  0  0  0  0  0  0  0  0  0
	0  i  0  1  1  0  i  0  0  0  0  0  0  0  0
	0  0  i  0  0  1  0  i  0  0  0  0  0  0  0
	0  0  0  i  0  1  1  0  i  0  0  0  0  0  0
	0  0  0  0  i  0  1  0  0  i  0  0  0  0  0
	0  0  0  0  0  i  0  1  1  0  i  0  0  0  0
	0  0  0  0  0  0  i  0  1  1  0  i  0  0  0
	0  0  0  0  0  0  0  i  0  0  1  0  i  0  0
	0  0  0  0  0  0  0  0  i  0  1  1  0  i  0
	0  0  0  0  0  0  0  0  0  i  0  1  0  0  i
	0  0  0  0  0  0  0  0  0  0  i  0  1  1  0
	0  0  0  0  0  0  0  0  0  0  0  i  0  1  1

	1  0  i  0  0  0  0  0  0  0  0  0  0  0  0
	0  1 -i  i  0  0  0  0  0  0  0  0  0  0  0
	0  1  0  0  i  0  0  0  0  0  0  0  0  0  0
	0  0  2  1  0  i  0  0  0  0  0  0  0  0  0
	0  i  0  1  1  0  i  0  0  0  0  0  0  0  0
	0  0  i  0  0  1  0  i  0  0  0  0  0  0  0
	0  0  0  i  0  1  1  0  i  0  0  0  0  0  0
	0  0  0  0  i  0  1  0  0  i  0  0  0  0  0
	0  0  0  0  0  i  0  1  1  0  i  0  0  0  0
	0  0  0  0  0  0  i  0  1  1  0  i  0  0  0
	0  0  0  0  0  0  0  i  0  0  1  0  i  0  0
	0  0  0  0  0  0  0  0  i  0  1  1  0  i  0
	0  0  0  0  0  0  0  0  0  i  0  1  0  0  i
	0  0  0  0  0  0  0  0  0  0  i  0  1  1  0
	0  0  0  0  0  0  0  0  0  0  0  i  0  1  1
 
	1  0  i  0  0  0  0  0  0  0  0  0  0  0  0
	0  1 -i  i  0  0  0  0  0  0  0  0  0  0  0
	0  0  i -i  i  0  0  0  0  0  0  0  0  0  0
	0  0  2  1  0  i  0  0  0  0  0  0  0  0  0
	0  0 -1  1  1  0  i  0  0  0  0  0  0  0  0
	0  0  i  0  0  1  0  i  0  0  0  0  0  0  0
	0  0  0  i  0  1  1  0  i  0  0  0  0  0  0
	0  0  0  0  i  0  1  0  0  i  0  0  0  0  0
	0  0  0  0  0  i  0  1  1  0  i  0  0  0  0
	0  0  0  0  0  0  i  0  1  1  0  i  0  0  0
	0  0  0  0  0  0  0  i  0  0  1  0  i  0  0
	0  0  0  0  0  0  0  0  i  0  1  1  0  i  0
	0  0  0  0  0  0  0  0  0  i  0  1  0  0  i
	0  0  0  0  0  0  0  0  0  0  i  0  1  1  0
	0  0  0  0  0  0  0  0  0  0  0  i  0  1  1
 
	1  0  i  0  0  0  0  0  0  0  0  0  0  0  0
	0  1 -i  i  0  0  0  0  0  0  0  0  0  0  0
	0  0  i -i  i  0  0  0  0  0  0  0  0  0  0
	0  0  0  3 -2  i  0  0  0  0  0  0  0  0  0
	0  0  0  0  2  0  i  0  0  0  0  0  0  0  0
	0  0  0  i -i  1  0  i  0  0  0  0  0  0  0
	0  0  0  i  0  1  1  0  i  0  0  0  0  0  0
	0  0  0  0  i  0  1  0  0  i  0  0  0  0  0
	0  0  0  0  0  i  0  1  1  0  i  0  0  0  0
	0  0  0  0  0  0  i  0  1  1  0  i  0  0  0
	0  0  0  0  0  0  0  i  0  0  1  0  i  0  0
	0  0  0  0  0  0  0  0  i  0  1  1  0  i  0
	0  0  0  0  0  0  0  0  0  i  0  1  0  0  i
	0  0  0  0  0  0  0  0  0  0  i  0  1  1  0
	0  0  0  0  0  0  0  0  0  0  0  i  0  1  1

	1  0  i  0  0  0  0  0  0  0  0  0  0  0  0
	0  1 -i  i  0  0  0  0  0  0  0  0  0  0  0
	0  0  i -i  i  0  0  0  0  0  0  0  0  0  0
	0  0  0  3 -2  i  0  0  0  0  0  0  0  0  0
	0  0  0  0  2  0  i  0  0  0  0  0  0  0  0
	0  0  0  i -i  1  0  i  0  0  0  0  0  0  0
	0  0  0  i  0  1  1  0  i  0  0  0  0  0  0
	0  0  0  0  i  0  1  0  0  i  0  0  0  0  0
	0  0  0  0  0  i  0  1  1  0  i  0  0  0  0
	0  0  0  0  0  0  i  0  1  1  0  i  0  0  0
	0  0  0  0  0  0  0  i  0  0  1  0  i  0  0
	0  0  0  0  0  0  0  0  i  0  1  1  0  i  0
	0  0  0  0  0  0  0  0  0  i  0  1  0  0  i
	0  0  0  0  0  0  0  0  0  0  i  0  1  1  0
	0  0  0  0  0  0  0  0  0  0  0  i  0  1  1

	"""
	S = 10
	M, N = 5, 6

	# d(2, 4) = 5
	# d(6, 6) = 6728
	# d(10, 10) = 258584046368 = 584044562
	# d(20, 20) = 1269984011256235834242602753102293934298576249856 = 752148172
	# d(30, 30) = ... = 671246513
	# d(40, 40) = ... = 768466191

	t0 = time()
	d = solve(M, N, ComplexMod)
	t1 = time()
	print(d)
	print(t1 - t0, "sec")
	print()

	# test(M, N, type_=ComplexMod)

