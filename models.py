import copy
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import platform

from pathlib import Path
import os
import cv2

import config
import services

'''
class с набором функций для выполнения определенных тестов.
Параметры каждого теста прописанны индивидуально поскольку названия блоков разные для разных страниц
Функции получения шаблона только сохраняют шаблон
Функции Теста получаютновое изображение и сравнивают его с шаблоном
Каждая функция создает экземпляр класса с определенными параметрами в зависимости от вида теста или шаблона
На выходе мы имеем сохраненные файлы на диске, а в случае с "проввльным" тестом еще и список файлов необходимых для возврата пользователю как результата
'''

slash = services.slash

class MainTestPicture(object):

    def get_new_cutomer_template(self, message, url, ):
        class_list = config.CLASS_LIST_NEW_CUSTOMER
        get_template = GetTemplate()
        get_template.dir = config.DIR_TEMPLATE_NEW_CUSTOMER
        get_template.get_template(message, url, class_list)
        if get_template.get_error():
            crash_list = ['Error']
            return crash_list

        # Verify platform and create path related to platform.

    def test_picture_new_customer(self, message, url):
        class_list = config.CLASS_LIST_NEW_CUSTOMER
        get_template = GetTemplate()
        get_template.dir = config.DIR_TEST_NEW_CUSTOMER
        get_template.get_template(message, url, class_list)
        if get_template.get_error():
            crash_list = ['Error']
            return crash_list

        test_picture = TestPicture()
        test_picture.dir = config.DIR_WORK_NEW_CUTOMER
        crash_list = test_picture.test_picture(message)
        return crash_list

    def get_delivery_template(self, message, url, ):
        class_list = config.CLASS_LIST_DELIVEY
        get_template = GetTemplate()
        get_template.delivey = True
        get_template.dir = 'delivery/template'
        get_template.get_template(message, url, class_list)
        if get_template.get_error():
            crash_list = ['Error']
            return crash_list

    def test_picture_delivery(self, message, url):
        class_list = config.CLASS_LIST_DELIVEY
        get_template = GetTemplate()
        get_template.delivey = True
        get_template.dir = 'delivery/test'
        get_template.get_template(message, url, class_list)
        if get_template.get_error():
            crash_list = ['Error']
            return crash_list

        test_picture = TestPicture()
        test_picture.dir = 'delivery'

        crash_list = test_picture.test_picture(message)
        return crash_list

    def get_product_template(self, message, url, ):
        class_list = config.CLASS_LIST_PRODUCT
        get_template = GetTemplate()
        get_template.product = True
        get_template.dir = 'product/template'
        get_template.get_template(message, url, class_list)
        if get_template.get_error():
            crash_list = ['Error']
            return crash_list

    def test_picture_product(self, message, url, ):
        class_list = config.CLASS_LIST_PRODUCT
        get_template = GetTemplate()
        get_template.product = True
        get_template.dir = 'product/test'
        get_template.get_template(message, url, class_list)

        if get_template.get_error():
            crash_list = ['Error']
            return crash_list

        test_picture = TestPicture()
        test_picture.dir = 'product'
        crash_list = test_picture.test_picture(message)
        return crash_list

    def get_headfoot_template(self, message, url, ):
        class_list = config.CLASS_LIST_HEADFOOT
        get_template = GetTemplate()
        get_template.dir = 'headfoot/template'
        get_template.get_template(message, url, class_list)
        if get_template.get_error():
            crash_list = ['Error']
            return crash_list

    def test_picture_headfoot(self, message, url):
        class_list = config.CLASS_LIST_HEADFOOT
        get_template = GetTemplate()
        get_template.dir = 'headfoot/test'
        get_template.get_template(message, url, class_list)
        if get_template.get_error():
            crash_list = ['Error']
            return crash_list

        test_picture = TestPicture()
        test_picture.dir = 'headfoot'
        crash_list = test_picture.test_picture(message)
        return crash_list

    def get_menu_template(self, message, url):
        class_list = config.CLASS_LIST_MENU
        get_template = GetTemplate()
        get_template.menu = True
        get_template.dir = 'menu/template'
        get_template.get_template(message, url, class_list)
        if get_template.get_error():
            crash_list = ['Error']
            return crash_list

    def test_picture_menu(self, message, url):
        class_list = config.CLASS_LIST_MENU
        get_template = GetTemplate()
        get_template.menu = True
        get_template.dir = 'menu/test'
        get_template.get_template(message, url, class_list)

        if get_template.get_error():
            crash_list = ['Error']
            return crash_list

        test_picture = TestPicture()
        test_picture.dir = 'menu'
        crash_list = test_picture.test_picture(message)
        return crash_list

    def get_home_template(self, message, url):
        class_list = config.CLASS_LIST_HOME
        get_template = GetTemplate()
        get_template.home = True
        get_template.dir = 'home/template'
        get_template.get_template(message, url, class_list)
        if get_template.get_error():
            crash_list = ['Error']
            return crash_list

    def test_picture_home(self, message, url):
        class_list = config.CLASS_LIST_HOME
        get_template = GetTemplate()
        get_template.dir = 'home/test'
        get_template.get_template(message, url, class_list)
        if get_template.get_error():
            crash_list = ['Error']
            return crash_list

        test_picture = TestPicture()
        test_picture.dir = 'home'
        crash_list = test_picture.test_picture(message)
        return crash_list


'''
class получения шаблона эземпляр создается пределенными параметрами в зависимости от вида теста или шаблона 
'''


class GetTemplate(object):
    # параметры инициализации класса
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.dir = ''
        self.delivey = False
        self.product = False
        self.menu = False
        self.home = False
        self._error = False

    def get_error(self):
        return self._error

    # Фукцция закрытия браузера и вебдрайвера
    def close_driver(self):

        self.driver.close()
        self.driver.quit()

    # получение шаблона
    def get_template(self, message, url, class_list):
        self.chrome_options.headless = True
        # Хром в режим инкогнито
        self.chrome_options.add_argument("--incognito")
        # Одинаковые действия в зависимости от ОС. Инициализация ВебДрайвера
        if platform.uname().system in ('Linux', 'Darwin'):

            self.driver = webdriver.Chrome('/usr/bin/chromedriver', options=self.chrome_options)
        else:
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.chrome_options)
        # Открытие и загрузка страницы
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(10)

        except:
            self._error = True
            return
        # Прокрутка \\скролл\\ страницы
        S = lambda X: self.driver.execute_script('return document.body.parentNode.scroll' + X)
        # Если это тест для меню каталога то высталяем определенное расширение окна браузера
        if self.menu:
            self.driver.set_window_size(('1920'), ('1080'))
        else:
            self.driver.set_window_size(('1920'), S('Height'))
        # Начинаем поиск неоходимых элементов на странце
        for element in class_list:
            j = 0

            image_path = Path(
                    os.getcwd() + slash + 'images' + slash +  str(message.chat.id) + slash +  self.dir + slash +  str(element))


            # Create images subdir inside project directory if not exists.
            if not image_path.parent.exists():
                    os.makedirs(os.getcwd() + slash +  'images' + slash +  str(message.chat.id) + slash +  self.dir)

            # для теста карточки товара дополнительно кликаем по ссылке что бы открылось описание товара,
            # а не отзывы(по умолчанию), Описание более статично и не вызывает ложных страбатываний
            if self.product == True:
                try:
                    odt = self.driver.find_element_by_class_name('xf-product-new-section-tabs__item')
                    odt.click()
                except:
                    self._error = True
                    self.close_driver()

                    return

            # Для теста меню каталога дополнительно кликаем по кнопке Каталог для раскрытия меню и ждем прогрузки 2 сек
            if self.menu == True:
                try:
                    odt = self.driver.find_element_by_class_name('xfnew-header__catalog-button')
                    odt.click()
                    time.sleep(2)
                except:
                    self._error = True
                    self.close_driver()

                    return
                # Для главной страницы.....
            if self.home == True:

                banner_list = len(self.driver.find_elements_by_class_name('xfnew-mp-banner-carousel__bullet'))
                for i in range(0, banner_list):
                    i += 1
                    odt = self.driver.find_element_by_xpath(
                        '//*[@id="main-app"]/div[5]/main/div/aside/div[2]/div/div[1]/div/div[1]/button[' + str(1) + ']')
                    odt.click()
                    self.driver.find_element_by_class_name(str(element)).screenshot(str(image_path) + str(i) + '.png')

                # Закрытие браузера и выход их драйвера
                self.close_driver()

                return
            # Для страницы доставки с помощью JS выставляем размер не статичных элементов на 0

            if self.delivey == True:
                try:
                    self.driver.execute_script(
                    """function getElementByXpath(path) {
      return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    }

    getElementByXpath("/html/body/div[2]/section[2]/div/div/div/div/p[3]/strong/iframe").height="0"; """)

                    self.driver.execute_script(
                        """function getElementByXpath(path) {
          return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        }
    
        getElementByXpath("/html/body/div[2]/section[2]/div/div/div/div/h2[2]").innerHTML = "";""")
                except:
                    None

            # Для каждого элемента имеющего размер делаем скриншот и сохраняем
            # try:
            if self.driver.find_elements_by_class_name(str(element)):
                for i in self.driver.find_elements_by_class_name(str(element)):
                        j += 1
                        if i.size['height'] and i.size['width']:
                            i.screenshot(str(image_path) + str(j) + '.png')
                            # Тут пытался закрыть ненужные элементы квадратами
                            # if self.delivey:
                            #     img = cv2.imread(str(image_path) + str(j) + '.png')
                            #     cv2.rectangle(img, (0, 520), (710, 1040), (0, 0, 0), -1)
                            #     cv2.imwrite(str(image_path) + str(j) + '.png', img)
            else:
                self._error = True
                self.close_driver()
                return

        # Закрытие браузера и выход их драйвера
        self.close_driver()


'''
class тестирования полученных изображений
'''


class TestPicture(object):

    def __init__(self):
        self.dir_template = 'template'
        self.dir_test = 'test'
        self.dir_result = 'result'
        # Размер до которого сжимается сравниваемое изображение (256 - это 256 на 256 пикселей)
        self.size = config.SIZE_PICTURE_TO_TEST
        self.dir = ''

    def calcimagehush(self, file):  # Получение хэш из изображения
        image = cv2.imread(file)  # Прочитаем картинку
        height, width = image.shape[:2]  # Сохраним исходный размер
        resized = cv2.resize(image, (self.size, self.size), interpolation=cv2.INTER_AREA)  # Уменьшим картинку
        gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)  # Переведем в черно-белый формат
        avg = gray_image.mean()  # Среднее значение пикселя где 0 белый, а 255 черный
        ret, threshold_image = cv2.threshold(gray_image, avg, 255,
                                             0)  # Бинаризация по порогу, то есть то что ниже среднего становиться 0, что выше 255

        # Рассчитаем хэш каждое значение становится 0 если меньше 255 и 1 если больше. последовательно
        # запи сываем каждое знаечение в переменную
        _hash = ""
        for x in range(self.size):
            for y in range(self.size):
                val = threshold_image[x, y]
                if val == 255:
                    _hash = _hash + "1"
                else:
                    _hash = _hash + "0"

        return _hash, width, height  # Возвращаем хэш и исхлжные значения изображения

    def comparehash(self, hash1,
                    hash2):  # Сравним хэш двух изображений. Те порядковые номера которые отличаются в хешах запишем в список и вернем его
        l = len(hash1)
        i = 0
        point = list()
        count = 0
        while i < l:
            if hash1[i] != hash2[i]:
                point.append(i)
                count = count + 1
            i = i + 1

        return point

    '''
    
    '''

    def resizepicture(self, point, width_hash_1, height_has_1, ):
        point_ccord = list()

        # В зависимости от размера до которого было сжато изображение (self.size)

        for i in point:  # для каждого найденого отличающегося пикселя
            if i <= self.size:  # определяем строчку в которой находился пиксель, если число меньше чем self.size:
                y = 1  # первая строка
                x = i  # i'тый столбец
            else:
                if (i % self.size) == 0:  # Если делится без остатка то
                    y = (i // self.size)  # Результат деления - строка
                    x = 1  # х всегда при этом равен 1

                else:  # Что тут происходит? Я не помню как это писал, но это работает
                    y = (i // self.size) + 1
                    x = i - (self.size * (i // self.size))
            # За основу размера берем первое из сравниваемых изображений
            y = int(height_has_1 * y / self.size)  # Находим координату y с небольшой погрешностью
            x = int(width_hash_1 * x / self.size)  # Находим координату x с небольшой погрешностью
            z = list()
            # Добавляем координату в список
            z.append(x)
            z.append(y)
            # добавляем список  координаты в список что бы хранить координаты всех
            # различных пикселей
            point_ccord.append(z)

            del x
            del y
        return point_ccord  # вовращаем список координат

    def open_picture(self, place, pic):  # Прочитаем картинку
        return cv2.imread(str(place) + str(pic))

    def hconcat_resize_min(self, im_list,
                           interpolation=cv2.INTER_CUBIC):  # Подогнать размер склеить изображения по горизонтали
        h_min = min(im.shape[0] for im in im_list)
        im_list_resize = [
            cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
            for im in im_list]
        return cv2.hconcat(im_list_resize)

    def vconcat_resize_min(self, im_list,
                           interpolation=cv2.INTER_CUBIC):  # Подогнать размер склеить изображения по вертикали
        w_min = min(im.shape[1] for im in im_list)
        im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                          for im in im_list]
        return cv2.vconcat(im_list_resize)

    def paint_picture(self, open_image_test, open_image_template, point_ccord, place,
                      pic):  # Получаем список координат и делаем в этих местах отметки
        # РАзница только в ОС
        open_image_test_first = copy.deepcopy(open_image_test)  # Делаем копию шаблона
        for i in range(0, len(point_ccord), 1):  # Перебираем координаты и рисуем небольшой кург на изображении
            cv2.circle(open_image_test, (point_ccord[i][0], point_ccord[i][1]), 15, (0, 0, 255), 1)

        cv2.imwrite(str(place) + slash +  pic, open_image_test)
        # Узнаем размер изображения что бы понять
        # склеивать по вертикали или горизонтаци. Все это для наглядности в результате который отпраляется пользователю
        height, width = open_image_test_first.shape[:2]

        im_list = [open_image_template, open_image_test_first,
                   open_image_test]  # три пикчи 1 шаблон, 2 оригинальная пикча теста, 3 пикча теста, но с отметками
        if height >= width:
            vis = self.hconcat_resize_min(im_list)
        else:
            vis = self.vconcat_resize_min(im_list)

        cv2.imwrite(str(place) + slash + pic, vis)  # сохраняем


    def test_picture(self, message):  # Функция последовательности действий при тесте
        # Получаем списки файлов и создаем папку результатов, если ее нет


        path = os.listdir(
            os.getcwd() + slash + 'images' + slash + str(message.chat.id) + slash + self.dir + slash + self.dir_template)

        self.dir_template = os.getcwd() + slash + 'images' + slash + str(
            message.chat.id) + slash + self.dir + slash + self.dir_template + slash

        self.dir_test = os.getcwd() + slash + 'images'+ slash + str(
            message.chat.id) + slash + self.dir + slash + self.dir_test + slash 

        self.dir_result = os.getcwd() + slash + 'images' + slash + str(
            message.chat.id) + slash + self.dir + slash + self.dir_result  + slash 
        if not os.path.exists(self.dir_result):
            os.makedirs(str(self.dir_result))

        crash_list = []  # наш будущий список имен файлов

        for pic in path:

            # Получение хэш из сравниваемых изображений
            hash1 = self.calcimagehush(self.dir_test + str(pic))
            hash2 = self.calcimagehush(self.dir_template + str(pic))

            # Сравним хэш двух изображений.
            # Те порядковые номера которые отличаются в хешах запишем в список и вернем его
            point = self.comparehash(hash1[0], hash2[0])

            if point:  # Если есть разница
                point_ccord = self.resizepicture(point, hash1[1], hash1[
                    2])  # В зависимости от размера до которого было сжато изображение (self.size) получаем координаты
                open_image_template = self.open_picture(self.dir_template, pic)  # открываем изображение шаблона

                open_image_test = self.open_picture(self.dir_test, pic)  # открываем изображение тестовое

                # Получаем список координат и делаем в этих местах отметки
                # склеиваем и сохраняем результаты
                self.paint_picture(open_image_test, open_image_template, point_ccord, self.dir_result, pic)

                crash_list.append(pic)
        return crash_list  # Список с именами файлов которые необходимо передать пользователю
