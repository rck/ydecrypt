#!/usr/bin/env python3

# ydecrypt - Crack/Check Hashes with Google
# Copyright (C) 2011 Roland Kammerer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Thanks to Juuso Salonen, ydecrypt is heavily inspired by his project:
# https://github.com/juuso/BozoCrack

import sys
import hashlib
import urllib.request
import argparse

def crackhash(myhash):
    myhash = myhash.strip().lower()

    # google does not like urllibs user-agent, fabricate one
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    f = opener.open("http://www.google.com/search?q=%s" % myhash)
    
    wordlist = f.read().split()

    for word in wordlist:
        word = word.strip()
        #TODO: check which algorithm is used, and use the correct one
        #for now it is md5
        m = hashlib.md5()
        m.update(word)

        if m.hexdigest() == myhash:
            return bytes.decode(word)

    return False


parser = argparse.ArgumentParser(description="Crack/Check Hashes with Google.")
parser.add_argument("--crack-hash", metavar="HASH", help="crack the given hash")
parser.add_argument("--check", metavar="STRING", help="check if google has a hash for the given string")
parser.add_argument("-f", "--file", help="read hashes from file")

args = parser.parse_args()

if len(sys.argv) == 1: parser.print_help()

if args.crack_hash:
    ret = crackhash(args.crack_hash)
    if ret: print(args.crack_hash.strip(), "==>", ret)

if args.check:
    checkenc = args.check.strip().encode()
    m = hashlib.md5()
    m.update(checkenc)
    genhash = m.hexdigest()
    ret = crackhash(genhash)
    if ret: print("Found:", args.check.strip(), "==>", genhash)
    else: print("Nothing found on google")

if args.file:
    for line in open(args.file):
        line = line.strip()
        ret = crackhash(line)
        if ret: print(line, "==>", ret)
        else: print(line, "!=> Nothing found")
    


   
