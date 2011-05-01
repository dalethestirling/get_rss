#! /bin/env python

# _____             ____  _     _           _   _                         
#|  _  |_ _ ___ ___|    \|_|___| |_ ___ ___| |_|_|___ ___   ___ ___ _____ 
#|   __| | |  _| -_|  |  | |_ -|  _| . |  _|  _| | . |   |_|  _| . |     |
#|__|  |___|_| |___|____/|_|___|_| |___|_| |_| |_|___|_|_|_|___|___|_|_|_|
# 

# Script to get URL for last Item in RSS feed.
# Dale Stirling feedback -at- puredistortion.com

import feedparser
import sys
import syck
import os
import urllib2

config_file = sys.argv[1]

#read in YAML from config file.
open_config = open(config_file)
get_config = syck.load(open_config.read())
open_config.close()

#validate base config exists
for akey in get_config.keys():
    if akey == 'config':
        for subkey in get_config['config'].keys():
            print subkey
            if subkey == 'root_dir':
                continue 
            elif subkey == 'check_back':
                continue
            else:
                sys.exit()
                
#create config and feeds variables.
get_config_vars = get_config['config'] 
get_feeds = get_config['feeds']

print get_config
print get_feeds
print get_config_vars['root_dir']

print get_config['config'].keys()


#check for the root dir exists
if not os.path.isdir(get_config_vars['root_dir']):
    sys.exit()

print 'bcool'

for category in get_feeds.keys():
	print category
	#create the complete path to category path directory
	category_path = '%s/%s' % (get_config_vars['root_dir'], category)
	#if directory exists continue else create the directory
	if not os.path.isdir(category_path):
		os.mkdir(category_path)
	#dictionary for fileName(s) to go into
	valid_podcast = {}
	#get the rss urls and process them. 
	print get_feeds[category]
	#for rss_url in get_feeds[category]:
	rss_url = get_feeds[category]
	print rss_url 
	feed = feedparser.parse(rss_url)
	#adjust value to suit python list, first item is at 0
	item_ammount = get_config_vars['check_back']-1
	print item_ammount
	item_number = 0
	print feed #go through list amount and build downloads dictionary (aka. valid_podcat)
	while item_number <= item_ammount:  
		item = feed['items'][item_number]
		enclosures = item['enclosures']
		for entry in enclosures:
			print entry['href']
			#split fileName from url for dictionary
			(dirName, fileName) = os.path.split(entry['href'])
			print fileName
			#add entry to dictionary
			valid_podcast[str(fileName)] = str(entry['href'])
		#increment by 1
		item_number = item_number+1
	print 'dale'
	print valid_podcast
	
	# clean files in category directory.
	# if the filename is not in valid_podcast.keys() list it is removed.
	for downloaded_podcast in os.listdir(category_path):
		# check file against list if not in list remove.
		if not downloaded_podcast in valid_podcast.keys():
			# remove file here.
			print downloaded_podcast
			os.remove('%s/%s' % (category_path, downloaded_podcast))
	
	for podcast_file in valid_podcast.keys():
		print podcast_file
        url = valid_podcast[podcast_file]
        dest_file = '%s/%s/%s' % (get_config_vars['root_dir'], category, podcast_file)
        remote_file = urllib2.urlopen(url)
        local_file = open(dest_file, 'w')
        local_file.write(remote_file.read())
        local_file.close()