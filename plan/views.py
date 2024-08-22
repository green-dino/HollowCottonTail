from django.shortcuts import render , HttpResponse
from .models import Post

def index(request):
    return HttpResponse("hi")

def post_list(reqest):
    return render(request=reqest, template_name="post_list.html", context={"items":Post.objects.all()})


