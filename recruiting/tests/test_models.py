#!/usr/bin/env python3
import pytest


@pytest.mark.django_db
class TestModel:

    def test_str_method(self, vacancy, company, city):
        assert str(vacancy) == vacancy.title
        assert str(company) == company.name
        assert str(city) == city.name
