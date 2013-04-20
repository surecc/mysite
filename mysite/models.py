#coding=utf-8
from django.db import models

# Create your models here.
class Cate1(models.Model):
	catename1 = models.CharField(max_length=200)
	def __unicode__(self):
		return(self.catename1)

class Cate2(models.Model):
	catename1 = models.ForeignKey(Cate1)
	catename2 = models.CharField(max_length=200)
	def __unicode__(self):
		return(unicode(self.catename1) + '>>' + self.catename2)

class Commidity(models.Model):
	price = models.FloatField(default=0.0)
	desc = models.CharField(max_length=300)
	url = models.URLField()
	def __unicode__(self):
		return (self.desc + '_' + self.url)

class Feature(models.Model):
	total = models.FloatField(default=0.0)
	h_gray = models.FloatField(default=0.0)
	h_R = models.FloatField(default=0.0)
	h_G = models.FloatField(default=0.0)
	h_B = models.FloatField(default=0.0)
	shape = models.CharField(max_length=200, default='0')
	feedback = models.CharField(max_length=200, default='0')
	def __unicode__(self):
		return str(self.total)

class Imagedata(models.Model):
	FEMALE = 'fm'
	MALE = 'ml'
	OTHER = 'ot'
	GENDER_CHOICES = (
		(FEMALE,'female'),
		(MALE,'male'),
		(OTHER,'other'),
	)
	category = models.ForeignKey(Cate2)
	commidity = models.ForeignKey(Commidity)
	feature = models.ForeignKey(Feature)
	localfile = models.ImageField(upload_to='upload/%Y/%m/%d/')	
	gender = models.CharField(max_length=6, 
				choices=GENDER_CHOICES,
				default=FEMALE)
	is_featured = models.BooleanField(default=False)
	def __unicode__(self):
		return str(self.localfile.name)
