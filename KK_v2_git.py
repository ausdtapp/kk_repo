import random

#This is the family member class which contains their name, family identifying number, and email
class Fmemb:
    def __init__(self, string, identifier, email):
        self.family = identifier
        self.name = string
        self.email = email

    def __eq__(self, other):
        return self.family == other.family and self.name == other.name

    def __hash__(self):
        return hash(self.name + ',' + str(self.family))

    def __str__(self):
        return str(self.family) + ' ' + self.name + ' ' + self.email

#Finds the location of a member's family's position in the family list
def find_fam_loc(memb, list):
    for i in range(len(list)):
        if memb in list[i]:
            return i
    return 'error'

#Gets the total amount of family members in the family list
def sum_fams(list):
    sum = 0
    for i in list:
        sum += len(i)
    return sum

#Sorts the list of families
def sort_clean(list):
    for i in list:
        if len(i) == 0:
            list.remove(i)
    return sorted(list, key=lambda family: len(family), reverse=True)

#Gives each family member a KK, and should always form a continuous loop
def match_members(family_list):
    sorted_list = sort_clean(family_list)
    pairs_dict = {}
    start_group = sorted_list[random.choice(range(len(sorted_list)))]
    start_memb = start_group[random.choice(range(len(start_group)))]
    original_memb = start_memb
    origin_group_loc = find_fam_loc(original_memb, sorted_list)
    origin_group = sorted_list[origin_group_loc]
    start_group_loc = find_fam_loc(start_memb, sorted_list)
    while len(sorted_list) > 1:
        if len(origin_group) == sum_fams(sorted_list) - 1 and (start_memb not in origin_group):
            pair_memb = origin_group[random.choice(list(range(len(origin_group))))]
            pairs_dict[start_memb] = pair_memb
            sorted_list[start_group_loc].remove(start_memb)
            start_memb = pair_memb
            sorted_list = sort_clean(sorted_list)
            start_group_loc = find_fam_loc(start_memb, sorted_list)
        elif len(sorted_list[0]) == sum_fams(sorted_list[1:]) and (start_memb not in sorted_list[0]):
            pair_memb = sorted_list[0][random.choice(list(range(len(sorted_list[0]))))]
            pairs_dict[start_memb] = pair_memb
            sorted_list[start_group_loc].remove(start_memb)
            start_memb = pair_memb
            sorted_list = sort_clean(sorted_list)
            start_group_loc = find_fam_loc(start_memb, sorted_list)
        else:
            start_group = sorted_list.pop(start_group_loc)
            rand_fam = sorted_list[random.choice(list(range(len(sorted_list))))]
            pair_memb = rand_fam[random.choice(range(len(rand_fam)))]
            pairs_dict[start_memb] = pair_memb
            sorted_list.insert(start_group_loc, start_group)
            sorted_list[start_group_loc].remove(start_memb)
            start_memb = pair_memb
            sorted_list = sort_clean(sorted_list)
            start_group_loc = find_fam_loc(start_memb, sorted_list)
    pairs_dict[start_memb] = original_memb
    return pairs_dict
