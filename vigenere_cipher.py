# Created by 5114100148

import sys
import os.path

key = []
u_output = ''


def key_process(i_key):
    for i in range(0, len(i_key)-1):
        if 64 < ord(i_key[i]) < 91:
            key.append(int(ord(i_key[i]) - 65))

        elif 96 < ord(i_key[i]) < 123:
            key.append(int(ord(i_key[i]) - 97))


def encrypt(i_input):
    j = 0
    i_output = ''

    for i in range(0, len(i_input)):
        if 64 < ord(i_input[i]) < 91:
            result = ord(i_input[i]) + key[j]
            if result > 90:
                result -= 26
            i_output += chr(result)
            j += 1

        elif 96 < ord(i_input[i]) < 123:
            result = ord(i_input[i]) + key[j]
            if result > 122:
                result -= 26
            i_output += chr(result)
            j += 1

        else:
            i_output += i_input[i]

        if j == len(key):
            j = 0

    return i_output


def decrypt(i_input):
    j = 0
    i_output = ''

    for i in range(0, len(i_input)):
        if 64 < ord(i_input[i]) < 91:
            result = ord(i_input[i]) - key[j]
            if result < 65:
                result += 26
            i_output += chr(result)
            j += 1

        elif 96 < ord(i_input[i]) < 123:
            result = ord(i_input[i]) - key[j]
            if result < 97:
                result += 26
            i_output += chr(result)
            j += 1

        else:
            i_output += i_input[i]

        if j == len(key):
            j = 0

    return i_output


try:
    while True:
        sys.stdout.write('-- 1) Encode     2) Decode:\nAnswer: ')
        choice = sys.stdin.readline().strip()

        if int(choice) == 1:
            print '--> PlainText:'
            u_input = sys.stdin.readline()
            print '--> Key:'
            u_key = sys.stdin.readline()
            key_process(u_key)
            if '.txt' in str(u_input) and os.path.isfile(u_input.strip()):
                op_file = open(u_input.strip(), "r")
                data = op_file.read()
                op_file.close()
                enc_data = encrypt(data)
                op_file = open(u_input.strip(), "w")
                op_file.write(enc_data)
                op_file.close()

                u_output = u_input
            else:
                u_output = encrypt(u_input)
            print '--> CipherText:'
            print u_output.upper()
            del key[:]

        elif int(choice) == 2:
            print '--> CipherText:'
            u_input = sys.stdin.readline()
            print '--> Key:'
            u_key = sys.stdin.readline()
            key_process(u_key)
            if '.txt' in str(u_input) and os.path.isfile(u_input.strip()):
                op_file = open(u_input.strip(), "r")
                data = op_file.read()
                op_file.close()
                enc_data = decrypt(data)
                op_file = open(u_input.strip(), "w")
                op_file.write(enc_data)
                op_file.close()

                u_output = u_input
            else:
                u_output = decrypt(u_input)
            print '--> PlainText:'
            print u_output
            del key[:]


except KeyboardInterrupt:
    sys.exit(0)
