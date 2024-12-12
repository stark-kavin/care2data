from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from .models import *
import json

def login_view(request):
    error=False
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        print(request.POST)
        if "username" in request.POST:
            if "password" in request.POST:
                user = authenticate(username=request.POST["username"], password=request.POST["password"])
                if user is not None:
                    login(request,user)
                    return redirect("home")
        error = True
    return render(request,"login.html",context={"e":error})

def home_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == "POST":
        try:
            for i in dict(request.POST)["study"]:
                Study.objects.get(id=i).delete()
            redirect("login")
        except:redirect("login")

    phase = Phase.objects.all()
    sponser = Sponser.objects.all()
    all_studies = Study.objects.all()
    return render(request,"home.html",context={"studies":all_studies,"phase":phase,"sponser":sponser})

def edit_view(request,id):

    if not request.user.is_authenticated:
        return redirect("login")

    study = Study.objects.filter(pk=id)

    if not study:
        return HttpResponse("Study Doesn't exist <br><a href=\" /\">Go Home</a>")
    study = Study.objects.get(id=study[0].id)

    if request.method == "POST":

        {'s-name': ['Study 2'], 's-phase': ['new'], 'new-phase': ['asdsdas'], 's-sponser': ['new'], 'new-sponser-name': ['Hi'], 'new-sponser-contact': ['asdasd'], 'discription': ['for hospital']}
        edit = request.POST

        if 's-phase' in edit :
            if edit['s-phase'] == 'new':
                new_phase = Phase.objects.get_or_create(name=edit["new-phase"])
                study.phase=new_phase[0]
            else:
                study.phase=Phase.objects.get(id=edit['s-phase'])
        if 's-sponser' in edit :
            if edit["s-sponser"] == 'new':
                new_sponser = Sponser.objects.get_or_create(name=edit["new-sponser-name"],contact=edit["new-sponser-contact"])
                study.sponser=new_sponser[0]
            else:
                study.sponser=Sponser.objects.get(id=edit['s-sponser'])

        if edit["s-name"]:
            study.name=edit["s-name"]
        
        if "discription" in edit:
            study.discription=edit["discription"]

        study.save()
        return redirect("home")

    phases = Phase.objects.all()
    sponser = Sponser.objects.all()

    context = {
        "study":study,
        "phases":phases,
        "sponsers":sponser
    }
    return render(request,"edit.html",context=context)

def create_view(request):
    
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == "POST":
        Study.objects.create(name=request.POST['name'],phase_id=request.POST["phase"],sponser_id=request.POST["sponser"],discription=request.POST["discription"])
        return redirect("home")
    phases = Phase.objects.all()
    sponser = Sponser.objects.all()

    context = {
        "phases":phases,
        "sponsers":sponser
    }

    return render(request,"create_study.html",context)

def reset_view(request):

    file_path = '../reset-data.json'
    with open(file_path, 'r') as file:
        data = json.load(file)  
    
    studies = data["study"]
    sponsers = data["sponser"]
    phases = data["phase"]

    msg = ""
    
    all_studies = Study.objects.all()
    all_phases = Phase.objects.all()
    all_sponcers = Sponser.objects.all()

    msg += f"""
            <style>
            td{{padding:1rem}}
            </style>
            <table border="1px">
            <tr><th colspan="2"><h2>Content Deleted</h2></th></tr>
            <tr><td>Studies</td><td>{len(all_studies)}</td></tr>
            <tr><td>Phases</td><td>{len(all_phases)}</td></tr>
            <tr><td>Sponsers</td><td>{len(all_sponcers)}</td></tr>
            </table>
            <br><br>
            <ul>
            <h2>Added</h2>
            <li>10 studies added
            <li>05 phases added
            <li>05 sponsers added
            </ul>

            <br>

            <a href="/">Go Home</a>

            """

    for i in all_studies:
        i.delete()
    for i in all_sponcers:
        i.delete()
    for i in all_phases:
        i.delete()

    for i in sponsers:
        Sponser.objects.create(id=i["id"],name=i['name'],contact=i["contact"])
    
    for i in phases:
        Phase.objects.create(id=i["id"],name=i["name"])

    for i in studies:
        Study.objects.create(name=i["name"],sponser_id=i["sponcer"],phase_id=i["phase"],discription=i["description"])

    return HttpResponse(msg)
