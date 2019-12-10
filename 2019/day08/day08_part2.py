res_x = 25
res_y = 6
layers = []
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

final_image = {}
for layer in layers:
    for y in range(res_y):
        for x in range(res_x):
            if not (x,y) in final_image or final_image[(x,y)] == "2":
                final_image[(x,y)] = layer[y * res_x + x]

for y in range(res_y):
    row_data = ""
    for x in range(res_x):
        if final_image[(x,y)] == "0":
            row_data += " "
        else:
            row_data += final_image[(x,y)]
    print(row_data)
