#!/bin/bash

curl -L -o ./downloads/myanimelist-dataset.zip\
  https://www.kaggle.com/api/v1/datasets/download/svanoo/myanimelist-dataset

unzip ./downloads/myanimelist-dataset.zip -d ./downloads/