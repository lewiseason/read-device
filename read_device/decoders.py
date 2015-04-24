import struct
from . import errors

def shift(words, by):
	if len(words) is 1:
		return words[0]

	if len(words) is 2:
		hi, lo = tuple(words)
		return (hi << by) + lo

	raise errors.DataError('Tried to shift %i words by %i bits.' % (len(words), by))

def shift16(words):
	return shift(words, 16)

def ieee754(words):
	value = shift16(words)
	return struct.unpack('>f', struct.pack('>I', value))[0]

def kJ_to_kWh(raw):
	return round(float(raw) * 0.00027777777777778, 3)

decode = {
	'ieee754': ieee754,
	'shift': shift16,
	'kJ_to_kWh': kJ_to_kWh,
}
