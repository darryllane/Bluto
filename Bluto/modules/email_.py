import requests
import re
import json
import os
import random
import traceback
import threading
from multiprocessing import Queue
from bs4 import BeautifulSoup
from .logger_ import info, error
import queue as Queue

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
        self.EmailQue = Queue.Queue()
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
            print('An unhandled exception has occured, please check the \'Error log\' for details')
            info('An unhandled exception has occured, please check the \'Error log\' for details')
            error(traceback.print_exc())
            
        try:
            with open(self.country_file) as fin:
                    for line in fin:
                        key, value = line.strip().split(';')
                        self.tcountries_dic.update({key: value})
            
            self.countries_dic = dict((k.lower(), v.lower()) for k,v in self.tcountries_dic.items())
            
        except Exception:
            print('An unhandled exception has occured, please check the \'Error log\' for details')
            info('An unhandled exception has occured, please check the \'Error log\' for details')
            error(traceback.print_exc())
            
        
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
                print('\nAn unhandled exception has occured, please check the \'Error log\' for details')
                info('An unhandled exception has occured, please check the \'Error log\' for details')
                error(traceback.print_exc())
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
            print('An unhandled exception has occured, please check the \'Error log\' for details')
            info('An unhandled exception has occured, please check the \'Error log\' for details')
            error(traceback.print_exc())        
                
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
                                print('An unhandled exception has occured, please check the \'Error log\' for details')
                                info('An unhandled exception has occured, please check the \'Error log\' for details')
                                error(traceback.print_exc())
        
            except Exception:
                print('An unhandled exception has occured, please check the \'Error log\' for details')
                info('An unhandled exception has occured, please check the \'Error log\' for details')
                error(traceback.print_exc(), exc_info=True)                               
            
        
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
                print('An unhandled exception has occured, please check the \'Error log\' for details')
                info('An unhandled exception has occured, please check the \'Error log\' for details')
                error(traceback.print_exc())                     
                               
        
        self.EmailQue.put(email_seen)
    
    
    
    def exlead(self):
        """
        Carry out Exlead search scrape for email addresses
        on target domain
        
        !!!!remeber to cross reference email addresses with linkedin users for match
        """
        
        email_seen = []

        headers = {"Connection" : "close",
                   "User-Agent" : random.choice(self.uas).decode('utf-8'),
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
                    info('Exlead is responding with a Captcha, other searches will continue')               
                    error('Exlead is responding with a Captcha, other searches will continue')
                    return
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
                print('An unhandled exception has occured, please check the \'Error log\' for details')
                info('An unhandled exception has occured, please check the \'Error log\' for details')
                error(traceback.print_exc())              
                
        
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
                                    
            except Exception:
                print('An unhandled exception has occured, please check the \'Error log\' for details')
                info('An unhandled exception has occured, please check the \'Error log\' for details')
                error(traceback.print_exc())             
        
        
        self.EmailQue.put(email_seen)
        