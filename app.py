from flask import Flask, request
import json, os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
from datetime import datetime

app = Flask(__name__)

VALID_API_TOKENS = ['0doklcvjc6zMbcfS', 'NmSpjmpPPC1wFaKd', 'F2glZF0l1u5agAmC', '8qJIwvbs0Byb6i4R', 'l7ZIzRq88MYKHBpX', '1GzDyvlizJ4KaNPC', 'qLqUEZ8rzINkPvIA', '6hp6vefe24tWwzuu', 'Krm98XwcO3MHdiTy', 'RvGGfJbt9MXAxHCE', 'BBOafRowNQGNUnEt', 'AmjTWcfwnTlNh8dt', 'S0Bi3oypuqhrcjcd', 'ESpsOxeTosPCjTkH', 'JdDZd7yFpdUe3K5x', 'MarOUCZ2Y7DdEzuD', 'Fhbulp31aUxlQqfD', 'BYDIaOfiLcrh29g0', 'ye4wWE80f7bUtpvS', 'aL7Cy0UpQLZKdhV3', '6t5j6tqNoOoUFNtR', 'Q0uQlJpbcnWOwmmz', 'qZwMk92KLZeaIJsD', '7av0CvK45S5RFVzV', 'PCnTGsQ0PahgtlCq', 'Nbh2mAJ2sT32dZ62', 'ULIt91fdOPVXoopM', 'X69QuwMiBU3RIZyX', 'KjJXz6M2yv6uzXSS', 'LPBt52SQpObLydMj', '6TaxCwtwZFO1PRoD', '7l5bbyHC2K52lWHq', 'm25UREwzjXYImV9c', 'FPOOfCytf2RMPeFj', 'KYU80EfxO62Nwozj', 'WDecj3cw0WikGdMR', 'FLivOYpsEHX5zm2a', '2d6lRbVoQgUkz66r', 'ukuInD2pAathCv2m', 'WZZmMtxGYOTjADpf', 'NK7WZazVHocmR0f9', 'FUquKZeL8QQpPyuN', 'su39EuB5W50eERQi', 'iwmoKww79U6q6HGT', 'vGeU98ae1puwDeSi', 'ESYQ0gRB7H4XobeG', 'plhJQYvrJ9UYGpCF', 'rvf0AXdfSTG8ZBWH', '68q2V8av8pGZg0xc', '8nABHw0Fc1RkW8yI', 'a7ZadJlaHarXLU0i', '8RgK5K3IPmhCk01H', 'co8INrg6IgXJOKqp', 'B69EL1jGUH56xbPA', 'mh1Zz8lIJcqF1V5i', 'RrsxVlR6dd3wt4zv', 'MNgAcb5DvcXXiLgz', 'zZndkMeKN3gCS5DB', 'Tc07wy34kPoGU4uU', 'cNF1zador2K5CdU5', 'qsZ97c8NQNX6bwzK', '8pIW2TrLuxKocpil', 'Rn2rTMwAkb9VzAe7', 'lxQdvGGEFi3bqe27', 'WOnJOAjsq9JgkSpo', 'OPTYmdmX81ZWCvcM', '3K44EnsgG25ypCzL', 'uvvLeTr7ac8J10Qw', 'r5nt1qbvervwB1C0', 'U556kjY1PRItB4pb', 'p2pKUU1LzLlEL0fz', 'M3DvSXc4G5AaEqdF', 'Pu4oR5gMzcujr3LY', '01QLWIcAIGavmh7t', 'PgeXdEXNNB1S5dqg', 'qsad8d013SSDHxTj', 'xi6NAIiufFGbVWFN', 'E0VQv5CUtYo1lIYP', 'jTKo6Zq6EXqwPW8N', 'ZwV435Zs6wP2b2da', 'zHK4aj1mgOeSFERL', 'WkWBp2s0uUdg5mZV', 'Org5rOp6znjeIEmw', 'v9ResWwixbISXBmR', 'Y6RZ2kJKW8RYESTW', 'WPq4oSCp2rGJ1IyN', 'wctU5HE3Ez8k05Kq', 'uutLWw4YbljmoIq7', 'dpAX2AP5LTVvsJte', 'ivPOmdl5sdbDFEOw', 'VGlNsMjC6BFIRNwp', 'jC86IVQhoJDtrGje', 'SxRXJZXV7DI8ae7m', 'FQsw5ClpxGlJDIff', 'JbcunTAD2eGO0UeA', 'li0SF601hlnDTl4I', 'VueiGZsOXcSGzZLm', 'LHL5O26lDHiFZdBC', 'JhhpSmn7iz9k8IJC', 'OSJjtd15ZsUWb7fs']

def get_data_from_etherscan(txn_hash):
	try:
		PATH_TO_DRIVER = os.environ.get('CHROMEDRIVER_PATH') # Replace with ChromeDriver Path

		url = f"https://etherscan.io/tx/{txn_hash}"
		options = Options()
		options.headless = True
		#options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

		options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
		options.add_argument('accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
		options.add_argument('accept-encoding=gzip, deflate, br')
		options.add_argument('accept-language=en-US,en;q=0.9')
		options.add_argument('--lang=en_US') 
		options.add_argument('--disable-dev-shm-usage')
		options.add_argument('--no-sandbox')
		driver = webdriver.Chrome(PATH_TO_DRIVER, options=options)
		driver.get(url)

		time.sleep(2)

		amount_val = driver.find_element_by_id('ContentPlaceHolder1_spanValue').text
		hash_val = driver.find_element_by_id('spanTxHash').text
		success_or_not = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[2]/div[2]/span').text
		clock = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[4]/div[2]').text
		to_address = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[7]/div[2]/ul/li/div/span[4]/a/span').text
		from_address = driver.find_element_by_id('addressCopy').text

		amount_val = float(amount_val.split('$')[-1].split(')')[0])

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



