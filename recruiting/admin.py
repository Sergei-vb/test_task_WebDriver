from django.contrib import admin
from .models import Company, Image, City, Vacancy, ExchangeResult

admin.site.register(Company)
admin.site.register(Image)
admin.site.register(City)
admin.site.register(Vacancy)
admin.site.register(ExchangeResult)
