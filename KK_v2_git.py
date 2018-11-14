import random

#This is the family member class to keep track of information
#Name and email are self explanitory
#Family is the number that identifies the family they belong to when matching
#kidKKs is the list of KKs as they are added
#kidKK_num is the amount of kidKKs they can recieve (decreases as they gain kidKKs)

class Fmemb:
    def __init__(self, string, identifier, email, number):
        self.family = identifier
        self.name = string
        self.email = email
        self.kidKKs = []
        self.kidKK_num = int(number)
    def __eq__(self, other):
        return self.family == other.family and self.name == other.name

    def __hash__(self):
        return hash(self.name + ',' + str(self.family))

    def __str__(self):
        return str(self.family) + ' ' + self.name + ' ' + self.email

#This is the kid class, contains their family identifying number and name
class kid:
    def __init__(self, string, identifier):
        self.family = identifier
        self.name = string


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

#Sorts the list of families and removes empty families
def sort_clean(list):
    for i in list:
        if len(i) == 0:
            list.remove(i)
    return sorted(list, key=lambda family: len(family), reverse=True)

#Gives each family member a KK, and should always form a continuous loop
#This function takes the list that contains other lists that represent families (with the fmemb class)
#It should work as long as the largest family has less members than the sum of all the other families' at the beginning

#Starts by:
#   Sorts and removes empty list, creates the end dictionary, determines a starting group and member,
#   Defines an original group and original member (for when the loop ends)
#
#How the loop works:
#If the length of the sorted list > 1 (end condition is there being 1 family left with 1 member(original memb))
#
#Conditions of the loop:
#
#There are 3 conditions written to make sure the macthes are continuous and is random, based on the length of the
#group that is starting in the loop and whether or not the starting member is in the original or largest group
#(the list is sorted by family member size each loop)
#
#1. The first case is if the first picked family member's family size is equal to the sum of all the others minus 1 and
#       your starting member is not in the origin group
#   1a. This is to ensure that at the end there is at least 1 person to match to the original member at the end
#
#2. The second case is if the group with the most people is equal to the sum of all the other groups and the starting member
#       is not in the largest group
#   2a. This case is to ensure that one group doesn't have an unmatchable amount of members at the end
#       and it matches your starting member with one from the original group
#
#3. This is all other cases where the previous two don't apply
#   3a. In this condition it choose a random family to choose a random pairing member with and it matches your
#       starting member with a random member from the largest group

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

#This function matches kidKKs to each member

def match_kids(fmembs_dict, kid_list):
    list1 = []  #list of people who can receive kid KKs
    list2 = []  #list of people that have received and can take more (to refresh list 1)
    for memb in fmembs_dict:    #creates first list of adults that can take kid KKs
        if memb.kidKK_num > 0:
            list1.append(memb)
    kid_list = sort_clean(kid_list)
    while len(kid_list) > 0:
        if not list1:       #if list 1 is empty it is replaced by next list of eligible adults
            list1 = list2
            list2 = []
        child = random.choice(kid_list[0])
        adult = random.choice(list1)
        if child.family == adult.family:
            continue
        else:
            adult.kidKKs.append(child.name)
            list1.remove(adult)     #removes adult given child and adds to list of those with kids added
            kid_list[0].remove(child)  # removes kid since matches
            adult.kidKK_num = adult.kidKK_num - 1   #lowers kid num to keep track of kid additions
            if adult.kidKK_num > 0: #adds adult to next list to loop through if can accept more kids
                list2.append(adult)
        kid_list = sort_clean(kid_list)

#Takes the dictionary of pairs and creates a csv for easy manipulation and checking
def create_csv(dict):
    csv = []
    for i, j in dict.items():
        csv.append([i.name, j.name, i.email, ','.join(i.kidKKs)])    #Changed to have kid KKs
    return csv
