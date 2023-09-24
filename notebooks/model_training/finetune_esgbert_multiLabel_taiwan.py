#!/usr/bin/env python
# coding: utf-8

# ## import package

# In[1]:


import torch
import torch.nn as nn
from torch.utils.data.dataset import Dataset
from torch.utils.data import DataLoader
import torch.nn.functional as F
from torch.nn import CrossEntropyLoss
import math
import numpy as np
import time
import torch
import pandas as pd
import re
import os
import random
from sklearn.model_selection import train_test_split
from transformers import set_seed
from imblearn.over_sampling import SMOTE
from sklearn.datasets import make_classification
from sklearn.neighbors import NearestNeighbors
set_seed(777)
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)


# In[2]:


READ_DIRECTORY = '../../data/CSV25Company/multi_label/source_50_3label.csv'


# ## Data process

# In[12]:


df = pd.read_csv(READ_DIRECTORY, dtype={'label': object})


# In[13]:


import ast
df['label'] = df['label'].apply(ast.literal_eval)


# In[6]:


def convert_onehot(row):
    y = []
    for i in range(27):
        if i in row:
            y.append(1)
        else:
            y.append(0)
    return y


# In[7]:


df['label'] = df['label'].apply(convert_onehot)


# In[9]:


x = df['paragraph']
y = df['label']


# ## Tokenizer

# In[ ]:


from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('nbroad/ESG-BERT')


# In[ ]:


train_encodings = tokenizer(x.to_list(), truncation=True, padding=True)


# ## Dataset

# In[ ]:


class qrDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, y):
        self.encodings = encodings
        self.y = y
    def __getitem__(self, idx):
        input_ids =  {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        label = torch.tensor(self.y[idx])
        return input_ids, label

    def __len__(self):
        return len(self.encodings.input_ids)


# In[ ]:


x_dataset = qrDataset(train_encodings, y)


# In[ ]:


train, test= train_test_split(x_dataset, test_size=0.2, random_state=45)
valid, test= train_test_split(test, test_size=0.5, random_state=42)


# ## Model

# In[ ]:


from transformers import AutoModelForSequenceClassification
from torch.nn import LogSoftmax
class myModel(torch.nn.Module):

    def __init__(self):

        super(myModel, self).__init__()

        self.bert = AutoModelForSequenceClassification.from_pretrained('nbroad/ESG-BERT')
        self.fc = nn.Linear(26, 27)

    def forward(self, input_ids, attention_mask):

        output = self.bert(input_ids=input_ids, attention_mask=attention_mask, return_dict=True)
        logits = output[0]
        out = self.fc(logits)
        return out


# In[ ]:


from transformers import AdamW
from tqdm import tqdm

# Set GPU / CPU
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
# Put model on device
model = myModel().to(device)

optim = AdamW(model.parameters(), lr=1e-5)


# ## Training

# In[ ]:


# Pack data into dataloader by batch
batch_size = 8
train_loader = DataLoader(train, batch_size=batch_size, shuffle=True)


# In[ ]:


training_epoch = 2


# In[ ]:


class_weight = torch.FloatTensor([1.36779, 2.48801, 2.98224, 2.17655, 8.49189, 3.29992, 4.87132, 5.50538, 0.86167, 2.54855, 1.68795, 1.92845, 1.66811, 1.82674, 6.92724, 4.61574, 38.92743, 1.24085, 5.62506, 3.98803, 4.34664, 36.65667, 12.05151, 3.57045, 2.16476, 1.96463, 4.14590]
                                ).to(device)
loss_fct = nn.BCELoss(weight=class_weight)
criterion = nn.Sigmoid()


# In[ ]:


for epoch in range(training_epoch):
    model.train()
    running_loss = 0.0

    loop = tqdm(train_loader, leave=True)
    for batch_id, batch in enumerate(loop):
        # reset
        optim.zero_grad()
        inputs, y = batch

        input_ids = inputs['input_ids'].to(device)
        attention_mask = inputs['attention_mask'].to(device)
        y = y.to(device)

        # model output
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        outputs = criterion(outputs)
        loss = loss_fct(outputs, y.float())

        # calculate loss
        loss.backward()
        # update parameters
        optim.step()

        running_loss += loss.item()
        if batch_id % 50 == 0 and batch_id != 0:
            print(f'Epoch {epoch} Batch {batch_id} Loss {running_loss / 50:.4f}')
            running_loss = 0.0

        loop.set_description(f'Epoch {epoch}')
        loop.set_postfix(loss=loss.item())


# In[ ]:


torch.save(model.state_dict(), '../../model/' + '50_Multi_lr1e-5')
