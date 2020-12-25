from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import QueryForm
from .models import EngineModel, Result

ml = EngineModel()

def home(request):
    context = {
        "form": QueryForm()
    }
    return render(request,'search_app/home.html', context)

def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QueryForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            query = form.cleaned_data["query"]
            (qr, dt), (qr_pb, dt_pb), classes = ml.search(query)
            print(qr, qr_pb, classes)
            dt["bloom"] = dt_pb.values

            return render(request, 'app/index.html', {'form': form, "results": Result.createResults(dt)})
    form = QueryForm()
    return render(request, 'search_app/index.html', {'form': form})




"""
    resultats_list = None
    paginator = Paginator(resultats_list, 7)
    nombre_page = int(len(resultats_list)/7) if len(resultats_list)%7 == 0  else int(len(resultats_list)/7 + 1)
    x = range(nombre_page)
    page = request.GET.get('page')
    try:
        resultats = paginator.page(page)
    except PageNotAnInteger:
        resultats = paginator.page(1)
    except EmptyPage:
        resultats = paginator.page(paginator.num_pages)
    context = {'resultats': resultats, 
                'x': x,
    }
    return render(request,'search_app/index.html', context)
"""