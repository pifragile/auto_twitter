import tweepy
import os
import csv
import random 
from dotenv import load_dotenv
import time

load_dotenv()

# Consumer keys and access tokens, used for OAuth
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')
bearer_token = os.getenv('bearer_token')
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)

#print(api.me())

def get_post_text(name, opensea_link):
	return f'''{name}
Generative Art by pifragile.

Each piece features a sample of the official source code of Ethereum.

Check it out on @opensea:
{opensea_link}

#NFT #NFTCommunity #opensea #nftcollector #nftart'''

def post_nft():
	if not os.path.exists('shared_nfts.txt'):
		os.system('touch shared_nfts.txt')

	shared_nfts = []
	with open('shared_nfts.txt', 'r') as f:
		shared_nfts = [l.rstrip() for l in f.readlines()]

	with open('nfts.csv') as csv_file:
		reader = csv.reader(csv_file, delimiter=',')
		rows = list(reader)

	available_nfts = [row for row in rows if row[0] not in shared_nfts]

	if available_nfts == []:
		available_nfts = rows
		os.system('rm shared_nfts.txt')

	filename, name, opensea_link = random.choice(available_nfts)



	with open('shared_nfts.txt', 'a') as f:
		f.write(f'{filename}\n')

	with open('dropbox_links.csv') as csv_file:
		reader = csv.reader(csv_file, delimiter=',')
		rows = list(reader)

		# second element of first row
		dropbox_link = [row for row in rows if row[0] == filename][0][1]

	os.system(f'wget -O nft.gif {dropbox_link}')

	status = get_post_text(name, opensea_link)


	media_id = api.media_upload('nft.gif', chunked = True, media_category = "tweet_gif").media_id
	#api.update_status(status, media_ids=[media_id])


while True:
	try:
		post_nft()
		time.sleep(random.randint(3600, 14400))
	except Exception as e:
		print(e)
		time.sleep(60)
	


