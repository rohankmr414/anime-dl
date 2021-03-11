import os
import argparse
from downloader_cli import download

from scraper import dllink_scraper

sc = dllink_scraper()

parser = argparse.ArgumentParser(prog='anime-dl')

args, unknown = parser.parse_known_args()

links = sc.search(unknown[0])

index = input('Enter your selection: ')

eplinks = sc.get_eplinks(os.link[index+1])

print(eplinks)