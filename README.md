# WebProject

Currently hosted on www.gkwebsite.herokuapp.com

Implements a very simple flask-based website, that implements a steganographic algorithm to hide messages in images.
It takes a message and key, and provides encoding and decoding functions for the steganography in an arbitrary image or the default sample.
The current algorithm, for practical reasons, isn't that cryptographically secure.
To increase security, simply remove the message header and do not use a terminator.
