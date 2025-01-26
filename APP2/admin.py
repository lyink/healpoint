from django.contrib import admin
from . import models

class RegistrationAdmin(admin.ModelAdmin):
    list_per_page = 6
    list_max_show_all = 6
    # list_editable = ('marital','resident','program',)
    search_fields = ('marital','resident','program','firstname',)
    list_display=('accomodation','marital','resident','program','certificate','disability','tutorial_session','firstname','lastname','date_of_birth')
admin.site.register(models.Registration,RegistrationAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_per_page = 6
    list_max_show_all = 6
    list_display=('message','created_at','closed_date')
admin.site.register(models.MessageToForm,MessageAdmin)