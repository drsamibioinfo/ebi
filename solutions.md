# EBI Challenges

## Question 1

#### what does the following python code do ?
foo function returns a list of unique random numbers within a range bounded by a numeric length parameter 
from [1,length parameter] inclusively.
#### How could the same result be achieved in a simpler way?

By taking advantage of a data structure called "Set" which only can contain unique numbers

```python
import random

def foo(length):
    if length < 0:
        raise Exception("can't accept negative numbers")
    bag = set()
    while len(bag) < length:
        bag.add(random.randint(1,length))
    return bag
```

## Question 2

#### Explain the following code. What version of java does this need? 

This code relies on stream API introduced in Java 8 

## Social Network

#### GroupA Social Network function

```python
from typing import Mapping


def findGroupA(network: Mapping[str,list], employer: Mapping[str, str]) -> []:

    if not isinstance(network, dict) or not isinstance(employer, dict):
        raise Exception("network and employer should be python dictionaries")
    if not set(network.keys()) == set(employer.keys()):
        raise Exception("Keys of network and employer should be the same")
    groupA = []
    for member, friends in network.items():
        friends_employer = [employer[x].lower() for x in friends]
        member_employer = employer[member].lower()
        if member_employer in friends_employer:
            continue
        else:
            groupA.append(member)

    return groupA
```

## DevOps

#### What is the difference between a VM and a container ?

VM stands for Virtual machine, it is a type of machine virtualization in which we are able to run multiple operating systems either directly 
on bare-metal hardware or on top of a suitable guest Operating System. It requires a special type of software called "Hypervisor" that 
is capable of managing multiple instances of full operating systems. There are two types of hypervisors, Type-1 hypervisor which is bare-metal hypervisor, 
it is installed directly on the hardware i.e: Hyper-V; Type-2 hypervisor which requires a guest operating system i.e: Vmware Workstation and/or virtualbox from oracle.


Each VM, is a completely isolated environment with its own host OS + user space libraries + installed apps. VM technology was introduced 
to better utilize system resources but it introduced many management bottlenecks for system administrators and didn't completely solve 
the problem of scientific reproducibility (i.e. in Bioinformatics) 
due to numerical instability among different software libraries versions. for this, operating system virtualization was introduced.

A container: 

