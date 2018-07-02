#!/usr/bin/env python3
import datetime
import json

import pytest

from recruiting.views import VacancyViewSet, CompanyViewSet, CityViewSet, \
    ExchangeResultViewSet

JSON_TYPE = 'application/json'


@pytest.mark.django_db
class TestVacancyViewSet:

    def test_vacancy_create(self, rf, company):
        view = VacancyViewSet.as_view(actions={'post': 'create'})
        data = {"is_active": True, "title": "vacancy11",
                "description": "description11",
                "company": "/companies/{0}/".format(company.id)}
        request = rf.post('/vacancies/', data=json.dumps(data),
                          content_type=JSON_TYPE)
        response = view(request)
        assert response.status_code == 201

    def test_vacancy_list(self, rf):
        view = VacancyViewSet.as_view(actions={'get': 'list'})
        request = rf.get('/vacancies/')
        response = view(request)
        assert response.status_code == 200

    def test_vacancy_detail(self, rf, vacancy):
        view = VacancyViewSet.as_view(actions={'get': 'retrieve'})
        request = rf.get('/vacancies/')
        response = view(request, pk=vacancy.id)
        assert response.status_code == 200


@pytest.mark.django_db
class TestCompanyViewSet:

    def test_company_create(self, rf):
        view = CompanyViewSet.as_view(actions={'post': 'create'})
        data = {"name": "name11"}
        request = rf.post('/companies/', data=json.dumps(data),
                          content_type=JSON_TYPE)
        response = view(request)
        assert response.status_code == 201

    def test_company_list(self, rf):
        view = CompanyViewSet.as_view(actions={'get': 'list'})
        request = rf.get('/companies/')
        response = view(request)
        assert response.status_code == 200

    def test_company_detail(self, rf, company):
        view = CompanyViewSet.as_view(actions={'get': 'retrieve'})
        request = rf.get('/companies/')
        response = view(request, pk=company.id)
        assert response.status_code == 200


@pytest.mark.django_db
class TestCityViewSet:

    def test_city_create(self, rf):
        view = CityViewSet.as_view(actions={'post': 'create'})
        data = {"name": "city11"}
        request = rf.post('/cities/', data=json.dumps(data),
                          content_type=JSON_TYPE)
        response = view(request)
        assert response.status_code == 201

    def test_city_list(self, rf):
        view = CityViewSet.as_view(actions={'get': 'list'})
        request = rf.get('/cities/')
        response = view(request)
        assert response.status_code == 200

    def test_city_detail(self, rf, city):
        view = CityViewSet.as_view(actions={'get': 'retrieve'})
        request = rf.get('/cities/')
        response = view(request, pk=city.id)
        assert response.status_code == 200


@pytest.mark.django_db
class TestExchangeResultViewSet:

    def test_exchange_result_create(self, rf, vacancy):
        view = ExchangeResultViewSet.as_view(actions={'post': 'create'})
        time = datetime.datetime.now().isoformat()
        data = {"vacancy": "/vacancies/{0}/".format(vacancy.id),
                "created": time, "success": True}
        request = rf.post('/exchange_results/', data=json.dumps(data),
                          content_type=JSON_TYPE)
        response = view(request)
        assert response.status_code == 201

    def test_exchange_result_list(self, rf):
        view = CompanyViewSet.as_view(actions={'get': 'list'})
        request = rf.get('/exchange_results/')
        response = view(request)
        assert response.status_code == 200

    def test_exchange_result_detail(self, rf, exchange_result):
        view = CompanyViewSet.as_view(actions={'get': 'retrieve'})
        request = rf.get('/exchange_results/')
        response = view(request, pk=exchange_result.id)
        assert response.status_code == 200
