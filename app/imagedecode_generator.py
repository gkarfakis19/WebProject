from PIL import Image
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from app.imageprocess_generator import GenerateKey,dec_to_bin

def imagedecode(string_seed,fileName):

    returnvalue=0 #0 means: decryption successful, terminator found. 1 means: decryption successful, terminator not found. -1 means decryption unsucessful.
    im = Image.open(fileName)
    pixels = im.load()
    decode_bin_list=[]

    im_size=im.height*im.width
    seed=bytes(string_seed,"utf-8")
    temp_salt = bytes(GenerateKey(seed, bytes("unicorns and rainbows","utf-8"), 256, 50), 'utf-8')
    print("step1")
    xor_key = GenerateKey(seed, temp_salt, im_size + 6, 350)  # key generated
    print("step2")

    #getting individual bits back out
    for y in range(0,im.height):
        for x in range (0,im.width):
            for i in range(0,3):
                if pixels[x,y][i] % 2 ==1:
                   decode_bin_list.append(1)
                else:
                   decode_bin_list.append(0)
    #descrambling
    xorindex=0
    for i in range(0,len(decode_bin_list)):
        xorindex=xorindex %65524
        decode_bin_list[i]=decode_bin_list[i] ^ int(xor_key[xorindex])
        xorindex+=1


    #getting 7bit groupings of the descrambled bits
    decode_ascii_list=[]
    for bindex in range(0,len(decode_bin_list),7):
        temp_string=""
        try:
            for index in range(0,7):
                temp_string+= str(decode_bin_list[bindex+index])
            #print (temp_string)
            decode_ascii_list.append(int(temp_string,2))
        except IndexError:
            break

    f=open("DecodedMessage.txt","w+" )
    should_stop=False
    #getting ascii letters from the 7bit groupings
    stringbuffer=""
    terminator=""
    terminator_used=False
    #cleaning ascii list and finding terminator
    if decode_ascii_list[0]==35:
        #print("Decryption probably succesful")
        if decode_ascii_list[1]==0:
            #print("Terminator not found.")
            returnvalue=1
        else:
            #print("Terminator found")
            returnvalue=0
            terminator_used=True
            index=1
            while True:
                if (decode_ascii_list[index]!=0):
                    terminator+= decode_ascii_list[index].to_bytes((decode_ascii_list[index].bit_length() + 7) // 8, 'big').decode()
                    index+=1
                else:
                    break
    else:
        #print("Incorrect file formatting. Decryption probably unsucessful")
        returnvalue=-1
    for i in range(0,2+len(terminator)):
        decode_ascii_list.pop(0)

    for n in decode_ascii_list:
        if terminator_used==True:
            if should_stop:
                break
            next_string=(n.to_bytes((n.bit_length() + 7) // 8, 'big').decode())
            if next_string==chr(10): #if next string is NEWLINE (\n), which is an illegal terminator character, we should check to see if the terminator has been reached.
                stringbuffer+=next_string
                loc=stringbuffer.find(terminator)
                if loc==-1:
                    f.write(stringbuffer)
                    stringbuffer=""
                else: #terminator found
                    f.write(stringbuffer[:loc])
                    should_stop=True
                    stringbuffer=""
            else:
                stringbuffer+=next_string
        else:
            next_string=(n.to_bytes((n.bit_length() + 7) // 8, 'big').decode())
            f.write(next_string)
    f.write(stringbuffer)
    im.close()
    return returnvalue
