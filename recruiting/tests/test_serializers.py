#!/usr/bin/env python3
import datetime

import pytest
from rest_framework.request import Request

from recruiting.serializers import VacancySerializer, CitySerializer, \
    CompanySerializer, ExchangeResultSerializer


@pytest.mark.django_db
class TestVacancySerializers:

    def test_serialize(self, rf, vacancy):
        request = rf.get('/')
        serializer_context = {'request': Request(request), }
        serializer = VacancySerializer(
            instance=vacancy, context=serializer_context
        )
        data = serializer.data
        assert set(data.keys()) == {'url', 'is_active', 'title', 'description',
                                    'company', 'locations', 'image_list'}

    def test_deserialize(self, company, city, another_city):

        data = {"is_active": True, "title": "title111",
                "description": "description111",
                "company": "/companies/{0}/".format(company.id),
                "locations": ["/cities/{0}/".format(city.id),
                              "/cities/{0}/".format(another_city.id)]}
        serializer = VacancySerializer(data=data)
        assert serializer.is_valid() is True


@pytest.mark.django_db
class TestExchangeResultSerializers:

    def test_serialize(self, rf, exchange_result):
        request = rf.get('/')
        serializer_context = {'request': Request(request), }
        serializer = ExchangeResultSerializer(
            instance=exchange_result, context=serializer_context
        )
        data = serializer.data
        assert set(data.keys()) == {'url', 'vacancy', 'created', 'success',
                                    'screenshot_list'}

    def test_deserialize(self, vacancy):
        time = datetime.datetime.now().isoformat()
        data = {"vacancy": "/vacancies/{0}/".format(vacancy.id),
                "created": time, "success": True}
        serializer = ExchangeResultSerializer(data=data)
        assert serializer.is_valid() is True


@pytest.mark.django_db
class TestCompanySerializers:

    def test_serialize(self, rf, company):
        request = rf.get('/')
        serializer_context = {'request': Request(request), }
        serializer = CompanySerializer(
            instance=company, context=serializer_context
        )
        data = serializer.data
        assert set(data.keys()) == {'url', 'name'}

    def test_deserialize(self, company):
        data = {"name": "/companies/{0}/".format(company.id)}
        serializer = CompanySerializer(data=data)
        assert serializer.is_valid() is True


@pytest.mark.django_db
class TestCitySerializers:

    def test_serialize(self, rf, city):
        request = rf.get('/')
        serializer_context = {'request': Request(request), }
        serializer = CitySerializer(
            instance=city, context=serializer_context
        )
        data = serializer.data
        assert set(data.keys()) == {'url', 'name'}

    def test_deserialize(self, city):
        data = {"name": "/cities/{0}/".format(city.id)}
        serializer = CitySerializer(data=data)
        assert serializer.is_valid() is True
