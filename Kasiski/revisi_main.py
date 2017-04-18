# Created by 5114100148 and 5114100138
# Method used were kasiski test, Friedman (Index of Coincidence), chi-squared, and english dictionary suggestion
# Constraint:
# - Key length in range 3 - 12
# - Cipher text must longer than cipher key
# - There must be a substring with length more than 2 that repeating more than 1

import sys
import re
import copy
import enchant
from collections import Counter
import time
from difflib import SequenceMatcher

alphabets_frequent = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772,
                      0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978,
                      0.02360, 0.00150, 0.01974, 0.00074]

one_two_char = ["i", "a", "an", "am", "is", "he", "if", "it", "in", "on", "me", "my", "of", "to", "be", "as", "at",
                "so", "we", "by", "or", "do", "up", "go", "no", "us"]


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def key_process(i_key):
    key = []

    for i in range(0, len(i_key)):
        if 64 < ord(i_key[i]) < 91:
            key.append(int(ord(i_key[i]) - 65))

        elif 96 < ord(i_key[i]) < 123:
            key.append(int(ord(i_key[i]) - 97))

    return key


def decrypt(i_input, key):
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


def find_position(text, f_char):
    return [i for i, letter in enumerate(text) if letter == f_char]


def most_alphabet(text, num_count):
    three_alphabet = Counter(text).most_common(num_count)
    most_alpha = three_alphabet[0]
    return most_alpha[0]


def largest_substring(string):
    list_substring = []
    list_count = []

    for y in range(len(string)):
        for x in range(len(string)):
            substring = string[y:x]
            count = len(list(re.finditer(substring, string)))
            if count > 1 and len(substring) > 2:
                counter = len(list_substring)

                if counter == 0:
                    list_substring.append(substring)
                    list_count.append(count)
                elif substring not in list_substring:
                    list_substring.append(substring)
                    list_count.append(count)

    # Checking repetition part 2
    temp_list = copy.copy(list_substring)
    list_substring.sort(key=lambda j: len(j), reverse=True)
    checked_list = []
    flagged = False
    counter = 0

    for s in list_substring:
        for o in checked_list:
            count_s = list_count[temp_list.index(s)]
            count_o = list_count[temp_list.index(o)]
            if s not in o:
                counter += 1
            elif s in o and count_s > count_o:
                flagged = True
                break

        if flagged or counter == len(checked_list):
            checked_list.append(s)

        flagged = False
        counter = 0
    return checked_list


def calculate_ioc(substring):
    length = len(substring)
    ioc = 0
    if length - 1:
        ioc = (1 / (float(length) * (length - 1))) * (sum([substring.count(a) * (substring.count(a) - 1)
                                                           for a in substring]))
    return ioc


def index_of_coincidence(e_string):
    list_avg_ioc = []
    for x in range(2, 13):
        ioc_total = 0.0
        # avg_ioc = 0.0
        for y in range(x):
            temp = ""
            for j in range(0, len(e_string[y:]), x):
                temp += (e_string[y:][j])
            ioc = calculate_ioc(temp)
            ioc_total += ioc
        avg_ioc = ioc_total / x
        list_avg_ioc.append(avg_ioc)
    temp_list = copy.copy(list_avg_ioc)
    list_avg_ioc.sort(reverse=True)
    k_length = [temp_list.index(list_avg_ioc[0]) + 2]

    return k_length[0]


def calc_length_key(list_substring, text):
    all_distance = []

    for x in list_substring:
        all_position = [m.start() for m in re.finditer(x, text)]

        for i in range(1, len(all_position)):
            temp = all_position[i] - (all_position[i-1])

            if temp not in all_distance:
                all_distance.append(temp)

    all_distance.sort()
    all_factor = []
    all_count = []

    for y in all_distance:
        n_factor = list(set(reduce(list.__add__, ([i, y // i] for i in range(1, int(y ** 0.5) + 1) if y % i == 0))))

        for z in n_factor:
            if 2 < z < 13:
                if z not in all_factor:
                    all_factor.append(z)
                    all_count.append(1)
                elif z in all_factor:
                    index = all_factor.index(z)
                    temp_n = all_count[index]
                    temp_n += 1
                    all_count[index] = temp_n

    max_count = max(all_count)
    max_index = [i for i, j in enumerate(all_count) if j == max_count]
    k_length = [all_factor[i] for i in max_index]
    k_length.sort(reverse=True)

    return k_length


def get_common(k_length, text):
    text = text.replace(" ", "")
    temp_matrix = []
    temp = ""
    most_common = ""

    for i in range(0, k_length):
        count = i
        while count < len(text):
            temp += text[count]
            count += k_length

        temp_matrix.append(temp)
        temp = ""

    for i in range(0, k_length):
        most_common += most_alphabet(temp_matrix[i], 1)

    return most_common, temp_matrix


def get_key_value(encoded_val, plain_val):
    temp = encoded_val - plain_val
    if temp < 0:
        temp += 26
    temp = chr(temp + 65)

    return temp


def check_sentence(processed_text):
    last_position = 0
    list_step = []
    finished = False
    eng_dict = enchant.Dict("en_US")
    result = ""
    possible = ""
    temp_position = 0
    while last_position < len(processed_text):
        flag = False

        for i in range(1, len(processed_text)+1):
            if i == len(processed_text):
                temp = processed_text[last_position:].strip()
            else:
                temp = processed_text[last_position:i].strip()

            if temp.lower() in one_two_char or (len(temp) > 2 and eng_dict.check(temp)):
                count = len(list_step)
                possible = temp
                temp_position = i
                flag = True

                if count > 0:
                    temp_step = list_step[count-1]
                    if temp_step[1] < last_position:
                        list_step[count-1] = [(result + possible + " "), last_position, i]
                    else:
                        list_step.append([(result + possible + " "), last_position, i])
                else:
                    list_step.append([(result + possible + " "), last_position, i])

        if flag:
            last_position = temp_position
            temp = possible + " "
            result += temp

        if not flag:
            if len(list_step) > 1:
                del list_step[-1]
                temp_step = list_step[len(list_step) - 1]
                result = temp_step[0]
                last_position = temp_step[2]
            else:
                break
        elif flag and last_position > len(processed_text)-2:
            finished = True
            break

    return finished, result.strip()


def check_structure(processed_text):
    list_word = processed_text.split()
    finished = False
    eng_dict = enchant.Dict("en_US")
    flag = 0

    for i in list_word:
        if eng_dict.check(i):
            flag += 1
        else:
            break

    if flag == len(list_word):
        finished = True

    return finished, processed_text.strip()


def chi_squared(p_plaintext):
    p_plaintext = p_plaintext.lower()
    english_count = []
    normal_count = []
    calculated = []
    for x in range(0, 26):
        alpha = x + 97
        english_count.append((alphabets_frequent[x] * len(p_plaintext)))
        normal_count.append(p_plaintext.count(chr(alpha)))
    for y in range(0, 26):
        if normal_count[y] != 0:
            calculated.append(((normal_count[y] - english_count[y]) ** 2) / normal_count[y])

    chi_square = sum(calculated)
    return chi_square


def possible_key(k_length, split_string):
    list_chi_square = []
    k_possible = ""
    for x in range(k_length):
        for m in range(0, 26):
            p_text = decrypt(split_string[x], [m])
            list_chi_square.append(chi_squared(p_text))
        k = chr(list_chi_square.index(min(list_chi_square)) + 97)
        k_possible += k
        del list_chi_square[:]

    return k_possible


def decrypt_text(substring, k_length, s_string, e_string):
    list_suggestion = []
    brute_force = []
    alphabet_count = []
    index_rank = []
    n_string = e_string.replace(" ", "")
    for i in range(0, k_length):
        alphabet_count.append(str(s_string[i]).count(substring[i]))

    for i in range(0, k_length):
        indexes = alphabet_count.index(max(alphabet_count))
        index_rank.append(indexes)
        alphabet_count[indexes] = 0

    key = possible_key(k_length, s_string)
    print "Temporary Result:"
    sys.stdout.write("Chi-square result : ")
    print key
    csqrt_key = key
    list_key = key_process(key)
    raw_plain = decrypt(n_string, list_key)
    sys.stdout.write("Result : ")
    print raw_plain
    flag, plain = check_sentence(raw_plain)

    if not flag:
        print "Attemping decrypting text"
        eng_dict = enchant.Dict("en_US")
        temp_suggest = eng_dict.suggest(key)

        for i in temp_suggest:
            if len(i) == k_length:
                list_suggestion.append(i.lower())

        for i in list_suggestion:
            key = i
            list_key = key_process(key)
            raw_plain = decrypt(n_string, list_key)
            flag, plain = check_sentence(raw_plain)

            if flag:
                raw_plain = decrypt(e_string, list_key)
                temp_flag, temp_plain = check_structure(raw_plain)
                if temp_flag:
                    plain = temp_plain
                break

        if not flag:
            past_suggestion = copy.copy(list_suggestion)
            del list_suggestion[:]
            path = "word_" + str(k_length) + ".txt"
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line not in past_suggestion and similar(line, csqrt_key) > 0.4:
                        list_suggestion.append(line)
                    elif line not in past_suggestion:
                        brute_force.append(line)

            for i in list_suggestion:
                key = i
                list_key = key_process(key)
                raw_plain = decrypt(n_string, list_key)
                flag, plain = check_sentence(raw_plain)

                if flag:
                    raw_plain = decrypt(e_string, list_key)
                    temp_flag, temp_plain = check_structure(raw_plain)
                    if temp_flag:
                        plain = temp_plain
                    break

        if not flag:
            print "Attemping brute forcing the key"
            for i in brute_force:
                key = i
                list_key = key_process(key)
                raw_plain = decrypt(n_string, list_key)
                flag, plain = check_sentence(raw_plain)
                if flag:
                    raw_plain = decrypt(e_string, list_key)
                    temp_flag, temp_plain = check_structure(raw_plain)
                    if temp_flag:
                        plain = temp_plain
                    break

    return flag, key, plain


try:
    print "Insert encrypted text: "
    sys.stdout.write("Input: ")
    encrypt_text = sys.stdin.readline().strip()
    while encrypt_text != "EXIT":
        start_time = time.time()
        temp_index = 0
        main_flag = False
        normalize_text = encrypt_text.replace(" ", "")
        list_cs = largest_substring(normalize_text)
        key_length = calc_length_key(list_cs, normalize_text)
        temp_ioc = index_of_coincidence(normalize_text)

        if temp_ioc in key_length:
            temp_index = key_length.index(temp_ioc)
        # else:
        #     key_length.append(temp_ioc)
        #     temp_index = key_length.index(temp_ioc)

        sys.stdout.write("Possible Key Length: ")
        print key_length
        for p in range(len(key_length)):
            if temp_index > len(key_length) - 1:
                temp_index = 0
            test = key_length[temp_index]

            print "\n--Trying with key length " + str(test)
            common_alpha, separate_length = get_common(test, normalize_text)
            sys.stdout.write("Most alphabet: ")
            print common_alpha
            main_flag, key_decrypted, plain_text = decrypt_text(common_alpha, test, separate_length, encrypt_text)

            if main_flag:
                print "\n--Actual Result: "
                sys.stdout.write("Key Length: ")
                print test
                sys.stdout.write("Key: ")
                print key_decrypted
                sys.stdout.write("Plain Text: ")
                print plain_text
                break

            temp_index += 1
        if not main_flag:
            print "Possible Key Not Found"
        print("Time consumed: %s seconds" % (time.time() - start_time))
        print "\nInsert encrypted text: "
        sys.stdout.write("Input: ")
        encrypt_text = sys.stdin.readline().strip()

except KeyboardInterrupt:
    sys.exit(0)
