#! /usr/bin/env python3
# mission_05_solver.py - Decrypts text from HTS Realistic Mission 6.

import logging

logging.basicConfig(level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')

encrypted_text = open('mission_05_crypt.txt')
triplet = []
triplet_sums = []
c = 0

for line in encrypted_text:
    # Trim each line to the line break.
    l = line.split('\n')[0]
    # logging.debug(l)
    for i in l.split('.'):
        # logging.debug(i)
        # Splitting each line by the line break adds a space in each line.
        # This makes sure the space is excluded going forward.
        if i != '':
            # Add each int value to the triplet list.
            triplet.append(int(i))
            c += 1
            if c % 3 == 0:
                # Once the list has three values, get the sum, which is what we
                # really want for brute force decryption.
                triplet_sums.append(sum(triplet))
                # logging.debug(triplet_sums)
                triplet = []

# Brute force fun.
for diff in range(max(triplet_sums)-255, min(triplet_sums)+1):
    # The number appended to each file is the password combination.
    # When we find the file with the correct decryption, the number appended
    # will be the password.
    file_name = 'bruteforce-%s.txt' % diff
    brute_force = open(file_name, 'w')
    for i in triplet_sums:
        # Subtract the password combination from each character, then convert
        # it to a Unicode character using chr(). One of these combinations will
        # correctly decrypt the file.
        brute_force.write(chr(i-diff))
    brute_force.close()

encrypted_text.close()