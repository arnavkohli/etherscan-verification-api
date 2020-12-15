# from bs4 import BeautifulSoup as bs
# import requests
from flask import Flask, request
import json, os

from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
import time
from datetime import datetime

app = Flask(__name__)

VALID_API_TOKENS = [
	'yaAgVgF06EH1v5ea'
]

def get_data_from_etherscan(txn_hash):
	try:
		#PATH_TO_DRIVER = './drivers/chromedriver'
		#PATH_TO_DRIVER = os.environ.get('CHROMEDRIVER_PATH')
		PATH_TO_DRIVER = os.environ.get('GECKODRIVER_PATH')

		url = f"https://etherscan.io/tx/{txn_hash}"
		options = Options()
		options.headless = True
		# options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
		options.binary_location = os.environ.get("FIREFOX_BIN")

		options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
		options.add_argument('accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
		options.add_argument('accept-encoding=gzip, deflate, br')
		options.add_argument('accept-language=en-US,en;q=0.9')
		options.add_argument('--lang=en_US') 
		options.add_argument('--disable-dev-shm-usage')
		options.add_argument('--no-sandbox')
		#driver = webdriver.Chrome(PATH_TO_DRIVER, options=options)
		driver = webdriver.Firefox(PATH_TO_DRIVER, options=options)
		driver.get(url)

		time.sleep(2)

		amount_val = driver.find_element_by_id('ContentPlaceHolder1_spanValue').text
		hash_val = driver.find_element_by_id('spanTxHash').text
		success_or_not = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[2]/div[2]/span').text
		clock = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[4]/div[2]').text
		to_address = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[7]/div[2]/ul/li/div/span[4]/a/span').text
		from_address = driver.find_element_by_id('addressCopy').text

		# print ('amount', amount_val)
		# print ('hash_val', hash_val)
		# print ('success_or_not', success_or_not)
		# print ('to_address', to_address)
		# print ('from_address', from_address)
		# print ('min', minute_diff)

		amount_val = float(amount_val.split('$')[-1].split(')')[0])

		'''
			Nov-25-2020 07:25:00 PM +UTC
		'''
		clock = clock.split('(')[-1].split(')')[0]
		clock = datetime.strptime(clock, "%b-%d-%Y %I:%M:%S %p +%Z")
		now = datetime.utcnow()
		minute_diff = (now - clock).total_seconds() / 60

		return {
			"data_retrieved" : True,
			"amount" : amount_val,
			"txn_hash" : hash_val,
			"success" : True if (success_or_not == 'Success') else False,
			"to_address" : to_address,
			"from_address" : from_address,
			"minutes_passed" : minute_diff
		}
	except Exception as err:
		return {
			"data_retrieved" : False,
			"msg" : str(err)
		}


@app.route('/check', methods=['POST'])
def check():
	try:
		data = request_data = request.get_json()
		api_token = data.get('api_token')
		amount = data.get('amount')
		txn_hash = data.get('txn_hash')
		to_address = data.get('to_address')

		if api_token not in VALID_API_TOKENS:
			return json.dumps({'success':False, 'error':'Invalid API token'}), 400, {'ContentType':'application/json'}

		etherscan_data = get_data_from_etherscan(txn_hash)
		if not etherscan_data.get('data_retrieved'):
			return json.dumps({'success':False, 'error':etherscan_data.get('msg')}), 400, {'ContentType':'application/json'}

		if (etherscan_data.get('amount') != amount) or (not etherscan_data.get('success')) or (etherscan_data.get('minutes_passed') > 15) or (etherscan_data.get('to_address') != to_address):
			return json.dumps({'success':False, 'error':'Invalid request.'}), 400, {'ContentType':'application/json'}

		return json.dumps({'success':True, 'from_address' : etherscan_data.get('from_address')}), 200, {'ContentType':'application/json'}
	except Exception as err:
		return json.dumps({'success':False, 'error':str(e)}), 400, {'ContentType':'application/json'}

if __name__ == '__main__':
	app.run(port=8000)

# # headers = {
# # 	'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
# # 	'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
# # 	'accept-encoding' : 'gzip, deflate, br',
# # 	'accept-language' : 'en-US,en;q=0.9'
# # }



