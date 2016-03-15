from . import db
from sqlalchemy.orm import backref
from sqlalchemy.sql import func
import datetime
import cloudinary.utils

include_schemas=True


class Member(db.Model):
	__tablename__='Members'
	id = db.Column(db.Integer,primary_key=True)
	first_name = db.Column(db.String(100))
	last_name = db.Column(db.String(100))
	project = db.relationship('Project',backref = 'creator')
	pledges = db.relationship('Pledge',backref = 'pledge', foreign_keys= 'Pledge.member_id')

	def __init__(self, first_name, last_name, project, pledges):
		self.first_name = first_name
		self.last_name = last_name
		self.project = project
		self.pledges = pledges


class Project(db.Model):
	__tablename__='Projects'
	id=db.Column(db.Integer,primary_key = True)
	member_id=db.Column(db.Integer,db.ForeignKey('Members.id'), nullable=False)
	name=db.Column(db.String(100))
	short_description = db.Column(db.Text)
	long_description = db.Column(db.Text)
	goal_amount = db.Column(db.Integer)
	image_filename = db.Column(db.String(200))
	time_start = db.Column(db.DateTime)
	time_end = db.Column(db.DateTime)
	time_created = db.Column(db.DateTime)
	pledges = db.relationship('Pledge',backref = 'project', foreign_keys= 'Pledge.project_id')

	@property
	def num_pledges(self):
	    return len(self.pledges)

	@property
	def total_pledges(self):
	    total_pledges = db.session.query(func.sum(Pledge.amount)).filter(Pledge.project_id==self.id).one()[0]
	    if total_pledges is None:
	    	total_pledges = 0
	    return total_pledges


	"""@property
	def percentage_funded(self):
	    return int(self.total_pledges *100 / self.goal_amount)"""
	



	@property
	def num_days_left(self):
		now = datetime.datetime.now()
		num_days_left= (self.time_end - now).days 
		return num_days_left

	@property
	def image_path(self):
	    return cloudinary.utils.cloudinary_url(self.image_filename)[0]
	
		
	




class Pledge(db.Model):
	__tablename__='Pledgess'	
	id = db.Column(db.Integer,primary_key=True)
	amount=db.Column(db.Integer)
	time_created = db.Column(db.DateTime)
	project_id=db.Column(db.Integer,db.ForeignKey('Projects.id'), nullable=False)
	member_id=db.Column(db.Integer,db.ForeignKey('Members.id'), nullable=False)
	
		




















