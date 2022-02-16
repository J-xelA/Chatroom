from django.urls import path
from django.contrib import admin
from chat.views import index, join, user_login, user_logout
from ticket import views as ticket_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index), # SlaykCord home

    path('join/', join),
    path('login/', user_login),
    path('logout/', user_logout),

    path('ticket/', ticket_views.ticket),
    path('ticket/add/', ticket_views.add),
    path('ticket/hideStatus/', ticket_views.hideStatus),
    path('ticket/showStatus/', ticket_views.showStatus),
    path('ticket/updateStatus/<int:id>/', ticket_views.updateStatus),
]
