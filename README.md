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

#### Question 1 : What is the difference between a VM and a container ?

VM stands for Virtual machine, it is a type of machine virtualization in which we are able to run multiple operating systems either directly 
on bare-metal hardware or on top of a suitable guest Operating System. It requires a special type of software called "Hypervisor" that 
is capable of managing multiple instances of full operating systems. There are two types of hypervisors, Type-1 hypervisor which is bare-metal hypervisor, 
it is installed directly on the hardware i.e: Hyper-V; Type-2 hypervisor which requires a guest operating system i.e: Vmware Workstation and/or virtualbox from oracle.


Each VM, is a completely isolated environment with its own host OS + user space libraries + installed apps. VM technology was introduced 
to better utilize system resources but it introduced redundancy , consumed more storage and many management bottlenecks for system administrators and didn't completely solve 
the problem of scientific reproducibility (i.e. in Bioinformatics) 
due to numerical instability among different software libraries versions. for this, operating system virtualization was introduced.

A container is a lightweight virtualization in which it requires a suitable host operating system to provide isolation as well as 
common system capabilities (kernel). Linux has introduced the concept of namespaces which led to spawning of containers technology. 
a linux namespace is an isolated micro-environment within the operating system with its own file system, memory and processes space.

A container only shares kernel with the host operating system but provides virtualization for file system , memory and processes; 
besides, other system and user-space libraries in addition 
to the main running application(s). It requires only a container daemon service which manages different containers.

i.e. Docker and Singularity (the most common)


#### Question 2 : gocd,cfengine, ansible and puppet ?

gocd: I didn't use this tool before. but I have used a similar one called "Jenkins" and bitbucket pipelining feature. These are tools that 
help us as software developers to continuously test our software as it being built and deploy it on different deployment environments.

cfengine: I didn't use this tool before.

ansible and puppet are decentralized configuration management tools which help deploying software tools and 
dependent system libraries across many servers and/or cloud infrastructure all at once.

I have used ansible before as it is built in python and it integrates seamlessly with our internal python systems.
We have used it to deploy updated versions of the software and its related dependencies through a single configuration file and pushing 
that to all running cloud EC2 instances all at once. 


#### Question 3: Give 3 easy wins to reduce AWS compute costs ? 

From my experience, These are some of the quick wins that could reduce AWS compute costs substantially.

-  Utilizing cost management interface to determine low-utilized EC2 instances by averaging out the peaks of hyperactivities 
to determine the right sizing for that particular EC2 instance and probably down-sizing it, I have utilized AWS toolkit in 
python and I have wrote a simple python daemonized script that performs these kind of statistical calculation.

- Moving infrequently accessed data to AWS Glacier instead of S3 this substantially reduces AWS cost.

- Use Spot instances for fault-tolerant or short computing tasks.

I had some experiences monitoring my own AWS Cloud for one of my personal projects, I have used ganglia + Grafana to monitor and visualize my 7 cloud EC2 instances.


## Coding Challenge 

#### Question 1: XML Task

```python
#!/usr/bin/env python
from bs4 import BeautifulSoup as bs
from typing import Mapping
from collections import defaultdict
import lxml
from tabulate import tabulate


def parse_xml(xml_file: str) -> Mapping[str,list]:
    authors = defaultdict(list)
    if xml_file is None or len(xml_file) < 1:
        raise Exception("Xml file path should not be empty")
    with open(xml_file, "r") as input:
        contents = input.read()
    try:
        xml = bs(contents, "lxml")
        # find all articles
        found_articles = xml.find_all("article")
        if len(found_articles) < 1:
            return authors
        for article in found_articles:
            title = article.find("articletitle").text
            # find all authors contributed to this article
            for author in article.find_all("author"):
                firstName = author.find("forename").text
                lastName = author.find("lastname").text
                authors[f"{lastName},{firstName}"].append(title)

    except Exception as e:
        raise e
    finally:
        return authors


def main():
    xml_file = "articles.xml"
    authors = parse_xml(xml_file)
    # get the author names and sort them chronologically 
    author_names = sorted(list(authors.keys()))
    rows = []
    for i in range(len(author_names)):
        row = [0] * len(author_names)
        first_set = authors[author_names[i]]
        for j in range(len(author_names)):
            second_set = authors[author_names[j]]
            # get the length of the intersection between the two authors' articles
            row[j] = len(set(first_set) & set(second_set))
        rows.append([author_names[i]] + row)
    table = tabulate(rows,headers=["..."]+author_names,tablefmt="fancy_grid")
    print(table)



if __name__ == '__main__':
    main()

```

#### Question 2: How to write a test case for the above XML task ?

There are two strategies. These two strategies require predefined result matrix (Truth matrix) to compare the output with it 
but they differ on the assertion method used.

Both strategies require that the predefined test matrix  and the output matrix to be sorted in the same manner.

- The first strategy would be to loop over each row in both the truth matrix and the result matrix  and test whether the two numbers equal, if they equal set the current item to True otherwise False.
then check if all items are true in the resulting list for each row or not. If all are True, then assertion succeeds otherwise False. 
```python 
[[2, 1, 1, 0], [1, 3, 1, 1], [1, 1, 2, 0], [0, 1, 0, 1]]
``` 
- The second strategy is an easier and more efficient one. in this method, we will use `numpy` package and test for equality using `np.equal` coupled with `np.all`.

for instance, something like this

```python
import numpy as np

truth = [[2, 1, 1, 0], [1, 3, 1, 1], [1, 1, 2, 0], [0, 1, 0, 1]]
outcome = [[2, 1, 1, 0], [1, 3, 1, 1], [1, 1, 2, 0], [0, 1, 0, 1]]

truth_matrix = np.matrix(truth)
outcome_matrix = np.matrix(outcome)
assert np.all(np.equal(truth_matrix,outcome_matrix))
```

#### Question 3: Scaling out XML task....

The problem is XML is a very verbose Text markup language. To this end, to represent 22 million articles using XML, the resulting file will be very huge to be read fully in memory at once to begin parsing it as we did in this example.








