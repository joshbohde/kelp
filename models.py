from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Program(models.Model):
	name		=	models.CharField(max_length=64)
	url			=	models.CharField(max_length=64,null=True,blank=True)
	def __unicode__(self):
		return str(self.name)
		
class ProgramBlock(models.Model):
	start		=	models.TimeField()
	end			=	models.TimeField()
	def __unicode__(self):
		return str(self.start)
	def slots(self):
		slots = ProgramSlot.objects.filter(time=self)
		return slots
		
class ProgramSlot(models.Model):
	#blocks for programming
	
	#the active toggle is so you don't delete old
	#blocks with entries tied to them
	active		=	models.BooleanField()
	program		=	models.ForeignKey(Program)
	time		=	models.ForeignKey(ProgramBlock)

	def __unicode__(self):
		return str(self.time) + " - " + str(self.program)

	def isdone(self):
		try:
			e = Entry.objects.filter(date=datetime.datetime.today).get(slot=self)
			return e
		except:
			return False
				
class Entry(models.Model):
	#Individual program log entry
	slot	=	models.ForeignKey(ProgramSlot)
	date		=	models.DateField(auto_now=True)
	time		=	models.TimeField(auto_now=True)
	notes		=	models.CharField(max_length=64)
	def __unicode__(self):
		return str(self.time)
		
class DiskJockey(models.Model):
	user		=	models.OneToOneField(User)
	name		=	models.CharField(max_length=35)
	seniority	=	models.IntegerField(default=0)
	email		=	models.EmailField(max_length=64)


class Semester(models.Model):
	name		=	models.CharField(max_length=16)
	start		=	models.DateField()
	end			=	models.DateField()

DAY_CHOICES = (
  ('Monday', 'Mon'),
  ('Tuesday', 'Tues'),
  ('Wednesday', 'Wed'),
  ('Thursday', 'Thurs'),
  ('Friday', 'Fri'),
  ('Saturday', 'Sat'),
  ('Sunday', 'Sun'),
)

class ShowBlock(models.Model):
	day			=	models.CharField(max_length=10,choices=DAY_CHOICES)
	start		=	models.TimeField()
	end			=	models.TimeField()
	semester	=	models.ForeignKey(Semester)


class Show(models.Model):
	name		=	models.CharField(max_length=75)
	type		=	models.TextField()
	block		=	models.ForeignKey(ShowBlock,blank=True,null=True)
	dj			=	models.ForeignKey(DiskJockey)

class pick(models.Model):
	#this will be used for sorting through
	#show selections
	block		=	models.ForeignKey(ShowBlock)
	show		=	models.ForeignKey(Show)
	rank		=	models.IntegerField()