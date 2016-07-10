**BLUTO**
-----
**DNS Recon | Brute Forcer | DNS Zone Transfer | DNS Wild Card Checks | DNS Wild Card Brute Forcer | Email Enumeration | Staff Enumeration | Compromised Account Enumeration**
 
>Author: Darryl Lane  |  Twitter: @darryllane101

>https://github.com/darryllane/Bluto

Bluto has gone through a large code base change and various feature additions have been added since its first day on the job. Now that RandomStorm has been consumed and no longer exists, I felt it time to move the repo to a new location. So from this git push onwards Bluto will live here. I hope you enjoy the new Bluto.


The target domain is queried for MX and NS records. Sub-domains are passively gathered via NetCraft. The target domain NS records are each queried for potential Zone Transfers. If none of them gives up their spinach, Bluto will attempt to identify if SubDomain Wild Cards are being used. If they are not Bluto will brute force subdomains using parallel sub processing on the top 20000 of the 'The Alexa Top 1 Million subdomains' If Wild Cards are in place, Bluto will still Brute Force SubDomains but using a different technique which takes roughly 4 x longer. NetCraft results are then presented individually and are then compared to the brute force results, any duplications are removed and particularly interesting results are highlighted. 

Bluto now does email address enumeration based on the target domain, currently using Bing and Google search engines plus gathering data from the Email Hunter service and LinkedIn. https://haveibeenpwned.com/ is then used to identify if any email addresses have been compromised.

Search engine queries are configured in such a way to use a random `User Agent:` on each request and does a country look up to select the fastest Google server in relation to your egress address. Each request closes the connection in an attempt to further avoid captchas, however exsesive lookups will result in captchas (Bluto will warn you if any are identified). 
         
Bluto requires various other dependencies. So to make things as easy as possible, `pip` is used for the installation. This does mean you will need to have pip installed prior to attempting the Bluto install.

Bluto now takes command line arguments at launch, the new options are as follows;

-E  		This uses a very large subdomain list for bruting.
-api		You can supply your email hunter api key here to gather a considerably larger amount of email addresses.

Examples: 

	Bluto -api 2b0ab19df982a783877a6b59b982fdba4b6c3669
	Bluto -E
	Bluto - api 2b0ab19df982a783877a6b59b982fdba4b6c3669 -E



**Pip Install Instructions**

Note: To test if pip is already installed execute.

`pip -V`

(1) Mac and Kali users can simply use the following command to download and install `pip`.

`curl https://bootstrap.pypa.io/get-pip.py -o - | python`

**Bluto Install Instructions**

(1) Once `pip` has successfully downloaded and installed, we can install Bluto:

`sudo pip install git+git://github.com/darryllane/Bluto`

(2) You should now be able to execute 'bluto' from any working directory in any terminal.
 
`bluto`

**Upgrade Instructions**

(1) The upgrade process is as simple as;

`sudo pip install git+git://github.com/darryllane/Bluto --upgrade`

