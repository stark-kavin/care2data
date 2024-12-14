from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate , login , logout
from .models import *
import json
from django.core.files.storage import FileSystemStorage
from .utilities import validater

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("home")

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
    try:id = int(id)
    except:return HttpResponse("Study Doesn't exist <a href='/'>Go back</a>")
    study = Study.objects.get(pk=id)
    error = False
    if not study:
        return HttpResponse("Study Doesn't exist <br><a href=\" /\">Go Home</a>")

    if request.method == "POST":
        
        print(request.POST)
        
        if "s-name" in request.POST:
            if validater.validate_name(request.POST["s-name"]):
                study.name = validater.name_corrector(request.POST["s-name"])
                if "s-phases" in request.POST:
                    if request.POST["s-phases"] != "":
                        if Phase.objects.filter(id=request.POST["s-sponser"]):
                            study.phase = Phase.objects.filter(id=request.POST["s-sponser"])[0]
                if "s-sponser" in request.POST:
                    if request.POST["s-sponser"] != "":
                        if Sponser.objects.filter(id=request.POST["s-sponser"]):
                            study.sponser = Sponser.objects.filter(id=request.POST["s-sponser"])[0]
                if "s-discription" in request.POST:
                    study.discription = request.POST["s-discription"]
                if "attachment-delete" in request.POST:
                    if request.POST["attachment-delete"] == "delete":
                        study.attachment = None
                if 'attachment' in request.FILES:
                    if request.FILES["attachment"] != "":
                        file = request.FILES['attachment']
                        study.attachment=file
                study.save()
                return redirect("home")         
            error = "Name Must be 4 - 20 characters"
    
    
    study = Study.objects.get(id=study.id)
    phases = Phase.objects.all()
    sponser = Sponser.objects.all()

    context = {
        "study":study,
        "phases":phases,
        "sponsers":sponser,
        "error":error
    }
    return render(request,"edit.html",context=context)

def create_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    error=False
    if request.method == "POST":
        if not request.POST["name"]:
            error = True
        elif not validater.validate_name(request.POST["name"]):
            error = True
        else:    
            study = Study.objects.create(
                name=validater.name_corrector(request.POST['name']),
                phase_id=request.POST["phase"],
                sponser_id=request.POST["sponser"],
                discription=validater.name_corrector(request.POST["discription"])
            )
            
            if 'attachment' in request.FILES:
                file = request.FILES['attachment']
                study.attachment=file
                study.save()
            return redirect("home")
        
    phases = Phase.objects.all()
    sponser = Sponser.objects.all()

    context = {
        "phases":phases,
        "sponsers":sponser,
        "error":error
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

def sponser_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    all_sponser = Sponser.objects.all()
    
    error = None
    success = None
    
    if request.method == "POST":
        if "sponser-delete" in request.POST:
            s = Sponser.objects.filter(id=request.POST["sponser-delete"])
            if s:
                del_name = s[0].name
                if s:s.delete()
                success = f"Deleted sponser \"{del_name}\""
            else:error = f"Sponser doesn't Exist"
        elif "sponser" in request.POST:
            name = request.POST["sponser"]
            if validater.validate_name(name):
                new_sponser = Sponser.objects.create(name=validater.name_corrector(name))
                if "contact" in request.POST:    
                    new_sponser.contact = request.POST["contact"]
                    new_sponser.save()
                success = f"New Sponser added \"{new_sponser.name}\""
                return redirect("sponser")
            else:
                error = "Didn't create sponser,Name should be 4-20 characters "
    
    return render(request,"sponser.html",{"sponsers":all_sponser,"error":error,"success":success})
