This is an extended example or a deck of cards using the gamecrater api from
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

