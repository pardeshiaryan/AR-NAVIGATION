from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import json
import random
import re
import os
import markdown2
import math
from . import util
from .forms import NewPageForm

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": [entry.strip('[]\"') for entry in util.list_entries() if entry == "DEPARTMENTS"]
    })

def entryPage(request, title):
    markDownData = util.get_entry(title)
    if markDownData is None:
        return render(request, "encyclopedia/invalidpage.html", {
            "title": title
        })
    htmlData = markdown2.markdown(markDownData)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "html": htmlData
    })

def search(request):
    search_query = request.POST.get("q")
    search_query_cleaned = re.sub(r'[<>*#]', ' ', search_query)
    matched_results = search_in_md_files(search_query_cleaned)
    if matched_results:
        return render(request, "encyclopedia/searchresult.html", {
            "matched_results": matched_results,
            "search_query": search_query,
            "title": search_query,
            "filename": matched_results[0][0]
        })
    else:
        return render(request, "encyclopedia/invalidpage.html", {
            "title": search_query
        })

def search_in_md_files(query):
    matched_results = []
    directory = "C:/Users/pkart/OneDrive/Documents/GitHub/APSITwiki/APSITwiki/entries"
    for filename in os.listdir(directory):
        if filename == "cnnd.md":
            continue
        if filename.endswith(".md"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file, start=1):
                    if query.lower() in line.lower():
                        if line_number % 10 == 0:
                            line_round = line_number - 10
                        else:
                            line_round = math.floor(line_number / 10) * 10
                        line_content = re.sub(r'<.*?>|#|\*|\[.*?\]\(.*?\)', '', line.strip())
                        matched_results.append((filename[:-3], line_round, line_number, line_content))
    return matched_results

def createEntry(request):
    if request.method == "POST":
        formData = NewPageForm(request.POST)
        if formData.is_valid():
            title = formData.cleaned_data['title']
            data = formData.cleaned_data['data']
            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/newpage.html", {
                    "newform": NewPageForm(),
                    "error": "Such an entry already exists"
                })
            finalData = "#" + title + "\n" + data
            util.save_entry(title, finalData)
            return HttpResponseRedirect(reverse("entrypage", args=[title]))
    return render(request, "encyclopedia/newpage.html", {
        "title": "Create Entry",
        "newform": NewPageForm()
    })

def editEntry(request):
    if request.method == "GET":
        title = request.GET['title']
        data = util.get_entry(title)
        form = NewPageForm(initial={'title': title, 'data': data})
        return render(request, "encyclopedia/edit.html", {
            "title": "Edit data",
            "newform": form
        })
    if request.method == "POST":
        formData = NewPageForm(request.POST)
        if formData.is_valid():
            title = formData.cleaned_data['title']
            data = formData.cleaned_data['data']
            finalData = "#" + title + "\n" + data
            util.save_entry(title, finalData)
            return HttpResponseRedirect(reverse("entrypage", args=[title]))

def randomPage(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return HttpResponseRedirect(reverse("entrypage", args=[random_entry]))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return JsonResponse({'message': 'This is a protected view'})

def Function(request):
    return render(request, "encyclopedia/Function.html")
