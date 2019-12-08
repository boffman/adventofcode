
class Orbit(object):
    def __init__(self):
        self.parent = None
        self.children = []
    
    def set_parent(self, parent):
        self.parent = parent
    
    def add_child(self, child):
        self.children.append(child)

    def get_num_orbits(self):
        if not self.parent:
            return 0
        num = self.parent.get_num_orbits()
        return num + 1        

orbits = {}

with open("input") as infile:
    for l in infile:
        parent_name, child_name = l.strip().split(")")
        parent = None
        child = None
        if parent_name in orbits:
            parent = orbits[parent_name]
        else:
            parent = Orbit()
            orbits[parent_name] = parent

        if child_name in orbits:
            child = orbits[child_name]
        else:
            child = Orbit()
            orbits[child_name] = child
        
        child.set_parent(parent)
        parent.add_child(child)

tot_num_orbits = 0
for name,orbit in orbits.items():
    tot_num_orbits += orbit.get_num_orbits()

print(tot_num_orbits)

        
    