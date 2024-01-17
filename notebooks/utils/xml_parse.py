import xml.etree.ElementTree as ET
import os
import pandas as pd
import re
import contractions
import wordsegment
# Initialize the wordsegment library
wordsegment.load()
from concurrent.futures import ThreadPoolExecutor
import concurrent

paragraph = []
class XmlParse():
    def __init__(self, nation, xml_path, csv_path, sentence_min_len) -> None:
        self.NATION = nation
        self.XML_PATH = xml_path
        self.CSV_PATH = csv_path
        self.sentence_min_len = sentence_min_len
        pass
    def _recur_element(self, element, paragraph):
        if element == None or element.text==None:
            for sub_child in element:
                self._recur_element(sub_child, paragraph)
            return paragraph
        if element.tag == 'P' and len(element.text.split()) > self.sentence_min_len:
            paragraph.append(element.text)
        for sub_child in element:
            self._recur_element(sub_child, paragraph)
        return paragraph
    
    def _postprocess(self, x: str):
        x = x.replace('\n', ' ')
        x = re.sub(r'\’', '\'', x)
        x = contractions.fix(x)
        x = re.sub(r'[^\x00-\x7F]', '', x)
        x = re.sub(r'[\x0C]', r"\n\n", x)
        x = re.sub(r'[!\"#$%&\'()*\+,-.\/:;<=>?@\[\\\]^_`{|}~]', '', x)
        x = x.replace('\t', ' ')
        x = x.strip()
        x = ' '.join(wordsegment.segment(x))
        if len(x.split()) < self.sentence_min_len:
            return None
        return x


    def parse_xml(self, file_list: list[str]):
        for file in file_list:
            try:
                file_name = file.strip('.pdf')
                paragraph = []
                tree = ET.parse(f'{self.XML_PATH}/{self.NATION}/{file_name}.xml')
                root = tree.getroot()
                paragraph = self._recur_element(root, paragraph)
                paragraph = map(self._postprocess, paragraph)
                paragraph = [x for x in paragraph if x is not None]
                paragraph = pd.DataFrame({'paragraph': paragraph})
                paragraph.to_csv(f'{self.CSV_PATH}/{self.NATION}/{file_name}.csv', sep=',', index=False, encoding='utf-8')
            except Exception as e:
                print(f"An error occurred while processing {file}: {e}")

def __main__():
    file_list = [ '4_esun_1_154.pdf', '10_compal_1_169.pdf',
    '21_cathay_1_52.pdf', '24_mega_1_68.pdf', '25_ctbc_1_117.pdf']
    with ThreadPoolExecutor(max_workers=8) as executor:
        for file in file_list:
            print(file)
            try:
                executor.submit(parse_xml, file)
            except Exception as e:
                print(f"An error occurred while processing {file}: {e}")
