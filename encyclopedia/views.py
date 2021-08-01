from django.http.response import HttpResponse
from django.shortcuts import redirect, render
import markdown2
from . import util
import random

entry_list = []
def check_data(str, sub_str):
    if (str.find(sub_str) == -1):
        return 0
    else:
        return 1

def index(request):
    
    entry_list.clear()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entries(request, name):  
      
    html = util.get_entry(name)
    if html is None:
        error = f'The page {name} was not found'
        return render(request, "encyclopedia/error.html",{
                'name':name,
                'error':error
            })
    html = markdown2.markdown(f"{html}")
    entries = util.list_entries()
    for entry in entries:
        if entry in entries:
            return render(request,"encyclopedia/entry.html",{

                "name":name,
                "content": html

        })
    
    
    
    
def search(request):
     entries = util.list_entries()
     entry_list.clear()
     if request.method == 'POST':    
        q=request.POST['q'].lower()  
        q_html = util.get_entry(q)
        q_html = markdown2.markdown(f"{q_html}")
        for entry in entries:
            entry = entry.lower()
            if entry == q:
                return render(request, "encyclopedia/entry.html",{
                    "name":q,
                    "content":q_html
                }) 
            elif check_data(entry,q) == 1:
                entry_list.append(entry)
            
                
        return render(request,"encyclopedia/search_results.html",{
            'entries' : entry_list
        } )    
                
def random_result(request):
    return entries(request,random.choice(util.list_entries()))


def create_page(request):
    if request.method =='POST':
        title= request.POST['title']
        text_area = request.POST['text_area']
        entry_list = util.list_entries()
        for entry in entry_list:
            if title.lower() == entry.lower():
                error = 'Page already exist with this title'
                return render(request,"encyclopedia/error.html",{
                    'error': error
                })
        util.save_entry(title,text_area)
        return entries(request,title)
   
    else:    
        return render(request,"encyclopedia/create_page.html")

def edit_page(request):
    if request.method == 'POST':
        name = request.POST['name']
        md = util.get_entry(name)

        return render(request, "encyclopedia/edit_page.html",{
            'md':md,
            'name':name
        })

def save_page(request):
    if request.method=='POST':
        md=request.POST['text_area']
        title = request.POST['title']
        util.save_entry(title,md)
        return entries(request,title)