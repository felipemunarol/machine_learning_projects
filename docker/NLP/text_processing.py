# %%
# pip install tensorflow

# %%
# Libraries

print("ok")
import os
# import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
import json

# %% [markdown]
# Quando falamos de aprendizado Processamento de Linguagem Natual (NLP) diversos tratamentos devem ser feitos para facilitar o entendimento do texto
# para um modelo de Machine Learning. Um desses tratamentos por exemplo é o Tokenalization, em que realizamos o encoding da Frase. Dessa forma, por exemplo:
# 
# a frase,
# 
# I love my dog -> pode ser processada como [001, 002, 003, 004]
# 
# e a frase,
# 
# I love my cat -> pode ser processada como [001, 002, 003, 005]
# 
# Notem, que essas duas sequencias são muito parecidas, retirando a ultima palavra no final da frase. Dado esse método de realizar o ecoding de frases em numeros,
# vamos ver alguns codigos que podem atingir esse objetivo para nos.
# 
# Este é um exemplo bem simples de um tratamento anterior ao modelo. Vamos tentar realizar um codigo que realize esse tratamento e fazer o deploy via docker.

# %%
phrases = ["I love my dog", "I love my cat", "You love my dog"]

# %%
tokenizer = Tokenizer(num_words=100)

tokenizer.fit_on_texts(phrases)

word_index = tokenizer.word_index

# %%
path = "/home/felipe/machine_learning_projects/docker/NLP/test.json"

with open(path, "w") as f:
    json.dump(word_index, f)

print("ok")
# %%
# os.remove(path)

# %%



