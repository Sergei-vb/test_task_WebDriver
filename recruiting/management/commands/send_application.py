#!/usr/bin/env python3
import datetime
import json
import os
from urllib import parse
from urllib.request import urlretrieve

from django.conf import settings
from django.core.management.base import BaseCommand
from selenium import webdriver

from recruiting.models import Screenshot, ExchangeResult, Vacancy


class Command(BaseCommand):
    help = 'Create exchange handler.'

    def __init__(self):
        super().__init__()

        self.data = {}

        self.catalog_name = datetime.datetime.now().isoformat()
        self.path_to_screenshots = os.path.join(
            settings.MEDIA_ROOT, "screenshot_list/",
            "{0}".format(self.catalog_name)
        )
        os.mkdir(self.path_to_screenshots)

        self.screenshots = []
        self.driver = webdriver.Chrome(
            os.path.join(settings.BASE_DIR, "drivers/chromedriver")
        )

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='+', type=str)

    def handle(self, *args, **options):
        url = options['url'][0]

        try:
            self.handle_first_page(url)
            second_page_data = self.handle_second_page()
            third_page_data = self.handle_third_page(second_page_data)
            result = self.handle_fourth_page(third_page_data)

            instances_array = self.create_screenshot_instances(
                self.screenshots)
            self.create_exchange_result(instances_array, result)
        except:
            self.stderr.write("Unsuccessfully")
        else:
            self.stdout.write(self.style.SUCCESS('Successfully'))
        finally:
            self.driver.close()

    def handle_first_page(self, url):
        self.driver.get(url)

        self.do_screenshot(1)

        title = self.driver.find_element_by_xpath(
            "//h3[@class='title title--section']"
        ).text
        company = self.driver.find_element_by_xpath(
            "//h1[@class='title title--left']/a"
        ).text
        location = self.driver.find_element_by_xpath(
            "//div[@class='vacancies-info']/strong"
        ).text
        link_element = self.driver.find_element_by_xpath(
            "//a[@class='filled-button js-application-button "
            "js-application-button--online']"
        ).get_attribute("href")

        self.data.update({
            "link_element": link_element, "title": title,
            "location": location, "company": company
        })

    def handle_second_page(self):
        link_element = self.data["link_element"]
        title = self.data["title"]
        title = title if not title.endswith(" (m/w)") else title[:-6]
        location = self.data["location"]
        self.driver.get(link_element)

        self.do_screenshot(2)

        row_element = self.driver.find_element_by_xpath(
            "//table[@class='m-table m-table--stripe js-jobs-container']/tbody"
            "/tr[td[@data-title='Titel'][a[ text() = \"{0}\" ]] and "
            "td[@data-title='Arbeitsort'][ text() = \"{1}\" ]]".format(
                title, location)
        )

        link = row_element.find_element_by_xpath(
            "td[@data-title='Titel']/a"
        ).get_attribute("href")

        return link

    def handle_third_page(self, link):
        self.driver.get(link)

        self.do_screenshot(3)

        link = self.driver.find_element_by_xpath(
            "//a[@class='m-button m-button--wide m-button--has-suffix']"
        ).get_attribute("href")

        return link

    def handle_fourth_page(self, link):
        self.driver.get(link)

        self.do_screenshot(4)

        path_to_storage = os.path.join(
            settings.MEDIA_ROOT, "exchange_handler/"
        )

        data = settings.DATA_ENV_VAR

        self.driver.find_element_by_xpath(
            "//select[@name='geschlecht']/option[@value='{0}']".format(
                data["gender"].lower())
        ).click()
        self.do_screenshot(5)

        self.driver.find_element_by_xpath(
            "//input[@name='vorname']"
        ).send_keys(data["first_name"])
        self.do_screenshot(6)

        self.driver.find_element_by_xpath(
            "//input[@name='nachname']"
        ).send_keys(data["last_name"])
        self.do_screenshot(7)

        self.driver.find_element_by_xpath(
            "//input[@name='strasse']"
        ).send_keys(data["street"])
        self.do_screenshot(8)

        self.driver.find_element_by_xpath(
            "//input[@name='plz']"
        ).send_keys(data["postal_code"])
        self.do_screenshot(9)

        self.driver.find_element_by_xpath(
            "//input[@name='ort']"
        ).send_keys(data["city"])
        self.do_screenshot(10)

        self.driver.find_element_by_xpath(
            "//input[@name='geburtsdatum']"
        ).send_keys(data["birthday"])
        self.do_screenshot(11)

        self.driver.find_element_by_xpath(
            "//input[@name='handy']"
        ).send_keys(data["phone"])
        self.do_screenshot(12)

        self.driver.find_element_by_xpath(
            "//input[@name='mail']"
        ).send_keys(data["email"])
        self.do_screenshot(13)

        self.driver.find_element_by_xpath(
            "//select[@name='aufmerksam_geworden']/option[@value='62']"
        ).click()
        self.do_screenshot(14)

        url_cv = data["cv_path"]
        cv_filename = 'cv.pdf'
        cv_path = os.path.join(path_to_storage, cv_filename)
        urlretrieve(url_cv, filename=cv_path)

        url_photo = data["photo"]
        photo_filename = 'photo.jpg'
        photo_path = os.path.join(path_to_storage, photo_filename)
        urlretrieve(url_photo, filename=photo_path)

        self.driver.find_element_by_xpath(
            "//tr/td[@class='form_DATEN']/input[@name='upfile']"
        ).send_keys(cv_path)
        self.do_screenshot(15)

        self.driver.find_element_by_xpath(
            "//tr/td[@class='form_DATEN']/input[@name='upfile2']"
        ).send_keys(photo_path)
        self.do_screenshot(16)

        self.driver.find_element_by_xpath(
            "//tr/td[@class='form_DATEN']/input[@name='upfile3']"
        ).send_keys(cv_path)
        self.do_screenshot(17)

        self.driver.find_element_by_xpath(
            "//tr/td[@class='form_DATEN']/input[@name='upfile4']"
        ).send_keys(cv_path)
        self.do_screenshot(18)

        self.driver.find_element_by_xpath(
            "//td[@class='form_text']/div/input[@type='checkbox']"
        ).click()
        self.do_screenshot(19)

        self.driver.find_element_by_xpath(
            "//input[@id='bewerben']"
        ).click()
        self.do_screenshot(20)

        current_url = self.driver.current_url
        par = parse.parse_qs(parse.urlparse(current_url).query)

        return par.get("update") == ["ok"]

    def do_screenshot(self, number):
        screen = os.path.join(
            self.path_to_screenshots, "screen{0}___{1}.png".format(
                self.catalog_name, number
            )
        )
        self.driver.get_screenshot_as_file(screen)
        self.screenshots.append(screen)

    def create_screenshot_instances(self, screenshots_array):
        instances_array = []
        for screenshot in screenshots_array:
            screenshot = "/".join(screenshot.split("/")[-3:])
            obj = Screenshot.objects.create(file_screen=screenshot)
            instances_array.append(obj)

        return instances_array

    def create_exchange_result(self, instances_array, result):
        vacancy = Vacancy.objects.get(
            title=self.data["title"], company__name=self.data["company"]
        )
        instance = ExchangeResult.objects.create(
            vacancy=vacancy, created=datetime.datetime.now().isoformat(),
            success=result
        )
        instance.screenshot_list.add(*instances_array)
