**BLUTO**
-----
**DNS Recon | Brute Forcer | DNS Zone Transfer | DNS Wild Card Checks | DNS Wild Card Brute Forcer | Email Enumeration | Staff Enumeration | Compromised Account Enumeration | MetaData Harvesting**
 
>Author: Darryl Lane  |  Twitter: @darryllane101

>https://github.com/darryllane/Bluto

Like Bluto?
====
Give us a vote: https://n0where.net/dns-analysis-tool-bluto/

Bluto has gone through a large code base change and various feature additions have been added since its first day on the job. Now that RandomStorm has been consumed and no longer exists, I felt it time to move the repo to a new location. So from this git push onwards Bluto will live here. I hope you enjoy the new Bluto.


The target domain is queried for MX and NS records. Sub-domains are passively gathered via NetCraft. The target domain NS records are each queried for potential Zone Transfers. If none of them gives up their spinach, Bluto will attempt to identify if SubDomain Wild Cards are being used. If they are not Bluto will brute force subdomains using parallel sub processing on the top 20000 of the 'The Alexa Top 1 Million subdomains' If Wild Cards are in place, Bluto will still Brute Force SubDomains but using a different technique which takes roughly 4 x longer. NetCraft results are then presented individually and are then compared to the brute force results, any duplications are removed and particularly interesting results are highlighted. 

Bluto now does email address enumeration based on the target domain, currently using Bing and Google search engines plus gathering data from the Email Hunter service and LinkedIn. https://haveibeenpwned.com/ is then used to identify if any email addresses have been compromised. Previously Bluto produced a 'Evidence Report' on the screen, this has now been moved off screen and into an HTML report.

Search engine queries are configured in such a way to use a random `User Agent:` on each request and does a country look up to select the fastest Google server in relation to your egress address. Each request closes the connection in an attempt to further avoid captchas, however exsesive lookups will result in captchas (Bluto will warn you if any are identified). 
         
Bluto requires various other dependencies. So to make things as easy as possible, `pip` is used for the installation. This does mean you will need to have pip installed prior to attempting the Bluto install.

Bluto now takes command line arguments at launch, the new options are as follows;

	-e		This uses a very large subdomain list for bruting.
	-api	You can supply your email hunter api key here to gather a considerably larger amount of email addresses.
	-d		Used to specify the target domain on the commandline.
	-t		Used to set a timeout value in seconds. Default is 10

**Examples:** (feel free to use this EmailHunter API Key until it is removed)

	bluto -api 2b0ab19df982a783877a6b59b982fdba4b6c3669
	bluto -e
	bluto -api 2b0ab19df982a783877a6b59b982fdba4b6c3669 -e
	bluto -d example.com -api 2b0ab19df982a783877a6b59b982fdba4b6c3669 -e


**Pip Install Instructions**

Note: To test if pip is already installed execute.

`pip -V`

(1) Mac and Kali users can simply use the following command to download and install `pip`.

`curl https://bootstrap.pypa.io/get-pip.py -o - | python`

**Bluto Install Instructions**

(1) Once `pip` has successfully downloaded and installed, we can install Bluto:

`sudo pip install bluto`

(2) You should now be able to execute 'bluto' from any working directory in any terminal.
 
`bluto`

**Upgrade Instructions**

(1) The upgrade process is as simple as;

`sudo pip install bluto --upgrade`


**Install From Dev Branch**

(1) To install from the latest development branch (maybe unstable);

`sudo pip uninstall bluto`

`sudo pip install git+git://github.com/darryllane/Bluto@dev`

Change/Feature Requests
====
* ~~MetaData Scraping From Document Hunt On Target Domain~~
* ~~Target Domain Parsed As Argument~~
* Identification Of Web Portals
* Active Document Hunting

Changelog
====
* Version __2.4.7__ (__20/07/2018__):
  * GeoIP lookup refactor
  
* Version __2.3.10__ (__13/01/2017__):
  * BugFixes
  
* Version __2.3.6__ (__14/08/2016__):
  * BugFixes
  * Timeout value can be parsed as argument (-t 5)
  
* Version __2.3.2__ (__02/08/2016__):
  * MetaData Scraping From Document Hunt On Target Domain
  * Target Domain Parsed As Argument
  
* Version __2.0.1__ (__22/07/2016__):
  * Compromised Account Data Prensented In Terminal And HTML Report

* Version __2.0.0__ (__19/07/2016__):
  * Pushed Live 2.0
 
* Version __1.9.9__ (__09/07/2016__):
  * Email Hunter API Support Added.
  * Haveibeenpwned API Support Added.
  * HTML Evidence Report Added.
  * Modulated Code Base.
  * Local Error Logging.


**Help Section**

This section contains helpful snippets.

Check version of openssl being used by python

	python
	import ssl
	ssl.OPENSSL_VERSION`

Output

	>>> import ssl
	>>> ssl.OPENSSL_VERSION
	'OpenSSL 1.0.2j  26 Sep 2016'
	>>>

Please be aware that the current version of Bluto does not support Python 3. It is a python 2.7.x application.
