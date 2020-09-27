# 
# Begins web crawler process and saves data into csv file
# 
# loads data and indexes it for later use in search engine
#

import os
import math
import json
import pickle
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from django_pandas.io import read_frame
from django.apps import AppConfig

class indexConfig(AppConfig):
    name = 'searchApp'

    #loads and formats dataset
    def load_dataset(self):
        #importing from inside the function b/c I don't know why but it works
        from searchApp.models import productItem
        
        productModels = productItem.objects.all()
        dataframe = read_frame(productModels)
        return dataframe

    def index_data(self, dataframe):
        stop_words = set(stopwords.words('english')) 

        tf_data = {}        #term frequency (freq of term from doc)
        df_data = {}        #document frequency (freq of term from all docs)
        idf_data = {}       #inverse dense frequency (value you get from calculating DF)


        #iterates through the dataframe and counts tf for each product
        for indx in dataframe.index:
            tf = {}
            data = dataframe['product_name'][indx]
            word_list = word_tokenize(data)

            for word in word_list:
                if word in stop_words:
                    continue
                
                #calculates term freq for the word
                if word in tf:
                    tf[word] += 1
                else:
                    tf[word] = 1

                #calculates the doc freq of the word
                if word in df_data :
                    df_data[word] += 1
                else :
                    df_data[word] = 1

            tf_data[dataframe['product_url'][indx]] = tf

        #calculate idf
        for x in df_data:
            idf_data[x] = 1 + math.log10(len(tf_data)/df_data[x])

        tf_idf = {}

        for word in df_data:
            list_doc = []

            for indx in dataframe.index:
                tf_value = 0

                if word in tf_data[dataframe['product_url'][indx]]:
                    tf_value = tf_data[dataframe['product_url'][indx]][word]

                weight = tf_value * idf_data[word]
                doc = {
                    "product_url": dataframe['product_url'][indx],
                    "product_name": dataframe['product_name'][indx],
                    "image_url": dataframe['image_url'][indx],
                    "shop_name": dataframe['shop_name'][indx],
                    "price": dataframe['price'][indx],
                    "score": weight
                }

                if doc['score'] != 0:
                    if doc not in list_doc:
                        list_doc.append(doc)

            tf_idf[word] = list_doc

        return tf_idf

    # store tf_idf into the django database
    def dict_to_model(self, tf_idf):
        from searchApp.models import tfData

        #empties table if alrdy exists
        tfData.objects.all().delete()
        for key, value in tf_idf.items():
            data = tfData.create(key, json.dumps(value))
            data.save()

    # where start up code goes
    def ready(self):
        tf_idf = self.index_data(self.load_dataset())
        self.dict_to_model(tf_idf)
        pass
