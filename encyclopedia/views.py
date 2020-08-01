from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

class NewEntry(forms.Form):
    name = forms.CharField(label="Entry Name")
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":5}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def new(request):
    if request.method == "POST":
        form =  NewEntry(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            if util.get_entry(name) is None:
                util.save_entry(name, description)
                return HttpResponseRedirect(form.cleaned_data["name"])
            else:
                 return render(request, "encyclopedia/new.html", {
                        "form": form,
                        "error": "This entry already exist"
                    })
        else:
            return render(request, "encyclopedia/new.html", {
                    "form": form
                })

    return render(request, "encyclopedia/new.html", {
        "form": NewEntry()
    })

def edit(request):
    return render(request, "encyclopedia/edit.html", {
        "entries": util.list_entries()
    })

def search(request):
    return render(request, "encyclopedia/search.html", {
        "entries": util.list_entries_search(request.GET["q"]),
        "searchTerm": request.GET["q"]
    })

def random(request):
    return render(request, "encyclopedia/random.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    return render(request, "encyclopedia/entry.html", {
        "entry": util.get_entry(entry),
        "title": entry
    })

