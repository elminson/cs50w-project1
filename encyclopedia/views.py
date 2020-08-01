from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def new(request):
    return render(request, "encyclopedia/new.html", {
        "entries": util.list_entries()
    })

def edit(request):
    return render(request, "encyclopedia/edit.html", {
        "entries": util.list_entries()
    })

def search(request):
    return render(request, "encyclopedia/search.html", {
        "entries": util.list_entries(),
        "searchTerm": request.GET["q"]
    })

def random(request):
    return render(request, "encyclopedia/random.html", {
        "entries": util.list_entries()
    })

