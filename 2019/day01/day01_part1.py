def calc_fuel(mass):
    fuel = int(mass / 3) - 2
    return fuel

with open("input.txt") as infile:
    fuel_sum = 0
    for line in infile:
        mass = int(line.strip())
        fuel = calc_fuel(mass)
        fuel_sum += fuel
    print(fuel_sum)
