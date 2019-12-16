from collections import namedtuple
import itertools
import math

#Vector3 = namedtuple("Vector3", ('x','y','z'))
class Vector3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def abs_sum(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

class Moon(object):
    def __init__(self, name, vector3pos):
        self.name = name
        self.pos = vector3pos
        self.vel = Vector3(0,0,0)
    
    def __str__(self):
        s = "pos=<{:3d},{:3d},{:3d}>, vel=<{:3d},{:3d},{:3d}>"\
            .format(self.pos.x, self.pos.y, self.pos.z,\
            self.vel.x, self.vel.y, self.vel.z)
        return s
    
    def get_potential_energy(self):
        return self.pos.abs_sum()

    def get_kinetic_energy(self):
        return self.vel.abs_sum()
    
    def get_total_energy(self):
        return self.get_potential_energy() * self.get_kinetic_energy()

class Physics(object):
    def update_velocity(self, moon1, moon2):
        if moon1.pos.x < moon2.pos.x:
            moon1.vel.x += 1
            moon2.vel.x -= 1
        elif moon1.pos.x > moon2.pos.x:
            moon1.vel.x -= 1
            moon2.vel.x += 1

        if moon1.pos.y < moon2.pos.y:
            moon1.vel.y += 1
            moon2.vel.y -= 1
        elif moon1.pos.y > moon2.pos.y:
            moon1.vel.y -= 1
            moon2.vel.y += 1

        if moon1.pos.z < moon2.pos.z:
            moon1.vel.z += 1
            moon2.vel.z -= 1
        elif moon1.pos.z > moon2.pos.z:
            moon1.vel.z -= 1
            moon2.vel.z += 1

    def update_position(self, moon):
        moon.pos.x += moon.vel.x
        moon.pos.y += moon.vel.y
        moon.pos.z += moon.vel.z

moons = [
    Moon("Io",       Vector3(x=17, y=-9, z=4)),
    Moon("Europa",   Vector3(x=2, y=2, z=-13)),
    Moon("Ganymede", Vector3(x=-1, y=5, z=-1)),
    Moon("Callisto", Vector3(x=4, y=7, z=-7))
]
p = Physics()

for _ in range(1000):
    for pair in itertools.combinations(moons, 2):
        p.update_velocity(pair[0], pair[1])

    for moon in moons:
        p.update_position(moon)

for moon in moons:
    print(moon)

total_energy = sum([e.get_total_energy() for e in moons])
print(total_energy)