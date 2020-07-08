from PIL import Image
import random

def dec_to_bin(x):
    return (bin(x)[2:]).zfill(7)

def increment_pointer(pointer, meswidth):
    if pointer==meswidth-1:
        return (pointer-meswidth)+1
    else:
        return pointer+1

def ErrorOut():
    # input("Error thrown. Press enter to exit.")
    raise IOError

def ASCII_to_bitlist(string):
    binarylist=[]
    bitlist=[]
    for char in string:
        binarylist.append(dec_to_bin(ord(char)))
    for block in binarylist:
        for bit in block:
            bitlist.append(int(bit))
    return bitlist

def imageencode(seed, bool_use_terminator):
    if bool_use_terminator:
        use_terminator="Y"
    else:
        use_terminator="F"
    if use_terminator=="Y":
        # if False:
        #     print("Enter the custom terminator you wish to use. Use more than 1 ASCII character, preferably a symbol: ")
        #     terminator=input()
        #     if len(terminator)==1:
        #         ErrorOut()
        terminator="!@#$"

    random.seed(seed)
    xor_key=str(dec_to_bin(random.getrandbits(16400))) #standard number of bits taken is 16400, only first 16384 are used.
    im = Image.open("app/static/sample.png")
    pixels = im.load()
    #cleaning the image
    for y in range(0,im.height):
        for x in range (0,im.width):
            dummylist= list(pixels[x,y]) # casting to a list to make mutable
            for i in range(0,2):
                if dummylist[i] % 2 ==1:
                    dummylist[i] -= 1;
            pixels[x,y]=tuple(dummylist)
            #image is cleaned.

    #information will now be encoded into it
    f=open("Message.txt","rb")
    bin_list=[]
    #a list of binary contents is created.
    num=list(f.read())
    for pos in range(0,len(num)):
        binnumber=dec_to_bin(num[pos])
        for binchar in binnumber:
            bin_list.append(int(binchar))

    #the terminator and extra components are added to the message
    if use_terminator=="Y":
        terminator_bit_list=ASCII_to_bitlist(terminator)
        bin_list= ASCII_to_bitlist("#")+terminator_bit_list+ASCII_to_bitlist(chr(0))+bin_list+terminator_bit_list+ASCII_to_bitlist("\n")
    else:
        bin_list= ASCII_to_bitlist("#")+ASCII_to_bitlist(chr(0))+bin_list

    messagewidth=len(bin_list)
    if messagewidth>im.height*im.width:
        pass
        # print("Warning: message has been cropped. Use a larger resolution picture to encode the full message.")
        # input("Press enter to continue")

    #the contents are XOR scrambled in-place according to the xor_key
    xorindex=0
    for i in range(0,len(bin_list)):
        xorindex=xorindex %16384
        bin_list[i]= int(bin_list[i]) ^ int(xor_key[xorindex])
        xorindex+=1

    #main encoding loop
    binpointer=0
    for y in range(0,im.height):
        for x in range(0,im.width):
            dummylist= list(pixels[x,y]) # casting to a list to make mutable
            if binpointer==messagewidth:
                break
            for i in range(0,2):
                if binpointer==messagewidth:
                    break
                if (bin_list[binpointer]==1):
                    dummylist[i]+=1
                binpointer+=1
            pixels[x,y]=tuple(dummylist)
            #message is encoded
    f.close()
    im.save("app/static/encodedsamples/encodedsample"+str(seed)+".png", "PNG")
    im.close()
    print(seed)
