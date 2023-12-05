with open('input.txt', 'r', encoding='utf-8') as infile:
    total = 0
    for line in infile:
        first: None|int = None
        last: None|int = None
        for c in line:
            if c.isdigit():
                if first is None:
                    first = int(c)
                last = int(c)
        total += first * 10 + last
    print(total)