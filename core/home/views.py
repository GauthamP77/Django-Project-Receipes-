from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    
    peoples=[
        {'name':'Gautham','age':21},
        {'name':'Kaif','age':22}
    ]
    vegetables=['tomato','potato','onion']
    text ="Lorem dolodljfhewhfbqewhbfwh sdhbchsdbchdabuqefdujewncjksdnaciuqewhfiueqncjefuierhi"
       
    for people in peoples :
        if people['age'] :
            print("Yes")
    return render(request, "home/index.html",context={'Page':"Django",'peoples':peoples, 'text' :text, 'vegetables':vegetables})

def about(request):
    context={'Page':"Django/About"}
    return render(request, "home/about.html",context)

def contact(request):
    context={'Page':"Django/Contact"}
    return render(request, "home/contact.html",context)
    
   
def success_page(request):
    print("*" * 10)
    return HttpResponse("<h1>Hey this is Success Page</h1>")