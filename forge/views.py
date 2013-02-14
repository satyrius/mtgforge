from oracle.models import CardSet
from django.shortcuts import render_to_response


def index(request):
    qs = CardSet.objects.order_by('name').values_list('acronym', 'name')
    return render_to_response('index.html', dict(
        sets=[dict(name=n, acronym=a) for a, n in qs]))
