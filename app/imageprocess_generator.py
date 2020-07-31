from PIL import Image
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def dec_to_bin(x):
    return (bin(x)[2:]).zfill(7)


def increment_pointer(pointer, meswidth):
    if pointer == meswidth - 1:
        return (pointer - meswidth) + 1
    else:
        return pointer + 1


def ASCII_to_bitlist(string):
    binarylist = []
    bitlist = []
    for char in string:
        binarylist.append(dec_to_bin(ord(char)))
    for block in binarylist:
        for bit in block:
            bitlist.append(int(bit))
    return bitlist


def GenerateKey(seed, salt, size, iterations):
    backend = default_backend()
    info = b"xor_key_generation"
    pbkdf2hmac = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=size,
        salt=salt,
        iterations=iterations,
        backend=backend
    )
    tmp=bytearray(pbkdf2hmac.derive(seed))
    key = ''.join('{:08b}'.format(x) for x in tmp)  # makes the ugly bytearray into bits
    return key


def imageencode(string_seed, bool_use_terminator, fileName):
    if bool_use_terminator:
        terminator = "!@#$"
    else:
        terminator = ""
    im = Image.open("app/static/" + fileName)
    im = im.convert('RGB')
    pixels = im.load()
    im_size = im.height * im.width
    seed=bytes(string_seed,"utf-8")
    temp_salt = bytes(GenerateKey(seed, bytes("unicorns and rainbows","utf-8"), 256, 50), 'utf-8')
    print("step1")
    xor_key = GenerateKey(seed, temp_salt, im_size + 6, 350)  # key generated
    print("step2")
    # cleaning the image
    for y in range(0, im.height):
        for x in range(0, im.width):
            dummylist = list(pixels[x, y])  # casting to a list to make mutable
            for i in range(0, 3):
                if dummylist[i] % 2 == 1:
                    dummylist[i] -= 1
            pixels[x, y] = tuple(dummylist)
            # image is cleaned.

    # information will now be encoded into it
    f = open("Message.txt", "rb")
    bin_list = []
    # a list of binary contents is created.
    num = list(f.read())
    for pos in range(0, len(num)):
        binnumber = dec_to_bin(num[pos])
        for binchar in binnumber:
            bin_list.append(int(binchar))

    # the terminator and extra components are added to the message
    if bool_use_terminator:
        terminator_bit_list = ASCII_to_bitlist(terminator)
        bin_list = ASCII_to_bitlist("#") + terminator_bit_list + ASCII_to_bitlist(
            chr(0)) + bin_list + terminator_bit_list + ASCII_to_bitlist("\n")
    else:
        bin_list = ASCII_to_bitlist("#") + ASCII_to_bitlist(chr(0)) + bin_list

    # the contents are XOR scrambled in-place according to the xor_key
    xorindex = 0
    for i in range(0, len(bin_list)):
        xorindex = xorindex % (im_size)
        bin_list[i] = int(bin_list[i]) ^ int(xor_key[xorindex])
        xorindex += 1

    # main encoding loop
    binpointer = 0
    messagewidth = len(bin_list)
    for y in range(0, im.height):
        for x in range(0, im.width):
            dummylist = list(pixels[x, y])  # casting to a list to make mutable
            if binpointer == messagewidth:
                break
            for i in range(0, 3):
                if binpointer == messagewidth:
                    break
                if (bin_list[binpointer] == 1):
                    dummylist[i] += 1
                binpointer += 1
            pixels[x, y] = tuple(dummylist)
            # message is encoded
    f.close()
    im.save("app/static/encodedsamples/encodedsample" + str(ord(string_seed[0])) + ".png", "PNG")
    im.close()
