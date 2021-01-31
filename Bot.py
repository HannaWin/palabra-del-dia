import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from lxml import etree
from gtts import gTTS

try:
    with open('api_token.txt', 'r') as  file:
        token = file.read().strip()
except FileNotFoundError:
    raise Exception("Please create the file 'api_token.txt' that contains your bot's api token.")
    
bot = telebot.TeleBot(token, parse_mode=None)

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.197 Safari/537.36'}


def fetch_wotd():
	'''get data from indicated url and id'''	
	page = requests.get('https://www.spanishdict.com/', headers=headers)
	soup = BeautifulSoup(page.content, 'html.parser')
	data = soup.find(id='word-of-the-day-source').get_text().strip()
	return data
	

def create_tree(url):
	'''
	create html tree of web page
	and save to file
	'''
	headers = {'Content-Type': 'text/html',}
	response = requests.get(url, headers=headers)
	html = response.text
	with open ('wotd_html', 'w') as f:
		f.write(html)
		
	# read local html file and set up lxml html parser
	local = 'file:///home/pi/projects/palabra-del-dia/wotd_html'
	response = urlopen(local)
	htmlparser = etree.HTMLParser()
	tree = etree.parse(response, htmlparser)
	return tree


@bot.message_handler(commands=['start'])
def send_welcome_message(message):
	bot.send_message(message.chat.id, 'Bienvenido!')
	

@bot.message_handler(commands=['palabra'])
def word_of_the_day(message):
	'''get wotd from spanishdict and send it to chat'''
	bot.send_message(message.chat.id, f'{wotd}')
	
	
@bot.message_handler(commands=['example'])
def send_source_url(message):
	'''send example sentence with english translation'''
	source_url = 'https://www.spanishdict.com/translate/' + wotd
	tree = create_tree(source_url)
	spanish_exp = tree.xpath('//*[@id="dictionary-neodict-es"]/div[1]/div[2]/div[2]/div/div[2]/div[1]/div/div/div[1]/span[1]/text()')[0]
	english_translation = tree.xpath('//*[@id="dictionary-neodict-es"]/div[1]/div[2]/div[2]/div/div[2]/div[1]/div/div/div[1]/span[3]/text()')[0]
	
	bot.send_message(message.chat.id, spanish_exp + '\n\n' + english_translation)
	

@bot.message_handler(commands=['translation'])
def send_translation(message):
	'''send translation of wotd'''
	source_url = 'https://www.spanishdict.com/translate/' + wotd
	tree = create_tree(source_url)
	translation = tree.xpath('//*[@id="quickdef1-es"]/a/text()')[0]
	
	bot.send_message(message.chat.id, translation)


@bot.message_handler(commands=['audio'])
def send_wotd_audio(message):
	'''use Google's TTS Api to create audio'''
	tts = gTTS(wotd, lang='es')
	tts.save('wotd.mp3')
	bot.send_audio(message.chat.id, open('wotd.mp3', 'rb'))
	

@bot.message_handler(commands=['source'])
def get_source_info(message):
	'''send og spanish dict link'''
	url = 'https://www.spanishdict.com/translate/' + wotd
	bot.send_message(message.chat.id, url)
	
	
def handle_messages(messages):
	for message in messages:
		print(message.chat.id)
		print(message.text)


if __name__=='__main__':
	# run bot
	wotd = fetch_wotd()

	bot.set_update_listener(handle_messages)
	bot.polling()
