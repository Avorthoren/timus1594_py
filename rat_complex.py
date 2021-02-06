from __future__ import annotations
from fractions import Fraction
import math
from typing import Union


class RatComplex:
	def __init__(self, r: Union[int, float, Fraction] = 0, im: [int, float, Fraction] = 0):
		self.r = r if isinstance(r, Fraction) else Fraction(r)
		self.im = im if isinstance(im, Fraction) else Fraction(im)

	def abs2(self):
		return abs(self.r * self.r + self.im * self.im)

	def __abs__(self):
		return math.sqrt(self.abs2())

	def __str__(self):
		if self.r:
			res = str(self.r)
			if self.im:
				minus = self.im < 0
				a = abs(self.im)
				if a == 1:
					res += f" {'-' if minus else '+'} i"
				else:
					res += f" {'-' if minus else '+'} i*{a}"
		elif self.im:
			a = abs(self.im)
			if a == 1:
				minus = self.im < 0
				res = "-i" if minus else "i"
			else:
				res = f"i*{self.im}"
		else:
			res = "0"

		return res

	def __repr__(self):
		return str(self)

	def copy(self, neg=False):
		inst = RatComplex.__new__(RatComplex)
		if neg:
			inst.r = -self.r
			inst.im = -self.im
		else:
			inst.r = self.r
			inst.im = self.im

		return inst

	def __pos__(self):
		return self.copy()

	def __neg__(self):
		return self.copy(neg=True)

	def __bool__(self):
		return bool(self.r or self.im)

	def __add__(self, other):
		inst = RatComplex.__new__(RatComplex)
		if isinstance(other, RatComplex):
			inst.r = self.r + other.r
			inst.im = self.im + other.im
		else:
			other = Fraction(other)
			inst.r = self.r + other
			inst.im = self.im

		return inst

	def __iadd__(self, other):
		if isinstance(other, RatComplex):
			self.r += other.r
			self.im += other.im
		else:
			self.r += other

		return self

	def __radd__(self, other):
		return self + other

	def __sub__(self, other):
		inst = RatComplex.__new__(RatComplex)
		if isinstance(other, RatComplex):
			inst.r = self.r - other.r
			inst.im = self.im - other.im
		else:
			other = Fraction(other)
			inst.r = self.r - other
			inst.im = self.im

		return inst

	def __isub__(self, other):
		if isinstance(other, RatComplex):
			self.r -= other.r
			self.im -= other.im
		else:
			self.r -= other

		return self

	def __rsub__(self, other):
		inst = RatComplex.__new__(RatComplex)
		inst.r = other - self.r
		inst.im = -self.im

		return inst

	def __mul__(self, other):
		inst = RatComplex.__new__(RatComplex)
		if isinstance(other, RatComplex):
			inst.r = self.r * other.r - self.im * other.im
			inst.im = self.im * other.r + self.r * other.im
		else:
			other = Fraction(other)
			inst.r = self.r * other
			inst.im = self.im * other

		return inst

	def __imul__(self, other):
		if isinstance(other, RatComplex):
			r = self.r * other.r - self.im * other.im
			im = self.im * other.r + self.r * other.im
			self.r, self.im = r, im
		else:
			self.r *= other
			self.im *= other

		return self

	def __rmul__(self, other):
		return self * other

	def __truediv__(self, other):
		inst = RatComplex.__new__(RatComplex)
		if isinstance(other, RatComplex):
			den = other.r * other.r + other.im * other.im
			inst.r = (self.r * other.r + self.im * other.im) / den
			inst.im = (self.im * other.r - self.r * other.im) / den
		else:
			other = Fraction(other)
			inst.r = self.r / other
			inst.im = self.im / other

		return inst

	def __itruediv__(self, other):
		if isinstance(other, RatComplex):
			den = other.r * other.r + other.im * other.im
			r = (self.r * other.r + self.im * other.im) / den
			im = (self.im * other.r - self.r * other.im) / den
			self.r, self.im = r, im
		else:
			other = Fraction(other)
			self.r = self.r / other
			self.im = self.im / other

		return self

	def __mod__(self, other):
		inst = RatComplex.__new__(RatComplex)
		inst.r = self.r % other
		inst.im = self.im % other

		return inst

	def __imod__(self, other):
		self.r %= other
		self.im %= other

		return self


def tests():
	rc = RatComplex(4, -3)
	rcc = RatComplex(-1, 5)
	print(rc / rcc)


if __name__ == "__main__":
	tests()



