from collections import namedtuple
import itertools
import math
import time

#Vector3 = namedtuple("Vector3", ('x','y','z'))
class Vector3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def abs_sum(self):
        return abs(self.x) + abs(self.y) + abs(self.z)
    
    def __str__(self):
        return ",".join([str(self.x), str(self.y), str(self.z)])

class Moon(object):
    def __init__(self, vector3pos):
        self.pos = vector3pos
        self.vel = Vector3(0,0,0)
    
    def __str__(self):
        return "|".join([str(self.pos),str(self.vel)])
    
    def print(self):
        print("pos=<{:3d},{:3d},{:3d}>, vel=<{:3d},{:3d},{:3d}>"\
            .format(self.pos.x, self.pos.y, self.pos.z,\
            self.vel.x, self.vel.y, self.vel.z))

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

class Universe(object):
    def __init__(self, physics):
        # # 2772 steps
        # self.moons = [
        #     Moon(Vector3(x=-1, y=0, z=2)),
        #     Moon(Vector3(x=2, y=-10, z=-7)),
        #     Moon(Vector3(x=4, y=-8, z=8)),
        #     Moon(Vector3(x=3, y=5, z=-1))
        # ]
        # # 136136 steps
        # self.moons = [
        #     Moon(Vector3(x=0, y=0, z=2)),
        #     Moon(Vector3(x=2, y=-10, z=-7)),
        #     Moon(Vector3(x=4, y=-8, z=8)),
        #     Moon(Vector3(x=3, y=4, z=-1))
        # ]
        # # ??? steps (> 5M)
        # self.moons = [
        #     Moon(Vector3(x=0, y=0, z=2)),
        #     Moon(Vector3(x=2, y=-10, z=-7)),
        #     Moon(Vector3(x=4, y=-8, z=7)),
        #     Moon(Vector3(x=3, y=4, z=-1))
        # ]
        # # 4686774924 steps
        # self.moons = [
        #     Moon(Vector3(x=-8, y=-10, z=0)),
        #     Moon(Vector3(x=5, y=5, z=10)),
        #     Moon(Vector3(x=2, y=-7, z=3)),
        #     Moon(Vector3(x=9, y=-8, z=-3))
        # ]
        # challenge
        self.moons = [
            Moon(Vector3(x=17, y=-9, z=4)),
            Moon(Vector3(x=2, y=2, z=-13)),
            Moon(Vector3(x=-1, y=5, z=-1)),
            Moon(Vector3(x=4, y=7, z=-7))
        ]

        self.physics = physics

    def update(self):
        for pair in itertools.combinations(self.moons, 2):
            p.update_velocity(pair[0], pair[1])

        for moon in self.moons:
            p.update_position(moon)

    def print_moons(self):
        for m in self.moons:
            m.print()

    def __str__(self):
        return ";".join([str(m) for m in self.moons])


p = Physics()

u = Universe(p)

u.print_moons()

n = time.perf_counter()

counter = 0
previous_states = set()
u_str = str(u)
while u_str not in previous_states:
    previous_states.add(u_str)
    u.update()
    u_str = str(u)
    counter += 1
    if counter % 100000 == 0:
        print(counter)
        n2 = time.perf_counter()
        print("Time: {}".format(n2-n))

n2 = time.perf_counter()
print("Time: {}".format(n2-n))

print("It took {} iterations:".format(counter))
u.print_moons()
# for _ in range(1000):
#     for pair in itertools.combinations(moons, 2):
#         p.update_velocity(pair[0], pair[1])

#     for moon in moons:
#         p.update_position(moon)

# for moon in moons:
#     print(moon)

# total_energy = sum([e.get_total_energy() for e in moons])
# print(total_energy)