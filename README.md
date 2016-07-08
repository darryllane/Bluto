**BLUTO**
-----
**DNS recon | Brute forcer | DNS Zone Transfer | Email Enumeration**
 
>Author: Darryl Lane  |  Twitter: @darryllane101

>https://github.com/RandomStorm/Bluto


The target domain is queried for MX and NS records. Sub-domains are passively gathered via NetCraft. The target domain NS records are each queried for potential Zone Transfers. If none of them gives up their spinach, Bluto will brute force subdomains using parallel sub processing on the top 20000 of the 'The Alexa Top 1 Million subdomains'. NetCraft results are presented individually and are then compared to the brute force results, any duplications are removed and particularly interesting results are highlighted. 

Bluto now does email address enumeration based on the target domain, currently using Bing and Google search engines. It is configured in such a way to use a random `User Agent:` on each request and does a country look up to select the fastest Google server in relation to your egress address. Each request closes the connection in an attempt to further avoid captchas, however exsesive lookups will result in captchas (Bluto will warn you if any are identified). 
         
Bluto requires various other dependencies. So to make things as easy as possible, `pip` is used for the installation. This does mean you will need to have pip installed prior to attempting the Bluto install.

**Pip Install Instructions**

Note: To test if pip is already installed execute.

`pip -V`

(1) Mac and Kali users can simply use the following command to download and install `pip`.

`curl https://bootstrap.pypa.io/get-pip.py -o - | python`

**Bluto Install Instructions**

(1) Once `pip` has successfully downloaded and installed, we can install Bluto:

`sudo pip install git+git://github.com/RandomStorm/Bluto`

(2) You should now be able to execute 'bluto' from any working directory in any terminal.
 
`bluto`

**Upgrade Instructions**

(1) The upgrade process is as simple as;

`sudo pip install git+git://github.com/RandomStorm/Bluto --upgrade`

