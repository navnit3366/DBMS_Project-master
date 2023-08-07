class clubView:
	def __init__(self,li):
		self.id=li[0]
		self.name=li[1]
		self.date=li[2]
class postholderView:
	def __init__(self,li):
		self.id=li[0]
		self.name=li[1]
		self.post=li[2]
		self.contact=li[3]
		self.branch=li[4]
		self.batch=li[5]
		self.club=li[6]
class memberView:
	def __init__(self,li):
		self.id=li[0]
		self.name=li[1]
		self.contact=li[2]
		self.branch=li[3]
		self.batch=li[4]
		self.club=li[5]
class alumniView:
	def __init__(self,li):
		self.id=li[0]
		self.name=li[1]
		self.branch=li[2]
		self.contact=li[3]
		self.batch=li[4]
		self.club=li[5]
class allusersView:
	def __init__(self,li):
		self.id=li[0]
		self.name=li[1]
		self.email=li[2]
		self.post=li[3]
		self.club=li[4]
		self.contact=li[5]
		self.branch=li[6]
		self.batch=li[7]
class pasteventsView:
	def __init__(self,li):
		self.id=li[0]
		self.name=li[1]
		self.venue=li[2]
		self.time=li[3]
		self.club=li[4]
class presenteventsView:
	def __init__(self,li):
		self.id=li[0]
		self.name=li[1]
		self.venue=li[2]
		self.time=li[3]
		self.club=li[4]
class resourceView:
	def __init__(self,li):
		self.id=li[0]
		self.name=li[1]
		self.specs=li[2]
		self.cost=li[3]
class merchandiseView:
	def __init__(self,li):
		self.id=li[0]
		self.name=li[1]
		self.price=li[2]
		self.profit=li[3]
		self.quantity=li[4]
		self.contact=li[5]
		self.fundid=li[6]
		self.image=li[7]
class fundsView:
	def __init__(self,li):
		self.id=li[0]
		self.name=li[1]
		self.contact=li[2]
		self.amount=li[3]
		self.organisation=li[4]

