from django.http import HttpResponse
import os.path
BASE = os.path.dirname(os.path.abspath(__file__+"/../"))

#print(BASE)
#print(os.path.join(BASE, 'templates/index.html'))
def display(request):
    html = "<html><body>Failed to load tweetmap.</body></html>"
    with open(os.path.join(BASE, 'templates/index.html'), 'r') as myfile:
        html = myfile.read()
        myfile.close()
    return HttpResponse(html)