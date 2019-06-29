#!/usr/bin/python3.6

import argparse
import requests
import concurrent.futures
from xml.etree import ElementTree as ET

def parse_args():
    parser = argparse.ArgumentParser(description="Asynchronous S-rank check using seznam.cz RPC API", epilog="@vavkamil ~ https://vavkamil.cz")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", dest="domain", help="single domain name to scan")
    group.add_argument("-D", dest="domains", help="list of domains to scan", type=argparse.FileType('r'))
    parser.add_argument("-o", dest="output", help="save output to a file (csv separated by semicolon)", type=argparse.FileType('w'))
    parser.add_argument("-t", dest="threads", help="number of threads (default: 5)", default="5", type=int)
    return parser.parse_args()

def check_domain(domain):
    post_data = """
        <?xml version="1.0" encoding="UTF-8"?>
        <methodCall>
            <methodName>getRank</methodName>
            <params>
                <param>
                    <value>
                        <string>0</string>
                    </value>
                </param>
                <param>
                    <value>
                        <string>%s</string>
                    </value>
                </param>
                <param>
                    <value>
                        <i4>0</i4>
                    </value>
                </param>
            </params>
        </methodCall>
    """ % (domain)

    post_url        = "https://srank.seznam.cz/RPC2"
    post_data       = " ".join(post_data.split())   # Remove new lines and tabs
    http_headers    = {"Content-Type": "text/xml"}
    response        = requests.post(url=post_url, data=post_data, headers=http_headers)

    return (response.content, domain)

def parse_xml(xml, domain):
    root        = ET.fromstring(xml)
    status      = root.find(".//member[name='status']/value/i4").text
    if(status   == "200"):
        rank    = root.find(".//member[name='rank']/value/i4").text
        srank   = str(round(int(rank) * 100 / 255 / 10))
    else:
        srank   = "N/A"

    print("["+srank+"] "+domain)

    if(args.output):
        args.output.write(srank+";"+domain+"\n")

def load_domains(location):
    domains = []
    with location as domainlist:
        for domain in domainlist:
            if domain.strip() != '':
                domains.append(domain.strip())
    if not domains:
        print ("Error no domains were found in the file")

    return domains

if __name__ == "__main__":
    args = parse_args()
    print ("[S-rank] Check using seznam.cz RPC API")

    if(args.output):
        print ("[S-rank] Output will be saved to:", args.output.name+"\n")

    if(args.domain):
        print ("[S-rank] Scanning single domain:\n")
        (xml, domain) = check_domain(args.domain)
        parse_xml(xml, domain)

    elif(args.domains):
        domains = load_domains(args.domains)
        print ("[S-rank] Scanning multiple domains:", args.domains.name)
        print ("[S-rank] Domains in a list:", str(len(domains)), "\n")

        with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
            xml_response = {executor.submit(check_domain, domain): domain for domain in domains}
            for xml in concurrent.futures.as_completed(xml_response):
                try:
                    (xml, domain) = xml.result()
                    parse_xml(xml, domain)
                except Exception as exc:
                    print ("Error", exc)

    print ("\n[!] Play nice, don't abuse this ...")