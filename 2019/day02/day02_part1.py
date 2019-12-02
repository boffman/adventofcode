def handle_opcode_1(ix, opcodes):
    num1_pos = opcodes[ix+1]
    num2_pos = opcodes[ix+2]
    dst_pos = opcodes[ix+3]
    opcodes[dst_pos] = opcodes[num1_pos] + opcodes[num2_pos]
    return ix + 4

def handle_opcode_2(ix, opcodes):
    num1_pos = opcodes[ix+1]
    num2_pos = opcodes[ix+2]
    dst_pos = opcodes[ix+3]
    opcodes[dst_pos] = opcodes[num1_pos] * opcodes[num2_pos]
    return ix + 4

def restore_gravity_assist_program(opcodes):
    opcodes[1] = 12
    opcodes[2] = 2

opcodes = None
with open("input.txt", "r") as infile:
    for l in infile:
        opcodes = [int(x) for x in l.strip().split(",")]

restore_gravity_assist_program(opcodes)

num_opcodes = len(opcodes)
ix = 0
while True:
    cur_opcode = opcodes[ix]
    if cur_opcode == 1:
        ix = handle_opcode_1(ix, opcodes)
    elif cur_opcode == 2:
        ix = handle_opcode_2(ix, opcodes)
    elif cur_opcode == 99:
        break
    else:
        raise Exception("Unknown opcode at position {}: {}".format(ix, cur_opcode))

print(opcodes[0])

