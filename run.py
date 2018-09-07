from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3

ckey=""
csecret=""
atoken=""
asecret=""

class SaveErrortoFile():
    pass

class MyStreamListener(StreamListener):

    def on_data(self, data):
        conn = sqlite3.connect('tweets.db')
        c = conn.cursor()
        data = json.loads(data)
        _username = data['user']['screen_name']
        _message = data['text']
        _language = data['user']['lang']
        _date = data['created_at']
        _creationAccountDate = data['user']['created_at']
        _profileImageUrl = data['user']['profile_image_url']
        try:
            c.execute(
                '''INSERT INTO Tweets ('username','lang','profileImageUrl','date','creationAccountDate','message') VALUES ("''' + _username + '''","'''
                + _language + '''","''' + _profileImageUrl + '''","''' +_date+'''","'''+_creationAccountDate + '''","'''+_message+'''")''')
            conn.commit()
            conn.close()
            print('up')
        except Exception as _e:
            try:
                _error_file = open('error_file','a')
                _error_file.write('Error: ' + str(_e) +
                'Username: '+ _username +
                'Msg: '+ _message +
                'Lang: '+ _language +
                'Msg Date: '+ _date +
                'Create acnt date: '+ _creationAccountDate +
                'Profile picture: '+ _profileImageUrl)
            except:
                print('error with saving file')
        return(True)

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, MyStreamListener())
twitterStream.filter(track=["japan"],async=True)
