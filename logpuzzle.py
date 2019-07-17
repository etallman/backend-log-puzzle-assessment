#!/usr/bin/env python2

"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import argparse
import urllib

#Sample Apache
#10.254.254.28 - - [06/Aug/2007:00:14:08 -0700] "GET /foo/talks/ HTTP/1.1"
# 200 5910 "-" "Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.4) Gecko/
# 20070515 Firefox/2.0.0.4"#

def key_sort(url):
    match_obj = re.search(r"a-(\w+)\.jpg", url)
    if match_obj:
        return match_obj.group(1)
    else:
        return url
        
def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    
    with open(filename) as opened:
        puzzle_urls = []
        for line in opened:
            match_object = re.search(r'GET (\S+)', line)
            if match_object:
                puzzle_path = match_object.group(1)
                if "puzzle" in puzzle_path:
                    domain = "http://code.google.com" + puzzle_path 
                    puzzle_urls.append(domain)
    puzzle_urls = list(set(puzzle_urls))
    return sorted(puzzle_urls, key=key_sort)


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # +++your code here+++
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    filename = os.path.join(dest_dir, "index.html")
 
    with open(filename, 'w') as f:
        f.write("<html><body>")
        for i, img_url in enumerate(img_urls):
            print("Downloading Image: {}".format(img_url))
            img_dest = os.path.join(dest_dir, "img{}".format(i))
            urllib.urlretrieve(img_url, img_dest)
            f.write("<img src={}.format({}{})>")
            f.write(img_url)
            f.write("</img>")
        f.write("</body></html>")
         

def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if not parsed_args:
        parser.print_usage()
        sys.exit(1)

    

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))
    

if __name__ == '__main__':
    main(sys.argv[1:])