from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
import random


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

def edit(request, entry):

    if request.method == "POST":
            form =  NewEntry(request.POST)
            if form.is_valid():
                name = form.cleaned_data["name"]
                description = form.cleaned_data["description"]
                util.save_entry(name, description)
                return HttpResponseRedirect('/' +form.cleaned_data["name"])
            else:
                return render(request, "encyclopedia/edit.html", {
                        "form": form
                    })
    return render(request, "encyclopedia/edit.html", {
        "entry": util.get_entry(entry),
        "title": entry,
    })

def search(request):
    if (util.list_entries_match(request.GET["q"])) == True:
        return HttpResponseRedirect('/' + request.GET["q"])

    return render(request, "encyclopedia/search.html", {
        "entries": util.list_entries_search(request.GET["q"]),
        "searchTerm": request.GET["q"]
    })

def randomEntry(request):
    entry = random.choice(list(util.list_entries()))
    return render(request, "encyclopedia/entry.html", {
                "entry": markdown2.markdown(util.get_entry(entry)),
                "title": entry
            })
    return render(request, "encyclopedia/random.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if util.get_entry(entry) is None:
        return render(request, "encyclopedia/entry.html", {
                    "entry": "404",
                    "title": "Page not found"
                })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(util.get_entry(entry)),
            "title": entry
        })

