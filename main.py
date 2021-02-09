from itertools import chain
from time import time
from typing import Union, List

import complex_modulo

ComplexMod = complex_modulo.factory()
MatrixT = List[List[ComplexMod]]
SparseMatrixT = List[List[Union[int, ComplexMod]]]


def showMatrix(matrix: Union[MatrixT, SparseMatrixT]) -> None:
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


def createMatrixSparse(m: int, n: int) -> SparseMatrixT:
	"""
	Mark all cells and construct sparse neighbours matrix.
	If m is odd, m and n will be swapped.

	For m, n = 4, 7 we will mark field like that:
	 0  0  1  1
	 2  2  3  3
	 4  4  5  5
	 6  6  7  7
	 8  8  9  9
	10 10 11 11
	12 12 13 13

	we will get full matrix like that:
	1 0 i 0 0 0 0 0 0 0 0 0 0 0
	1 1 0 i 0 0 0 0 0 0 0 0 0 0
	i 0 1 1 i 0 0 0 0 0 0 0 0 0
	0 i 0 1 0 i 0 0 0 0 0 0 0 0
	0 0 i 0 1 0 i 0 0 0 0 0 0 0
	0 0 0 i 1 1 0 i 0 0 0 0 0 0
	0 0 0 0 i 0 1 1 i 0 0 0 0 0
	0 0 0 0 0 i 0 1 0 i 0 0 0 0
	0 0 0 0 0 0 i 0 1 0 i 0 0 0
	0 0 0 0 0 0 0 i 1 1 0 i 0 0
	0 0 0 0 0 0 0 0 i 0 1 1 i 0
	0 0 0 0 0 0 0 0 0 i 0 1 0 i
	0 0 0 0 0 0 0 0 0 0 i 0 1 0
	0 0 0 0 0 0 0 0 0 0 0 i 1 1

	and sparse matrix like that:
	0 0 1 0 i
	0 1 1 0 i
	i 0 1 1 i
	i 0 1 0 i
	i 0 1 0 i
	i 1 1 0 i
	i 0 1 1 i
	i 0 1 0 i
	i 0 1 0 i
	i 1 1 0 i
	i 0 1 1 i
	i 0 1 0 i
	i 0 1 0 0
	i 1 1 0 0
	"""
	if m & 1:
		if n & 1:
			raise ValueError("Either m or n must be even")
		m, n = n, m

	colCapacity = m // 2
	totalCols = m + 1
	totalRows = colCapacity * n

	matrix = []
	for rowI in range(totalRows):
		row = [0] * totalCols

		if rowI >= colCapacity:
			row[0] = ComplexMod(0, 1)  # i

		row[colCapacity] = ComplexMod(1)  # 1

		rest = rowI % m
		if rest not in (0, m-1):
			if rest < colCapacity:
				row[colCapacity - 1] = ComplexMod(1)  # 1
			else:
				row[colCapacity + 1] = ComplexMod(1)  # 1

		if rowI < (totalRows - colCapacity):
			row[-1] = ComplexMod(0, 1)  # i

		matrix.append(row)

	return matrix


def det(matrix: MatrixT, show: bool) -> ComplexMod:
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

	res = ComplexMod(1)
	# For each column nullify all elements under diagonal
	for i in range(n):
		diagEl = matrix[i][i]
		if not diagEl:
			# Fuck, it can be zero. We need to swap rows :(
			raise RuntimeError(f"{i}'th diagonal element is zero")

		if diagEl.r and diagEl.im:
			raise RuntimeError(f"{i}'th diagonal element is not simple")

		# res = res * (abs(diagEl.r) if diagEl.r else abs(diagEl.im)) % diagEl.MOD()
		res *= diagEl

		# Process needed rows under `diagEl`
		for rowI in range(i + 1, min(i + maxRowOffset + 1, n)):
			if matrix[rowI][i]:
				mult = matrix[rowI][i] / diagEl
				for colI in range(i, min(i + maxColOffset + 1, n)):
					matrix[rowI][colI] -= matrix[i][colI] * mult

		if show:
			showMatrix(matrix)

	return res


def detSparse(matrix: SparseMatrixT, show: bool) -> ComplexMod:
	totalRows = len(matrix)
	colCapacity = len(matrix[0]) // 2
	totalCols = colCapacity * 2 + 1

	res = ComplexMod(1)
	# For each column nullify all elements under diagonal
	for i in range(totalRows):
		diagEl = matrix[i][colCapacity]

		res *= diagEl

		# Process needed rows under `diagEl`
		for offset in range(1, min(colCapacity + 1, totalRows - i)):
			rowI = i + offset
			if matrix[rowI][colCapacity - offset]:
				mult = matrix[rowI][colCapacity - offset] / diagEl
				for colI in range(colCapacity - offset, min(totalCols, totalRows - i + colCapacity) - offset):
					matrix[rowI][colI] -= matrix[i][colI + offset] * mult

		if show:
			showMatrix(matrix)

	return res


def solve(m: int, n: int, show: bool = False) -> int:
	if m & 1:
		m, n = n, m

	try:
		matrix = createMatrix(m, n)
	except ValueError:
		return 0

	if show:
		showMatrix(matrix)

	determinant = det(matrix, show)

	return abs(determinant.r) if determinant.r else abs(determinant.im)


def solveSparse(m: int, n: int, show: bool = False) -> int:
	if m & 1:
		m, n = n, m

	try:
		matrix = createMatrixSparse(m, n)
	except ValueError:
		return 0

	if show:
		showMatrix(matrix)

	determinant = detSparse(matrix, show)

	return abs(determinant.r) if determinant.r else abs(determinant.im)


if __name__ == "__main__":
	S = 100
	M, N = 4, 7

	# t0 = time()
	# d = solve(M, N, show=True)
	# t1 = time()
	# print(f"d({M}, {N}) = {d}")
	# print(t1 - t0, "sec")
	# print()

	t0 = time()
	d = solveSparse(M, N, show=False)
	t1 = time()
	print(f"d({M}, {N}) = {d}")
	print(t1 - t0, "sec")
	print()

	# with open('res.txt', 'w') as f:
	# 	N_MAX = 100
	# 	for w in range(2, N_MAX+1, 2):
	# 		for h in chain(range(1, w+1), range(w+1, N_MAX+1, 2)):
	# 			try:
	# 				d = solve(w, h)
	# 			except RuntimeError as e:
	# 				errorMessage = f"{w} {h} -> ERROR: {e}"
	# 				print(errorMessage)
	# 				print(errorMessage, file=f)
	# 			else:
	# 				print(f"{w} {h} {d}")
	# 				print(f"{w} {h} {d}", file=f)
