from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect

from .forms import ZipcodeForm

def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ZipcodeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            data = form.cleaned_data
            #data['zipcode']
            return HttpResponseRedirect(data['zipcode'] + '/results/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ZipcodeForm()

    return render(request, 'index.html', {'form': form})

def results(request, zipcode):
    template = loader.get_template('results.html')
    context = { "zipcode" : zipcode }
    return HttpResponse(template.render(context, request))