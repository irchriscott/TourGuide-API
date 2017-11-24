from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from tourapi.models import *
from django.views.decorators.csrf import csrf_exempt
import json


def return_response(params):
	response = HttpResponse(params, content_type="application/json")
	response['Access-Control-Allow-Origin'] = "*"
	response['Access-Control-Allow-Headers'] = "origin, x-requested-with, content-type"
	response['Access-Control-Allow-Methods'] = "PUT, GET, POST, DELETE, OPTIONS"
	return response

def check_tourist_email(request, email):
	try:
		tourist = Tourist.objects.get(email=email)
		return True
	except Tourist.DoesNotExist:
		return None

def check_sp_email(request, email):
	try:
		sp = ServiceProviders.objects.get(email=email)
		return True
	except ServiceProviders.DoesNotExist:
		return None


#TOURISTS


def api_get_tourists(request):
	tourists = Tourist.objects.all().order_by('-full_name')
	tourists = [tourist.get_tourist_json() for tourist in tourists]
	return return_response(json.dumps(tourists, indent=4, default=str))


def api_get_single_tourist(request, tourist):
	try:
		tourist = Tourist.objects.get(pk=tourist)
		return return_response(json.dumps(tourist.get_tourist_json(), indent=4, default=str))
	except Tourist.DoesNotExist:
		error = [{"Error":"Tourist Not Found"}]
		return return_response(json.dumps(error, indent=4, sort_keys=False))


@csrf_exempt
def api_register_tourist(request):
	if request.method == "POST":
		tourist = json.loads(request.body)
		print tourist

		email_check = check_tourist_email(tourist["email"])

		if email_check == None:
			tourist_obj = Tourist(
					full_name = tourist["full_name"],
					email = tourist["email"]
				)
			try:

				tourist_obj.save()
				return return_response("Tourist Added !!!")

			except Exception:
				error = [{"Required Fields":"full_name, email", "Request":"POST", "Format":"json"}]
				return return_response(json.dumps(error, indent=4, sort_keys=True))
		else:
			error = [{"Error":"Email Already Taken"}]
			return return_response(json.dumps(error, indent=4, sort_keys=False))
	else:
		error = [{"Fields":"full_name, email", "Error":"Expecting POST REQUEST", "Format":"json"}]
		return return_response(json.dumps(error, indent=4, sort_keys=True))


@csrf_exempt
def api_register_tourism(request):
	if request.method == "POST":
		tourism = json.loads(request.body)
		tourism_obj = Tourism(
				tourist = Tourist.objects.get(email=tourism["email"]),
				origin = tourism["origin"],
				destination = tourism["destination"],
				is_private = tourism["is_private"],
				date = datetime.now()
			)
		try:

			tourism_obj.save()
			return return_response("Tourism Added !!!")
		except Exception:
			error = [{"Required Fields":"email, origin, destination, is_private(boolean)", "Request":"POST", "Format":"json"}]
			return return_response(json.dumps(error, indent=4, sort_keys=True))
	else:
		error = [{"Fields":"email, origin, destination, is_private(boolean)", "Error":"Expecting POST REQUEST", "Format":"json"}]
		return return_response(json.dumps(error, indent=4, sort_keys=True))


@csrf_exempt
def get_tourist_tourisms(request, tourist):
	if request.method == "POST":
		tourist_data = json.loads(request.body)
		print tourist_data
		try:
			tourist_obj = Tourist.objects.get(email=tourist_data["email"])

			if tourist_obj.pk == tourist:

				tourisms = Tourism.objects.filter(tourist=tourist).order_by('-date')
				tourisms = [tourism.get_tourism_json() for tourism in tourisms]
				return return_response(json.dumps(tourisms), indent=4, sort_keys=False)

			else:
				error = [{"Error":"Not Authorized"}]
				return return_response(json.dumps(error, indent=4, sort_keys=False))

		except Tourist.DoesNotExist:

			error = [{"Error":"Tourist Not Found"}]
			return return_response(json.dumps(error, indent=4, sort_keys=False))
	else:

		tourisms = Tourism.publics.filter(tourist=tourist).order_by('-date')
		tourisms = [tourism.get_tourism_json() for tourism in tourisms]
		return return_response(json.dumps(tourisms), indent=4, sort_keys=False)


def api_get_tourisms(request):
	tourisms = Tourism.publics.all().order_by('-date')
	tourisms = [tourism.get_tourism_json() for tourism in tourisms]
	return return_response(json.dumps(tourisms, indent=4, sort_keys=False))


def api_get_single_tourism(request, tourism):
	try:
		tourism = Tourism.publics.get(pk=tourism)
		return return_response(json.dumps(tourism, indent=4, sort_keys=False))
	except Tourism.DoesNotExist:
		error = [{"Error":"Tourism Not Found"}]
		return return_response(json.dumps(error, indent=4, sort_keys=False))

#SERVICE PROVIDERS

@csrf_exempt
def api_sp_register(request):
	if request.method == "POST":
		sp = json.loads(request.body)

		email_check = check_sp_email(sp["email"])
		print sp

		if email_check == None:
			sp_obj = ServiceProviders(
					full_name = sp["full_name"],
					country = sp["country"],
					city = sp["city"],
					email = sp["email"],
					password = sp["password"],
					contact = sp["contact"],
					image = sp["image"]
				)
			try:
				sp.save()
				return return_response("Service Provider Added !!!")
			except Exception:
				error = [{"Required Fields":"full_name, email, password, country, city, category, image, contact", "Request":"POST", "Format":"json"}]
				return return_response(json.dumps(error, indent=4, sort_keys=True))
		else:

			error = [{"Error":"Email Already Taken"}]
			return return_response(json.dumps(error, indent=4, sort_keys=False))

	else:
		error = [{"Fields":"full_name, email, password, country, city, category, image, contact", "Error":"Expecting POST REQUEST", "Format":"json"}]
		return return_response(json.dumps(error, indent=4, sort_keys=True))


def api_get_sp_all(request):
	sps = ServiceProviders.objects.all()
	sps = [sp.get_sp_json() for sp in sps]
	return return_response(json.dumps(sps))


def api_get_single_sp(request, sp):
	try:
		sp = ServiceProviders.objects.get(pk=sp)
		return return_response(json.dumps(sp))
	except ServiceProviders.DoesNotExist:
		error = [{"Error":"Service Provider Not Found"}]
		return return_response(json.dumps(error, indent=4, sort_keys=False))


def api_get_available_sp(request):
	sps = ServiceProviders.availables.all()
	sps = [sp.get_sp_json() for sp in sps]
	return return_response(json.dumps(sps), indent=4, sort_keys=False)


def api_sp_add_place(request):
	if request.method == "POST":
		place = json.loads(request.body)
	else:
		error = [{"Fields":"sp, name, longitude(optional), latitude(optional)", "Error":"Expecting POST REQUEST", "Format":"json"}]
		return return_response(json.dumps(error, indent=4, sort_keys=True))