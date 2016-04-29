# python foosbot app
import RPi.GPIO as GPIO
import sys
import time
import web
import requests
import json

foos_player = 'http://ec2-52-26-166-126.us-west-2.compute.amazonaws.com/api/player'
foos_game = 'http://ec2-52-26-166-126.us-west-2.compute.amazonaws.com/api/game'
headers = {'token':'HIRoMtqUHRWwCsK6f6GXpXtG'}

user_data = {}
r = requests.get(foos_player, headers=headers)
if (r.status_code == 200):
    user_data = r.json()
else:
    print('API request failed! Cannot run foosbot! Status code:'+str(r.status_code))
    print(r)
    sys.exit()

# remove for production
GPIO.cleanup()

#set up GPIO to use standard bcm numbering
GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(21, GPIO.RISING) #add rising edge detection on reset btn

urls = (
    '/', 'Index',
    '/reset', 'Index',
    '/game', 'Game',
    '/submit_game', 'Submit'
)

app = web.application(urls, globals())

render = web.template.render('templates/', base="layout")

# init globals
#b1 = b2 = r1 = r2 = bs = rs = "none"

class Index(object):
    def GET(self):
        #reset global score
        #b1 = b2 = r1 = r2 = bs = rs = "none"
        return render.index(user_data = user_data)
        
# Game is the main class
# form elements:
# b1/b2         player 1/2 black
# r1/r2         player 1/2 red
# bs/rs         black/red score
class Game(object):
    def POST(self):
        form = web.input(b1="none", b2="none", r1="none", r2="none", bs="none", rs="none")
        if (form.bs == "none" and form.rs == "none"):
            return render.game(b1=form.b1, b2=form.b2, r1=form.r1, r2=form.r2, bs=0, rs=0)
        
        # To simulate a game, uncomment this and update the scores to whatever you want to submit
        #return render.end_game(b1=form.b1, b2=form.b2, r1=form.r1, r2=form.r2, bs=10, rs=7)
        while True:
            if (GPIO.event_detected(21)):
                return render.end_game(b1=form.b1, b2=form.b2, r1=form.r1, r2=form.r2, bs=0, rs=0)
            if (GPIO.input(26) == 0):
                bs = int(form.bs)+1
                if (bs == 10):
                    return render.end_game(b1=form.b1, b2=form.b2, r1=form.r1, r2=form.r2, bs=bs, rs=form.rs)
                return render.game(b1=form.b1, b2=form.b2, r1=form.r1, r2=form.r2, bs=bs, rs=form.rs)
            if (GPIO.input(20) == 0):
                rs = int(form.rs)+1
                if (rs == 10):
                    return render.end_game(b1=form.b1, b2=form.b2, r1=form.r1, r2=form.r2, bs=form.bs, rs=rs)
                return render.game(b1=form.b1, b2=form.b2, r1=form.r1, r2=form.r2, bs=form.bs, rs=rs)

class Submit(object):
    def POST(self):
        
        form = web.input(b1="none", b2="none", r1="none", r2="none", bs="none", rs="none")
        b1 = form.b1
        b2 = form.b2
        r1 = form.r1
        r2 = form.r2
        bs = form.bs
        rs = form.rs
        
        # If no players were set, just skip the submittal process
        if (b1=="none" and b2=="none" and r1=="none" and r2=="none"):
            return render.submitted_game()
        
        # TODO: look up the player names in the user_data and get the id to submit to the api
        # or we can loop through all the players to find them :(
        for user in user_data:
            print("Looking for user: "+user[u'username'])
            if (b1 == user[u'username']):
                print("Found matching username for "+b1+", sending userid: "+user[u'userId'])
                bp1 = user[u'userId']
            elif (b2 == user[u'username']):
                print("Found matching username for "+b2+", sending userid: "+user[u'userId'])
                bp2 = user[u'userId']
            elif (r1 == user[u'username']):
                print("Found matching username for "+r1+", sending userid: "+user[u'userId'])
                rp1 = user[u'userId']
            elif (r2 == user[u'username']):
                print("Found matching username for "+r2+", sending userid: "+user[u'userId'])
                rp2 = user[u'userId']
            else:
                print("No match found")
                
        # build the text string that the api wants for submitting a game
        if (b2=="none" and r2=="none"):
            game = "game "+bp1+" "+rp1+" "+str(bs)+" "+str(rs)
        else:
            game = "game "+bp1+" "+bp2+" "+rp1+" "+rp2+" "+str(bs)+" "+str(rs)
        
        body={'username':'Foosbot', 'text':game}
        print(foos_game)
        print(headers)
        print(body)
        r = requests.post(foos_game, headers=headers, data=body)
        if (r.status_code == 200):
            return render.submitted_game()
        else:
            error_msg = "Could not communicate with Foosball API. Status code: "+str(r.status_code)
            return render.error(error_msg = error_msg)
        
if __name__ == "__main__":
    app.run()

