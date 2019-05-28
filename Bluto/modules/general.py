#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from termcolor import colored
import pythonwhois
import traceback
import requests
import datetime
import re
import sys
import socket
import dns.resolver
import dns.query
import dns.zone
import traceback
import os
from bluto_logging import info, INFO_LOG_FILE


default_s = False

def get_size(dir_location):
    start_path = dir_location
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    total_size = total_size / 1024.0
    total_size = total_size / 1024.0
    return total_size


def action_whois(domain):
    try:
        whois_things = pythonwhois.get_whois(domain)
        try:
            company = whois_things['contacts']['registrant']['name']
        except Exception:
            print ('\nThere seems to be no Registrar for this domain.')
            company = domain
            pass
        splitup = company.lower().split()
        patern = re.compile('|'.join(splitup))
        while True:
            if patern.search(domain):
                info('Whois Results Are Good ' + company)
                print ('\nThe Whois Results Look Promising: ' + colored('{}','green').format(company))
                accept = raw_input(colored('\nIs The Search Term sufficient?: ','green')).lower()
                if accept in ('y', 'yes'):
                    company = company
                    break
                elif accept in ('n', 'no'):
                    temp_company = raw_input(colored('\nRegistered Company Name: ','green'))
                    if temp_company == '':
                        info('User Supplied Blank Company')
                        company = domain
                        break
                    else:
                        info('User Supplied Company ' + company)
                        company = temp_company
                        break
                else:
                    print ('\nThe Options Are yes|no Or y|no Not {}'.format(accept))

            else:
                info('Whois Results Not Good ' + company)
                print (colored("\n\tThe Whois Results Don't Look Very Promissing: '{}'","red") .format(company))
                print('\nPlease Supply The Company Name\n\n\tThis Will Be Used To Query LinkedIn')
                temp_company = raw_input(colored('\nRegistered Company Name: ','green'))
                if temp_company == '':
                    info('User Supplied Blank Company')
                    company = domain
                    break
                else:
                    info('User Supplied Company ' + company)
                    company = temp_company
                    break

    except pythonwhois.shared.WhoisException:
        pass
    except socket.error:
        pass
    except KeyError:
        pass
    except pythonwhois.net.socket.errno.ETIMEDOUT:
        print(colored('\nWhoisError: You may be behind a proxy or firewall preventing whois lookups. Please supply the registered company name, if left blank the domain name ' + '"' + domain + '"' +' will be used for the Linkedin search. The results may not be as accurate.','red'))
        temp_company = raw_input(colored('\nRegistered Company Name: ','green'))
        if temp_company == '':
            company = domain
        else:
            company = temp_company
    except Exception:
        info('An Unhandled Exception Has Occured, Please Check The Log For Details\n' + INFO_LOG_FILE)
    if 'company' not in locals():
        print ('There is no Whois data for this domain.\n\nPlease supply a company name.')
        while True:
            temp_company = raw_input(colored('\nRegistered Company Name: ','green'))
            if temp_company == '':
                info('User Supplied Blank Company')
                company = domain
                break
            else:
                company = temp_company
                info('User Supplied Company ' + company)
                break

    return company

def action_country_id(countries_file, prox):
    info('Identifying Country')
    userCountry = ''
    userServer = ''
    userIP = ''
    userID = False
    o = 0
    tcountries_dic = {}
    country_list = []

    with open(countries_file) as fin:
        for line in fin:
            key, value = line.strip().split(';')
            tcountries_dic.update({key: value})

    countries_dic = dict((k.lower(), v.lower()) for k,v in tcountries_dic.iteritems())

    for country, server in countries_dic.items():
        country_list.append(country)

    country_list = [item.capitalize() for item in country_list]
    country_list.sort()

    while True:
        try:
            if prox == True:
                proxy = {'https' : 'http://127.0.0.1:8080'}
                r = requests.get(r'https://freegeoip.net/json/', proxies=proxy, verify=False)
                ip = r.json()['ip']
                originCountry = r.json()['country_name']

            else:
                r = requests.get(r'http://freegeoip.net/json/', verify=False)
                ip = r.json()['ip']
                originCountry = r.json()['country_name']

        except ValueError as e:
            if o == 0:
                print (colored('\nUnable to connect to the CountryID, we will retry.', 'red'))
            if o > 0:
                print ('\nThis is {} of 3 attempts' .format(o))
            time.sleep(2)
            o += 1
            if o == 4:
                break
            continue
        break

    if o == 4:
        print (colored('\nWe have been unable to connect to the CountryID service.\n','red'))
        print ('\nPlease let Bluto know what country you hale from.\n')
        print (colored('Available Countries:\n', 'green'))

        if len(country_list) % 2 != 0:
            country_list.append(" ")

        split = len(country_list)/2
        l1 = country_list[0:split]
        l2 = country_list[split:]

        for key, value in zip(l1,l2):
            print ("{0:<20s} {1}".format(key, value))

        country_list = [item.lower() for item in country_list]

        while True:
            originCountry = raw_input('\nCountry: ').lower()
            if originCountry in country_list:
                break
            if originCountry == '':
                print ('\nYou have not selected a country so the default server will be used')
                originCountry = 'United Kingdom'.lower()
                break
            else:
                print ('\nCheck your spelling and try again')

        for country, server in countries_dic.items():
            if country == originCountry:
                userCountry = country
                userServer = server
                userID = True

    else:

        for country, server in countries_dic.items():
            if country == originCountry.lower():
                userCountry = country
                userServer = server
                userID = True
        if userID == False:
            if default_s == True:
                userCountry = 'DEAFULT'
                pass
            else:
                print ('Bluto currently doesn\'t have your countries google server available.\nPlease navigate to "https://freegeoip.net/json/" and post an issue to "https://github.com/darryllane/Bluto/issues"\nincluding the country value as shown in the json output\nYou have been assigned to http://www.google.co.uk for now.')
                userServer = 'http://www.google.co.uk'
                userCountry = 'United Kingdom'

    print ('\n\tSearching From: {0}\n\tGoogle Server: {1}\n' .format(userCountry.title(), userServer))
    info('Country Identified: {}'.format(userCountry))
    return (userCountry, userServer)


def action_bluto_use(countryID):
    now = datetime.datetime.now()
    try:
        link = "http://darryllane.co.uk/bluto/log_use.php"
        payload = {'country': countryID, 'Date': now}
        requests.post(link, data=payload)
    except Exception:
        info('An Unhandled Exception Has Occured, Please Check The Log For Details\n' + INFO_LOG_FILE)
        pass


def check_dom(domain, myResolver):
    try:
        myAnswers = myResolver.query(domain, "NS")
        dom = str(myAnswers.canonical_name).strip('.')
        if dom:
            pass
    except dns.resolver.NoNameservers:
        print ('\nError: \nDomain Not Valid, Check You Have Entered It Correctly\n')
        sys.exit()
    except dns.resolver.NXDOMAIN:
        print ('\nError: \nDomain Not Valid, Check You Have Entered It Correctly\n')
        sys.exit()
    except dns.exception.Timeout:
        print ('\nThe connection hit a timeout. Are you connected to the internet?\n')
        sys.exit()
    except Exception:
        info('An Unhandled Exception Has Occured, Please Check The Log For Details\n' + INFO_LOG_FILE)
