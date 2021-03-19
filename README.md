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

We will use `numpy` package and test for equality using `np.equal` coupled with `np.all` between the truth matrix (predefined as input) and the resulting matrix from the method `get_matrix_result`

for instance, something like this

```python
import numpy as np
xml_file = "articles.xml"
truth = [[2, 1, 1, 0], [1, 3, 1, 1], [1, 1, 2, 0], [0, 1, 0, 1]]
outcome = get_matrix_result(xml_file)
truth_matrix = np.matrix(truth)
outcome_matrix = np.matrix(outcome)
assert np.all(np.equal(truth_matrix,outcome_matrix))
```

#### Question 3: Scaling out XML task....

The problem is XML is a very verbose Text markup. 
To this end, to represent 22 million articles using XML, the resulting file will be very huge to be read fully in memory at once to begin parsing it as we did in the previous example.

Instead, We can utilize some distributed solutions like Hadoop and/or Apache Spark which help in distributing the processing of large XML file into multiple mappers and reducers.

- In Apache Spark, we can either define a XSD schema to our input XML in order to overcome reading the whole file at once to infer the schema or 
we can utilize "SamplingRatio" which accepts a float between [0,1] to read parts of the file and infer its schema in chunks in case, we don't have a schema for this XML structure.

- There is another manual elaborate approach to solve this problem that runs in a single computer, In my case, I would implement my own SAX  parser in python in which, we read chunks of (4) bytes from the file in each iteration 
and saves the string in memory and concatenate it with other iterations, then we select only everything between `<Article>` and `</Article>` and keep track of the XML nested Levels and discard the whole data in memory, 
if we finished processing the current article.


## Developing a Simple Web Service

#### Question 1 : Develop a REST-like Web Service

I have utilized Python Flask which is a python micro-framework for developing web and restful applications.

```python
#!/usr/bin/env python3.8
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/date", methods=['GET'])
def get():
    import pytz
    from datetime import datetime
    tz = pytz.timezone('Europe/London')
    date_str = datetime.now(tz=tz).strftime("%a %b %d %H:%M:%S %Z %Y")
    return jsonify({
        "date": date_str
    })


if __name__ == '__main__':
    print("Starting Restful Server running on all interfaces with port : 8000 " )
    app.run(host="0.0.0.0", port=8000)
```

In order to run this file, all you have to do is execute the file using Python interpreter

```shell script
$ python restful.py
```

#### Question 2: Creating a Docker Image

I have created a Dockerfile extending Ubuntu base Image, using the following steps:

- Updated all ubuntu packages
- Installed python3.8 and its libraries
- Copied Requirements.txt to the image
- Used pip3 to install all restful API application dependencies.
- Copied the actual script as `/usr/bin/restful` onto the docker image.
- Made it Executable.
- I used CMD to execute the script upon booting up the container.

```dockerfile
FROM ubuntu

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3.8 python3-pip python3.8-dev

COPY requirements.txt .

RUN cat requirements.txt | xargs -n1 pip3 install

COPY restful.py /usr/bin/restful

RUN chmod a+x /usr/bin/restful

CMD ["/usr/bin/restful"]
```

- I have built the image locally and tested it well.
- Then, I have logged into `BioFlows` account which I made previously for me.
- I created a new repository on Docker, linked my personal GitHub account to it.
- Then, I have created a build rule with Source Type: Branch, Source: Master , Docker Tag: latest, Dockerfile location: Dockerfile, Build Caching: Enabled.
- This build rule will allow web hooks to be triggered upon pushing events to my GitHub account in order to fire building the latest docker image.

Now, If you want to test this, you can perform the following 

```shell script
$ docker run -p 8000:8000 -it bioflows/restful
```

The above command will bind port 8000/tcp in the container to port 8000/tcp in my Host OS, to enable user to request the service.

Now, you can test the service easily through 

```shell script
$ curl http://localhost:8000/date
``` 

#### Question 3: Scaling Up Date Service

We can scale out the previous docker container by one of the following methods

- we can manually run (n) number of containers for the above image on the same server but with different range of ports on the host.
- Then we can use a load balancer like "nginx" to distribute the load among these (n) containers by a single entry URL through nginx.

The second approach, which is more scalable and fault tolerant is to use `Kubernetes` because it can monitor the health of those containers and spawn a new container 
in case of failure. I just have started learning kubernetes, but I am creating a distributed execution environment for `Bioflows` similar to Kubernetes. 
I can answer from a generic point of view.

- Kubernetes run mainly through a master node and (n) worker nodes.
- A Worker node, will spawn the container locally and keeps monitoring it for failure.
- A master node is responsible for managing, scheduling and monitoring the health of the cluster.
- `etcd` which acts as a distributed cache or `key/value` data store, keeps metadata about each node and each node has access to this service.
- A master node through the scheduler, schedules a Pod to run on a worker node. In this pod definition, we can define the container image, define ports, 
define the range of ports on the host...etc. We can also specify how many replicas we need for this service, which kubernetes master node will make sure that the cluster
 stays consistent by always having these replicas up and running anywhere in the cluster.
 - Now, Kubernetes needs to keep track of these IP addresses and their corresponding ports











