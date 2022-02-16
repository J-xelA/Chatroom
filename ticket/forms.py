from django import forms
from ticket.models import TicketEntry

class TicketEntryForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))
    entry = forms.CharField(widget=forms.Textarea(attrs={'size': '40'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))
    class Meta():
        model = TicketEntry
        fields = ('description', 'entry')
