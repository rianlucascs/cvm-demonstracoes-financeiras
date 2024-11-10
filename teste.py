import requests

url = 'https://raw.githubusercontent.com/rianlucascs/cvm-demonstracoes-financeiras/master/Scripts/cvm.py'

response = requests.get(url)

exec(response.text)

cvm