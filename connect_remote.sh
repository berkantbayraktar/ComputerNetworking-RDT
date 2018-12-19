#!/usr/bin/env bash

host=pc5.instageni.rnet.missouri.edu
user=e2098770



eval `ssh-agent -s`
ssh-add ~/.ssh/id_geni_ssh_rsa 
for port in 25571 25573 25572 25570 25574 
do
    gnome-terminal -x bash -c "ssh ${user}@${host} -p ${port};exec bash" #destination
done
