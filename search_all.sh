#>!/bin/sh
#search_string=$1

grep "$1" /mnt/c/Users/brieh/Projects/KEY_RA/Environment_Canada/ECCC/fb/processed\ data/statuses/* > output.txt
grep "$1" /mnt/c/Users/brieh/Projects/KEY_RA/Environment_Canada/ECCC/tw/processed\ data/* >> output.txt
grep "$1" /mnt/c/Users/brieh/Projects/KEY_RA/Environment_Canada/ECCC/in/processed\ data/posts/* >> output.txt

