from django.shortcuts import render
from .forms import MeasurementForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .logic.logic_measurement import create_measurement, get_measurements
from django.contrib.auth.decorators import login_required
from monitoring.auth0backend import getRole

@login_required
def measurement_list(request):
    role=getRole(request)
    if role == "Supervisor":
        measurements = get_measurements()
        context = {
            'measurement_list': measurements
        }
        return render(request, 'Measurement/measurements.html', context)
    else:
        return HttpResponse("Unauthorized User")

def measurement_create(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            create_measurement(form)
            messages.add_message(request, messages.SUCCESS, 'Measurement create successful')
            return HttpResponseRedirect(reverse('measurementCreate'))
        else:
            print(form.errors)
    else:
        form = MeasurementForm()

    context = {
        'form': form,
    }

    return render(request, 'Measurement/measurementCreate.html', context)