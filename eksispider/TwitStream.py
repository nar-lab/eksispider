# -*- coding: utf-8 -*-
import tweepy
from textwrap import TextWrapper
from time import gmtime, strftime

class TwStreamListener(tweepy.StreamListener):

    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')

    def on_status(self,status):
        try:
            print self.status_wrapper.fill(status.text)
            print '\n %s  %s  via %s\n' % (status.author.screen_name, status.created_at, status.source)
        except:
            pass

    def on_error(self,status_code):
        print 'An error has occured! Status code = %s'  % status_code
        return True

    def on_timeout(self):
        print "Snoozing Zzzzz"

    def on_data(self,data):
        filename = "tweets-" + strftime("%Y%m%d%H%M%S", gmtime()) + ".json"
        with open(filename,"wb") as f:
            f.write(data)
        return True

def main():
    consumer_key = "YOUR_CONSUMER_KEY"
    consumer_secret = "YOUR_CONSUMER_SECRET"
    access_token = "YOUR_ACCESS_TOKEN"
    access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, TwStreamListener(), timeout=None)

    follow_list = ["hepsiburada","n11com","Morhipo","Trendyol","markafoni"]
    track_list = [  u"alışveriş",
                    u"gümüş kolye",
                    u"şikayet",
                    u"yüzük",
                    u"saat",
                    u"akıllı telefon",
                    u"spor ayakkabı",
                    u"şarj kablosu",
                    u"bileklik",
                    u"takı",
                    u"aksesuar"
                    ]

    userid_list = []
    for username in follow_list:
        user = tweepy.API(auth).get_user(username)
        userid_list.append(str(user.id))
    stream.filter(userid_list, track_list)

if __name__ == "__main__":
    main()
