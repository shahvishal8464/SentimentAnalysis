from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import Visualize as v
import json
import SentimentAnalyzer as s

consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""
count=0

class StdOutListener(StreamListener):
    def on_data(self, data):
        data = data.encode("ascii", errors="ignore").decode("ascii")
        all_data = json.loads(data)
        tweet = all_data["text"]
        tweet = tweet.encode("ascii", errors="ignore").decode("ascii").replace("\n"," ")
        user_name = str(all_data["user"]["screen_name"]).replace("u","").replace("'","\"")
        user_id = str(all_data["user"]["id"]).replace("u","").replace("'","\"")
        tweet_id = all_data["id"]
        sentiment_value, confidence = s.sentiment(tweet)


        if confidence >= 60:
            print (user_id, user_name, tweet, tweet_id,sentiment_value, confidence)
            output = open("tweets.txt","a")
            output.write(str(sentiment_value))
            output.write('\n')
            output.write(str(data))
            output.write('\n')                
            output.close()
            count = count+1            
            if(count>199):
                v.animate()
                output = open("tweets.txt","w")
                output.close()
                count=0;
        return True


    def on_error(self, status):
        print("Error found in: " +str(status))

if __name__ == '__main__':  
    count = 0
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)    
    stream = Stream(auth, StdOutListener())
    stream.filter(track=['@realDonaldTrump', 'donald trump', 'president'])