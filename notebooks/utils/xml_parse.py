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

def recur_element(element, paragraph):
    # print(element.tag, element.text)
    # if element.tag == 'H1' or element.tag == 'H2' or element.tag == 'H3' or element.tag == 'TOCI':
    #     paragraph.append(element.text)
    try:
        if element == None or element.text==None:
            for sub_child in element:
                recur_element(sub_child, paragraph)
            return paragraph
        if element.tag == 'P' and len(element.text.split()) > 5:
            paragraph.append(element.text)
        elif element.tag == 'L':
            text = ''
            for list_element in element:
                x = recur_element(list_element, paragraph)
                text = text if(x == None) else text + x
            paragraph.append(text)
        elif element.tag == 'LI':
            return element.text
        for sub_child in element:
            recur_element(sub_child, paragraph)
    except Exception as e:
        print(f"An error occurred while recur_element {file}: {e}")
    return paragraph
    
def preprocess(x):
    x = x.replace('\n', ' ')
    x = re.sub(r'\’', '\'', x)
    x = contractions.fix(x)
    x = re.sub(r'[^\x00-\x7F]', '', x)
    x = re.sub(r'[\x0C]', r"\n\n", x)
    x = re.sub(r'[!\"#$%&\'()*\+,-.\/:;<=>?@\[\\\]^_`{|}~]', '', x)
    x = x.replace('\t', ' ')
    x = x.strip()
    x = ' '.join(wordsegment.segment(x))
    if len(x.split()) < 10:
        return None
    return x


def parse_xml(file: str):
    try:
        file_name = file.strip('.pdf')
        paragraph = []
        tree = ET.parse(f'../taiwanxml/{file_name}.xml')
        root = tree.getroot()
        paragraph = recur_element(root, paragraph)
        paragraph = map(preprocess, paragraph)
        paragraph = [x for x in paragraph if x is not None]
        paragraph = pd.DataFrame({'paragraph': paragraph})
        paragraph.to_csv(f'../csv/taiwan_xml/{file_name}.csv', sep=',', index=False, encoding='utf-8')
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
