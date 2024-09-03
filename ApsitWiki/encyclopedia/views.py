from typing import Final
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, HttpResponse, redirect
import markdown2
import random
from django import forms
import os
import re
from encyclopedia import admin
from . import util
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
import math
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Form used to create a new entry/page 
class NewPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
            'placeholder': 'Enter title', 'id': 'new-entry-title','name':'title'}))
    data = forms.CharField(label="", widget=forms.Textarea(attrs={
        'id': 'new-entry','name':'data'}))


# controllers
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": [entry.strip('[]\"') for entry in util.list_entries() if entry == "DEPARTMENTS"]
    })

#titlepage
def entryPage(request, title):
    markDownData = util.get_entry(title)
    if(markDownData == None):
        print("No such entry")
        return render(request, "encyclopedia/invalidpage.html", {
            "title" : title
        })
    htmlData = markdown2.markdown(markDownData)
    return render(request, "encyclopedia/entry.html", {
        "title" : title,
        "html" : htmlData
    })

#searchpage

def search(request):
    search_query = request.POST.get("q")
    search_query_cleaned = re.sub(r'[<>*#]', ' ', search_query)
    # Search within Markdown files
    matched_results = search_in_md_files(search_query_cleaned)
    if matched_results:
        # Display the matched lines on the screen
        return render(request, "encyclopedia/searchresult.html", {
            "matched_results": matched_results, 
            "search_query": search_query,
            "title":search_query,
            "filename":matched_results[0][0]
            })
    else:
        # Handle case when no match is found
        return render(request, "encyclopedia/invalidpage.html", {
            "title" : search_query
        })

def search_in_md_files(query):
    matched_results = []
    # Directory where your .md files are stored
    directory = "C:/Users/pkart/OneDrive/Documents/GitHub/APSITwiki/APSITwiki/entries"
    for filename in os.listdir(directory):
        if filename == "cnnd.md":
            continue
        if filename.endswith(".md"):
            with open(os.path.join(directory, filename), 'r',encoding='utf-8') as file:
                for line_number, line in enumerate(file, start=1):
                    if query.lower() in line.lower():
                        # If query found in line, add filename, line number, and line content to matched_results
                        if line_number % 10 == 0:
                            line_round = line_number - 10
                        else:
                            line_round = math.floor(line_number / 10) * 10
                            # Exclude <>#* and anything between them from line content
                        line_content = re.sub(r'<.*?>|#|\*|\[.*?\]\(.*?\)', '', line.strip())
                        matched_results.append((filename[:-3],line_round, line_number, line_content))
    return matched_results





def createEntry(request):
    if request.method == "POST":
        formData = NewPageForm(request.POST)
        if formData.is_valid():
            title = formData.cleaned_data['title']
            data = formData.cleaned_data['data']
            if(util.get_entry(title)!=None):
                return render(request, "encyclopedia/newpage.html", {
                    "newform" : NewPageForm(),
                    "error": "Such an entry already exists"
                })
            finalData = "#" + title + "\n" + data
            util.save_entry(title, finalData)
            return HttpResponseRedirect(reverse("entrypage", args=[title]))
    return render(request, "encyclopedia/newpage.html", {
        "title" : "Create Entry",
        "newform" : NewPageForm()
    })

def editEntry(request):
     if request.method == "GET":
         title = request.GET['title']
         data = util.get_entry(title)
         form = NewPageForm(initial={'title': title, 'data': data})
         return render(request, "encyclopedia/edit.html", {
             "title":"Edit data",
            "newform" : form
         })
     if request.method == "POST":
         formData = NewPageForm(request.POST)
         if formData.is_valid():
            title = formData.cleaned_data['title']
            data = formData.cleaned_data['data']
            if(util.get_entry(title)!=None):
                util.save_entry(title, data)
                return HttpResponseRedirect(reverse("entrypage", args=[title]))

def randomPage(request):
    entries = util.list_entries()
    value = random.choice(entries)
    return HttpResponseRedirect(reverse("entrypage", args=[value]))
def Function(request):
    return HttpResponseRedirect(reverse("entrypage", args=["Function"]))
# def login(request):
#     return HttpResponseRedirect(request, "entrypage")

def loginpage(request):
    try:    
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Invalid Username')
                return redirect("login")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                messages.error(request, "Invalid Credentials")
                return redirect("login")
    except Exception as e:
        print(e)
    return render(request, 'encyclopedia/login.html')

def signuppage(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(username,email,password)
            try:
                if User.objects.filter(username=username).exists():
                    messages.info(request, "User with the same username already exists.")
                    return redirect("signup")
                user = User.objects.filter(email=email)
                if user.exists():
                    messages.info(request, "Email already exists.")
                    return redirect("signup")
                if len(password) < 8:
                    messages.error(request, "Password must be at least 8 characters long.")
                    return redirect("signup")
                if not re.search(r'[A-Za-z]', password):
                    messages.error(request, "Password must contain at least one letter.")
                    return redirect("signup")
                if not re.search(r'[0-9]', password):
                    messages.error(request, "Password must contain at least one number.")
                    return redirect("signup")
                else:
                    my_user = User.objects.create_user(username, email, password)
                    my_user.save()
                    messages.info(request, "Account created successfully. Please login to continue.")
                return redirect('login')
            except Exception as e:
                print(e)  
    except Exception as e:
        print(e)
    return render(request, 'encyclopedia/signup.html')