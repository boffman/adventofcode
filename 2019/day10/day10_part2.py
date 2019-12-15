import math
import logging
import time

class Map(object):
    def __init__(self):
        self.asteroids = set()
        self.dist_cache = {}
        self.norm_cache = {}
        self.collision_cache = set()
        self.asteroids_by_angle = {}
        self.zap_counter = 0
        self.zapped = set()

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

    def order_by_angle(self, pos_x, pos_y):
        for a in self.asteroids:
            angle = int(self._get_angle(pos_x, pos_y, a[0], a[1])*1000)/1000.0
            if not angle in self.asteroids_by_angle:
                self.asteroids_by_angle[angle] = []
            self.asteroids_by_angle[angle].append(a)            

    def _distance(self, x1, y1, x2, y2):  
        key = None
        if x1 < x2:
            key = (x1,y1,x2,y2)
        else:
            key = (x2,y2,x1,y1)
        if key in self.dist_cache:
            return self.dist_cache[key]
        dist = math.sqrt(float(x2 - x1)**2 + float(y2 - y1)**2)  
        self.dist_cache[key] = dist
        return dist  
    
    def _length(self, x, y):
        return math.sqrt(x**2 + y**2)

    def _normalized(self, a):
        key = (a[0],a[1])
        if key in self.norm_cache:
            return self.norm_cache[key]
        n = []
        #length = math.sqrt(a[0]**2 + a[1]**2)
        length = self._length(a[0], a[1])
        n = [a[0] / length, a[1] / length]
        self.norm_cache[key] = n
        return n

    def _equal_directions(self, dir1, dir2):
        d1 = [int(x*1000) for x in dir1]
        d2 = [int(x*1000) for x in dir2]
        return d1 == d2

    def _get_angle(self, xpos, ypos, x2, y2):
        if xpos == x2 and ypos == y2:
            return 0.0
        x1 = 0
        y1 = -1
        x2 -= xpos
        y2 -= ypos
        deg_add = 0.0
        p = x1 * x2 + y1 * y2
        l1 = self._length(x1, y1)
        l2 = self._length(x2, y2)
        f = l1 * l2
        a = p / f

        rc = math.acos(a) * 180.0 / math.pi
        if x2 < 0:
            return 360.0 - rc
        return rc

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

    def is_asteroid(self, x, y):
        if (x,y) in self.asteroids:
            return True
        return False

    def is_zapped(self, x, y):
        if (x,y) in self.zapped:
            return True
        return False

    def get_max_detections(self):
        max_detected = 0
        max_pos = None
        for x,y in self.asteroids:
            n = self.count_detected_astroids(x,y)
            if n > max_detected:
                max_detected = n
                max_pos = (x,y)
        return max_pos, max_detected

    def print_detection_map(self):
        for y in range(self.rows):
            s = ""
            for x in range(self.cols):
                if self.is_asteroid(x, y):
                    s += str(self.count_detected_astroids(x,y))
                else:
                    s += "."
            logging.info(s)

    def print_astroid_map(self):
        for y in range(self.rows):
            s = ""
            for x in range(self.cols):
                if self.is_asteroid(x, y):
                    s += "#"
                elif self.is_zapped(x, y):
                    s += "O"
                else:
                    s += "."
            print(s)

    def zap_one_lap(self, xpos, ypos):
        zapped = []
        for angle in sorted(self.asteroids_by_angle):
            astroids = self.asteroids_by_angle[angle]
            #print("angle {} : {} asteroids".format(angle, len(astroids)))
            min_distance = None
            astroid_to_zap = None
            for astroid in astroids:
                dist = self._distance(xpos, ypos, astroid[0], astroid[1])
                if min_distance is None or dist < min_distance:
                    min_distance = dist
                    astroid_to_zap = astroid
            
            if astroid_to_zap:
                # print("Zapping astroid #{}: {}".format(self.zap_counter+1, astroid_to_zap))
                astroids.remove(astroid_to_zap)
                self.asteroids.remove(astroid_to_zap)
                zapped.append(astroid_to_zap)
                self.zapped.add(astroid_to_zap)
                #print("Zapped Astroid {} is at angle {}".format(astroid_to_zap, angle))
                # self.print_astroid_map()
                # print("")
                self.zap_counter += 1
            continue
        return zapped

#logging.basicConfig(level=#logging.debug)
logging.basicConfig(level=logging.INFO)

# ((20, 19), 284)
# Time: 66.361312009
m = Map()
m.read("input")
m.print_astroid_map()
zap_pos = (20,19)
m.asteroids.remove(zap_pos)
m.order_by_angle(zap_pos[0], zap_pos[1])
zapped = []
while len(m.asteroids) > 0:
    zapped.extend(m.zap_one_lap(zap_pos[0], zap_pos[1]))
    #m.print_astroid_map()

print(len(zapped))
for n in [200]:
    print("The {} android to be vaporized is at {}".format(n,zapped[n-1]))
# for n in [1,2,3,10,20,50,100,199,200,201,299]:
#     print("The {} android to be vaporized is at {}".format(n,zapped[n-1]))
