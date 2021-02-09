from __future__ import annotations
import math
from typing import Union


DEFAULT_MOD = 10**9 + 7


class _ComplexMod:
	_MOD = DEFAULT_MOD  # MUST be prime

	@classmethod
	def MOD(cls):
		return cls._MOD

	def __init__(self, r: int = 0, im: int = 0):
		self._r = r % self._MOD
		self._im = im % self._MOD
		self._inv = None

	@property
	def r(self) -> int:
		return self._r

	@r.setter
	def r(self, value: int):
		if value != self._r:
			self._inv = None

		self._r = value

	@property
	def im(self) -> int:
		return self._im

	@im.setter
	def im(self, value: int):
		if value != self._im:
			self._inv = None

		self._im = value

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

	@classmethod
	def zero(cls) -> _ComplexMod:
		return cls()

	def copy(self) -> _ComplexMod:
		return self.__class__(self.r, self.im)

	def __copy__(self) -> _ComplexMod:
		return self.copy()

	def __pos__(self) -> _ComplexMod:
		return self.copy()

	def __neg__(self) -> _ComplexMod:
		return self.__class__(-self.r, -self.im)

	def abs2(self) -> int:
		return self.r * self.r + self.im * self.im

	def __abs__(self) -> float:
		return math.sqrt(self.abs2())

	def conjugate(self) -> _ComplexMod:
		return self.__class__(self.r, -self.im)

	def _inverse(self) -> _ComplexMod:
		if self._inv is None:
			self._inv = self.conjugate() * pow(self.abs2(), self._MOD - 2, self._MOD)

		return self._inv

	@property
	def inverse(self) -> _ComplexMod:
		return self._inverse().copy()

	def __bool__(self):
		return bool(self.r or self.im)

	def __eq__(self, other: Union[_ComplexMod, int]):
		if isinstance(other, self.__class__):
			return self.r == other.r and self.im == other.im
		else:
			return self.im == 0 and self.r == other

	def __ne__(self, other: Union[_ComplexMod, int]):
		return not self == other

	def __add__(self, other: Union[_ComplexMod, int]) -> _ComplexMod:
		if isinstance(other, self.__class__):
			return self.__class__(
				self.r + other.r,
				self.im + other.im
			)
		else:
			return self.__class__(
				self.r + other,
				self.im
			)

	def __iadd__(self, other: Union[_ComplexMod, int]) -> _ComplexMod:
		if isinstance(other, self.__class__):
			self.r = (self.r + other.r) % self._MOD
			self.im = (self.im + other.im) % self._MOD
		else:
			self.r = (self.r + other) % self._MOD

		return self

	def __radd__(self, other: Union[_ComplexMod, int]) -> _ComplexMod:
		return self + other

	def __sub__(self, other: Union[_ComplexMod, int]) -> _ComplexMod:
		if isinstance(other, self.__class__):
			return self.__class__(
				self.r - other.r,
				self.im - other.im
			)
		else:
			return self.__class__(
				self.r - other,
				self.im
			)

	def __isub__(self, other: Union[_ComplexMod, int]) -> _ComplexMod:
		if isinstance(other, self.__class__):
			self.r = (self.r - other.r) % self._MOD
			self.im = (self.im - other.im) % self._MOD
		else:
			self.r = (self.r - other) % self._MOD

		return self

	def __rsub__(self, other: Union[_ComplexMod, int]) -> _ComplexMod:
		return self.__class__(
			other - self.r,
			-self.im
		)

	def __mul__(self, other: Union[_ComplexMod, int]) -> _ComplexMod:
		if isinstance(other, self.__class__):
			return self.__class__(
				self.r * other.r - self.im * other.im,
				self.r * other.im + self.im * other.r
			)
		else:
			return self.__class__(
				self.r * other,
				self.im * other
			)

	def __imul__(self, other: Union[_ComplexMod, int]) -> _ComplexMod:
		if isinstance(other, self.__class__):
			r = (self.r * other.r - self.im * other.im) % self._MOD
			im = (self.r * other.im + self.im * other.r) % self._MOD
			self.r, self.im = r, im
		else:
			self.r = (self.r * other) % self._MOD
			self.im = (self.im * other) % self._MOD

		return self

	def __rmul__(self, other: Union[_ComplexMod, int]) -> _ComplexMod:
		return self * other

	def __truediv__(self, other: Union[_ComplexMod, int]) -> _ComplexMod:
		if isinstance(other, self.__class__):
			return self * other._inverse()
		else:
			return self * pow(other, self._MOD - 2, self._MOD)

	def __itruediv__(self, other: Union[_ComplexMod, int]) -> _ComplexMod:
		if isinstance(other, self.__class__):
			self.__imul__(other._inverse())
		else:
			self.__imul__(pow(other, self._MOD - 2, self._MOD))

		return self

	def __rdiv__(self, other: Union[_ComplexMod, int]) -> _ComplexMod:
		return other * self._inverse()


def factory(mod: int = DEFAULT_MOD) -> type(_ComplexMod):
	class ComplexMod(_ComplexMod):
		_MOD = mod

	return ComplexMod


def tests():
	# c = list()
	# c.append(_ComplexMod(13, -5))
	# c.append(_ComplexMod(-4, 31))
	# c.append(c[0] + c[1])
	# c.append(c[0] - c[1])
	# c.append(c[0] * c[1])
	# c.append(c[0] / c[1])
	#
	# for ci in c:
	# 	print(ci)
	#
	# c[0] += c[1]
	# print(c[0])

	# k = -11
	# c = _ComplexMod(0, k)
	# print(c.inverse)
	# print(f"i*{DEFAULT_MOD - pow(k, DEFAULT_MOD-2, DEFAULT_MOD)}")
	c = _ComplexMod(10, 8)
	c /= 2
	print(c)


if __name__ == "__main__":
	tests()
