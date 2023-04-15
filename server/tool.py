# -*- coding: utf-8 -*-
# @Description :
# @File : tool.py
# @Time : 2023/3/13 0:54
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


# from server.models import User
import os
import openai
from server.settings import OPENAI_API_KEY
import numpy as np

# def create_temperatures(n):
#     temperatures = np.random.uniform(low=14.0, high=20.0, size=n)
#     return temperatures


openai.api_key = OPENAI_API_KEY
# print("------key------")
# print(openai.api_key)
# print("------model list------")
# print(openai.Model.list())


# print("------情感分析------")
# prompt = "Decide whether a Mike's sentiment is positive, neutral, or negative: Mike: I don't like homework!"
# print("prompt: ", prompt)
# response = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=100, temperature=0)
# result = response.choices[0]['text'].strip()
# print(result)


# print("------代码生成-----------")
# response = openai.Completion.create(
#   model="code-davinci-002",
#   prompt="\"\"\"\nCreate an array of weather temperatures for Shanghai\n\"\"\"",
#   temperature=0,
#   max_tokens=256,
#   top_p=1,
#   frequency_penalty=0,
#   presence_penalty=0
# )
# print(response)


# print("------图像生成-------")
# # prompt = "Beautiful sunset by the West Lake, I want the image is in Monet's style"
# # prompt = "Image of Trump was taken by someone"
# prompt = "Create an image: A romantic scene for my girlfriend, including light bubble roses, sunset by the West Lake."
# response = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
# print("prompt: ", prompt)
# image_url = response['data'][0]['url']
# print(image_url)


# response = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo-0301",
#   prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: I'd like to cancel my subscription.\nAI:",
#   temperature=0.9,
#   max_tokens=150,
#   top_p=1,
#   frequency_penalty=0.0,
#   presence_penalty=0.6,
#   stop=[" Human:", " AI:"]
# )
# print(response)

