from time import time
from typing import Union, List

import complex_modulo

ComplexMod = complex_modulo.factory()
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


if __name__ == "__main__":
	"""
	d(1, 6) = i*1000000006 ??? 1
	d(2, 4) = 5
	d(3, 4) = 999999996 ??? 11
	d(3, 6) = i*41
	d(5, 4) = 999999912 ??? 95
	d(5, 6) = i*999998824 ??? 1183
	d(6, 6) = 6728
	d(7, 4) = 999999226 ??? 781
	d(7, 6) = i*31529
	d(9, 6) = i*999182016 ??? 817991
	d(10, 10) = 258584046368 = 584044562
	d(20, 20) = 1269984011256235834242602753102293934298576249856 = 752148172
	d(30, 30) = ... = 671246513
	d(40, 40) = ... = 768466191
	d(60, 60) = ... = 177942680
	d(100, 100) = ... = 136442580

	d(1, 2) = 1
	d(1, 4) = 1
	d(1, 6) = 1
	d(1, 8) = 1
	d(2, 1) = 1
	d(2, 2) = 2
	d(2, 3) = 3
	d(2, 4) = 5
	d(2, 5) = 8
	d(2, 6) = 13
	d(2, 7) = 21
	d(2, 8) = 34
	d(2, 9) = 55
	d(3, 2) = 1000000004 ???
	d(3, 4) = 11
	d(3, 6) = 999999966 ???
	d(3, 8) = 153
	d(4, 1) = 1
	d(4, 2) = 5
	d(4, 3) = 11
	d(4, 4) = 36
	d(4, 5) = 95
	d(4, 6) = 281
	d(4, 7) = 781
	d(4, 8) = 2245
	d(4, 9) = 6336
	d(5, 2) = 8
	d(5, 4) = 95
	d(5, 6) = 1183
	d(5, 8) = 14824
	d(6, 1) = 1
	d(6, 2) = 13
	d(6, 3) = 41
	d(6, 4) = 281
	d(6, 5) = 1183
	d(6, 6) = 6728
	d(6, 7) = 31529
	d(6, 8) = 167089
	d(6, 9) = 817991
	d(7, 2) = 999999986 ???
	d(7, 4) = 781
	d(7, 6) = 999968478 ???
	d(7, 8) = 1292697
	d(8, 1) = 1
	d(8, 2) = 34
	d(8, 3) = 153
	d(8, 4) = 2245
	d(8, 5) = 14824
	d(8, 6) = 167089
	d(8, 7) = 1292697
	d(8, 8) = 12988816
	d(8, 9) = 108435745
	d(9, 2) = 55
	d(9, 4) = 6336
	d(9, 6) = 817991
	d(9, 8) = 108435745

	d(1, 2) = i
	d(1, 4) = 1000000006 ???
	d(1, 6) = i*1000000006 ???
	d(1, 8) = 1
	d(2, 1) = 1
	d(2, 2) = 2
	d(2, 3) = 3
	d(2, 4) = 5
	d(2, 5) = 8
	d(2, 6) = 13
	d(2, 7) = 21
	d(2, 8) = 34
	d(2, 9) = 55
	d(3, 2) = i*1000000004 ???
	d(3, 4) = 999999996 ???
	d(3, 6) = i*41
	d(3, 8) = 153
	d(4, 1) = 1
	d(4, 2) = 5
	d(4, 3) = 11
	d(4, 4) = 36
	d(4, 5) = 95
	d(4, 6) = 281
	d(4, 7) = 781
	d(4, 8) = 2245
	d(4, 9) = 6336
	d(5, 2) = i*8
	d(5, 4) = 999999912 ???
	d(5, 6) = i*999998824 ???
	d(5, 8) = 14824
	d(6, 1) = 1
	d(6, 2) = 13
	d(6, 3) = 41
	d(6, 4) = 281
	d(6, 5) = 1183
	d(6, 6) = 6728
	d(6, 7) = 31529
	d(6, 8) = 167089
	d(6, 9) = 817991
	d(7, 2) = i*999999986 ???
	d(7, 4) = 999999226 ???
	d(7, 6) = i*31529
	d(7, 8) = 1292697
	d(8, 1) = 1
	d(8, 2) = 34
	d(8, 3) = 153
	d(8, 4) = 2245
	d(8, 5) = 14824
	d(8, 6) = 167089
	d(8, 7) = 1292697
	d(8, 8) = 12988816
	d(8, 9) = 108435745
	d(9, 2) = i*55
	d(9, 4) = 999993671 ???
	d(9, 6) = i*999182016 ???
	d(9, 8) = 108435745`
	"""
	# S = 100
	# M, N = S, S
	#
	# t0 = time()
	# d = solve(M, N, show=False)
	# t1 = time()
	# print(f"d({M}, {N}) = {d}")
	# print(t1 - t0, "sec")
	# print()

	with open('res.txt', 'w') as f:
		for w in range(2, 101, 2):
			for h in range(1, w+1):
				args = w, h
				try:
					d = solve(w, h)
				except RuntimeError as e:
					errorMessage = f"d{args} -> ERROR: {e}"
					print(errorMessage)
					print(errorMessage, file=f)
				else:
					print(f"d{args} = {d}")
					print(f"d{args} = {d}", file=f)
