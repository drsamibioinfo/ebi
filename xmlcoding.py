#!/usr/bin/env python
from bs4 import BeautifulSoup as bs
from typing import Mapping , Sequence
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


def get_matrix_result(xml_file:str ) -> Sequence[list]:
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
        rows.append(row)
    return rows


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
