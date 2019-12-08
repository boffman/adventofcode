
class Orbit(object):
    def __init__(self, name):
        self.parent = None
        self.children = []
        self.name = name
    
    def set_parent(self, parent):
        self.parent = parent
    
    def add_child(self, child):
        self.children.append(child)

    def get_num_orbits(self):
        if not self.parent:
            return 0
        num = self.parent.get_num_orbits()
        return num + 1        

    def get_orbital_transfers(self, dst_name, visited=set()):
        if self.name == dst_name:
            return 0

        if self.children:
            for child in self.children:
                if not child in visited:
                    branch_visited = set()
                    branch_visited.add(self)
                    num_transfers = child.get_orbital_transfers(dst_name, branch_visited)
                    if num_transfers > -1:
                        print("Visited {}".format(self.name))
                        visited.update(branch_visited)
                        return num_transfers + 1

        if self.parent:
            if not self.parent in visited:
                branch_visited = set()
                branch_visited.add(self)
                num_transfers = self.parent.get_orbital_transfers(dst_name, branch_visited)                
                if num_transfers > -1:
                    print("Visited {}".format(self.name))
                    visited.update(branch_visited)
                    return num_transfers + 1

        return -1




orbits = {}

with open("input") as infile:
    for l in infile:
        parent_name, child_name = l.strip().split(")")
        parent = None
        child = None
        if parent_name in orbits:
            parent = orbits[parent_name]
        else:
            parent = Orbit(parent_name)
            orbits[parent_name] = parent

        if child_name in orbits:
            child = orbits[child_name]
        else:
            child = Orbit(child_name)
            orbits[child_name] = child
        
        child.set_parent(parent)
        parent.add_child(child)

src = orbits["YOU"].parent
dst = orbits["SAN"].parent
print("Traveling from {} to {} ...".format(src.name, dst.name))
num_orbital_transfers = src.get_orbital_transfers(dst.name)
print(num_orbital_transfers)

        
    