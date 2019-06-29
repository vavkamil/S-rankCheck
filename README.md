# S-rankCheck
Asynchronous S-rank check using seznam.cz RPC API

## S-rank
A ranking used by the Czech search engine Seznam.cz. It is a similar to PageRank with a range from 0 to 10.

More info: https://napoveda.seznam.cz/cz/fulltext-hledani-v-internetu/s-rank-faq/

## Usage
```
vavkamil@desktop:~/Documents/Python/S-rankCheck$ python3 srankcheck.py 
usage: srankcheck.py [-h] (-d DOMAIN | -D DOMAINS) [-o OUTPUT] [-t THREADS]
srankcheck.py: error: one of the arguments -d -D is required

vavkamil@desktop:~/Documents/Python/S-rankCheck$ python3 srankcheck.py -d seznam.cz
[S-rank] Check using seznam.cz RPC API
[S-rank] Scanning single domain:

[9] seznam.cz

[!] Play nice, don't abuse this ...
```

## Input
This script can be used with @spaze [tld-cz.txt ](https://github.com/spaze/domains) unofficial list

## Output
See output.txt for example of most of all .cz domains with s-rank > 0
