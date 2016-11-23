from django.shortcuts import render, loader
from django.http import HttpResponse


def index(request):
    #template = loader.get_template("html/sockets.html")
    return render(request, "html/sockets.html")
