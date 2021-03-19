#!/usr/bin/env python
import random, argparse


def foo(length):
    if length < 0:
        raise Exception("can't accept negative numbers")
    bag = set()
    while len(bag) < length:
        bag.add(random.randint(1, length))
    return bag


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--length", "-l", required=True, help="Length parameter")
    args = p.parse_args()
    if args.length is None:
        p.print_help()
        return
    print(foo(int(args.length)))


if __name__ == '__main__':
    main()