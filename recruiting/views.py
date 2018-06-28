from rest_framework import viewsets

from recruiting.models import Vacancy, ExchangeResult, Company, City, Image,\
    Screenshot
from recruiting.serializers import VacancySerializer, \
    ExchangeResultSerializer, CompanySerializer, CitySerializer, \
    ImageSerializer, ScreenshotSerializer
from recruiting.filters import ExchangeResultFilter


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    filter_fields = ('title', 'company', 'is_active', 'locations')


class ExchangeResultViewSet(viewsets.ModelViewSet):
    queryset = ExchangeResult.objects.all()
    serializer_class = ExchangeResultSerializer
    filter_class = ExchangeResultFilter


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ScreenshotViewSet(viewsets.ModelViewSet):
    queryset = Screenshot.objects.all()
    serializer_class = ScreenshotSerializer
