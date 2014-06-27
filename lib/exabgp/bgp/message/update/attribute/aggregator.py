# encoding: utf-8
"""
aggregator.py

Created by Thomas Mangin on 2012-07-14.
Copyright (c) 2009-2013 Exa Networks. All rights reserved.
"""

from exabgp.protocol.family import AFI,SAFI
from exabgp.bgp.message.open.asn import ASN
from exabgp.protocol.ip.inet import Inet

from exabgp.bgp.message.update.attribute.id import AttributeID
from exabgp.bgp.message.update.attribute import Flag,Attribute

# =================================================================== AGGREGATOR (7)

class Aggregator (Attribute):
	ID = AttributeID.AGGREGATOR
	FLAG = Flag.TRANSITIVE|Flag.OPTIONAL
	MULTIPLE = False

	def __init__ (self,asn,speaker):
		self.asn = asn
		self.speaker = speaker
		self._str = None

	def pack (self,asn4,as4agg=False):
		if as4agg:
			backup = self.ID
			self.ID = AttributeID.AS4_AGGREGATOR
			packed = self._attribute(self.asn.pack(True)+self.speaker.pack())
			self.ID = backup
			return packed
		elif asn4:
			return self._attribute(self.asn.pack(True)+self.speaker.pack())
		elif not self.asn.asn4():
			return self._attribute(self.asn.pack(False)+self.speaker.pack())
		else:
			return self._attribute(self.asn.trans()+self.speaker.pack()) + self.pack(True,True)

	def __len__ (self):
		raise RuntimeError('size can be 6 or 8 - we can not say')

	def __str__ (self):
		if not self._str:
			self._str = '%s:%s' % (self.asn,self.speaker)
		return self._str

	@classmethod
	def unpack (cls,data):
		asn = 0
		for value in (ord(_) for _ in data[:-4]):
			asn = (asn << 8) + value
		return cls(ASN(asn),Inet(AFI.ipv4,SAFI.unicast,data[-4:]))
