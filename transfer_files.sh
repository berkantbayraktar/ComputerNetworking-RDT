#!/bin/bash

directory=/home/ilker/Desktop/courses/435-network/tp-part2/ceng435-tp-part2/
host=pc4.instageni.rnet.missouri.edu
user=e2098770


eval `ssh-agent -s`
ssh-add ~/.ssh/id_geni_ssh_rsa 


scp -P 25571 ${directory}'destination.py' ${user}@${host}':/users/'${user}
scp -P 25571 ${directory}'compute_distance.py' ${user}@${host}':/users/'${user}
scp -P 25571 ${directory}'diff_match_patch.py' ${user}@${host}':/users/'${user}
scp -P 25571 ${directory}'demofile.txt' ${user}@${host}':/users/'${user}
#scp -P 25572 ${directory}'r1.py' ${user}@${host}':/users/'${user}
#scp -P 25573 ${directory}'r2.py' ${user}@${host}':/users/'${user}
scp -P 25570 ${directory}'broker.py' ${user}@${host}':/users/'${user}
scp -P 25574 ${directory}'source.py' ${user}@${host}':/users/'${user}
#scp -P 25574 ${directory}'demofile.txt' ${user}@${host}':/users/'${user}
scp -P 25574 ${directory}'demofile.txt' ${user}@${host}':/users/'${user}
