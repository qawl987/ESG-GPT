# WorkFlow

1. Get PDF
   - Download online
2. Transform PDF to XML
   - use FoxitPDF convert to XML
3. parse XML to csv
   - run notebooks/data_processing/xml_parse.ipynb
4. Inference or Finetune
   1. Inference (use esgbert directly)
      - Run notebooks/model_training/esgbert_inference.ipynb
   2. Finetune & Inference (use gpt-3.5 finetune and inference)
      - Run notebooks/data_processing/openai.ipynb
      - Run notebooks/data_processing/multi_gpt_label_clean.ipynb
      - Run notebooks/model_training/esgbert_finetune.ipynb
5. Visualization (Radar chart)
   - Run notebooks/visualization/main_radar.ipynb

# How to run each file

### Get PDF and Transform PDF to XML not discuss here

### 3. Parse XML to csv

1. Change hyper parameter here

```
# american or taiwan
NATION = 'american'
# xml source path
XML_PATH = '../../data/xml'
# csv source path
CSV_PATH = '../../data/csv_source/'
# min sentence length below will be ignore (to maintain the quality of sentence)
MIN_SENTENCE_LEN = 10
```

2. Run the cell

```
xml_parse = XmlParse(NATION, XML_PATH, CSV_PATH, )
xml_parse.parse_xml(file_list)
```

### 4-1. ESGBert Inference

1. Open notebooks/model_training/esgbert_inference.ipynb
2.

```
# csv path after xml_parse
CSV_SOURCE = '../../data/csv_source'
# csv path inference output
CSV_OUTPUT = '../../data/csv_output'
# american or taiwan you want to put, or can keep empty
NATION = ''
# the csv file you want to inference
FILE = '4_apple_1_72'
```

3. Run the cell

```
esgbert = EsgBertPredict(CSV_SOURCE, CSV_OUTPUT, NATION, FILE, HYPER_PARAMETERS)
esgbert.main()
```

### 4-2. Finetune & Inference (use gpt-3.5 finetune and inference)

#### 4-2-a. GPT-3.5 mark label

1. copy notebooks/data_processing/.env.example to notebooks/data_processing/.env
2. paste your openai_api_key in .env
   `OPENAI_API_KEY=Your openai key`
3.

```
# american or taiwan
NATION = 'american'
# csv source path
CSV_SOURCE_PATH = '../../data/csv_source'
# csv output path
CSV_OUTPUT_PATH = '../../data/csv_gpt_label'
# max token length (because we desire only output number label like [3, 4, 5] so 10 token is enough, and can save your money if accident happen)
MAX_TOKENS = 10
```

4. Run the cell

```
openai_label = OpenAILabel(file_list, NATION, CSV_SOURCE_PATH, CSV_OUTPUT_PATH, MAX_TOKENS)
openai_label.loop_folder()
```

#### 4-2-b. clean gpt label and concate to one csv

1.

```
NATION = 'american'
# the csv after gpt label
SOURCE_PATH = '../../data/csv_gpt_label/'
# where you want to output the clean and concate csv
OUTPUT_PATH = '../../data/csv_gpt_label/'
```

2. Run the cell

```
clean_multi_gpt_label = CleanMutliGptLabel(file_list, NATION, SOURCE_PATH, OUTPUT_PATH)
clean_multi_gpt_label.loop_folder()
```

#### 4-2-c. ESG-GPT multi-label finetune

1. Open notebooks/model_training/esgbert_finetune.ipynb
2. Change hyper parameter here

```
HYPER_PARAMETERS = {
    'batch_size': 8,
    'lr': 1e-5,
    'epoch': 1,
    # multilabel output threshold
    'threshold': 0.02
}
```

3. change directory as you want

```
# csv path after gpt mark label
TRAIN_CSV_PATH = '../../data/csv_gpt_label'
# csv path you want to predict
TEST_CSV_PATH = '../../data/csv_source'
# csv path after finetune esgbert predict
TEST_CSV_OUTPUT_PATH = '../../data/csv_output'
# american or taiwan or ''
NATION = 'american'
# train csv file name
TRAIN_SOURCE = 'gpt_small'
# test csv file name
TEST_SOURCE = '4_apple_small'
#
TEST_OUTPUT = 'finetune_output'
```

4. Run the cell

```
esgbert = EsgBertPredict(TRAIN_CSV_PATH, TEST_CSV_PATH, TEST_CSV_OUTPUT_PATH, NATION, TRAIN_SOURCE, TEST_SOURCE, TEST_OUTPUT, HYPER_PARAMETERS)
esgbert.main()
```

### 5. Visualization (Radar chart)

1. Open notebooks/visualization/main_radar.ipynb
2.

```
# csv path contain american and taiwan csv
CSV_PATH = f'../../data/csv_output'
# output png folder
PNG_PATH = f'../../data/png'
# which nation you are drawed
NATION = 'american'
draw = MultiRadar(NATION, PNG_PATH, CSV_PATH, label_cnt=27)
```

3. Choose which you want to draw

- draw_average(csv_path): draw the average radar chart for the csv folder
- draw_full25(csv_path): draw all the company radar chart int the csv folder
- draw_company_average(csv_path): draw all company vs average in the csv folder
- taiwan_vs_american(): draw taiwan average vs american average

```
#   choose picture to draw
draw.draw_average(draw.AMERICAN_CSV_PATH)
# draw.draw_full25(draw.AMERICAN_CSV_PATH)
# draw.draw_company_average(draw.AMERICAN_CSV_PATH)
# draw.taiwan_vs_american()
```
