import math
import logging
import time

class Map(object):
    def __init__(self):
        self.asteroids = set()
        self.dist_cache = {}
        self.norm_cache = {}
        self.collision_cache = set()

    def read(self, filename):
        rows = 0
        cols = 0
        with open(filename, "r") as infile:
            rows = 0
            for y, line in enumerate(infile):
                cols = 0
                for x, char in enumerate(line.strip()):
                    if char != ".":
                        self.asteroids.add((x, y))
                    cols += 1                    
                rows += 1
                
        self.rows = rows
        self.cols = cols
    
    def _distance(self, x1, y1, x2, y2):  
        key = None
        if x1 < x2:
            key = (x1,y1,x2,y2)
        else:
            key = (x2,y2,x1,y1)
        if key in self.dist_cache:
            return self.dist_cache[key]
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
        self.dist_cache[key] = dist
        return dist  
    
    def _normalized(self, a):
        key = (a[0],a[1])
        if key in self.norm_cache:
            return self.norm_cache[key]
        n = []
        length = math.sqrt(a[0]**2 + a[1]**2)
        n = [a[0] / length, a[1] / length]
        self.norm_cache[key] = n
        return n

    def _equal_directions(self, dir1, dir2):
        d1 = [int(x*1000) for x in dir1]
        d2 = [int(x*1000) for x in dir2]
        return d1 == d2

    def count_detected_astroids(self, x1, y1):
        num_detected = 0

        collided_with = set()

        #logging.debug("Testing from {},{}".format(x1,y1))

        for x2,y2 in self.asteroids:
            if x1 == x2 and y1 == y2:
                continue

            #logging.debug("..testing against {},{}".format(x2,y2))

            collision_key = (x1,y1,x2,y2)
            if collision_key in self.collision_cache:
                num_detected += 1
                collided_with.add((x2,y2))
                #logging.debug("..YES, cached")
                continue

            dist = self._distance(x1, y1, x2, y2)
            direction = self._normalized([(x2-x1), (y2-y1)])
            
            collided = False
            min_collide_distance = None
            current_collider = None

            for x3, y3 in self.asteroids:
                #logging.debug("....Checking if {},{} is on the way".format(x3,y3))
                if (x3 == x2 and y3 == y2) or (x3 == x1 and y3 == y1):
                    #logging.debug("......NOPE, dupe")
                    continue

                new_dist = self._distance(x1, y1, x3, y3)
                if new_dist > dist or \
                    (min_collide_distance is not None and new_dist > min_collide_distance):
                    #logging.debug("......NOPE, too far")
                    continue

                new_direction = self._normalized([(x3-x1), (y3-y1)])

                if self._equal_directions(new_direction, direction):
                    if min_collide_distance is None or new_dist < min_collide_distance:
                        #logging.debug("......YES")
                        min_collide_distance = new_dist
                        current_collider = (x3,y3)
                    else:
                        #logging.debug("......NOPE, found closer already")
                        pass
                else:
                    #logging.debug("......NO")
                    pass

            if current_collider:
                if current_collider not in collided_with:
                    collided_with.add(current_collider)
                    #logging.debug("....collided with {},{} -----------------------------------".format(current_collider[0], current_collider[1]))
                    num_detected += 1
                else:
                    #logging.debug("....no new collision found! -------------------------------")
                    pass
            else:
                if (x2,y2) not in collided_with:
                    collided_with.add((x2,y2))
                    #logging.debug("....collided with {},{} -----------------------------------".format(x2,y2))            
                    num_detected += 1
                else:
                    #logging.debug("....no new collision found! -------------------------------")
                    pass

                

        for m in collided_with:        
            key = (x1,y1,m[0],m[1])
            self.collision_cache.add(key)
            key = (m[0],m[1],x1,y1)
            self.collision_cache.add(key)
        return len(collided_with)

    def is_empty(self, x, y):
        if (x,y) in self.asteroids:
            return False
        return True

    def get_max_detections(self):
        max_detected = 0
        max_pos = None
        for x,y in self.asteroids:
            n = self.count_detected_astroids(x,y)
            if n > max_detected:
                max_detected = n
                max_pos = (x,y)
        return max_pos, max_detected

#logging.basicConfig(level=#logging.debug)
logging.basicConfig(level=logging.INFO)

m = Map()
# input3, 1.073 sek
# input4, 1.099 sek
# input5, 2.12 sek
# input6, 479 sek

# BORTKOMMENTERAD DEBUG:
# input3, 0.375 sek
# input4, 0,372 sek
# input5, 0,726 sek
# input6, 156 sek
# input, 346 sek
m.read("input")

#logging.info(m.count_detected_astroids(0, 0))
# for y in range(m.rows):
#     s = ""
#     for x in range(m.cols):
#         if m.is_empty(x, y):
#             s += "."
#         else:
#             s += str(m.count_detected_astroids(x,y))
#     logging.info(s)

n = time.perf_counter()
print(m.get_max_detections())
n2 = time.perf_counter()
print("Time: {}".format(n2-n))
