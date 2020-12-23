#!/bin/python3 

import requests
import json
from sense_hat import SenseHat
from random import randint
from time import sleep

def animation(sense, color = (randint(0, 255), randint(0, 255), randint(0, 255))): 
    for i in range(8):
        for j in range(8):
            sense.set_pixel(i, j, color)
            sleep(0.005)

def load_apikey(apikey_file):
    apikey = None
    with open(apikey_file) as f:
        apikey = f.read().strip()
    return apikey

def get_location(url):
    res = requests.get(url)
    return res.text.strip()

def add_field(res, field, end = 0):
    addition = f"{field}" if end else f"{field},"
    res += addition
    return res

def get_weather(url, sense):
    res_raw = requests.get(url)
    res = json.loads(res_raw.text)
    res_str = ""
    res_str = add_field(res_str, str(res["dt"]))
    res_str = add_field(res_str, res["name"])
    res_str = add_field(res_str, res["sys"]["country"])
    res_str = add_field(res_str, res["coord"]["lon"])
    res_str = add_field(res_str, res["coord"]["lat"])
    res_str = add_field(res_str, res["weather"][0]["main"])
    res_str = add_field(res_str, res["weather"][0]["description"])
    res_str = add_field(res_str, res["weather"][0]["icon"])
    res_str = add_field(res_str, res["sys"]["sunrise"])
    res_str = add_field(res_str, res["sys"]["sunset"])
    res_str = add_field(res_str, res["clouds"]["all"])
    res_str = add_field(res_str, res["wind"]["speed"])
    res_str = add_field(res_str, res["wind"]["deg"])
    res_str = add_field(res_str, res["visibility"])
    res_str = add_field(res_str, res["main"]["temp_min"])
    res_str = add_field(res_str, res["main"]["temp_max"])
    res_str = add_field(res_str, res["main"]["temp"])
    res_str = add_field(res_str, res["main"]["feels_like"])
    res_str = add_field(res_str, res["main"]["humidity"])
    res_str = add_field(res_str, res["main"]["pressure"])
    res_str = add_field(res_str, str(sense.get_temperature()))
    res_str = add_field(res_str, str(sense.get_pressure()))
    res_str = add_field(res_str, str(sense.get_humidity()))
    print(res_str)

if __name__ == '__main__':
    sense = SenseHat()

    animation(sense)
    location = get_location('http://ip-api.com/line/?fields=city')
    apikey = load_apikey("apikey")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={apikey}"
    get_weather(url, sense)

    sense.clear(0, 255, 0)
    animation(sense, (0, 0, 0))
