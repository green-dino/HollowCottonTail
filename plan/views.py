from django.shortcuts import render

from django.shortcuts import render
from .models import PlanItem


def plan_list(request):
    items = PlanItem.objects.all()
    return render(request, "plan/plan_list.html", {"items": items})
