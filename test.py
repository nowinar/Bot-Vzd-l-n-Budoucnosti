import requests

API_ENDPOINT = 'https://discord.com/api/v8'
CLIENT_ID = '909015370864689162'
CLIENT_SECRET = '937it3ow87i4ery69876wqire'
REDIRECT_URI = 'https://vzdelanibudoucnosti.cz'

def exchange_code(code):
  data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': REDIRECT_URI
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
  r.raise_for_status()
  return r.json()
exchange_code("V8WFF4QBf31VwnISWJH5o1jFIEhtjs")