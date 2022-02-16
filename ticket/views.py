from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ticket.models import TicketEntry
from ticket.forms import TicketEntryForm
from django.contrib.auth.models import User
from django.shortcuts import render
# Create your views here.

@login_required(login_url='/login/')
def ticket(request):
	if (request.method == "GET" and "delete" in request.GET):
		id = request.GET["delete"]
		TicketEntry.objects.filter(id=id).delete()
		return redirect("/ticket/")
	else:
		table_data = TicketEntry.objects.filter()
		context = {
			"table_data": table_data,
		}
		return render(request, 'ticket/ticket.html', context)

@login_required(login_url='/login/')
def add(request):
	if (request.method == "POST"):
		if ("add" in request.POST):
			add_form = TicketEntryForm(request.POST)
			if (add_form.is_valid()):
				description = add_form.cleaned_data["description"]
				entry = add_form.cleaned_data["entry"]
				name = add_form.cleaned_data["name"]
				TicketEntry(description=description, entry=entry, name=name).save()
				return redirect("/")
			else:
				context = {
					"form_data": add_form
				}
				return render(request, 'ticket/add.html', context)
		else:
			# Cancel
			return redirect("/")
	else:
		context = {
			"form_data": TicketEntryForm()
		}
		return render(request, 'ticket/add.html', context)


def updateStatus(request, id):
	entry = TicketEntry.objects.get(id=id)
	stat = entry.status
	entry.status = not stat
	entry.id = id
	entry.save()
	return redirect("/ticket/")

def showStatus(request):
	table_data = TicketEntry.objects.filter()
	context = {
	"table_data": table_data
	}
	return render(request, 'ticket/ticket.html', context)

def hideStatus(request):
	table_data = TicketEntry.objects.filter(status=False)
	context = {
	"table_data": table_data
	}
	return render(request, 'ticket/ticket.html', context)
