İlker Ayçiçek - 2098770

Berkant Bayraktar- 2098796


We have 3 different python files. Namely,

* destination.py
* broker.py
* source.py

Each of them is  uploaded different vm machines with respect to their name.
(i.e. destination into vm machine `d` etc.)

First , we run ssh-agent to add ssh public key :
```
    eval `ssh-agent -s`
    ssh-add ~/.ssh/id_geni_ssh_rsa 
```
After these commands, we enter our passphrase. Then use scp to upload files 
to remote virtual machines by :

```
    scp -P <port-number-of-the-machine> <path-to-your-file> berkantb@pc4.instageni.rnet.missouri.edu
    :/users/berkantb
```

* path-to-your-file: directory of the file that you want to copy
* host : target hostname {e.g. pc4.instageni.rnet.missouri.edu}
* user : GENI username (e.g. berkantb)

After we upload our files to each machine, we connect to machines via ssh.

```
   ssh -i <path-to-your-private-key-file> berkantb@pc4.instageni.rnet.missouri.edu
    -p <port-number-of-the-machine>
```
* path-to-your-private-key-file : directory of the private key for GENI 
* host : target hostname {e.g. pc4.instageni.rnet.missouri.edu}
* user : GENI username (e.g. berkantb)


We connected to machines.Then, for time syncronization between
machines we use ntp on source and destination machines:

```
sudo service ntp stop
sudo ntpdate 1.ro.pool.ntp.org

```
We checked if it is syncronized or not by :
```
timedatectl status
```
You don't need to synchronize again. We already did.It is enough to
do it once. After synchronizing,we ran our socket programs on each machine:
```
    python destination.py
    python broker.py
    python source.py
```

In our `source.py`, we take input from our predefined file. It automatically,
parses file into chunks and send them one by one. You can find end-to-end delay
of each packets and average end-to-end delay of these packets, 
in the standard output of `source` node.

After finding correct internet interfaces of nodes by ```ifconfig``` command,

We set routing tables of broker and the destination nodes as follows:

At Broker(b) machine,

If destination is 10.10.3.2(destination node) go from the r1 link
```bash
route add -net 10.10.3.2 netmask 255.255.255.255 gw 10.10.2.2 dev eth3
```
If destination is 10.10.5.2(destination node) go from the r2 link
```bash
route add -net 10.10.5.2 netmask 255.255.255.255 gw 10.10.4.2 dev eth1
```

At Destination (d) machine ,
If destination is 10.10.1.2(broker node) go from the r1 link
```bash
route add -net 10.10.1.2 netmask 255.255.255.255 gw 10.10.3.1 dev eth1
```

If destination is 10.10.2.1(broker node) go from the r2 link
```bash
route add -net 10.10.2.1 netmask 255.255.255.255 gw 10.10.5.1 dev eth2
```

After making routing table work ,

For experiment 1:

* part a)

* We applied 0.5% packet loss for all links between broker and destination 

* For r1-destination link , run this at destination node :
```
    tc qdisc add dev eth1 root netem loss 0.5% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%
```

* For r2-destination link, run this at destination node:
```
    tc qdisc add dev eth2 root netem loss 0.5% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%
```

* For r1-broker link, run this at r1 node :
```
    tc qdisc add dev eth1 root netem loss 0.5% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%
```
* For r2 link, run this at r2 node:
```
    tc qdisc add dev eth1 root netem loss 0.5% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%
```

* part b)

* We applied 10% packet loss for all links between broker and destination 

* For r1-destination link , run this at destination node :
```
    tc qdisc add dev eth1 root netem loss 10% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%
```

* For r2-destination link, run this at destination node:
```
    tc qdisc add dev eth2 root netem loss 10% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%
```

* For r1-broker link, run this at r1 node :
```
    tc qdisc add dev eth1 root netem loss 10% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%
```
* For r2 link, run this at r2 node:
```
    tc qdisc add dev eth1 root netem loss 10% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%
```


* part c)

* We applied 20% packet loss for all links between broker and destination 

* For r1-destination link , run this at destination node :
```
    tc qdisc add dev eth1 root netem loss 20% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%
```

* For r2-destination link, run this at destination node:
```
    tc qdisc add dev eth2 root netem loss 20% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%
```

* For r1-broker link, run this at r1 node :
```
    tc qdisc add dev eth1 root netem loss 20% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%
```
* For r2 link, run this at r2 node:
```
    tc qdisc add dev eth1 root netem loss 20% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%
```

For experiment 2:

* part a)

* We applied 0.2% packet corruption for all links between broker and destination

* For r1-destination link, run this at destination :
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 0.2% duplicate 0% delay 3ms reorder 0% 0%
```
* For r2-destination link, run this at destination:
```
    tc qdisc change dev eth2 root netem loss 0% corrupt 0.2% duplicate 0% delay 3ms reorder 0% 0%
```

* For r1-broker link, run this at r1 :
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 0.2% duplicate 0% delay 3ms reorder 0% 0%
```
* For r2-broker link, run this at r2 :
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 0.2% duplicate 0% delay 3ms reorder 0% 0%
```

* part b)

* We applied 10% packet corruption for all links between broker and destination

* For r1-destination link, run this at destination :
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 10% duplicate 0% delay 3ms reorder 0% 0%
```
* For r2-destination link, run this at destination:
```
    tc qdisc change dev eth2 root netem loss 0% corrupt 10% duplicate 0% delay 3ms reorder 0% 0%
```

* For r1-broker link, run this at r1 :
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 10% duplicate 0% delay 3ms reorder 0% 0%
```
* For r2-broker link, run this at r2 :
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 10% duplicate 0% delay 3ms reorder 0% 0%
```

* part c)

* We applied 20% packet corruption for all links between broker and destination

* For r1-destination link, run this at destination :
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 20% duplicate 0% delay 3ms reorder 0% 0%
```
* For r2-destination link, run this at destination:
```
    tc qdisc change dev eth2 root netem loss 0% corrupt 20% duplicate 0% delay 3ms reorder 0% 0%
```


* For r1-broker link, run this at r1 :
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 20% duplicate 0% delay 3ms reorder 0% 0%
```
* For r2-broker link, run this at r2 :
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 20% duplicate 0% delay 3ms reorder 0% 0%
```

For experiment 3:

* part a)

* We applied 1% reorder of packets for all links between broker and destination


* For r1-destination link, run this at destination node :
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 0% duplicate 0% delay 3ms reorder 1% 50%
```
* For r2-destination link, run this at destination node:
```
    tc qdisc change dev eth2 root netem loss 0% corrupt 0% duplicate 0% delay 3ms reorder 1% 50%
```

* For r1-broker link, run this at r1 node :
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 0% duplicate 0% delay 3ms reorder 1% 50%
```
* For r2-broker link, run this at r2 node:
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 0% duplicate 0% delay 3ms reorder 1% 50%
```

* part b)

* We applied 10% reorder of packets for all links between broker and destination


* For r1-destination link, run this at destination node :
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 0% duplicate 0% delay 3ms reorder 10% 50%
```
* For r2-destination link, run this at destination node:
```
    tc qdisc change dev eth2 root netem loss 0% corrupt 0% duplicate 0% delay 3ms reorder 10% 50%
```

* For r1-broker link, run this at r1 node :
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 0% duplicate 0% delay 3ms reorder 10% 50%
```
* For r2-broker link, run this at r2 node:
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 0% duplicate 0% delay 3ms reorder 10% 50%
```


* part a)

* We applied 35% reorder of packets for all links between broker and destination


* For r1-destination link, run this at destination node :
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 0% duplicate 0% delay 3ms reorder 35% 50%
```
* For r2-destination link, run this at destination node:
```
    tc qdisc change dev eth2 root netem loss 0% corrupt 0% duplicate 0% delay 3ms reorder 35% 50%
```

* For r1-broker link, run this at r1 node :
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 0% duplicate 0% delay 3ms reorder 35% 50%
```
* For r2-broker link, run this at r2 node:
```
    tc qdisc change dev eth1 root netem loss 0% corrupt 0% duplicate 0% delay 3ms reorder 35% 50%
```


___

Then, for each experiment we calculated total time when transferring 5 MB file.

```bash
time source <filename>
```




