import tweepy

#class for grab tweets by tweepy
class TweetCrawler:
	def __init__(self):
		self.auth = tweepy.OAuthHandler("5suI57mteJ2Wgk0O3Ng5SRTWv", "qQsUGUN0Vxgvd7jGGZBCDNZhGM6XDyuurFSY1o569ikYpZrptB")
		self.auth.set_access_token("916874837464842240-k0nGURmcKqhMVvoedTkjSVa8H7410fm", "mKJHjZslKib2zdY8iqmDMPXsrSavqBuhAum0RcxLRf9te")
		self.api = tweepy.API(self.auth)	

	#get user profile by id
	def get_userProfile(self, userID):
		userProfile = self.api.get_user(userID)
		return userProfile
	
	#get friends screen name
	def get_friends(self, userID, maxNumber):
		friendList = self.api.friends_ids(userID)
		count = 0
		friendNameList = [];
		for friendID in friendList:
			user = self.api.get_user(friendID)
			friendNameList.append(user.screen_name)
			if count >= maxNumber:
				break
			count = count + 1
		return friendNameList		

	#get followers screen name
	def get_followers(self, userID, maxNumber):
		followerList = self.api.followers_ids(userID)
		count = 0
		followerNameList = [];
		for followerID in followerList:
			user = self.api.get_user(followerID)
			followerNameList.append(user.screen_name)
			if count >= maxNumber:
				break
			count = count + 1
		return followerNameList

	#search tweets by keywork
	def search_tweetsbyKeyword(self, query, count):
		tweets = self.api.search(q=query, count=count)
		return tweets

	#search tweet by region
	def search_tweetsbyRegion(self, latitude, longitude, range, count):
		geo = latitude+','+longitude+','+range+'mi'
		tweets = self.api.search(count=count, geocode=geo)
		return tweets


