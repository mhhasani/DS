from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
# Import mimetypes module
import mimetypes
# import os module
import os
# Import HttpResponse module
from django.http.response import HttpResponse

def Home(request):
    user = User.objects.all().filter(username = request.user)
    if user:
        user = User.objects.all().get(username = request.user)
    daneshjoo = Daneshjoo.objects.all()
    f= open("daneshjooyan.txt","w+")
    all=[]
    for daneshjoo in Daneshjoo.objects.all():
        all.append([Friend.objects.all().get(daneshjoo=daneshjoo).friend.count(),daneshjoo])
        for F in Friend.objects.all().get(daneshjoo__id = daneshjoo.id).friend.all():
            f.write(f"{daneshjoo.id}\t{F.id}\r\n")
    f.close()
    context = {'daneshjoo':all}
    return render(request, 'Home.html',context=context)

@login_required
def download_file(request):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'daneshjooyan.txt'
    # Define the full file path
    filepath = '/home/DSDrRahmani/daneshjooyan.txt'
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response

@login_required
def add_daneshjoo(request,length):
    if request.method == "GET":
        DaneshjooFormSet = formset_factory(add_daneshjoo_form,extra=length)
        Daneshjoos = DaneshjooFormSet()
        context = {'Daneshjoos':Daneshjoos}
        return render(request,'add_daneshjoo.html',context = context)

    if request.method == "POST":
        DaneshjooFormSet = formset_factory(add_daneshjoo_form,extra=length)
        Daneshjoos = DaneshjooFormSet(request.POST)
        if Daneshjoos.is_valid():
            for i in range(length):
                cd = Daneshjoos[i].cleaned_data
                if cd:
                    d = Daneshjoo.objects.create(
                        name = cd['name']
                    )
                    d.save()
                    f = Friend.objects.create(
                        daneshjoo = d
                    )
                    f.save()
        context = {'Daneshjoos':Daneshjoos}
        return render(request,'add_daneshjoo.html',context = context)

@login_required
def add_daneshjoo2(request):
    if request.method == "GET":
        form = add_daneshjoo_form2()
        context = {'form':form}
        return render(request,'add_daneshjoo2.html',context = context)

    if request.method == "POST":
        form = add_daneshjoo_form2(request.POST)
        if form.is_valid():
            name = []
            word = ''
            for i in list(form.cleaned_data['names']):
                if i == '\r':
                    name.append(word)
                    word =''
                    continue
                if i == '\n':
                    continue
                word+=i
            name.append(word)
            for i in name:
                d = Daneshjoo.objects.create(
                    name = i
                )
                d.save()
                f = Friend.objects.create(
                    daneshjoo = d
                )
                f.save()
        context = {'form':form}
        return render(request,'add_daneshjoo2.html',context = context)

@login_required
def add_friend(request,id):
    daneshjoo = get_object_or_404(Daneshjoo,id=id)
    doostan = []
    for d in Friend.objects.all():
        for f in d.friend.all():
            if daneshjoo == f:
                doostan.append(d)
                break
    if request.method == "GET":
        FRIENDS = []
        FriendFormSet = formset_factory(add_friend_form,extra=3)
        my_friend = Friend.objects.all().filter(daneshjoo=daneshjoo)
        for F in my_friend:
            for f in F.friend.all():
                FRIENDS.append(Daneshjoo.objects.all().get(id = f.id))
        Friends = FriendFormSet()
        for i in range(len(FRIENDS)):
            Friends[i]['friend'].initial = FRIENDS[i].name
        context = {'Friends':Friends,'daneshjoo':daneshjoo,'doostan':doostan}
        return render(request,'add_friend.html',context = context)

    if request.method == "POST":
        FriendFormSet = formset_factory(add_friend_form,extra=3)
        Friends = FriendFormSet(request.POST)
        if Friends.is_valid():
            d = Friend.objects.get(daneshjoo = daneshjoo)
            d.friend.clear()
            for i in range(3):
                cd = Friends[i].cleaned_data
                if cd:
                    ff = Daneshjoo.objects.all().get(name = cd['friend'])
                    if not ff.name == daneshjoo.name:
                        d.friend.add(ff)
                    else:
                        return HttpResponse("خودتان نمی توانید دوست خودتان باشید:)")
                    d.save()
        context = {'Friends':Friends,'daneshjoo':daneshjoo,'doostan':doostan}
        return render(request,'add_friend.html',context = context)

