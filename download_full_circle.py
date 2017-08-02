#!/usr/bin/env python
import os
import re
import requests
import grequests
from bs4 import BeautifulSoup

__version__ = '0.1'
__author__ =  'Norbert Bota'
__author_email__= 'botanorbert1@gmail.com'

def make_soup(url):
	req_url = requests.get(url)
	soup = BeautifulSoup(req_url.content, "lxml")
	return soup

def editions(issue, base_url):
	"""Find all editions"""
	all_table = []
	
	if issue == 'special':
		table_elements = make_soup(base_url + "/python-special-editions")
		table_contents = table_elements.find("div", {"class":"td-pb-padding-side td-page-content"})
		for i in table_contents.find_all('a'):
			all_pdfs = i.get('href')
			# get only english version
			en_ver = re.compile("en.pdf$", re.IGNORECASE)          
			if en_ver.search(all_pdfs):
				all_table.append(all_pdfs)
		return all_table
		
	elif issue == 'past':
		issue_table = make_soup(base_url + "/downloads")
		table_links = issue_table.find("table", {"class":"issuetable"}) 
		all_links = table_links.find_all('a')
		for i in range(1, len(all_links)+1):
			links = "http://dl.fullcirclemagazine.org/issue{0}_en.pdf".format(i) 
			all_table.append(links)
		return all_table

def make_grequests(urls_table):
	requests = (grequests.get(u, stream=True) for u in urls_table)
	responses = grequests.map(requests, size=10)
	return responses
	
def download_editions(dir_name, link_list):
	""" Create folder and download editions """
	try:
		os.makedirs(dir_name)
	except OSError:
		pass
	# cd to dir
	os.chdir(dir_name)
	for i in make_grequests(link_list):
		with open(str(i.url.rpartition('/')[2]), 'wb') as f:
			f.write(i.content)
			
def main():
	base_url = "http://fullcirclemagazine.org"
	
	user_prompt = raw_input("--- Downloadn Full-Circle magazine editions ---\
				\nEneter: \
				\n[1] for special-python editions \
				\n[2] for all past editions \
				\n--->")

	if user_prompt == "1":
		special_editions = editions("special", base_url)
		download_editions("special-editions", special_editions)
	elif user_prompt == "2":
		past_editions = editions("past", base_url)
		download_editions("past-editions", past_editions)

if __name__=='__main__':
	main()
