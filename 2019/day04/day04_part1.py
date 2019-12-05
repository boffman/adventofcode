def is_valid(input):
    sinp = str(input)
    slen = len(sinp)
    if slen != 6:
        return False
    has_dupe = False
    for ix in range(slen-1):
        if sinp[ix] > sinp[ix+1]:
            return False
        if sinp[ix] == sinp[ix+1]:
            has_dupe = True
    return has_dupe

num_valid = 0
ix = 372037
while ix <= 905157:
    if is_valid(ix):
        num_valid += 1
    ix += 1
print(num_valid)