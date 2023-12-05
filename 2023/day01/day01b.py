
str_nums = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine'
]

def check_string_number(s: str) -> None|int:
    for ix,str_num in enumerate(str_nums):
        if s.startswith(str_num):
            return ix+1
    return None
        
with open('input.txt', 'r', encoding='utf-8') as infile:
    total = 0
    for line in infile:
        first: None|int = None
        last: None|int = None
        for ix,c in enumerate(line):
            if c.isdigit():
                if first is None:
                    first = int(c)
                last = int(c)
            else:
                s_num = check_string_number(line[ix:])
                if s_num:
                    if first is None:
                        first = s_num
                    last = s_num
        total += first * 10 + last
    print(total)