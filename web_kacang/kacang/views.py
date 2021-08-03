from django.shortcuts import render

# Create your views here.
def index(request):
    title = 'Dashboard'
    author = 'Made with 💚 by Diaz Ardian'
    content = {
        'title': title,
        'author': author,
        'logo': 'KACANG SERVER'
    }
    return render(request, 'index.html', content)