from django.shortcuts import render

from . import util

from django import forms
from django.http import HttpResponseRedirect

#Código autoral abaixo:
import random 

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

#View para cada entrada da enciclopédia:
def entry(request, title):
    content = util.get_entry(title)
    form = NewSearchForm()
    
    #Se a página não existir nos arquivos:
    if content == None:
        return render(request, "encyclopedia/entry.html", {
            "title": title, "content": "A página solicitada não foi encontrada.", "form_search": form
        })

    return render(request, "encyclopedia/entry.html", {
        "title": title, "content": content, "form_search": form
    })

#View para criar uma página nova:
def create(request):
    form_search = NewSearchForm()

    if request.method == "POST":
        form = NewEntryForm(request.POST)
        
        if form.is_valid():

            title = form.cleaned_data["title"]
    
            #Se uma página com o mesmo título já existir:
            if util.get_entry(title) != None:
                return render(request, "encyclopedia/entry.html", {
                    "title": title, "content": "Esta página já existe.", "form_search": form_search
                })

            content = form.cleaned_data["content"]
            util.save_entry(title, content)

            return render(request, "encyclopedia/entry.html", {
                "title": title, "content": content, "form_search": form_search
            })

    return render(request, "encyclopedia/create.html", {
        "form_create": NewEntryForm(), "form_search": form_search
    })

#View para pesquisa:
def search(request):

    if request.method == "POST":
        form = NewSearchForm(request.POST)

        if form.is_valid():

            query = form.cleaned_data["query"]
            
            #Se o título pesquisado for EXATAMENTE igual a algum já presente nos arquivos:
            if util.get_entry(query) != None:
                return HttpResponseRedirect("wiki/"+query) #Ir para a página com este título

            l = util.list_entries()
            
            #Se o começo do texto pesquisado corresponder ao que existe nos arquivos:
            results_low = list(filter(lambda x: x.startswith(query.lower()), l))
            results_up = list(filter(lambda x: x.startswith(query.upper()), l))

            results = results_low + results_up #Desconsiderar caixa alta/baixa para o título

            return render(request, "encyclopedia/index.html", {
                "entries": results, "text": "Resultados: ", "form_search": NewSearchForm()
            })

#View para edição de página:
def edit(request, title):

    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            
            #Faz a troca do título antigo da página pelo novo:
            title_old = title
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            #Salva a nova página e apaga a antiga:
            util.save_entry(title, content)
            util.delete_entry(title_old)

            return render(request, "encyclopedia/entry.html", {
                "title": title, "content": content, "form_search": NewSearchForm()
            })

    form = NewEntryForm(initial={
        "title": title, "content": util.get_entry(title)
    })

    return render(request, "encyclopedia/edit.html", {
        "form_create": form, "title": title, "form_search": NewSearchForm()
    })

#Função para página aleatória:
def randomize(request):
    l = util.list_entries()
    num = random.randint(0,(len(l)-1))
    target = l[num]
    
    #Seleciona um número aleatório, com valores entre 0 e o total de páginas,
    #depois usa esse valor para redirecionar

    return HttpResponseRedirect("wiki/"+target)
