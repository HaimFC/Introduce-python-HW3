class Base64DecodeError(Exception):
    pass


class CyclicCharsError(Exception):
    pass


class CyclicCharsDecodeError(Exception):
    pass


class BytePairError(Exception):
    pass


class BytePairDecodeError(Exception):
    pass


class String:
    def __init__(self, val, rules=[]):
        self.val = val
        self.index_of_itr = -1
        self.rules = []

    def __mul__(self, other):
        return self.val * other

    def __rmul__(self, other):
        return self.val * other

    def __add__(self, other):
        return self.val + other.val

    def __eq__(self, other):
        return self.val == other

    def isupper(self):
        str_temp = str(self.val)
        return str_temp.isupper()

    def islower(self):
        str_temp = str(self.val)
        return str_temp.islower()

    def count(self, l1, start, end):
        str_temp = str(self.val)
        return str_temp.count(l1, start, end)

    def slice(self, start=0, end=False, jumps=1):
        str_new = String("")

        if not end and end != 0:
            end = self.length()

        str_temp = str(self.val)
        str_new.val = str_temp[start:end:jumps]
        return str_new

    def replace(self, a, b):
        self.val = str(self.val).replace(a, b)
        return self

    def index(self, string_to_index, start=0, end="none"):
        if end == "none":
            end = self.length()
        try:
            str_temp = str(self.val)
            return str_temp.index(string_to_index, start, end)
        except ValueError:
            return False

    def length(self):
        str_temp = str(self.val)
        return len(str_temp)

    def __iter__(self):
        return self

    def __next__(self):
        self.index_of_itr += 1
        if self.index_of_itr >= self.length():
            self.index_of_itr = -1
            raise StopIteration
        else:
            return str(self.val)[self.index_of_itr]

    def base64(self) -> 'String':
        translate_dict_coding = {
            '000000': 'A', '000001': 'B', '000010': 'C', '000011': 'D', '000100': 'E', '000101': 'F', '000110': 'G',
            '000111': 'H', '001000': 'I', '001001': 'J', '001010': 'K', '001011': 'L', '001100': 'M', '001101': 'N',
            '001110': 'O', '001111': 'P', '010000': 'Q', '010001': 'R', '010010': 'S', '010011': 'T', '010100': 'U',
            '010101': 'V', '010110': 'W', '010111': 'X', '011000': 'Y', '011001': 'Z', '011010': 'a', '011011': 'b',
            '011100': 'c', '011101': 'd', '011110': 'e', '011111': 'f', '100000': 'g', '100001': 'h', '100010': 'i',
            '100011': 'j', '100100': 'k', '100101': 'l', '100110': 'm', '100111': 'n', '101000': 'o', '101001': 'p',
            '101010': 'q', '101011': 'r', '101100': 's', '101101': 't', '101110': 'u', '101111': 'v', '110000': 'w',
            '110001': 'x', '110010': 'y', '110011': 'z', '110100': '0', '110101': '1', '110110': '2', '110111': '3',
            '111000': '4', '111001': '5', '111010': '6', '111011': '7', '111100': '8', '111101': '9', '111110': '+',
            '111111': '/'}

        sliced_str = String("")
        binary_representation = String("")
        base64_representation = String("")

        res = ''.join(format(ord(byte), '08b') for byte in self.val)
        binary_representation.val = res

        while binary_representation.length() % 6 != 0:
            binary_representation.val = binary_representation.val + '0'

        division_by_six = int(binary_representation.length() / 6)
        counter = 0
        while counter < division_by_six:
            sliced_str.val = binary_representation.slice(counter * 6, counter * 6 + 6, 1).val
            for letter in translate_dict_coding:
                if sliced_str.val == letter:
                    base64_representation.val = base64_representation.val + translate_dict_coding[letter]
            counter += 1
        return base64_representation

    def byte_pair_encoding(self) -> 'String':

        list_of_dup = self.count_dup()
        list_of_dup.sort(key=lambda x: (-x[1], x[2]))

        # even num index is star, odd num index is end, 1-4 is other, 5 digits, 6 is upper and 7 is lower
        list_groups = [[33, 47, 58, 64, 91, 96, 124, 126], [48, 57], [65, 90], [97, 122]]
        list_groups_filt = []

        other = 0
        digits = 0
        upper = 0
        lower = 0

        other_index = 33
        digits_index = 48
        upper_index = 65
        lower_index = 97

        # check which groups are in the original string
        for i in self:
            if i.isupper():
                upper += 1
            elif i.islower():
                lower += 1
            elif i.isdigit():
                digits += 1
            else:
                other += 1

        if other == 0:
            list_groups_filt.append(list_groups[0])
        if digits == 0:
            list_groups_filt.append(list_groups[1])
        if upper == 0:
            list_groups_filt.append(list_groups[2])
        if lower == 0:
            list_groups_filt.append(list_groups[3])

        if not list_groups_filt:
            raise BytePairError()

        check_if_need = 0

        for i in list_of_dup:
            if i[1] > 1:
                check_if_need += 1

        if check_if_need >= 1:
            check_if_need = 0
        else:
            check_if_need = 1

        while check_if_need == 0:
            if other == 0:
                if other_index == list_groups[0][1] + 1:
                    other_index = list_groups[0][2]
                elif other_index == list_groups[0][3] + 1:
                    other_index = list_groups[0][4]
                elif other_index == list_groups[0][5] + 1:
                    other_index = list_groups[0][6]
                elif other_index == list_groups[0][5] + 1:
                    other_index = list_groups[0][0]

                self.replace(list_of_dup[0][0], chr(other_index))
                self.rules.append(str(chr(other_index)) + " = " + list_of_dup[0][0])
                other_index += 1

            elif digits == 0:
                if digits_index == list_groups[1][1] + 1:
                    digits_index = list_groups[1][0]
                self.replace(list_of_dup[0][0], chr(digits_index))
                self.rules.append(str(chr(digits_index)) + " = " + list_of_dup[0][0])
                digits_index += 1

            elif upper == 0:
                if upper_index == list_groups[2][1] + 1:
                    upper_index = list_groups[2][0]
                self.replace(list_of_dup[0][0], chr(upper_index))
                self.rules.append(str(chr(upper_index)) + " = " + list_of_dup[0][0])
                upper_index += 1

            elif lower == 0:
                if lower_index == list_groups[3][1] + 1:
                    lower_index = list_groups[3][0]
                self.replace(list_of_dup[0][0], chr(lower_index))
                self.rules.append(str(chr(lower_index)) + " = " + list_of_dup[0][0])
                lower_index += 1
            else:
                raise BytePairError
            list_of_dup = self.count_dup()

            for i in list_of_dup:
                if i[1] > 1:
                    check_if_need += 1

            if check_if_need >= 1:
                check_if_need = 0
            else:
                check_if_need = 1
        return self

    def cyclic_bits(self, num: int) -> 'String':
        counter_of_dig = String("")
        res = String("")
        new_str = String("")
        res.val = ''.join(format(ord(byte), '08b') for byte in self.val)
        while num > 0:
            counter_of_dig = res.slice(0, 1, 1)
            res = res.slice(1, res.length(), 1)
            res.val = res + counter_of_dig
            num -= 1
        new_str.val = ''.join(chr(int(res.val[i * 8:i * 8 + 8], 2)) for i in range(len(res.val) // 8))
        return new_str

    def cyclic_chars(self, num: int) -> 'String':
        new_str = String("")
        ascii_list = [ord(byte) for byte in self.val]
        for i in range(0, len(ascii_list)):
            if 32 <= ascii_list[i] <= 126 - 15:
                ascii_list[i] = ascii_list[i] + 15
            elif 111 < ascii_list[i] <= 126:
                ascii_list[i] = 32 + ((ascii_list[i] + 15) - 127)
            else:
                raise CyclicCharsError()
        new_str.val = ''.join(chr(i) for i in ascii_list)
        return new_str

    def histogram_of_chars(self) -> dict:
        bins_dict = {
            'control code': 0, 'digits': 0, 'upper': 0, 'lower': 0, 'other printable': 0, 'higher than 128': 0}
        ascii_list = [ord(byte) for byte in self.val]
        for i in ascii_list:
            if 0 <= i <= 31 or i == 127:
                bins_dict['control code'] += 1
            elif 48 <= i <= 57:
                bins_dict['digits'] += 1
            elif 65 <= i <= 90:
                bins_dict['upper'] += 1
            elif 97 <= i <= 122:
                bins_dict['lower'] += 1
            elif i >= 128:
                bins_dict['higher than 128'] += 1
            else:
                bins_dict['other printable'] += 1
        return bins_dict

    def decode_base64(self) -> 'String':
        translate_dict_coding = {
            '000000': 'A', '000001': 'B', '000010': 'C', '000011': 'D', '000100': 'E', '000101': 'F', '000110': 'G',
            '000111': 'H', '001000': 'I', '001001': 'J', '001010': 'K', '001011': 'L', '001100': 'M', '001101': 'N',
            '001110': 'O', '001111': 'P', '010000': 'Q', '010001': 'R', '010010': 'S', '010011': 'T', '010100': 'U',
            '010101': 'V', '010110': 'W', '010111': 'X', '011000': 'Y', '011001': 'Z', '011010': 'a', '011011': 'b',
            '011100': 'c', '011101': 'd', '011110': 'e', '011111': 'f', '100000': 'g', '100001': 'h', '100010': 'i',
            '100011': 'j', '100100': 'k', '100101': 'l', '100110': 'm', '100111': 'n', '101000': 'o', '101001': 'p',
            '101010': 'q', '101011': 'r', '101100': 's', '101101': 't', '101110': 'u', '101111': 'v', '110000': 'w',
            '110001': 'x', '110010': 'y', '110011': 'z', '110100': '0', '110101': '1', '110110': '2', '110111': '3',
            '111000': '4', '111001': '5', '111010': '6', '111011': '7', '111100': '8', '111101': '9', '111110': '+',
            '111111': '/'}

        counter_of_match = 0
        for byte in self.val:
            for letter in translate_dict_coding:
                if byte == translate_dict_coding[letter]:
                    counter_of_match += 1
        if counter_of_match != self.length():
            raise Base64DecodeError()

        new_str = String('')
        for byte in self.val:
            for letter in translate_dict_coding:
                if byte == translate_dict_coding[letter]:
                    new_str.val = new_str.val + letter
        while new_str.length() % 8 != 0:
            new_str = new_str.slice(0, new_str.length() - 1, 1)
        new_str.val = ''.join(chr(int(new_str.val[i * 8:i * 8 + 8], 2)) for i in range(len(new_str.val) // 8))
        return new_str

    def decode_byte_pair(self) -> 'String':
        if not self.rules:
            raise BytePairDecodeError

        self.rules.reverse()
        for i in self.rules:
            self.replace(i.split(' = ')[0], i.split(' = ')[1])
        return self

    def decode_cyclic_bits(self, num: int) -> 'String':
        counter_of_dig = String("")
        res = String("")
        new_str = String("")
        res.val = ''.join(format(ord(byte), '08b') for byte in self.val)
        while num > 0:
            counter_of_dig = res.slice(res.length() - 1, res.length(), 1)
            res = res.slice(0, res.length() - 1, 1)
            res.val = counter_of_dig + res
            num -= 1
        new_str.val = ''.join(chr(int(res.val[i * 8:i * 8 + 8], 2)) for i in range(len(res.val) // 8))
        return new_str

    def decode_cyclic_chars(self, num: int) -> 'String':
        new_str = String("")
        ascii_list = [ord(byte) for byte in self.val]
        for i in range(0, len(ascii_list)):
            if 32 + 15 <= ascii_list[i] <= 126:
                ascii_list[i] = ascii_list[i] - 15
            elif 32 <= ascii_list[i] < 37:
                ascii_list[i] = 127 - (32 - (ascii_list[i] - 15))
            else:
                raise CyclicCharsDecodeError()
        new_str.val = ''.join(chr(i) for i in ascii_list)
        return new_str

    def count_dup(self):
        find_str = String("")
        new_str = String("")
        count = self.length() - 1
        index_of_num = 0
        inc_num = 0
        dup_count = 0
        list_of_dup = []
        check_if_exist = 0
        index_counter = 0

        while count > 0:
            find_str = self.slice(inc_num, inc_num + 2, 1)
            for i in list_of_dup:
                if i[0] == find_str.val:
                    check_if_exist += 1
            if check_if_exist == 0:
                index_of_num = self.index(find_str.val, 0, inc_num + 2)
                new_str.val = self.slice(0, index_of_num, 1).val + self.slice(index_of_num + 2, self.length(), 1).val
                if new_str.val != "":
                    dup_count = 1 + new_str.count(find_str.val, 0, new_str.length())
                index_counter += 1
                list_of_dup.append([find_str.val, dup_count, index_counter])
            inc_num += 1
            count -= 1
            check_if_exist = 0
        return list_of_dup