from __future__ import unicode_literals
from django.db import models
from datetime import datetime

# Create your models here.

def set_sp_image_url(instance, filename):
	return "sp_images/%s_%s" % (str(time()).replace('.','_'), filename)


class TourismFilterQuerySet(models.QuerySet):

	def my_tourism(self):
		return self.exclude(is_private=True)

class TourismFilterManager(models.Manager):

	def get_queryset(self):
		return TourismFilterQuerySet(self.model, using=self._db)

class ServiceProviderAvailabilityManager(models.Manager):

	def get_queryset(self):
		return super(ServiceProviderAvailabilityManager, self).get_queryset().exclude(is_available=False)

class ObjectManager(models.Manager):

	def get_queryset(self):
		return super(ObjectManager, self).get_queryset()


class Tourist(models.Model):
	full_name = models.CharField(max_length=100)
	email = models.EmailField(max_length=100, unique=True, null=False, blank=False)

	def __unicode__(self):
		return self.full_name

	def get_tourism_count(self):
		return Tourism.objects.filter(tourist=self.pk).count()

	def get_tourisms(self):
		return Tourism.publics.filter(tourist=self.pk).order_by('-date')

	def get_tourismguide_count(self):
		return TourismGuide.objects.filter(tourism__tourist=self.pk).count()

	def get_tourismguide(self):
		return TourismGuide.objects.filter(tourism__tourist=self.pk).order_by('-date')

	def get_tourist_feedbacks_count(self):
		return TouristFeedBack.objects.filter(tourism_guide__tourism__tourist=self.pk).count()

	def get_tourist_feedbacks(self):
		return TouristFeedBack.objects.filter(tourism_guide__tourism__tourist=self.pk).order_by('-date')

	def get_tourist_json(self):
		return {
					"id": self.pk, 
					"name": self.full_name, 
					"email": self.email,
					"tourisms": [tourism.get_tourism_json() for tourism in self.get_tourisms()]
				}
	

class Tourism(models.Model):
	tourist = models.ForeignKey(Tourist)
	origin = models.CharField(max_length=255, null=False, blank=False)
	destination = models.CharField(max_length=255, null=False, blank=False)
	is_private = models.BooleanField(default=False)
	date = models.DateTimeField(auto_created=True)

	publics = TourismFilterManager()
	objects = ObjectManager()

	def __unicode__(self):
		return self.tourist.full_name

	def get_tourism_tg_count(self):
		return TourismGuide.objects.filter(tourism=self.pk).count()

	def get_tourism_tg(self):
		return TourismGuide.objects.filter(tourism=self.pk)

	def get_tourism_json(self):
		return {
					"id": self.pk, 
					"tourist": self.tourist.get_tourist_json(), 
					"origin": self.origin,
					"destination": self.destination,
					"is_private": self.is_private,
					"tourism_guide": [tour.get_tourism_guide_json() for tour in self.get_tourism_tg()] ,
					"date": self.date
				}

class ServiceProvidersCategories(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

	def get_category_json(self):
		return {"id": self.pk, "name": self.name}

class ServiceProviders(models.Model):
	full_name = models.CharField(max_length=100, null=False, blank=False)
	country = models.CharField(max_length=100, null=False, blank=False)
	city = models.CharField(max_length=100, null=False, blank=False)
	email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
	password = models.CharField(max_length=100, null=False, blank=False)
	contact = models.CharField(max_length=100, null=False, blank=False)
	category = models.ForeignKey(ServiceProvidersCategories)
	is_available = models.BooleanField(default=True)
	is_trusted = models.BooleanField(default=False)
	image = models.ImageField(upload_to=set_sp_image_url, null=True, blank=True)

	availables = ServiceProviderAvailabilityManager()
	objects = ObjectManager()

	def __unicode__(self):
		return self.full_name

	def get_sp_image(self):
		if self.image:
			return self.image
		else:
			return None

	def get_sp_places_count(self):
		return Places.objects.filter(service_provider=self.pk).count()

	def get_sp_places(self):
		return Places.objects.filter(service_provider=self.pk).order_by('-name')

	def get_sp_languages_count(self):
		return ServiceProvidersLanguages.objects.filter(service_provider=self.pk).count()

	def get_sp_languages(self):
		return ServiceProvidersLanguages.objects.filter(service_provider=self.pk)

	def get_sp_tourismguide_count(self):
		return TourismGuide.objects.filter(service_provider=self.pk).count()

	def get_sp_tourismguide(self):
		return TourismGuide.objects.filter(service_provider=self.pk).order_by('-date')

	def get_sp_json(self):
		return {
					"id": self.pk,
					"name": self.full_name,
					"email": self.email,
					"country": self.country,
					"city": self.city,
					"contact": self.contact,
					"category": self.category.get_category_json(),
					"image": self.get_sp_image(),
					"is_available": self.is_available,
					"is_trusted": self.is_trusted,
					"places_count": self.get_sp_places_count(),
					"places": [place.get_place_json() for place in self.get_sp_places()],
					"languages_count": self.get_sp_languages_count(),
					"languages": [language.get_language_json() for language in self.get_sp_languages()],
					"tourism_guide_count": self.get_sp_tourismguide_count(),
					"tourism_guide": [tour.get_tourism_guide_json() for tour in self.get_sp_tourismguide()]
				}



class Places(models.Model):
	service_provider = models.ForeignKey(ServiceProviders)
	name = models.CharField(max_length=255)
	longitude = models.CharField(max_length=100, blank=True, null=True)
	latitude = models.CharField(max_length=100, blank=True, null=True)

	def __unicode__(self):
		return self.name

	def get_place_activities(self):
		return PlaceActivities.objects.filter(place=self.pk)

	def get_place_json(self):
		return {
					"id": self.pk,
					"name": self.name,
					"latitude": self.latitude,
					"longitude": self.longitude,
					"activities": [activity.get_activity_json() for activity in self.get_place_activities()]
				}

class Languages(models.Model):
	language = models.CharField(max_length=100)

	def __unicode__(self):
		return self.language

	def get_language_json():
		return {"id": self.pk, "language": self.language}

class ServiceProvidersLanguages(models.Model):
	service_provider = models.ForeignKey(ServiceProviders)
	language = models.ForeignKey(Languages)

	def __unicode__(self):
		return self.language

	def get_sp_language_json(self):
		return {"id": self.pk, "language": self.language.get_language_json()}

class PlaceActivities(models.Model):
	place = models.ForeignKey(Places)
	activity = models.CharField(max_length=255)

	def __unicode__(self):
		return self.activity

	def get_activity_json(self):
		return {"id": self.pk, "activity": self.activity}

class TourismGuide(models.Model):
	service_provider = models.ForeignKey(ServiceProviders)
	tourism = models.ForeignKey(Tourism)
	start_date = models.DateTimeField(auto_created=True)
	end_date = models.DateTimeField(auto_created=True)
	is_tourist_care = models.BooleanField(default=False)
	date = models.DateTimeField(auto_created=True)

	def __unicode__(self):
		return self.tourism

	def get_tourism_guide_places(self):
		return TourismGuidePlaces.objects.filter(tourism_guide=self.pk)

	def get_tourism_guide_places_count(self):
		return TourismGuidePlaces.objects.filter(tourism_guide=self.pk).count()

	def get_tourism_guide_json(self):
		return {
					"id": self.pk, 
					"start_date": self.start_date, 
					"end_date": self.end_date, 
					"is_tourist_care": self.is_tourist_care,
					"places_count": self.get_tourism_guide_places_count(),
					"places": [place.get_tp_json() for place in self.get_tourism_guide_places()],
					"date": self.date
				}


class TourismGuidePlaces(models.Model):
	tourism_guide = models.ForeignKey(TourismGuide)
	place = models.ForeignKey(Places, blank=True, null=True)

	def __unicode__(self):
		return self.place.name

	def get_tp_json(self):
		return {"id": self.pk, "place": self.place.get_place_json()}


class TouristFeedBack(models.Model):
	tourism_guide = models.ForeignKey(TourismGuide, null=True, blank=True)
	text = models.TextField()
	date = models.DateTimeField(auto_created=True)

	def __unicode__(self):
		return self.tourism_guide

	def get_tfb_json(self):
		return {"id": self.pk, "text": self.text, "date": self.date}


class ServiceProviderFeedBack(models.Model):
	tourism_guide = models.ForeignKey(TourismGuide, null=True, blank=True)
	text = models.TextField()
	date = models.DateTimeField(auto_created=True)

	def __unicode__(self):
		return self.tourism_guide

	def get_sp_fb_json(self):
		return {"id": self.pk, "text": self.text, "date": self.date}

