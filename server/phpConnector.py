import crawler
import os
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("mode", type=str, choices=['mode1','mode2'], help="choose different mode of tweepy")
parser.add_argument('-k', '--keyword', type=str)
parser.add_argument('-uid', '--userID', type=str)

args = parser.parse_args()

#create object
tweetCrawler = crawler.TweetCrawler()

if args.mode == "mode1":
	print("mode1")
	user = tweetCrawler.get_userProfile(args.userID)
	userProfile_dict = { 
	"user_id": user.id,
	"screen_name": user.screen_name, 
	"name": user.name, 
	"location": user.location, 
	"description": user.description, 
	"N_followes": user.followers_count, 
	"N_friends": user.friends_count, 
	"N_statues": user.statuses_count, 
	"URL": user.url 
	}
	# json_str = json.dumps(userProfile_dict)
	#save json file
	filePath = 'output'+os.sep+'userProfile.json'
	with open(filePath, 'w') as f:
		json.dump(userProfile_dict, f)
		f.write('\n')
elif args.mode == "mode2":
	print("mode2")
	print("search tweets by keyword:")
	query = args.keyword
	count = 20
	tweets = tweetCrawler.search_tweetsbyKeyword(query, count)
	print('found',len(tweets),'tweets by keyword(weather)')
	#save json file
	filePath = 'output'+os.sep+'tweets_keyword.json'
	with open(filePath, 'w') as f:
		for tweet in tweets:
			#save json line by line
			json.dump(tweet._json, f)
			f.write('\n')	
else:
	print("unknown")
