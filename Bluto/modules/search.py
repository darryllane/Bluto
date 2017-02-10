#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import dns.resolver
import unicodedata
import traceback
import sys
import re
import requests
import random
import time
import urllib2
import json
from termcolor import colored
from bs4 import BeautifulSoup
from bluto_logging import info, INFO_LOG_FILE

requests.packages.urllib3.disable_warnings()

def action_google(domain, userCountry, userServer, q, user_agents, prox):
    info('Google Search Started')
    uas = user_agents
    searchfor = '@' + '"' + domain + '"'
    entries_tuples = []
    seen = set()
    results = []
    for start in range(1,10,1):
        ua = random.choice(uas)
        try:
            if prox == True:
                proxy = {'http' : 'http://127.0.0.1:8080'}
            else:
                pass
            headers = {"User-Agent" : ua,
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Language': 'en-US,en;q=0.5',
                       'Accept-Encoding': 'gzip, deflate',
                       'Referer': 'https://www.google.com'}
            payload = { 'nord':'1', 'q': searchfor, 'start': start*10}

            link = '{0}/search?num=200' .format(userServer)
            if prox == True:
                response = requests.get(link, headers=headers, params=payload, proxies=proxy, verify=False)
            else:
                response = requests.get(link, headers=headers, params=payload, verify=False)

            response.raise_for_status()
            response.text.encode('ascii', 'ignore').decode('ascii')
            soup = BeautifulSoup(response.text, "lxml")

            for div in soup.select("div.g"):

                for div in soup.select("div.g"):

                    email_temp = div.find("span", class_="st")
                    clean = re.sub('<em>', '', email_temp.text)
                    clean = re.sub('</em>', '', email_temp.text)
                    match = re.findall('[a-zA-Z0-9.]*' + '@' + domain, clean)
                    try:
                        if match:
                            if match is not '@' + domain:
                                if match is not '@':
                                    url = div.find('cite').text
                                    email = str(match).replace("u'",'').replace('[','').replace(']','').replace("'",'')
                                    entries_tuples.append((email.lower(),str(url).replace("u'",'').replace("'","")))
                    except Exception, e:
                        pass
            time.sleep(3)
            for urls in entries_tuples:
                if urls[1] not in seen:
                    results.append(urls)
                    seen.add(urls[1])
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 503:
                info('Google is responding with a Captcha, other searches will continue')
                break
        except AttributeError as f:
            pass
        except Exception:
            info('An Unhandled Exception Has Occured, Please Check The Log For Details' + INFO_LOG_FILE)

    info('Google Search Completed')
    q.put(sorted(results))


#Takes [list[tuples]]email~url #Returns [list[tuples]]email_address, url_found, breach_domain, breach_data, breach_date, /
#breach_added, breach_description
def action_pwned(emails):
    info('Compromised Account Enumeration Search Started')
    pwend_data = []
    seen = set()
    for email in emails:
        link = 'https://haveibeenpwned.com/api/v2/breachedaccount/{}'.format(email)
        try:
            headers = {"Connection" : "close",
                       "User-Agent" : "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Language': 'en-US,en;q=0.5',
                       'Accept-Encoding': 'gzip, deflate'}

            response = requests.get(link, headers=headers, verify=False)
            json_data = response.json()
            if json_data:
                if email in seen:
                    pass
                else:
                    for item in json_data:
                        seen.add(email)
                        email_address = email
                        breach_domain = str(item['Domain']).replace("u'","")
                        breach_data = str(item['DataClasses']).replace("u'","'").replace('"','').replace('[','').replace(']','')
                        breach_date = str(item['BreachDate']).replace("u'","")
                        breach_added = str(item['AddedDate']).replace("u'","").replace('T',' ').replace('Z','')
                        breach_description = str(item['Description']).replace("u'","")
                        pwend_data.append((email_address, breach_domain, breach_data, breach_date, breach_added, breach_description))

        except ValueError:
            pass
        except Exception:
            info('An Unhandled Exception Has Occured, Please Check The Log For Details\n' + INFO_LOG_FILE, exc_info=True)

    info('Compromised Account Enumeration Search Completed')
    return pwend_data


#Takes domain[str], api[list], user_agents[list] #Returns email,url [list[tuples]] Queue[object], prox[str]
def action_emailHunter(domain, api, user_agents, q, prox):
    info('Email Hunter Search Started')
    emails = []
    uas = user_agents
    ua = random.choice(uas)
    link = 'https://api.emailhunter.co/v1/search?domain={0}&api_key={1}'.format(domain,api)

    if prox == True:
                proxy = {'http' : 'http://127.0.0.1:8080'}
    else:
        pass
    try:
        headers = {"User-Agent" : ua,
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'en-US,en;q=0.5',
                   'Accept-Encoding': 'gzip, deflate'}
        if prox == True:
            response = requests.get(link, headers=headers, proxies=proxy, verify=False)
        else:
            response = requests.get(link, headers=headers, verify=False)
        if response.status_code == 200:
            json_data = response.json()
            for value in json_data['emails']:
                for domain in value['sources']:
                    url = str(domain['uri']).replace("u'","")
                    email =  str(value['value']).replace("u'","")
                    emails.append((email,url))
        elif response.status_code == 401:
            json_data = response.json()
            if json_data['message'] =='Too many calls for this period.':
                print colored("\tError:\tIt seems the Hunter API key being used has reached\n\t\tit's limit for this month.", 'red')
                print colored('\tAPI Key: {}\n'.format(api),'red')
                q.put(None)
                return None
            if json_data['message'] == 'Invalid or missing api key.':
                print colored("\tError:\tIt seems the Hunter API key being used is no longer valid,\nit was probably deleted.", 'red')
                print colored('\tAPI Key: {}\n'.format(api),'red')
                print colored('\tWhy don\'t you grab yourself a new one (they are free)','green')
                print colored('\thttps://hunter.io/api_keys','green')
                q.put(None)
                return None
        else:
            raise ValueError('No Response From Hunter')
    except UnboundLocalError,e:
        print e
    except KeyError:
        pass
    except ValueError:
        info(traceback.print_exc())
        pass
    except Exception:
        traceback.print_exc()
        info('An Unhandled Exception Has Occured, Please Check The Log For Details\n' + INFO_LOG_FILE, exc_info=True)

    info('Email Hunter Search Completed')
    q.put(sorted(emails))


def action_bing_true(domain, q, user_agents, prox):
    info('Bing Search Started')
    emails = []
    uas = user_agents
    searchfor = '@' + '"' + domain + '"'
    for start in range(0,30):
        ua = random.choice(uas)
        if prox == True:
            proxy = {'http' : 'http://127.0.0.1:8080'}
        else:
            pass
        try:
            headers = {"Connection" : "close",
                       "User-Agent" : ua,
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Language': 'en-US,en;q=0.5',
                       'Accept-Encoding': 'gzip, deflate'}
            payload = { 'q': searchfor, 'first': start}
            link = 'https://www.bing.com/search'
            if prox == True:
                response = requests.get(link, headers=headers, params=payload, proxies=proxy, verify=False)
            else:
                response = requests.get(link, headers=headers, params=payload, verify=False)
            reg_emails = re.compile('[a-zA-Z0-9.-]*' + '@' + '<strong>')
            temp = reg_emails.findall(response.text)
            time.sleep(1)
            for item in temp:
                clean = item.replace("<strong>", "")
                email.append(clean + domain)

        except Exception:
            continue
    info('Bing Search Completed')
    q.put(sorted(emails))

def doc_exalead(domain, user_agents, prox, q):
    document_list = []
    uas = user_agents
    info('Exalead Document Search Started')
    for start in range(0,80,10):
        ua = random.choice(uas)
        link = 'http://www.exalead.com/search/web/results/?search_language=&q=(filetype:xls+OR+filetype:doc+OR++filetype:pdf+OR+filetype:ppt)+site:{}&search_language=&elements_per_page=10&start_index={}'.format(domain, start)
        if prox == True:
            proxy = {'http' : 'http://127.0.0.1:8080'}
        else:
            pass
        try:
            headers = {"Connection" : "close",
                       "User-Agent" : ua,
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Language': 'en-US,en;q=0.5',
                       'Accept-Encoding': 'gzip, deflate'}
            if prox == True:
                response = requests.get(link, headers=headers, proxies=proxy, verify=False)
            else:
                response = requests.get(link, headers=headers, verify=False)
            soup = BeautifulSoup(response.text, "lxml")
            if soup.find('label', {'class': 'control-label', 'for': 'id_captcha'}):
                info("So you don't like spinach?")
                info("Captchas are preventing some document searches.")
                break
            for div in soup.findAll('li', {'class': 'media'}):
                document = div.find('a', href=True)['href']
                document = urllib2.unquote(document)
                document_list.append(document)

        except Exception:
            info('An Unhandled Exception Has Occured, Please Check The Log For Details' + INFO_LOG_FILE)
            continue

        time.sleep(10)
    potential_docs = len(document_list)
    info('Exalead Document Search Finished')
    info('Potential Exalead Documents Found: {}'.format(potential_docs))
    q.put(document_list)

def doc_bing(domain, user_agents, prox, q):
    document_list = []
    uas = user_agents
    info('Bing Document Search Started')
    for start in range(1,300,10):
        ua = random.choice(uas)
        if prox == True:
            proxy = {'http' : 'http://127.0.0.1:8080'}
        else:
            pass
        try:
            headers = {"Connection" : "close",
                       "User-Agent" : ua,
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Language': 'en-US,en;q=0.5',
                       'Accept-Encoding': 'gzip, deflate'}
            payload = { 'q': 'filetype:(doc dot docx docm dotx dotm docb xls xlt xlm xlsx xlsm xltx xltm xlsb xla xlam xll xlw ppt pot pps pptx pptm potx potm ppam ppsx ppsm sldx sldm pub pdf) site:{}'.format(domain), 'first': start}
            link = 'http://www.bing.com/search'
            if prox == True:
                response = requests.get(link, headers=headers, proxies=proxy, params=payload, verify=False)
            else:
                response = requests.get(link, headers=headers, params=payload, verify=False)

            soup = BeautifulSoup(response.text, "lxml")

            divs = soup.findAll('li', {'class': 'b_algo'})
            for div in divs:
                h2 = div.find('h2')
                document = h2.find('a', href=True)['href']
                document = urllib2.unquote(document)
                document_list.append(document)
        except requests.models.ChunkedEncodingError:
            continue
        except Exception:
            traceback.print_exc()
            continue
    potential_docs = len(document_list)
    info('Bing Document Search Finished')
    q.put(document_list)

def action_linkedin(domain, userCountry, q, company, user_agents, prox):
    info('LinkedIn Search Started')
    uas = user_agents
    entries_tuples = []
    seen = set()
    results = []
    who_error = False
    searchfor = 'site:linkedin.com/in ' + '"' + company + '"'
    ua = random.choice(uas)
    for start in range(1,50,1):
        if prox == True:
            proxy = {'http' : 'http://127.0.0.1:8080'}
        else:
            pass
        try:
            headers = {"Connection" : "close",
                       "User-Agent" : ua,
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Language': 'en-US,en;q=0.5',
                       'Accept-Encoding': 'gzip, deflate'}
            payload = { 'q': searchfor, 'first': start}
            link = 'http://www.bing.com/search'
            if prox == True:
                response = requests.get(link, headers=headers, params=payload, proxies=proxy, verify=False)
            else:
                response = requests.get(link, headers=headers, params=payload, verify=False)

            response.text.encode('utf-8')
            soup = BeautifulSoup(response.text, "lxml")

            for div in soup.findAll('li', {'class': 'b_algo'}):
                title_temp = div.find('a').text
                url = div.find('cite').text.encode('utf-8')
                person = str((title_temp.split(' | ')[0]))
                description_temp = div.find('div', {'class': 'b_caption'})
                description = description_temp.find('p').text.encode('utf-8').lstrip('View ').replace("’s","").replace("professional profile on LinkedIn. ... ","").replace(" professional profile on LinkedIn. LinkedIn is the world's largest business network, ...","").replace("’S","").replace("’","").replace("professional profile on LinkedIn.","").replace(person, '').lstrip(' ').lstrip('. ').replace("LinkedIn is the world's largest business network, helping professionals like  discover ...","").replace("LinkedIn is the world's largest business network, helping professionals like  discover inside ...","").replace("professional profile on ... • ","").replace("professional ... ","").replace("...","").lstrip('•').lstrip(' ')
                entries_tuples.append((url, person.title(), description))

        except Exception:
            continue

    for urls in entries_tuples:
        if urls[1] not in seen:
            results.append(urls)
            seen.add(urls[1])

    info('LinkedIn Search Completed')
    q.put(sorted(results))


def action_netcraft(domain, myResolver):
    info('NetCraft Search Started')
    netcraft_list = []
    print "\nPassive Gatherings From NetCraft\n"
    try:
        link = "http://searchdns.netcraft.com/?restriction=site+contains&host=*.{}&lookup=wait..&position=limited" .format (domain)
        response = requests.get(link, verify=False)
        soup = BeautifulSoup(response.content, 'lxml')
        pattern = 'rel="nofollow">([a-z\.\-A-Z0-9]+)<FONT COLOR="#ff0000">'
        sub_results = re.findall(pattern, response.content)
    except dns.exception.Timeout:
        pass
    except Exception:
        info('An Unhandled Exception Has Occured, Please Check The Log For Details\n' + INFO_LOG_FILE, exc_info=True)

    if sub_results:
        for item in sub_results:
            try:
                netcheck = myResolver.query(item + '.' + domain)
                for data in netcheck:
                    netcraft_list.append(item + '.' + domain + ' ' + str(data))
                    print colored(item + '.' + domain, 'red')
            except dns.exception.Timeout:
                pass
            except dns.resolver.NXDOMAIN:
                pass
            except Exception:
                info('An Unhandled Exception Has Occured, Please Check The Log For Details\n' + INFO_LOG_FILE, exc_info=True)
    else:
        print '\tNo Results Found'

    info('NetCraft Completed')
    return netcraft_list
