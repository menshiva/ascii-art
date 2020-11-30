#TODO: extend this implementation

class Roman:
    
    def __init__(self, roman_num):
        self.roman_num = roman_num
        self.decimal_value = self.__roman_to_int(roman_num)

    @classmethod
    def from_int(cls, int_value):
        return cls(cls.__int_to_roman(int_value))
    
    def __str__(self):
        return f"Roman({self.roman_num})"
        
    def __repr__(self):
        return self.roman_num
    
    @classmethod
    def __int_to_roman(cls, input):
        """ Convert an integer to a Roman numeral. """

        ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
        nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
        result = []
        for i in range(len(ints)):
            count = input // ints[i]
            result.append(nums[i] * count)
            input -= ints[i] * count
        return ''.join(result)

    @classmethod
    def __roman_to_int(cls, input):
        """ Convert a Roman numeral to an integer. """

        input = input.upper(  )
        nums = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}
        sum = 0
        for i in range(len(input)):
            try:
                value = nums[input[i]]
                # If the next place holds a larger number, this value is negative
                if i+1 < len(input) and nums[input[i+1]] > value:
                    sum -= value
                else: sum += value
            except KeyError:
                raise ValueError('input is not a valid Roman numeral: %s' % input)
        return sum
