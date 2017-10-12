import crawler
import os
import pandas as pd
import csv
import json

if __name__ == '__main__':
	#create folder for output file
	if not os.path.exists('output'):
		os.makedirs('output')

	#create object
	tweetCrawler = crawler.TweetCrawler()

	userID_list = ['34373370', '26257166', '12579252']
	#grab profile
	userProfileList = [];
	for userID in userID_list:
		userProfile = tweetCrawler.get_userProfile(userID)
		userProfileList.append(userProfile)	
	#save file
	filePath='output'+os.sep+'userProfile.csv'
	fieldnames = ['user_id', 'screen_name', 'name', 'location', 'description', 'N_followes', 'N_friends', 'N_statues', 'URL']
	fullFilePath = os.path.join(os.getcwd(),filePath)
	if not os.path.isfile(fullFilePath):
		with open(filePath, "w") as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
	with open(filePath, "a+") as csvfile:
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)	    
	    for user in userProfileList:
	    	writer.writerow({'user_id': user.id, 'screen_name': user.screen_name, 'name': user.name, 'location': user.location, 'description': user.description, 'N_followes': user.followers_count, 'N_friends': user.friends_count, 'N_statues': user.statuses_count, 'URL': user.url})

	#grab social Network Information
	df = pd.DataFrame()
	for userID in userID_list:
		friendNameList = tweetCrawler.get_friends(userID, 20)
		colName = userID + "'s friends"
		df[colName] = friendNameList
		followerNameList = tweetCrawler.get_followers(userID, 20)
		colName = userID + "'s followers"
		df[colName] = followerNameList
	#save file
	filePath = 'output'+os.sep+'socialNetwork.csv'
	df.to_csv(filePath)

	#search tweets by keyword
	query = 'weather'
	count = 50
	tweets = tweetCrawler.search_tweetsbyKeyword(query, count)
	print('found',len(tweets),'tweets by keyword(weather)')
	#save json file
	filePath = 'output'+os.sep+'tweets_keyword.json'
	with open(filePath, 'w') as f:
		for tweet in tweets:
			#save json line by line
			json.dump(tweet._json, f)
			f.write('\n')	

	latitude = '41.63'
	longitude = '-86.33'
	range = '20'
	tweets = tweetCrawler.search_tweetsbyRegion(latitude, longitude, range, count)
	print('found',len(tweets),'tweets near South Bend')
	#save json file
	filePath = 'output'+os.sep+'tweets_region.json'
	with open(filePath, 'w') as f:
		for tweet in tweets:
			#save json line by line
			json.dump(tweet._json, f)
			f.write('\n')

	print("done")