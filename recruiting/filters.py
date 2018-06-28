#!/usr/bin/env python3
import django_filters

from recruiting.models import ExchangeResult


class ExchangeResultFilter(django_filters.FilterSet):
    created = django_filters.CharFilter(lookup_expr='date')

    class Meta:
        model = ExchangeResult
        fields = ['vacancy', 'success']
