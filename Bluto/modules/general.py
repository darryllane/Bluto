#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from termcolor import colored
import pythonwhois
import traceback
import requests
import datetime
from bluto_logging import warning

default_s = False

def action_whois(domain):

    try:
        whois_things = pythonwhois.get_whois(domain)
        company = whois_things['contacts']['registrant']['name']
    except KeyError, pythonwhois.net.socket.errno.ETIMEDOUT:
        print colored('\nWhoisError: You may be behind a proxy or firewall preventing whois lookups. Please supply the registered company name, if left blank the domain name ' + '"' + domain + '"' +' will be used for the Linkedin search. The results may not be as accurate.','red')
        temp_company = raw_input(colored('\nRegistered Company Name: ','green'))
        if temp_company == '':
            company = domain
        else:
            company = temp_company
    except Exception:
        traceback.print_exc()

    return company

def action_country_id(countries_file, prox):
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
                proxy = {'http' : 'http://127.0.0.1:8080'}
                r = requests.get(r'http://freegeoip.net/json/', proxies=proxy)
                ip = r.json()['ip']
                originCountry = r.json()['country_name']

            else:
                r = requests.get(r'http://freegeoip.net/json/')
                ip = r.json()['ip']
                originCountry = r.json()['country_name']

        except ValueError as e:
            if o == 0:
                print colored('\nUnable to connect to the CountryID, we will retry.', 'red')
            if o > 0:
                print '\nThis is {} of 3 attempts' .format(o)
            time.sleep(2)
            o += 1
            if o == 4:
                break
            continue
        break

    if o == 4:
        print colored('\nWe have been unable to connect to the CountryID service.\n','red')
        print '\nPlease let Bluto know what country you hale from.\n'
        print colored('Available Countries:\n', 'green')

        if len(country_list) % 2 != 0:
            country_list.append(" ")

        split = len(country_list)/2
        l1 = country_list[0:split]
        l2 = country_list[split:]

        for key, value in zip(l1,l2):
            print "{0:<20s} {1}".format(key, value)

        country_list = [item.lower() for item in country_list]

        while True:
            originCountry = raw_input('\nCountry: ').lower()
            if originCountry in country_list:
                break
            if originCountry == '':
                print '\nYou have not selected a country so the default server will be used'
                originCountry = 'United Kingdom'.lower()
                break
            else:
                print '\nCheck your spelling and try again'

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
                print 'Bluto currently doesn\'t have your countries google server available.\nPlease navigate to "http://www.telize.com/geoip/" and post an issue to "https://github.com/RandomStorm/Bluto/issues"\nincluding the country value as shown in the json output\nYou have been assigned to http://www.google.com for now.'
                userServer = 'http://www.google.co.uk'
                userCountry = 'United Kingdom'

    print '\n\tSearching From: {0}\n\tGoogle Server: {1}\n' .format(userCountry.title(), userServer)
    return (userCountry, userServer)


def action_bluto_use(countryID):
    now = datetime.datetime.now()
    try:
        link = "http://darryllane.co.uk/bluto/log_use.php"
        payload = {'country': countryID, 'Date': now}
        requests.post(link, data=payload)
    except Exception:
        warning(traceback.print_exc())
        pass
