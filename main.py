from bs4 import BeautifulSoup, Tag 
import requests
from telebot import TeleBot 
from telebot import types as t
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import lxml
from typing import List 
import json
import webbrowser

token = '6576256434:AAG-5uoSuEDh1t4vlo63bVMGL5Gy6Q1C_4s' 
bot = TeleBot(token)

url = 'https://kaktus.media/?lable=8'

def get_html(url: str) -> str:
    response = requests.get(url)
    return response.text 

def get_soup(html:str) -> BeautifulSoup:
    soup = BeautifulSoup(html, 'lxml')
    return soup


def get_news_from_soup(soup: BeautifulSoup) -> List[Tag]:
    all_news = soup.find_all('div', {'class': 'ArticleItem'})
    return all_news


def get_data_from_news(all_news: List[Tag]) -> dict:
    data = []
    for news in all_news:
        info = {
            'title': news.find('a', {'class': 'ArticleItem--name'}).text,
            'img': news.find('img').get('src'),
            'description': news.find('a',{'class':'ArticleItem--image'}).get('href')
        }
        data.append(info)
    return(data)




html = get_html(url)
soup = get_soup(html)
all_news = get_news_from_soup(soup)
data = get_data_from_news(all_news)

   

@bot.message_handler(['site', 'website'])
def site(message):
    webbrowser.open('https://kaktus.media/?lable=8')


@bot.message_handler(['start'])
def start_message(message: t.Message):
    keyboard = t.ReplyKeyboardMarkup(resize_keyboard=True)
    button_get_news = t.KeyboardButton('get_news')
    button_say_bye = t.KeyboardButton('Goodbye')
    keyboard.add(button_get_news, button_say_bye)


@bot.message_handler(func=lambda message: message.text == 'buttons')
def get_buttons(message: Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('photo')
    button2 = KeyboardButton('description')
    keyboard.add(button1, button2)

    bot.send_message(message.chat.id, reply_markup=keyboard)


def description_from_data(news_data: dict) -> str:
    news_dsc = f"Описание: {news_data['description']}\n"
    return news_dsc


def img_from_data(news_data: dict) -> str:
    news_img = f"Изображение: {news_data['image']}\n"
    return news_img


bot.infinity_polling()


