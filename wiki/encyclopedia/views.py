from django.shortcuts import render

from . import util

from django import forms
from django.http import HttpResponseRedirect

class NewEntryForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content")

class NewSearchForm(forms.Form):
    query = forms.CharField(label="Search")

def index(request):
    form = NewSearchForm()

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form_search": form, "text": "All Pages"
    })

def entry(request, title):
    content = util.get_entry(title)

    if content == None:
        return render(request, "encyclopedia/entry.html", {
            "title": title, "content": "A página solicitada não foi encontrada."
        })

    return render(request, "encyclopedia/entry.html", {
        "title": title, "content": content
    })

def create(request):

    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():

            title = form.cleaned_data["title"]

            if util.get_entry(title) != None:
                return render(request, "encyclopedia/entry.html", {
                    "title": title, "content": "Esta página já existe."
                })

            content = form.cleaned_data["content"]
            util.save_entry(title, content)

            return render(request, "encyclopedia/entry.html", {
                "title": title, "content": content
            })

    return render(request, "encyclopedia/create.html", {
        "form_create": NewEntryForm()
    })

def search(request):

    if request.method == "POST":
        form = NewSearchForm(request.POST)

        if form.is_valid():

            query = form.cleaned_data["query"]

            if util.get_entry(query) != None:
                return HttpResponseRedirect("wiki/"+query)

            l = util.list_entries()

            results_low = list(filter(lambda x: x.startswith(query.lower()), l))
            results_up = list(filter(lambda x: x.startswith(query.upper()), l))

            results = results_low + results_up

            return render(request, "encyclopedia/index.html", {
                "entries": results, "text": "Resultados: "
            })

def edit(request, title):

    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():

            title_old = title
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            util.save_entry(title, content)
            util.delete_entry(title_old)

            return render(request, "encyclopedia/entry.html", {
                "title": title, "content": content
            })

    form = NewEntryForm(initial={
        "title": title, "content": util.get_entry(title)
    })

    return render(request, "encyclopedia/edit.html", {
        "form_create": form, "title": title
    })