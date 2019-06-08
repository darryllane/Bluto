import requests
import re
import json
import os
import random
import time
import traceback
import threading
from termcolor import colored
from bs4 import BeautifulSoup
from .logger_ import error, info, INFO_LOG_FILE, ERROR_LOG_FILE
from multiprocessing import Queue

requests.packages.urllib3.disable_warnings()

class Search(object):
    """
    
    Email search class
    
    
    """
    
    def __init__(self, args):
        """ 
        initiat
        """
        info('email module init')
        self.EmailQue = Queue()
        self.uas = []
        self.args =  args[0][0]
        self.proxy = self.args.proxy
        self.user_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../doc/user_agents.txt'))
        self.country_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../doc/countries.txt'))
        self.tcountries_dic = {}
        try:
            info('gathering user_agents')
            with open(self.user_file, 'rb') as uaf:
                for ua in uaf.readlines():
                    if ua:
                        ua = ua.strip(b'\n')
                        self.uas.append(ua)
    
            info('completed gathering user_agents')
        except Exception:
            if self.args.verbose:
                    print('An unhandled exception has occured, please check the \'Error log\' for details')
                    print(traceback.print_exc())
            info('An unhandled exception has occured, please check the \'Error log\' for details')
            error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)
            
        try:
            with open(self.country_file) as fin:
                    for line in fin:
                        key, value = line.strip().split(';')
                        self.tcountries_dic.update({key: value})
            
            self.countries_dic = dict((k.lower(), v.lower()) for k,v in self.tcountries_dic.items())
            
        except Exception:
            if self.args.verbose:
                print('An unhandled exception has occured, please check the \'Error log\' for details')
                print(traceback.print_exc())
            info('An unhandled exception has occured, please check the \'Error log\' for details')
            error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)       
            
        
        while True:
            try:
                if self.args.proxy:
                    
                    self.proxy = {'http' : 'http://{}'.format(self.proxy),
                                'https': 'https://{}'.format(self.proxy)}
                    r = requests.get(r'http://api.ipstack.com/check?access_key=dd763372274e9ae8aed34a55a7a4b36a', 
                                proxies=self.proxy, verify=False)
    
                else:
                    
                    r = requests.get(r'http://api.ipstack.com/check?access_key=dd763372274e9ae8aed34a55a7a4b36a', verify=False)
                
                self.originCountry = r.json()['country_name']
                
            except ValueError:
                self.originCountry = 'United Kingdom'
                continue
            except Exception:
                if self.args.verbose:
                    print('An unhandled exception has occured, please check the \'Error log\' for details')
                    print(traceback.print_exc())
                info('An unhandled exception has occured, please check the \'Error log\' for details')
                error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)    
                print('The Google UK server has been selected')
                self.originCountry = 'United Kingdom'
                continue
                
            break


    def google(self):
        """
        Carry out Google search scrape for email addresses
        on target domain
        
        !!!!remeber to cross reference email addresses with linkedin users for match
        """
        
        try:
            for country, server in self.countries_dic.items():
                if country.lower() == self.originCountry.lower():
                    self.userServer = server
                    if self.args.debug:
                        print('\n\tSearching From: {0}\n\tGoogle Server: {1}\n'.format(self.originCountry.title(), self.userServer))
                    
        except Exception:
            info('An unhandled exception has occured, please check the \'Error log\' for details')
            error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)                       
                
        email_seen = []
        
        for start in range(1,20,1):
            try:
                
                searchfor = '@' + '"{}"'.format(self.args.domain)
                
                headers = {"User-Agent" : random.choice(self.uas).decode('utf-8'),
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                           'Accept-Language': 'en-US,en;q=0.5',
                           'Accept-Encoding': 'gzip, deflate',
                           'Referer': 'https://www.google.com'}
                
                payload = { 'nord':'1', 'q': searchfor, 'start': start*10}
    
                link = '{0}/search?num=200' .format(self.userServer)
                if self.args.proxy:
                    response = requests.get(link, headers=headers, params=payload, proxies=self.proxy, verify=False, allow_redirects=True)
                else:
                    response = requests.get(link, headers=headers, params=payload, verify=False, allow_redirects=True)
                
                if response.status_code == 503:
                    if self.args.verbose:
                        print('Google is responding with a Captcha, other searches will continue')
                    info('Google is responding with a Captcha, other searches will continue')               
                    error('Google is responding with a Captcha, other searches will continue')
                    break        
                
                soup = BeautifulSoup(response.content, "lxml")
                
                for div in soup.select("div.g"):
                    
                    for div in soup.select("div.g"):
                        
                        url_tag = div.find("h3", class_="r")
                        if url_tag is not None:
                            url = url_tag.find('a', href=True)['href'].replace('/url?q=', '').replace('/url?url=', '')
            
                        email_temp = div.find("span", class_="st")
                        if email_temp is not None:
                            clean = re.sub('<em>', '', email_temp.text)
                            clean = re.sub('</em>', '', email_temp.text)
                            match = re.findall('[a-zA-Z0-9.]*' + '@' + self.args.domain, clean)
                            try:    
                                if len(match):
                                    for person in match:
                                        if '...' in person:
                                            pass
                                        else:
                                            if ((url, person)) in email_seen:
                                                pass
                                            else:
                                                email_seen.append((url, person.lower()))
                            
                            except UnboundLocalError:
                                pass
                            except Exception:
                                if self.args.verbose:
                                    print('An unhandled exception has occured, please check the \'Error log\' for details')
                                    print(traceback.print_exc())
                                info('An unhandled exception has occured, please check the \'Error log\' for details')
                                error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)                                   
        
            except Exception:
                if self.args.verbose:
                    print('An unhandled exception has occured, please check the \'Error log\' for details')
                    print(traceback.print_exc())
                info('An unhandled exception has occured, please check the \'Error log\' for details')
                error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)                                              
            
        if self.args.verbose:
            print('Google Out: {}'.format(email_seen))
            print('Google Count: {}\n'.format(len(email_seen)))
            
        self.EmailQue.put(email_seen)
             
                        
    def bing(self):
        """
        Carry out Bing search scrape for email addresses
        on target domain
        
        !!!!remeber to cross reference email addresses with linkedin users for match
        """
        
        email_seen = []
            
                
        headers = {"Connection" : "close",
                   "User-Agent" : random.choice(self.uas).decode('utf-8'),
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'en-US,en;q=0.5',
                   'Accept-Encoding': 'gzip, deflate'}
        
        for start in range(1,100,1):
            searchfor = '@' + self.args.domain
            try:
                
                link = 'https://www.bing.com/search?q=' + searchfor + '&first={}'.format(start)
            
                if self.args.proxy:
                    response = requests.get(link, headers=headers, proxies=self.proxy, verify=False)
                else:
                    response = requests.get(link, headers=headers, verify=False)
                    
                    
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "lxml")
                
                for li in soup.findAll('li', {'class': 'b_algo'}):
                    if li.find('div', {'class': 'b_caption'}):
                        caption = li.find('div', {'class': 'b_caption'})
                        clean = str(caption.find('p')).replace('<strong>', '').replace('</strong>', '')
                        if re.match(r'.*?([a-zA-Z0-9.-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*).*?', clean):
                            p = re.match(r'.*?([a-zA-Z0-9.-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*).*?', clean)
                            email = p.groups()[0]
                            url =  li.find('a')['href']
                            if (url, email) in email_seen:
                                pass
                            else:
                                email_seen.append((url, email.lower()))

            except Exception:
                if self.args.verbose:
                    print('An unhandled exception has occured, please check the \'Error log\' for details')
                    print(traceback.print_exc())
                info('An unhandled exception has occured, please check the \'Error log\' for details')
                error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)                            
                               
        if self.args.verbose:
            print('Bing Out: {}'.format(email_seen))
            print('Bing Count: {}\n'.format(len(email_seen)))   
            
        self.EmailQue.put(email_seen)
    
    
    def exlead(self):
        """
        Carry out Exlead search scrape for email addresses
        on target domain
        
        !!!!remeber to cross reference email addresses with linkedin users for match
        """
        
        email_seen = []

        headers = {"User-Agent" : random.choice(self.uas).decode('utf-8'),
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'en-US,en;q=0.5',
                   'Accept-Encoding': 'gzip, deflate'}
                            
        for start in range(0,1000,10):
            try:
                
                link = 'http://www.exalead.com/search/web/results/?q="@{}"&search_language=&elements_per_page=80&start_index={}'.format(self.args.domain, start)
            
                if self.args.proxy:
                    response = requests.get(link, headers=headers, proxies=self.proxy, verify=False)
                else:
                    response = requests.get(link, headers=headers, verify=False)
                    
                if 'We are sorry, but your request has been blocked' in response.text:
                    if self.args.verbose:
                        print('Exlead request has been blocked\n')                    
                    info('Exlead request has been blocked')               
                    error('Exlead request has been blocked')
                    break
                else:
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, "lxml")
                    
                    for li in soup.findAll('li', {'class': 'media'}):
                        span = li.find('span', {'class': 'ellipsis'})
    
                        if re.match(r'.*[\s|\">]([a-zA-Z0-9.-].*\@\<b\>.*?\<\/b\>).*'.format(self.args.domain), str(span)):
                            email = re.match(r'.*[\s|\">]([a-zA-Z0-9.-].*\@\<b\>.*?\<\/b\>).*'.format(self.args.domain), str(span)).groups()[0].replace('<b>', '').replace('</b>', '')
                            url =  li.find('a')['href']
                            
                            if (url, email) in email_seen:
                                pass
                            else:
                                email_seen.append((url, email.lower()))
    
            except Exception:
                if self.args.verbose:
                    print('An unhandled exception has occured, please check the \'Error log\' for details')
                    print(traceback.print_exc())
                info('An unhandled exception has occured, please check the \'Error log\' for details')
                error('An unhandled exception has occured, please check the \'Error log\' for details', exc_info=1)                              
                
        if self.args.verbose:
            print('Exlead Out: {}'.format(email_seen))
            print('Exlead Count: {}\n'.format(len(email_seen)))
            
        self.EmailQue.put(email_seen)
    
    
    def baidu(self):
        """
        Carry out Baidu search scrape for email addresses
        on target domain
        
        !!!!remeber to cross reference email addresses with linkedin users for match
        """
        
        email_seen = []
        headers = {"User-Agent" : random.choice(self.uas).decode('utf-8'),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate'}                        
        
        def url_clean(link):
            if self.proxy:
                    response = requests.get(link, headers=headers, proxies=self.proxy, verify=False)
            else:
                response = requests.get(link, headers=headers, verify=False)
                
            url = response.url
            return url
        

        
        for start in range(0,1000,10): 
            try:
                saerchfor = '"@{}"'.format(self.args.domain)
            
                link = 'https://www.baidu.com/s?wd={}&pn={}'.format(saerchfor, start)
    
                if self.proxy:
                    response = requests.get(link, headers=headers, proxies=self.proxy, verify=False)
                else:
                    response = requests.get(link, headers=headers, verify=False)
    
    
                soup = BeautifulSoup(response.content, "lxml")
    
                for li in soup.findAll('div', {'id': 'content_left'}):
                    if re.search(r'.*?([a-zA-Z0-9.-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*).*?', li.text):
                        match = re.search(r'.*?([a-zA-Z0-9.-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*).*?', li.text)
                        if self.args.domain in match.groups()[0]:
                            email = match.groups()[0]
                            if li.find('h3', {'class': 't c-title-en'}):
                                h = li.find('h3', {'class': 't c-title-en'})
                                url =  h.find('a')['href']
                                url = url_clean(url)
                                if (url, email) in email_seen:
                                    pass
                                else:
                                    email_seen.append((url, email.lower()))  
                                    
            except requests.exceptions.ConnectionError:
                if self.args.verbose:
                    print('DNS resolution failed for www.baidu.com')

                info('DNS resolution failed for www.baidu.com')
                error('DNS resolution failed for www.baidu.com')
                self.EmailQue.put(email_seen)
                return
            except Exception:
                info('An unhandled exception has occured, please check the \'Error log\' for details')
                error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)                        
        
        if self.args.verbose:
            print('Baidu Out: {}'.format(email_seen))
            print('Baidu Count: {}\n'.format(len(email_seen)))
        self.EmailQue.put(email_seen)
                        
                    
    def hunter_io(self):
        info('Hunter Search Started')
        emails = []
        link = 'https://api.hunter.io/v2/domain-search?domain=={0}&api_key={1}'.format(self.args.domain, self.args.api)
        if self.args.proxy == True:
            proxy = {'http' : 'http://127.0.0.1:8080'}
        else:
            pass
        try:
            headers = {"User-Agent" : random.choice(self.uas).decode('utf-8'),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate'}            
            if self.args.proxy == True:
                response = requests.get(link, headers=headers, proxies=proxy, verify=False)
            else:
                response = requests.get(link, headers=headers, verify=False)
            if response.status_code == 200:
                json_data = response.json()
                if json_data['pattern']:
                    info('Pattern Search Started')
                    self.pattern = json_data['pattern']
                for value in json_data['emails']:
                    for domain in value['sources']:
                        url = str(domain['uri']).replace("u'","")
                        email =  str(value['value']).replace("u'","")
                        emails.append((url, email))
            elif response.status_code == 401:
                json_data = response.json()
                if json_data['message'] =='Too many calls for this period.':
                    print(colored("\tError:\tIt seems the Hunter API key being used has reached\n\t\tit's limit for this month.", 'red'))
                    print(colored('\tAPI Key: {}\n'.format(self.args.api),'red'))
                    q.put(None)
                    return None
                if json_data['message'] == 'Invalid or missing api key.':
                    print(colored("\tError:\tIt seems the Hunter API key being used is no longer valid", 'red'))
                    print(colored('\tAPI Key: {}\n'.format(self.args.api),'red'))
                    print(colored('\tWhy don\'t you grab yourself a new one (they are free)','green'))
                    print(colored('\thttps://hunter.io/api_keys','green'))
                    q.put(None)
                    return None
            else:
                raise Valueerror('No Response From Hunter')
        except UnboundLocalError:
            error('An UnboundLocalError Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)
        except KeyError:
            pass
        except ValueError:
            pass
        except Exception:
            info('An unhandled exception has occured, please check the \'Error log\' for details')
            error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)   
    
        info('Hunter Search Completed')
        self.EmailQue.put(emails)