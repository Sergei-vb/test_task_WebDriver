#!/usr/bin/env python3
import os
from urllib.request import urlretrieve
from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from recruiting.models import Vacancy, Company, Image, City
from test_task_WebDriver.settings import MEDIA_ROOT


class Command(BaseCommand):
    help = 'Runs parser.'

    def __init__(self):
        super().__init__()
        self.driver = webdriver.Chrome()

    def handle(self, *args, **options):
        try:
            self.driver.get(
                "https://www.ausbildung.de/unternehmen/blg-logistics/stellen/"
            )

            elements = self.driver.find_elements_by_xpath(
                "//a[@class='simple-card__link simple-card__link--column']"
            )
            links = [link.get_attribute("href") for link in elements]

            actual_vacancies = []
            for link in links:
                vacancy = self.link_parser(link)
                actual_vacancies.append(vacancy)
                self.driver.back()

            self.check_vacancies_in_db(actual_vacancies)
            self.driver.close()
        except:
            self.stderr.write("Unsuccessfully")
        else:
            self.stdout.write(self.style.SUCCESS('Successfully'))

    def link_parser(self, link):
        self.driver.get(link)

        company, _ = Company.objects.get_or_create(
            name=self.driver.find_element_by_xpath(
                "//h1[@class='title title--left']/a"
            ).text
        )
        title = self.driver.find_element_by_xpath(
            "//h3[@class='title title--section']"
        ).text

        exist_in_db = Vacancy.objects.filter(
            title=title,
            company=company
        )

        if not exist_in_db:
            description = self.driver.find_element_by_xpath(
                "//div[@class='entity-description__description']"
            ).text

            location_objects = self.get_locations()
            images_array = self.get_images()

            vacancy = Vacancy()
            vacancy.is_active = True
            vacancy.title = title
            vacancy.description = description
            vacancy.company = company
            vacancy.save()

            vacancy.locations.add(*location_objects)

            vacancy.image_list.add(
                *[obj for obj in Image.objects.filter(image__in=images_array)]
            )

            vacancy.save()

            return vacancy.id

        vacancy = Vacancy.objects.get(title=title, company=company)
        return vacancy.id

    def get_locations(self):
        try:
            element_click = self.driver.find_element_by_css_selector(
                "div.selectize-input"
            )
            element_click.click()

            all_elements = self.driver.find_elements_by_css_selector(
                "div.selectize-dropdown-content > div"
            )
            all_locations = [el.text for el in all_elements]
        except NoSuchElementException:
            all_locations = [self.driver.find_element_by_xpath(
                "//div[@class='vacancies-info']/strong"
            ).text]

        location_objects = []
        for location in all_locations:
            location, _ = City.objects.get_or_create(name=location)
            location_objects.append(location)

        return location_objects

    def get_images(self):
        elements = self.driver.find_elements_by_xpath(
            "//div[@class='quadruple-media__media-list']/div/img"
        )

        images_array = []
        for element in elements:
            url = element.get_attribute('src')
            images_array.append(url)

            check_for_exist = Image.objects.filter(image=url)
            if not check_for_exist:
                image = Image()
                image.image = url

                path_to_images = os.path.join(MEDIA_ROOT, "images/")
                filename = url.split("/")[-1]
                file = os.path.join(path_to_images, filename)
                urlretrieve(url, filename=file)

                image.file_image.name = "images/{0}".format(filename)
                image.save()
        return images_array

    def check_vacancies_in_db(self, actual_vacancies):
        deactivate_vacancies = Vacancy.objects.exclude(id__in=actual_vacancies)
        if deactivate_vacancies:
            for vacancy in deactivate_vacancies:
                vacancy.is_active = False
                vacancy.save()
