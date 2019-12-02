def calc_fuel(mass):
    fuel = int(mass / 3) - 2
    return fuel

def calc_total_fuel(mass):
    tot_fuel = 0
    fuel = mass
    while True:
        fuel = calc_fuel(fuel)
        if fuel <= 0:
            break
        tot_fuel += fuel
    return tot_fuel

with open("input.txt") as infile:
    fuel_sum = 0
    for line in infile:
        mass = int(line.strip())
        fuel = calc_total_fuel(mass)
        fuel_sum += fuel
    print(fuel_sum)
