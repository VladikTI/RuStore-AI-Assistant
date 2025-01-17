# -*- coding: utf-8 -*-
"""selectors

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HcGEmoBy0cNOpjERMX3TMlQCsB2As7TM
"""

import importlib
from parsel import Selector

def convert_html_to_selector(html):
    return Selector(html)

class RuStoreSelectorExtractor(object):

    @staticmethod
    def get_list_data(elements=None):
        data_cleaned = []
        data = elements.extract()
        for i, datum in enumerate(data):
            if datum:
                data_cleaned.append(datum.strip())
        return data_cleaned

    @staticmethod
    def get_single_data(elements=None):
        data = elements.extract_first()
        if data:
            return data.strip()
        return data

def transform_data(data=None, data_type=None):
    fields = importlib.import_module("rustore.fields")
    Klass = getattr(fields, data_type)
    data = Klass(data=data).transform()
    return data

def clean_data(elements=None, item_extractor=None):
    """
    This is where all the extracted data will be cleaned up and applied functions and data types as needed.

    :param elements:
    :param item_extractor:
    :return:
    """
    data_type = item_extractor.data_type
    multiple = data_type.startswith("List")

    data_extractor = RuStoreSelectorExtractor()
    if multiple:
        extracted_data = data_extractor.get_list_data(elements=elements)
    else:
        extracted_data = data_extractor.get_single_data(elements=elements)
    data = transform_data(data=extracted_data, data_type=data_type)
    return data

def extract_html_field(html_selector, item_extractor):
    element_query = item_extractor.element_query
    if item_extractor.data_attribute == 'text':
        if element_query.get("type") == 'css':
            elements = html_selector.css("{0}::{1}".format(element_query.get('value'), item_extractor.data_attribute))
            return clean_data(elements=elements, item_extractor=item_extractor)
        else:
            elements = html_selector.xpath("{0}/{1}".format(element_query.get('value'), item_extractor.data_attribute))
            return clean_data(elements=elements, item_extractor=item_extractor)
    elif item_extractor.data_attribute == 'html':
        if element_query.get('type') == 'css':
            elements = html_selector.css(element_query.get('value'))
            return clean_data(elements=elements, item_extractor=item_extractor)
        else:
            elements = html_selector.xpath("{0}/{1}".format(element_query.get('value'), item_extractor.data_attribute))
            return clean_data(elements=elements, item_extractor=item_extractor)
    else:
        if element_query.get('type') == 'css':
            elements = html_selector.css(element_query.get('value')).xpath("@{0}".format(item_extractor.data_attribute))
            return clean_data(elements=elements, item_extractor=item_extractor)
        else:
            elements = html_selector.xpath("{0}/{1}".format(element_query.get('value'), item_extractor.data_attribute))
            return clean_data(elements=elements, item_extractor=item_extractor)