from collections import defaultdict

def is_valid(input):
    sinp = str(input)
    slen = len(sinp)
    if slen != 6:
        return False
    dupes = defaultdict(int)
    for ix in range(slen-1):
        if sinp[ix] > sinp[ix+1]:
            return False
        if sinp[ix] == sinp[ix+1]:
            dupes[sinp[ix]] += 1
    if dupes:
        for v in dupes.values():
            if v == 1:
                return True
    return False

num_valid = 0
ix = 372037
while ix <= 905157:
    if is_valid(ix):
        num_valid += 1
    ix += 1
print(num_valid)