from time import time
from typing import Union, List

from complex_modulo import factory

ComplexMod = factory(7)
MatrixT = List[List[ComplexMod]]


def showMatrix(matrix: MatrixT) -> None:
	for row in matrix:
		print(" ".join(str(i) for i in row))
	print()


def createMatrix(m: int, n: int) -> MatrixT:
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

	matrix = [[ComplexMod.zero() for _ in range(matrixWidth)] for __ in range(matrixWidth)]

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


def det(matrix: MatrixT) -> int:
	# Prepare
	n = len(matrix)

	# Find i in first row
	maxColOffset = 0
	for colI in range(1, n):
		if matrix[0][colI].im == 1:
			maxColOffset = colI
			break

	# Find i in first col
	maxRowOffset = 0
	for rowI in range(1, n):
		if matrix[rowI][0].im == 1:
			maxRowOffset = rowI
			break

	res = 1
	# For each column nullify all elements under diagonal
	for i in range(n):
		diagEl = matrix[i][i]
		if not diagEl:
			# Fuck, it can be zero. We need to swap rows :(
			raise RuntimeError(f"{i}'th diagonal element is zero")

		if diagEl.r and diagEl.im:
			raise RuntimeError(f"{i}'th diagonal element is not simple")

		res = res * (abs(diagEl.r) if diagEl.r else abs(diagEl.im)) % diagEl.MOD()

		# Process needed rows under `diagEl`
		for rowI in range(i + 1, min(i + maxRowOffset + 1, n)):
			if matrix[rowI][i]:
				mult = matrix[rowI][i] / diagEl
				for colI in range(i, min(i + maxColOffset + 1, n)):
					matrix[rowI][colI] -= matrix[i][colI] * mult

		showMatrix(matrix)

	return res


def solve(m: int, n: int) -> int:
	t0_ = time()
	try:
		matrix = createMatrix(m, n)
	except ValueError:
		return 0
	t1_ = time()
	print(t1_ - t0_, "sec")
	print()
	showMatrix(matrix)

	return det(matrix)


if __name__ == "__main__":
	S = 100
	M, N = 9, 6

	# d(1, 6) = i*1000000006 ??? 1
	# d(2, 4) = 5
	# d(3, 4) = 999999996 ??? 11
	# d(3, 6) = i*41
	# d(5, 4) = 999999912 ??? 95
	# d(5, 6) = i*999998824 ??? 1183
	# d(6, 6) = 6728
	# d(7, 4) = 999999226 ??? 781
	# d(7, 6) = i*31529
	# d(9, 6) = i*999182016 ??? 817991
	# d(10, 10) = 258584046368 = 584044562
	# d(20, 20) = 1269984011256235834242602753102293934298576249856 = 752148172
	# d(30, 30) = ... = 671246513
	# d(40, 40) = ... = 768466191
	# d(60, 60) = ... = 177942680
	# d(100, 100) = ... = 136442580

	t0 = time()
	d = solve(M, N)
	t1 = time()
	print(f"d({M}, {N}) = {d}")
	print(t1 - t0, "sec")
	print()
