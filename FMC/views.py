# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .viewClasses import *
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render,get_object_or_404,render_to_response
from django.views import generic
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.context_processors import auth
from django.db import connection
import datetime
import smtplib
from email.mime.text import MIMEText
from django.contrib.auth.models import User
import json
from base64 import b64encode

# Create your views here.
def signup(request):
	if request.method=="POST":
		username=request.POST.get("username")
		name=request.POST.get("name")
		pwd1=request.POST.get("pwd1")
		pwd2=request.POST.get("pwd2")
		emailid=request.POST.get("emailid")
		contact=request.POST.get("contact")
		branch=request.POST.get("branch")
		batch=request.POST.get("batch")
		post="Participant"
		names=[]
		with connection.cursor() as cursor:
			cursor.execute('select username from auth_user')
			names=cursor.fetchall()
		if [username] in names:
			errors=["Username already exists!"]
			return render(request,'error.html',{"errors":errors})
		with connection.cursor() as cursor:
			cursor.execute('select email from auth_user')
			names=cursor.fetchall()
		if [emailid] in names:
			errors=["EmailID already registered!"]
			return render(request,'error.html',{"errors":errors})
		if pwd1!=pwd2:
			errors=["Password not same in both the fields!"]
			return render(request,'error.html',{"errors":errors})
		k=True
		for i in contact:
			if i>'9' or i<'0':
				k=False
		if len(contact)!=10 or k==False:
			errors=["Provide 10 digit mobile number!"]
			return render(request,'error.html',{"errors":errors})
		userID=User.objects.create_user(username=username,first_name=name,password=pwd1,email=emailid)
		with connection.cursor() as cursor:
			cursor.execute('update auth_user set Contact="%s", Branch="%s", Batch=%d, Post="%s" where username="%s"'%(str(contact),str(branch),int(batch),str(post),str(username)))
		errors=["Signup Successful"]
		return render(request,'error.html',{"errors":errors})
	return render(request,'signup.html')
def logged_out(request):
	return render(request,'logged_out.html')

def clubs(request):
	data=[]
	DATA=[]
	CLUBS=[]
	with connection.cursor() as cursor:
		cursor.execute('select * from Club')
		DATA=cursor.fetchall()
	for i in DATA:
		CLUBS.append(i[1])
	if request.method=="POST" and 'add' in request.POST:
		club=request.POST.get("club")
		date=request.POST.get("date")
		if club in CLUBS:
			errors=["Club already exists!"]
			return render(request,'error.html',{"errors":errors})	
		with connection.cursor() as cursor:
			cursor.execute('insert into Club (Name,EstablishmentDate) values ("%s","%s")' %(str(club),str(date)))
	if request.method=="POST" and 'delete' in request.POST:
		club=request.POST.get("clubid")
		with connection.cursor() as cursor:
			cursor.execute('delete from Club where Name="%s"'%(str(club)))
	with connection.cursor() as cursor:
		cursor.execute('select * from Club')
		data=cursor.fetchall()
	clubs=[]
	for i in data:
		if i[0]!=-1:
			clubs.append(clubView(i))
	return render(request,'clubs.html',{"clubs":clubs})

def home(request):	
	return render(request,'home.html')

def people(request):
	return render(request,'people.html')

def postholders(request):
	data=[]
	with connection.cursor() as cursor:
		cursor.execute('select p.id,p.first_name,p.Post,p.Contact,p.Branch,p.Batch,c.Name from auth_user as p, Club as c where p.ClubID=c.ClubID and p.Post!="Participant" and p.Post!="Member"')
		data=cursor.fetchall()
	placeholders=[]
	for i in data:
		placeholders.append(postholderView(i))	
	return render(request,'postholders.html',{"placeholders":placeholders})

def members(request):
	data=[]
	with connection.cursor() as cursor:
		cursor.execute('select m.id,m.first_name,m.Contact,m.Branch,m.Batch,c.Name from auth_user as m, Club as c where m.ClubID=c.ClubID and m.Post="Member" and m.Batch>=YEAR(CURDATE())')
		data=cursor.fetchall()
	members=[]
	for i in data:
		members.append(memberView(i))	
	return render(request,'members.html',{"members":members})

def alumni(request):
	data=[]
	with connection.cursor() as cursor:
		cursor.execute('select m.id,m.first_name,m.Contact,m.Branch,m.Batch,c.Name from auth_user as m, Club as c where m.ClubID=c.ClubID and m.Post="Member" and m.Batch<YEAR(CURDATE())')
		data=cursor.fetchall()
	alumni=[]
	for i in data:
		alumni.append(alumniView(i))	
	return render(request,'alumni.html',{"alumni":alumni})

def allusers(request):
	data=[]
	if request.method=="POST":
		email=request.POST.get("email")
		post=request.POST.get("post")
		club=request.POST.get("club")
		print(post)
		with connection.cursor() as cursor:
			if post=="General Secretary" or post=="Joint General Secretary":
				cursor.execute('update auth_user set Post="%s", ClubID=-1, is_superuser=1 where email="%s"'%(post,email))
			elif post!="Participant":
				print(email)
				cursor.execute('update auth_user set Post="%s", ClubID="%s", is_superuser=0 where email="%s"'%(post,club,email))
			else:
				cursor.execute('update auth_user set Post="%s", ClubID=-1, is_superuser=0 where email="%s"'%(post,email))
	with connection.cursor() as cursor:
		cursor.execute('select * from Club')
		data=cursor.fetchall()
	clubs=[]
	z=[]
	for i in data:
		if i[0]!=-1:
			clubs.append(clubView(i))
	with connection.cursor() as cursor:
		cursor.execute('select p.id,p.first_name,p.email,p.Post,c.Name,p.Contact,p.Branch,p.Batch from auth_user as p, Club as c where p.ClubID=c.ClubID')
		data=cursor.fetchall()
		for i in z:
			data.append(i)
	allusers=[]
	for i in data:
		allusers.append(allusersView(i))	
	return render(request,'allusers.html',{"allusers":allusers,"clubs":clubs})

def events(request):
	return render(request,'events.html')

def pastevents(request):
	data=[]
	with connection.cursor() as cursor:
		cursor.execute('select m.EventID,m.Name,m.Venue,m.Time,c.Name from Events as m, Club as c where m.ClubID=c.ClubID and m.Time<NOW()')
	pastevents=[]
	for i in data:
		pastevents.append(pasteventsView(i))	
	return render(request,'pastevents.html',{"pastevents":pastevents})

def presentevents(request):
	data=[]
	if request.method=="POST" and 'add' in request.POST:
		name=request.POST.get("name")
		venue=request.POST.get("venue")
		date=request.POST.get("date")
		clubid=request.POST.get("clubid")
		events=[]
		with connection.cursor() as cursor:
			cursor.execute('select Name from Events')
			data=cursor.fetchall()
		if [name] in data:
			errors=["Event Name cannot be same!"]
			return render(request,'error.html',{"errors":errors})
		with connection.cursor() as cursor:
			cursor.execute('insert into Events(Name,Venue,Time,ClubID) values("%s","%s","%s",%d)'%(str(name),str(venue),str(date),int(clubid)))
	if request.method=="POST" and 'delete' in request.POST:
		eventid=request.POST.get("eventid")
		with connection.cursor() as cursor:
			cursor.execute('delete from Events where EventID="%s"'%(eventid))
	if request.method=="POST" and 'participate' in request.POST:
		eventid=request.POST.get("eventid")
		userid=request.user.id
		with connection.cursor() as cursor:
			cursor.execute('insert into participate(id,EventID) values(%d,%d)'%(int(userid),int(eventid)))
	with connection.cursor() as cursor:
		cursor.execute('select * from Club')
		data=cursor.fetchall()
	clubs=[]
	for i in data:
		if i[0]!=-1:
			clubs.append(clubView(i))
	with connection.cursor() as cursor:
		cursor.execute('select m.EventID,m.Name,m.Venue,m.Time,c.Name from Events as m, Club as c where m.ClubID=c.ClubID and m.Time>NOW()')
		data=cursor.fetchall()
	presentevents=[]
	present=[]
	userid=request.user.id
	for i in data:
		presentevents.append(presenteventsView(i))
	data=[]
	if request.user.is_authenticated():
		with connection.cursor() as cursor:
			cursor.execute('select m.EventID,m.Name,m.Venue,m.Time,c.Name from Events as m, Club as c where m.ClubID=c.ClubID and m.Time>NOW() and NOT EXISTS(select * from participate as p where p.id=%d and p.EventID=m.EventID)'%(int(userid)))
			data=cursor.fetchall()
	present=[]
	for i in data:
		present.append(presenteventsView(i))	
	return render(request,'presentevents.html',{"presentevents":presentevents,"clubs":clubs,"present":present})

def support(request):
	return render(request,'support.html')

def resources(request):
	data=[]
	if request.method=="POST" and 'add' in request.POST:
		name=request.POST.get("name")
		specs=request.POST.get("specs")
		cost=request.POST.get("cost")
		with connection.cursor() as cursor:
			cursor.execute('insert into Resources (Name,Specifications,Cost) values ("%s","%s",%d)' %(str(name),str(specs),int(cost)))
	with connection.cursor() as cursor:
		cursor.execute('select * from Resources')
		data=cursor.fetchall()
	resources=[]
	for i in data:
			resources.append(resourceView(i))
	return render(request,'resources.html',{"resources":resources})

def merchandise(request):
	data=[]
	if request.method=="POST" and "ins" in request.POST:
		name=request.POST.get("name")
		price=request.POST.get("price")
		profit=request.POST.get("profit")
		quantity=request.POST.get("quantity")
		contact=request.POST.get("contact")
		with connection.cursor() as cursor:
			cursor.execute('insert into Funds(Name,Contact,Amount,Organisation) values ("%s","%s",0,"FMC")'%(str(name),str(contact)))
			cursor.execute('select LAST_INSERT_ID();')
			z=cursor.fetchone()
			image = request.FILES["image"].read()	
			image=b64encode(image)
			query='insert into Merchandise(Name,Price,Profit,Quantity,Contact,FundID,Image) values(%s,%s,%s,%s,%s,%s,%s)'
			args=(name,price,profit,quantity,contact,z[0],image)
			cursor.execute(query,args)
	elif request.method=="POST":
		idfund=request.POST.get("idfund")
		with connection.cursor() as cursor:
			cursor.execute('update Merchandise set Quantity=Quantity-1 where FundID=%d'%(int(idfund)))
			cursor.execute('select Price from Merchandise where FundID=%d'%(int(idfund)))
			z=cursor.fetchall()
			print(z[0][0])
			cursor.execute('update Funds set Amount=Amount+%d where FundID=%d'%(int(z[0][0]),int(idfund)))
			response_data={}
			return HttpResponse(json.dumps(response_data),content_type='application/json')
	with connection.cursor() as cursor:
		cursor.execute('select * from Merchandise')
		data=cursor.fetchall()
	merchandise=[]
	for i in data:
		merchandise.append(merchandiseView(i))
	with connection.cursor() as cursor:
		cursor.execute('select * from Merchandise where Quantity>0')
		data=cursor.fetchall()
	leftones=[]
	for i in data:
		leftones.append(merchandiseView(i))
	return render(request,'merchandise.html',{"merchandise":merchandise,"leftones":leftones})

def funds(request):
	data=[]
	if request.method=="POST":
		name=request.POST.get("name")
		contact=request.POST.get("contact")
		amount=request.POST.get("amount")
		organisation=request.POST.get("organisation")
		with connection.cursor() as cursor:
			cursor.execute('insert into Funds(Name,Contact,Amount,Organisation) values ("%s","%s",%d,"%s")'%(str(name),str(contact),int(amount),str(organisation)))
			response_data={}
			return HttpResponse(json.dumps(response_data),content_type='application/json')
	with connection.cursor() as cursor:
		cursor.execute('select * from Funds')
		data=cursor.fetchall()
	funds=[]
	for i in data:
			funds.append(fundsView(i))
	return render(request,'funds.html',{"funds":funds})