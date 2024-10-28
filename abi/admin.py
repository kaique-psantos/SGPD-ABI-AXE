
from django.apps import apps
from django.contrib import admin
from .models import Cargo

# Register your models here.

app_models = apps.get_app_config('abi').get_models()
for model in app_models:
    try:

        admin.site.register(model)

    except Exception:
        pass


#class CargoAdmin(admin.ModelAdmin):
#    list_display = ('car_descricao', 'car_ativo')
#    search_fields = ('car_descricao',)

#admin.site.register(Cargo, CargoAdmin)
