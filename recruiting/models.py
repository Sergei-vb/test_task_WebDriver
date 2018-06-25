from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'


class Image(models.Model):
    image = models.FileField()


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cities'


class Vacancy(models.Model):
    is_active = models.BooleanField()
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=5000)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    locations = models.ManyToManyField(City, blank=True)
    # image_list = models.ManyToManyField(Image)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Vacancies'


class ExchangeResult(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    created = models.DateField()
    success = models.BooleanField()
    screenshot_list = models.ManyToManyField(Image)
