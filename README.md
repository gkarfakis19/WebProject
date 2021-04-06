# WebProject

Currently hosted on https://gkwebsite.herokuapp.com/

Implements a very simple flask-based website, that implements a steganographic algorithm to hide messages in images.
It takes a message and key, and provides encoding and decoding functions for the steganography in an arbitrary image or the default sample.

In order to use, click the header "Image Encoding", and follow the instructions.

For ease of decryption, use a terminator.
The message and key can both be random ASCII strings.
You will require the key in order to decrypt the message.

The current algorithm works exclusively with png files, as jpg files implement fancy compression schemes that ruin the encrypted contents of the file.
Statistic analysis of image entropy will reveal the existance of a hidden message within the file.

The current algorithm, for hosting and performance reasons, isn't cryptographically secure.
To increase security, simply remove the message header and do not use a terminator.
Make sure to also change the random key string in the PKDF2 function to something else, and increase the number of PKDF2 iterations.
