from django.http import HttpResponse
from models import Album, Lists, Position, Notification, Transfer, AddToWallet
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.views.generic import View
from .forms import UserForm, TaskForm, NotifyForm, TransferForm, AddWalletForm
from django.template import loader
from translate import Translator
from django.http import JsonResponse
from classify import getCategory
from nearby import common_elements, GoogPlac
from urllib2 import Request, urlopen, URLError
import urllib
import json
from Savoir import Savoir


reqRates = Request('http://api.fixer.io/latest?base=USD')
response_bolt = urlopen(reqRates)
json_bolt_value= json.loads(response_bolt.read())

rpcuser = 'multichainrpc'
rpcpasswd = 'jmx29EYjMa7CsQw1qwLRhGdKsn9N575C5XSsQTyZg3V'
rpchost = 'localhost'
rpcport = '6724'
chainname = 'newchain1'

wallet_address = "1G9VrgtaTnQHJhWqca9UN1xHCn62q6Kgdredk2"
my_wallet_address = "15w1Sxu4D1mAJCLgJhUNx2zRJFjL7KWqsS7nfz"
asset = "bolt1"


api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
#print getbalance()
#blah = json.loads(api.gettotalbalances())


def getbalance():
    balance = api.gettotalbalances()
    for key in balance:
     if key['name']=='bolt1':
       return key['qty']
     else: 
        return '0'
#print balance

#amount = 10


def index(request):
    all_albums = Album.objects.all()
    template = loader.get_template('music/index.html')
    context = {

        "all_albums" : all_albums,
    }
    html = ''
    return HttpResponse(template.render(context,request))



def get_list(request):
    all_tasks = Lists.objects.all()
    template = loader.get_template('music/todo.html')
    context = {

        "all_tasks" : all_tasks,
    }
    html = ''
    return HttpResponse(template.render(context,request))


'''
   for album in all_albums:
        id = album.id
        url = "/music/" + str(id) + "/"
        html += "<a href="+ url + "> " + album.artist +" </a><br> "

'''
def play(request):
    translator = Translator(to_lang="zh")
    translation = translator.translate("This is a pen.")
    return HttpResponse(translation)

def details(request, album_id):
    return HttpResponse("<h1> music id :" + str(album_id) + "</h1>")

def routes(request):
    template = loader.get_template('music/routes.html')
    return HttpResponse(template.render('',request))

def todo(request):
    template = loader.get_template('music/todo.html')

    if request.method == 'POST':
        return redirect('https://www.google.com')
        #return redirect('https://www.google.com')
        form = TaskForm(request.POST)
        if form.is_valid():
            return redirect('https://www.google.com')
            user = form.save(commit=False)
            task = form.cleaned_data['custom_textbox']
            user.save()

    return HttpResponse(template.render('',request))


def login(request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
  #      return HttpResponse("sdff",password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                #albums = Album.objects.filter(user=request.user)
                return redirect('wallet')
            else:
                return render(request, 'music/index.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/index.html', {'error_message': 'Invalid login'})


def logout_user(request):
    logout(request)
    return render(request, 'music/index.html')

class StartSearch(View):
    form_class = ""



class CreateLists(View):

    form_class = TaskForm
    template_name = "music/todo.html"



    def get(self, request):

        if not request.user.is_authenticated():
            return render(request, 'music/index.html')

        form = self.form_class(None)
        user_id = request.user.id

        lists = Lists.objects.all().filter(user_id= user_id).order_by('-id')
        all_notifications = Notification.objects.all()
        notification_count = all_notifications.count()
        #all_notifications = Notification.objects.all().count()
        return render(request, self.template_name, {'form' : form , 'lists' : lists, 'all_notifications' : all_notifications , 'notification_count': notification_count})

    def post(self,request):
        #return redirect('https://www.google.com')
        #  return redirect('https://www.google.com')
        #return redirect('https://www.google.com')
        user_id = request.user.id

        lists = Lists.objects.all().filter(user_id= user_id).order_by('-id')
        all_notifications = Notification.objects.all()
        notification_count = all_notifications.count()


        form = TaskForm(request.POST)
        if form.is_valid():
            my_task = form.save(commit=False)
            task = form.cleaned_data['amount']

            recipient = form.cleaned_data['recipient']

            add_task = Lists.objects.create(amount=task, user_id = user_id, recipient = recipient)

        return render(request, self.template_name, {'form' : form , 'lists' : lists, 'all_notifications' : all_notifications , 'notification_count': notification_count})


class UserFormView(View):
    form_class = UserForm
    template_name = "music/registration_form.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form' : form })

    def post(self,request):
        #return redirect('https://www.google.com')
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    #request.user
                    return redirect('index')

        return render(request, self.template_name, {'form': form})


def view_list(request):

        lists = Lists.objects.all()
        return render(request, 'music/view_list.html', {
                'lists': lists,
            })

def add_new_task(request):
    task = request.GET.get('task', None)

    add_task = Lists.objects.create( task = task)
    add_task.save()
    #all_tasks = Lists.objects.all()
    #template = loader.get_template('music/todo.html')
    #context = {

       # "all_tasks" : all_tasks,
    #}
    html = ''
    return JsonResponse("")

def delete_task(request, id):

    list = Lists.objects.get(pk=id)
    list.delete()
    lists = Lists.objects.filter(user=request.user)
    return redirect('/music/todo.html')
    return render(request, 'music/todo.html', {'lists': lists})


def start_search(request, user_id):
    try:

        lists = Position.objects.get(user_id=user_id)
        current_latitude = 19.1239
        current_longitude = 72.8361
        pl = (GoogPlac(current_latitude, current_longitude, 500,
                       'department_store,store,bakery,beauty_salon,bicycle_store,book_store,car_repair,clothing_store,electronics_store,florist,furniture_store,hair_care,hardware_store,jewelry_store,laundary,pet_store,pharmacy,plumber,shoe_store,shopping_mall',
                       'AIzaSyA6udyv0riUcZQnn_8TqzqMjOevOIcZHX4'))

        categories = Lists.objects.filter(user_id=user_id).values('category')
        #print categories
        myList = []

        for i in range(len(categories)):
            myList.append(categories[i]["category"])
            #   print myList
            # category_list = list(categories)


        list1 = myList

        #print list1
        #print list1
        storeName=""
        store_type=""
        store_latitude=""
        store_longitude=""
        all_store_names=""
        all_store_types=""

        for i in range(len(pl['results'])):
            if len(common_elements((pl['results'][i]['types']), list1)) != 0:
#                storeName = storeName.join(pl['results'][i]['name'])
#               store_type = store_type.join(common_elements((pl['results'][i]['types']), list1))


                #   print storeName
                #  print store_type
                #        store_latitude = store_latitude.join(pl['results'][i]['latitude'])
                #       store_longitude = store_longitude.join(pl['results'][i]['longitude'])
                #                all_store_names = all_store_names + storeName
                #               all_store_types = all_store_types + " " + store_type
                add_position = Notification.objects.create(user_id=user_id,
                                                           store_name=pl['results'][i]['name'])

        all_notifications = Notification.objects.all()
        render(request,'music/todo.html',{"all_notifications": all_notifications})


    except Position.DoesNotExist:
        add_position = Position.objects.create(user_id=user_id)
        current_latitude = 19.1239
        current_longitude = 72.8361
        pl = (GoogPlac(current_latitude, current_longitude, 500,
                       'department_store,store,bakery,beauty_salon,bicycle_store,book_store,car_repair,clothing_store,electronics_store,florist,furniture_store,hair_care,hardware_store,jewelry_store,laundary,pet_store,pharmacy,plumber,shoe_store,shopping_mall',
                       'AIzaSyA6udyv0riUcZQnn_8TqzqMjOevOIcZHX4'))

        categories = Lists.objects.filter(user_id=user_id).values('category')

        myList = []

        for i in range(len(categories)):
            myList.append(categories[i]["category"])

        list1 = myList

        for i in range(len(pl['results'])):
            if len(common_elements((pl['results'][i]['types']), list1)) != 0:
                add_position = Notification.objects.create(user_id=user_id,
                                                           store_name=pl['results'][i]['name'])

        all_notifications = Notification.objects.all()
        render(request, 'music/todo.html', {"all_notifications": all_notifications})

    lists = Lists.objects.all().filter(user_id=user_id).order_by('-id')
    return redirect('/music/todo.html')
    return render(request, 'music/todo.html', {'lists':lists,'add_position': add_position})


def get_directions(request):
    template_name = "music/getdirections.html"

    return render(request, template_name)


def wallet(request):
    template_name = "music/wallet.html"

    usd = getOneBoltToUSD(1)
    btc = getBoltToBTC(1)
    inr = getBoltToINR(1)
    euro = getBoltToEUR(1)
    #print api.gettotalbalances()
    balance = getbalance()
    #balance = 1000
    return render(request, template_name, {'usd': usd, 'btc' : btc, 'inr' : inr , 'euro' : euro, 'balance' : balance})

def add_to_wallet(request):
    template_name = "music/add_to_wallet.html"

    balance = getbalance()
    #balance = 1000
    #print api.gettotalbalances()
    return render(request, template_name, { 'balance' : balance})

def transfer(request):
    template_name = "music/transfer.html"

    #balance = 1000
    return render(request, template_name, { 'balance' : balance} )

class TransferFormView(View):

    form_class = TaskForm
    template_name = "music/transfer.html"

    def get(self, request):

        if not request.user.is_authenticated():
            return render(request, 'music/index.html')

        form = self.form_class(None)
        user_id = request.user.id
     #   balance = 1000
        balance = getbalance()

        return render(request, self.template_name, {'form' : form , 'balance' : balance})

    def post(self,request):
        user_id = request.user.id

        form = TaskForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            recipient = form.cleaned_data['recipient']
            #amount = 10
            balance = getbalance()

            blah = api.sendassettoaddress(wallet_address, asset, int(amount))
            add_task = Lists.objects.create(amount=amount, user_id=user_id, recipient=recipient)
            balance = getbalance()
        #            transfer_to_recipient(amount)
        return render(request, self.template_name, {'form': form,'balance' : balance})



#
class AddWalletView(View):
    form_class = AddWalletForm
    template_name = "music/add_to_wallet.html"

    def get(self, request):

        if not request.user.is_authenticated():
            return render(request, 'music/index.html')

        form = self.form_class(None)
        user_id = request.user.id
        balance = getbalance()

        return render(request, self.template_name, {'form' : form , 'balance' : balance})

    def post(self,request):
        user_id = request.user.id
        #print "haha"
        form = AddWalletForm(request.POST)
        print form.errors
        if form.is_valid():
        #    print "huhu"
            amount = form.cleaned_data['amount']

            blah = request.POST['mySelect']

            #currency = form.cleaned_data['mySelect']
            #CHOICES = (('usd', 'usd'), ('inr', 'inr'),('btc', 'btc'),('eur', 'eur'))
           # field = form.ChoiceField(choices=CHOICES)


            if blah=="inr":
                amount = getINRtoBOLT(int(amount))
                api.issuemore(my_wallet_address, asset, amount)
            elif blah=="usd":
                amount = getUSDtoBOLT(int(amount))
                api.issuemore(my_wallet_address, asset, amount)
            elif blah=="btc":
                amount = getBTCtoBOLT(int(amount))
                api.issuemore(my_wallet_address, asset, amount)
            elif blah=="eur":
                amount = getEURtoBOLT(int(amount))
                api.issuemore(my_wallet_address, asset, amount)


            balance = getbalance()

            add_task = AddToWallet.objects.create(amount=amount, user_id=user_id, currency=blah)
            balance = getbalance()

        #            transfer_to_recipient(amount)
        return render(request, self.template_name, {'form': form,'balance' : balance})


#def transfer_to_recipient(amount):
#api.sendassettoaddress(wallet_address, asset, amount)

def getBoltToBTC(bolt):
	btcurl= 'https://blockchain.info/tobtc?currency=USD&value='+str(bolt)
	myrequest = Request(btcurl)
	response = urlopen(myrequest)
	btc = response.read()
	return round(float(btc),4)

def getBoltToEUR(bolt):
	reqRatesEUR = Request('http://api.fixer.io/latest?base=USD&symbols=EUR')
	response_EUR = urlopen(reqRates)
	json_EUR_value= json.loads(response_EUR.read())
	EUR_val= json_EUR_value['rates']['EUR']
	return round(EUR_val*bolt*getOneBoltToUSD(1),4)


def getOneBoltToUSD(bolt):
	top_8= ['AUD','EUR','GBP','CAD','SGD','JPY','CHF','CNY']
	dem_val=0
	for values in top_8:
		dem_val=dem_val+ json_bolt_value['rates'][values]
	bolt_value= (1000)*1/(dem_val/8)
	return round(bolt_value*bolt,4)

def getBoltToINR(bolt):
	eqRatesINR = Request('http://api.fixer.io/latest?base=USD&symbols=INR')
	response_INR = urlopen(reqRates)
	json_INR_value= json.loads(response_INR.read())
	INR_val= json_INR_value['rates']['INR']
	return round(INR_val*bolt*getOneBoltToUSD(1),4)

def getINRtoBOLT(INR):
	rate= 1/getBoltToINR(1)
	return round(rate*INR,4)

def getEURtoBOLT(EUR):
	rate= getBoltToEUR(1)
	return round((1/rate)*(EUR),4)

def getUSDtoBOLT(USD):
	rate= getOneBoltToUSD(1)
	return round((1/float(rate))*float(USD),4)

def getBTCtoBOLT(BTC):
	rate= getBoltToBTC(1)
	return round((1/float(rate))*float(BTC),4)
