res_x = 25
res_y = 6
layers = []
min_num_zeroes = None
min_ix = -1
ix = -1
with open("input", "r") as img_file:
    eof = False
    while not eof:
        layer = img_file.read(res_x * res_y)
        if layer is None or not layer.strip():
            eof = True
        else:
            layers.append(layer)
            ix += 1

            num_zeroes = 0
            for b in layer:
                if b == "0":
                    num_zeroes += 1
            if min_num_zeroes is None or num_zeroes < min_num_zeroes:
                min_num_zeroes = num_zeroes
                min_ix = ix

num_ones = 0
num_twos = 0
for b in layers[min_ix]:
    if b == "1":
        num_ones += 1
    elif b == "2":
        num_twos += 1

print(num_ones * num_twos)

