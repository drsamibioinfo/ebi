network = {
    "Alice": ["Ben", "Fred"],
    "Ben": ["Alice", "Darcey", "Carrie", "Eve"],
    "Darcey": ["Ben", "Eve"],
    "Eve": ["Carrie", "Ben", "Darcey", "Fred"],
    "Carrie": ["Ben", "Eve"],
    "Fred": ["Alice", "Eve"]
}
employers = {
    "Alice": "UCA",
    "Ben": "EBI",
    "Darcey": "EBI",
    "Eve": "BioB",
    "Carrie": "OFC",
    "Fred": "EBI"
}

# employer = set([x.lower() for x in employers.values()])
from typing import Mapping


def findGroupA(network: Mapping[str, list], employer: Mapping[str, str]) -> []:
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


def main():
    members = findGroupA(network, employers)
    print(members)

if __name__ == '__main__':
    main()
