from random import randint
import json
from faker import Faker


class ParseJson:
    """Класс, содержащий основную функцию parse_json, методы генерации данных и словарь, в который записывается
    статистика по найденным значениям """

    def __init__(self):
        """Инициализация атрибутов: данные, требуемые поля, требуемые значения"""
        self.info_dict = {}
        self.data = self.data_generation()
        self.required_fields = self.required_fields_generation(self.data)
        self.keywords = self.generate_keywords(self.data)

    @staticmethod
    def data_generation():
        """Генерация и вывод данных"""
        fake = Faker(locale="Ru_ru")
        doc = {
            'name': fake.name(),
            'address': fake.address(),
            'job': fake.job(),
            'country': fake.country(),
            'city': fake.city(),
            'company': fake.company(),
            'email': fake.email(),
            'company_email': fake.company_email(),
            'time': fake.time()
        }
        print("Data:")
        for key, val in doc.items():
            print(f"{key}:{val}")
        json_doc = json.dumps(doc)
        return json_doc

    @staticmethod
    def required_fields_generation(data, quantity=3):
        """Выбор трех полей (по умолчанию) из JSON объекта случайным образом"""
        data_ = json.loads(data)
        fields = []
        data_list = list(data_.keys())
        for i in range(quantity + 1):
            flag = 0
            while not flag:
                item = data_list[randint(0, len(data_list) - 1)]
                if item not in fields:
                    flag = 1
                    fields.append(item)
        return fields

    @staticmethod
    def generate_keywords(data, quantity=3):
        """Разбиение 3 случайных значений (по умолчанию) JSON объекта, выбор случайных подзначений"""
        data_ = json.loads(data)
        keywords = []
        data__ = list(data_.values())
        for i in range(quantity + 1):
            item = data__[randint(0, len(data__) - 1)]
            if isinstance(item, str):
                after_split = item.split(sep=' ')
                split_item = after_split[randint(0, len(after_split) - 1)]
                if split_item not in keywords:
                    keywords.append(split_item)
        return keywords

    def parse_json(self, json_str: str, required_fields=None, keywords=None, keyword_callback=None):
        """Сопоставление требуемых полей и значений JSON объекта, их обработка"""
        if not isinstance(json_str, str):
            json_str = str(json_str)
        json_doc = json.loads(json_str)
        print(f"Требуемые поля: {required_fields}")
        print(f"Требуемые значения: {keywords}")
        for key, value in json_doc.items():
            if key in required_fields:
                if isinstance(value, str):
                    for item in value.split(sep=' '):
                        if item in keywords:
                            keyword_callback(item)
        for key, value in self.info_dict.items():
            print(f"'{key}' получен {value} раз(а)")

    def keyword_func(self, item=None):
        """Обработка требуемых значений, содержащихся в требуемых полях"""
        if item not in self.info_dict:
            self.info_dict[item] = 1
            return
        self.info_dict[item] += 1

    def __call__(self):
        self.parse_json(self.data, self.required_fields, self.keywords, self.keyword_func)
        
