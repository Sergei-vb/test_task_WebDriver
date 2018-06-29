#!/usr/bin/env python3
import datetime

import pytest

from recruiting.models import Vacancy, ExchangeResult, Company, City

created_datetime = datetime.datetime.now().isoformat()


@pytest.fixture
def city(db):
    return City.objects.create(name='city1')


@pytest.fixture
def another_city(db):
    return City.objects.create(name='city2')


@pytest.fixture
def company(db):
    return Company.objects.create(name='company1')


@pytest.fixture
def locations(db, city, another_city):
    return [city, another_city]


@pytest.fixture
def vacancy(db, company, locations):
    obj = Vacancy(
        is_active=True, title='vacancy1', description='description1',
        company=company
    )
    obj.save()
    obj.locations.add(*locations)
    obj.save()
    return obj


@pytest.fixture
def exchange_result(db, vacancy):
    return ExchangeResult.objects.create(
        vacancy=vacancy, created=created_datetime, success=True
    )
