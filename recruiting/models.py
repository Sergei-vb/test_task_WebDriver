from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'


class Image(models.Model):
    image = models.CharField(max_length=500, null=True)
    file_image = models.FileField(null=True)

    def __str__(self):
        return self.image


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
    image_list = models.ManyToManyField(Image, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Vacancies'


class Screenshot(models.Model):
    file_screen = models.FileField(null=True)

    def __str__(self):
        return str(self.file_screen)


class ExchangeResult(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    created = models.DateTimeField()
    success = models.BooleanField()
    screenshot_list = models.ManyToManyField(Screenshot, blank=True)

    def __str__(self):
        return str(self.created)
