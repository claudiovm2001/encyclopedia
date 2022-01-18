from django.shortcuts import render

from . import util

from django import forms

class NewEntryForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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
            content = form.cleaned_data["content"]
            util.save_entry(title, content)

    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm()
    })