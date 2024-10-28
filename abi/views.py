from django.shortcuts import render


def index(request):

  context = {
    'segment'  : 'index',
  }
  return render(request, "pages/index.html", context)

def teste(request):

  context = {
    'segment'  : 'teste',
  }
  return render(request, "pages/teste.html", context)

def cargo(request):

  context = {
    'segment'  : 'cargo',
  }
  return render(request, "pages/cargo.html", context)
