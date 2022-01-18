from django.shortcuts import render

from . import util


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