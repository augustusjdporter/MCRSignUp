import csv
import os
import random
from shutil import copyfile


this_exchange = "Linacre"
number_of_people_to_accept = 3

def weighted_choice(sign_up_dictionary):
    total_weight = 0.
    for person in sign_up_dictionary:
        total_weight += sign_up_dictionary[person]
    r = random.uniform(0., total_weight)
    upto = 0.
    for person in sign_up_dictionary:
        if upto + sign_up_dictionary[person] >= r:
            return person
        upto += sign_up_dictionary[person]
    assert False, "Shouldn't get here"

print("Gus is the best social secretary.")

oldSignUpFileName = "SignUpHistory.csv"
newSignUpFileName = "SignUpHistory.csv"


signUpsFileName = "Linacre (Responses) - Form Responses 1.csv"


old_sign_ups = dict()
previous_exchanges = dict()
if os.path.isfile(oldSignUpFileName):
    copyfile(oldSignUpFileName, "{}_save.csv".format(oldSignUpFileName.replace(".csv", "")))
    with open(oldSignUpFileName) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            print(row[0], row[1])
            old_sign_ups[row[0]] = float(row[1])
            previous_exchanges[row[0]] = row[2]

new_sign_ups = dict()
print("\nNew Sign Ups")
with open(signUpsFileName) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if "@pmb.ox.ac.uk" in row[2]:
            print(row[2])
            new_sign_ups[row[2]] = 1.
            if row[2] in old_sign_ups:
                new_sign_ups[row[2]] = 1./(old_sign_ups[row[2]] + 1.)


accepted_sign_ups = []

while len(accepted_sign_ups) < number_of_people_to_accept and len(new_sign_ups) > 0:
    person = weighted_choice(new_sign_ups)
    accepted_sign_ups.append(person)
    del new_sign_ups[person]

print("\n***** ACCEPTED SIGN UPS *****")
for accepted_person in accepted_sign_ups:
    print(accepted_person)
    if accepted_person in old_sign_ups:
        old_sign_ups[accepted_person] += 1.
    else:
        old_sign_ups[accepted_person] = 1.

    if accepted_person in previous_exchanges:
        previous_exchanges[accepted_person] += "{}.".format(this_exchange)
    else:
        previous_exchanges[accepted_person] = "{}.".format(this_exchange)

f = open(newSignUpFileName, "w")
for person in old_sign_ups:
    f.write("{}, {},{}\n".format(person, old_sign_ups[person], previous_exchanges[person]))
f.close()

