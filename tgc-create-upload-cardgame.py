'''This is an extended example or a deck of cards using the gamecrater api from
python.  It creates a game using a given client-specific name(and time incase
same client does more than one), then creates folders and decks and uploads the
cards.

While we use a more complex program, with a conf file and such, I wanted to keep
this simple for those with minimal python experience so there are few key
paramters It should be run from a directory containing the deck files. It
presmes that back.png is the common card back, and assumes all png files in the
current directory are the faces.


I started from andymeneely's tgc-client.py
(https://gist.github.com/andymeneely/8509982) which was helpful but very  basic start.  I  had a lot to do a lot of back and forth with the documents make it into
usable program for our needs.  Hopefully this will expanded tutorial will helps
others by showing a more complete process example.  

This is pretty useful in its own right even if you are not really a python programmer, just change the fields below, then run this the directory with your files and it will create the game, and upload and mark as proofed all the the files.  The BACKNAME defines the back of the cards, the BOXNAME defines the filename of the art for the tuckbox,  all other png define the faces.

'''
 
URL="https://www.thegamecrafter.com/api" 
API_KEY_ID = '' #Replace with yours
USERNAME = 'dr_innovation' #Replace with yours
PASSWORD = '' #Replace with yours
CLIENTNAME= ''

BACKNAME='back.png'
BOXNAME='box.png'


import requests #Found at python-requests.org/
import time
import os
#import PythonMagick

'''
 we name all the key items, folders, deck, cards, with client-time-date- prefix to make it easy to track/delete them after the client's project is shipped.
 I'll eventually add a clean-up script but for now I delete things by hand.

 to clean up/delete do it in this order.. 
 ALWAYS delete the deck first (there is no way to get it after game is gone, and you cannot delete the files if they are attached to a deck). 
 select the game, go to the deck, select the cards and say delete.
 Then go to your game and delete it.  
 Finally go to my files, fine the folder and "clean up folder", then delete folder
 For now this prints out the ID's of critical items for deleting just in case as there is no easy API to get to deck once you delete the game.  

If you do find youself with stuff you cannot delete, try going to 
https://www.thegamecrafter.com/api/user/USERID/games
and it will show you alot of stuff about including recently deleted games. 
'''


# computed parms
GNAME=CLIENTNAME+time.strftime("%H-%M-%S-%d-%m-%Y")
DECKNAME=GNAME+'-Deck'
BNAME=GNAME+'-'+BACKNAME;
BOXLNAME=GNAME+'-'+BOXNAME;


debuglevel=0;  #this allow skipping over stuff as you debug.. so you don't create tons of stuff, you take the id from an output and use it to set a field, but use with care and make sure you check your acount as if you do too much you may have a lot of cleaning up to do

#Get a Session
params = {'api_key_id': API_KEY_ID, 'username' : USERNAME, 'password': PASSWORD}
response = requests.post(URL + "/session", params=params)
if response.status_code==200:
  print("----Status code OK!----")
session = response.json()['result']
if debuglevel >1: 
    print("---Got a session---")
    print(response.json())
    print("-------------------")

 
# Fetch my account info
params = {
    'session_id': session['id'],
    '_include_relationships':1
}
response = requests.get(URL + "/user/" + session['user_id'], params=params)
if debuglevel >1: 
    print("---Get account with relationships info---")
    print(response.json())
    print("----------------------")
user = response.json()['result']
root_folder_id = user['root_folder_id']
developer_id= user['id']

#to build a game in code you need an designer ID, which I found by logging in then visiting
#https://www.thegamecrafter.com/publish/designers
#making sure I created a designer (I had not before this)
#click on edit designer for the designer you created and in the URL after /designers/ is their designer_id, e.g. tboult (me) is 
#https://www.thegamecrafter.com/publish/designer/1403A252-A262-11E3-934D-D98BE79A076C
designer_id = '1403A252-A262-11E3-934D-D98BE79A076C'





# Now we can  create a new game, with unique name
if debuglevel <2:
    params = {
        'name': GNAME,
        'developer_id': developer_id,
        'designer_id': designer_id,
        'description': 'Custome game for customer'+CLIENTNAME,
        'session_id': session['id']
    }
    
    if debuglevel > 0:    print("Game creation params are ",params)
    response = requests.post(URL + "/game", params=params)
    gameid = response.json()['result']['id']
    if debuglevel > 0:    
        print("---create game response---")
        print(response.json())
        print("---created gameid----"+gameid)
else:
    gameid='8923D3FE-A267-11E3-869B-D98BE79A076C'


#create a folder to upload into to keep it esier to find/delete stuff
if debuglevel < 2:
    params = {
        'name': GNAME,
        'parent_id': root_folder_id,
        'session_id': session['id'],
        'user_id' : developer_id
    }
    if debuglevel > 0:    print("Folder parms are ",params)
    response = requests.post(URL + "/folder", params=params)
    folderid = response.json()['result']['id']
    if debuglevel > 0:    
        print("---Create Folder response---")
        print(response.json())
        print("---------------------")
    print("Created folder id", folderid)
else :
#since it keeps recreating it and its a pain to delete them all, for testing it may be useful to comment the above out and just use root
    folderid = root_folder_id


    if debuglevel > 0:    
        print("Creating folderid ", folderid)


# Upload the box for the deck.. make the name from the gamename (to avoid confusion as its more confusing when there are many files with same name)

params = {
 'name': BOXLNAME,
 'folder_id': folderid,
 'session_id': session['id']
}
files = { 'file': open(BOXNAME,'rb') }
if debuglevel > 0:    print("fileupload parms are ",params)
response = requests.post(URL + "/file", params=params, files=files)
boxid = response.json()['result']['id']
if debuglevel > 0:    
    print("---Upload response---")
    print(response.json())
    print("---------------------")


# Create box
params = {
 'name': BOXLNAME,
 'game_id': gameid,
 'session_id': session['id'],
 'outside_id': boxid,
 'has_proofed_outside':1
}
files = { 'file': open(BOXNAME,'rb') }
if debuglevel > 0:    print("parms are ",params)

#We use a tuckbox108.. this could also be othersize replace 108 with the size
response = requests.post(URL + "/pokertuckbox108", params=params, files=files)
#response = requests.post(URL + "/pokertuckbox108", params=params)
if debuglevel > 0:    
    print("---Upload response---")
    print(response.json())
    print("---------------------")
boxid= response.json()['result']['id']
print("Created boxid ", boxid)


    

# Upload the back side for the deck.. make the name from the gamename (to avoid confusion as its more confusing when there are many files with same name)

params = {
 'name': BNAME,
 'folder_id': folderid,
 'session_id': session['id']
}
files = { 'file': open(BACKNAME,'rb') }
if debuglevel > 0:    print("fileupload parms are ",params)
response = requests.post(URL + "/file", params=params, files=files)
backid = response.json()['result']['id']
if debuglevel > 0:    
    print("---Upload response---")
    print(response.json())
    print("---------------------")
    
# Create deck, with preproof back image
params = {
 'name': DECKNAME,
 'game_id': gameid,
 'session_id': session['id'],
 'back_id': backid,
 'has_proofed_back':1
}
files = { 'file': open('back.png','rb') }
if debuglevel > 0:    print("parms are ",params)

#We use a pokerdeck.. this could also be /bridgedeck or /minideck as needed
response = requests.post(URL + "/pokerdeck", params=params, files=files)
if debuglevel > 0:    
    print("---Upload response---")
    print(response.json())
    print("---------------------")
deckid= response.json()['result']['id']
print("Created Deckid ", deckid)

#now iterate through all png files in the directory 
for fname in os.listdir(os.getcwd()):
    if(fname.endswith(".py")):
       continue
    elif(fname is BACKNAME): 
       continue
    elif(fname is BOXNAME): 
       continue
    elif not(fname.endswith(".png")):
       print 'skipping unknown file '+fname
       continue
    elif(fname.endswith(".png")) :
        if debuglevel > 0:            
            print "Uploading face"
        params = {
            'name': GNAME+'-'+fname,
            'folder_id': folderid,
            'session_id': session['id']
        }
        files = { 'file': open(fname,'rb') }
        if debuglevel > 0:            print("fileupload parms are ",params)
        response = requests.post(URL + "/file", params=params, files=files)
        faceid = response.json()['result']['id']
        if debuglevel > 0:    
            print("---Upload response for --"+faceid)
            print(response.json())
            print("---------------------")

        params = {
            'name': GNAME+'-'+fname,
            'session_id': session['id'],
            'deck_id': deckid,
            'face_id' :faceid,
            'back_id': backid,
            'has_proofed_face':1
        }
        response = requests.post(URL + "/pokercard", params=params)
        if debuglevel > 0:
            print("---Upload response---")
            print(response.json())
            print("---------------------")
        cardid = response.json()['result']['id']

        
# now
