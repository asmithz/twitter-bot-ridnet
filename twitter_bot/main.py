import tweepy, time, requests, pathlib, os 
import ridnet as rd
from datetime import datetime
from credentials import access_token, access_token_secret, api_key, api_key_secret, bearer_token

path = str(pathlib.Path().resolve())
path_input = path+"/twitter_bot/media_input"
path_output = path+"/twitter_bot/media_output"

hora_actual = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%dZ')

#API v1
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#API v2
client = tweepy.Client(bearer_token=bearer_token, 
                        consumer_key=api_key, 
                        consumer_secret=api_key_secret, 
                        access_token=access_token, 
                        access_token_secret=access_token_secret, 
                        wait_on_rate_limit=True)

# Your twitter account name
twitter_bot_name = ""
id_bot = client.get_user(username=twitter_bot_name).data.id

# Example: @twitter-account
command = ""

# Clean .txt
with open("tweets.txt", "w"):
    pass

tweets_list = []

def main():
    while True:
        try:
            # Obtain all mentions
            mentions = client.get_users_mentions(id=id_bot, max_results=5, 
                                                expansions=["attachments.media_keys", "referenced_tweets.id"], 
                                                tweet_fields=["attachments"], media_fields=["url"], 
                                                start_time=hora_actual, user_auth=True)
            with open("tweets.txt","r") as tweets:
                for tweet in tweets.readlines():
                    if(tweet.strip() not in tweets_list):
                        tweets_list.append(tweet.strip())
            if(mentions.data is not None):
                for mention in mentions.data:
                    # Save tweet for response
                    if str(mention.data["id"]) not in tweets_list:
                        with open("tweets_respondidos.txt","a") as tweets:
                            tweets.write("\n"+mention.data["id"])
                        if mention["attachments"] is not None:
                            mention_media_id = mention["attachments"]["media_keys"][0]
                            for media in mentions.includes["media"]:
                                # Check if tweet contiains media
                                if(mention_media_id == media.media_key):
                                    # Obtain media from tweet
                                    resp = requests.get(media.url)
                                    with open(os.path.join(path_input, (media.media_key+".png")), "wb") as img:
                                        img.write(resp.content)
                                    if command in mention.text:
                                        try:
                                            # Use RIDNET
                                            rd.ridnet(path_input+"/"+media.media_key+".png", media.media_key)
                                            # Upload image to twitter
                                            imagen = api.media_upload(path_output+"/"+media.media_key+".png")
                                            # Reply tweet
                                            client.create_tweet(in_reply_to_tweet_id=mention.id, text="adios ruido", media_ids=[imagen.media_id_string])
                                            print("Replied to: "+str(mention.id))
                                        except tweepy.errors.TweepyException as error:
                                            print("Unable to reply tweet, "+str(error))
                    else:
                        pass
            else:
                print("No tweets for now")
            time.sleep(10)
        except tweepy.errors.TweepyException as error:
            raise error

if __name__ == "__main__":
    main()
