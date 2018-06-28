#!/usr/bin/env python3
from rest_framework import serializers

from recruiting.models import Vacancy, ExchangeResult, Company, City, Image,\
    Screenshot


class VacancySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vacancy
        fields = "__all__"


class ExchangeResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExchangeResult
        fields = "__all__"


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class ScreenshotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Screenshot
        fields = "__all__"
