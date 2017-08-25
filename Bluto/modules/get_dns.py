#!/usr/local/bin/python

# -*- coding: utf-8 -*-

import sys
import traceback
import socket
import dns.resolver
import random
import string
from bluto_logging import info, INFO_LOG_FILE
from multiprocessing.dummy import Pool as ThreadPool
from termcolor import colored

targets = []

def set_resolver(timeout_value):
    myResolver = dns.resolver.Resolver()
    myResolver.timeout = timeout_value
    myResolver.lifetime = timeout_value
    myResolver.nameservers = ['8.8.8.8', '8.8.4.4']

    return myResolver


def get_dns_details(domain, myResolver):
    info('Gathering DNS Details')
    ns_list = []
    zn_list =[]
    mx_list = []
    try:
        print "\nName Server:\n"
        myAnswers = myResolver.query(domain, "NS")
        for data in myAnswers.rrset:
            data1 = str(data)
            data2 = (data1.rstrip('.'))
            addr = socket.gethostbyname(data2)
            ns_list.append(data2 + '\t' + addr)
            zn_list.append(data2)
            list(set(ns_list))
            ns_list.sort()
        for i in ns_list:
            print colored(i, 'green')
    except dns.resolver.NoNameservers:
        info('\tNo Name Servers\nConfirm The Domain Name Is Correct.' + INFO_LOG_FILE, exc_info=True)
        sys.exit()
    except dns.resolver.NoAnswer:
        print "\tNo DNS Servers"
    except dns.resolver.NXDOMAIN:
        info("\tDomain Does Not Exist" + INFO_LOG_FILE, exc_info=True)
        sys.exit()
    except dns.resolver.Timeout:
        info('\tTimeouted\nConfirm The Domain Name Is Correct.' + INFO_LOG_FILE, exc_info=True)
        sys.exit()
    except Exception:
        info('An Unhandled Exception Has Occured, Please Check The Log For Details\n' + INFO_LOG_FILE, exc_info=True)

    try:
        print "\nMail Server:\n"
        myAnswers = myResolver.query(domain, "MX")
        for data in myAnswers:
            data1 = str(data)
            data2 = (data1.split(' ',1)[1].rstrip('.'))
            addr = socket.gethostbyname(data2)
            mx_list.append(data2 + '\t' + addr)
            list(set(mx_list))
            mx_list.sort()
        for i in mx_list:
            print colored(i, 'green')
    except dns.resolver.NoAnswer:
        print "\tNo Mail Servers"
    except Exception:
        info('An Unhandled Exception Has Occured, Please Check The Log For Details' + INFO_LOG_FILE)

    info('Completed Gathering DNS Details')
    return zn_list


def action_wild_cards(domain, myResolver):
    info('Checking Wild Cards')
    try:
        one = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        myAnswers = myResolver.query(str(one) + '.' + str(domain))
        print myAnswers.rrset
    except dns.resolver.NoNameservers:
        pass

    except dns.resolver.NoAnswer:
        pass

    except dns.resolver.NXDOMAIN:
        info('Wild Cards False')
        return False
    else:
        info('Wild Cards True')
        return True


def action_brute(subdomain):
    global myResolverG
    try:
        myAnswers = myResolverG.query(subdomain)
        for data in myAnswers:
            targets.append(subdomain + ' ' + str(data))

    except dns.resolver.NoNameservers:
        pass
    except dns.resolver.NXDOMAIN:
        pass
    except dns.resolver.NoAnswer:
        pass
    except dns.exception.SyntaxError:
        pass
    except dns.exception.Timeout:
        info('Timeout: {}'.format(subdomain))
        pass
    except dns.resolver.Timeout:
        pass
    except Exception:
        info('An Unhandled Exception Has Occured, Please Check The Log For Details' + INFO_LOG_FILE)
        info(traceback.print_exc())


def action_brute_start(subs, myResolver):
    global myResolverG
    myResolverG = myResolver
    info('Bruting SubDomains')
    print '\nBrute Forcing Sub-Domains\n'
    pool = ThreadPool(8)
    pool.map(action_brute, subs)
    pool.close()
    info('Completed Bruting SubDomains')

    return targets


def action_brute_wild(sub_list, domain, myResolver):
    info('Bruting Wild Card SubDomains')
    target_results = []
    random_addrs = []
    for i in range(0,10,1):
        one = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        myAnswers = myResolver.query(str(one) + '.' + str(domain))
        name = myAnswers.canonical_name
        random_addr = socket.gethostbyname(str(name))
        random_addrs.append(random_addr)
    random_addrs = sorted(set(random_addrs))
    for host in sub_list:
        try:
            host_host, host_addr = host.split(' ')
            if host_addr in random_addrs:
                pass
            else:
                target_results.append(host)
        except dns.resolver.NoNameservers:
            pass
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.NXDOMAIN:
            pass
        except dns.name.EmptyLabel:
            pass
        except Exception:
            continue
    info('Completed Bruting Wild Card SubDomains')
    return target_results


def action_zone_transfer(zn_list, domain):
    info('Attempting Zone Transfers')
    global clean_dump
    print "\nAttempting Zone Transfers"
    zn_list.sort()
    vuln = True
    vulnerable_listT = []
    vulnerable_listF = []
    dump_list = []
    for ns in zn_list:
        try:
            z = dns.zone.from_xfr(dns.query.xfr(ns, domain, timeout=3, lifetime=5))
            names = z.nodes.keys()
            names.sort()
            if vuln == True:
                info('Vuln: {}'.format(ns))
                vulnerable_listT.append(ns)

        except Exception as e:
            error = str(e)
            if error == 'Errno -2] Name or service not known':
                pass
            if error == "[Errno 54] Connection reset by peer" or "No answer or RRset not for qname":
                info('Not Vuln: {}'.format(ns))
                vuln = False
                vulnerable_listF.append(ns)
            else:
                info('An Unhandled Exception Has Occured, Please Check The Log For Details\n' + INFO_LOG_FILE, exc_info=True)


    if vulnerable_listF:
        print "\nNot Vulnerable:\n"
        for ns in vulnerable_listF:
            print colored(ns, 'green')

    if vulnerable_listT:
        info('Vulnerable To Zone Transfers')
        print "\nVulnerable:\n"
        for ns in vulnerable_listT:
            print colored(ns,'red'), colored("\t" + "TCP/53", 'red')


        z = dns.zone.from_xfr(dns.query.xfr(vulnerable_listT[0], domain, timeout=3, lifetime=5))
        names = z.nodes.keys()
        names.sort()
        print "\nRaw Zone Dump\n"
        for n in names:
            data1 = "{}.{}" .format(n,domain)
            try:
                addr = socket.gethostbyname(data1)
                dump_list.append("{}.{} {}" .format(n, domain, addr))

            except Exception as e:
                error = str(e)
                if error == "[Errno -5] No address associated with hostname":
                    pass
                if error == 'Errno -2] Name or service not known':
                    pass
                else:
                    info('An Unhandled Exception Has Occured, Please Check The Log For Details\n' + INFO_LOG_FILE, exc_info=True)

            print z[n].to_text(n)

    info('Completed Attempting Zone Transfers')
    clean_dump = sorted(set(dump_list))
    return ((vulnerable_listT, clean_dump))
