from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse


def index(request):
    return render(request, 'index.html')