from termcolor import colored

def des():
	value = """

Optional Arguments:
 bluto -t      --timeo Set DNS Timeout value | Default 5
 bluto -ts     --top   Set value for top Subdomains, eg --top 100
 bluto -b      --brute Enable Subdomain BruteForcing*
 bluto -dns    --dsn  Carry out DNS enumeration
    
 *(This includes WildCard Checks and ZoneTrafer Checks)
"""
	return value

def soa_build(data):
	m_name, ttl, class_, ns, email, serial, refresh, retry, expiry, minim = data
	value = '''{{
		"soa_data":
		    [{{
		                "Main Name In Zone": "{a}",
		                "Cache TTL": "{b}",
		                "Class": "{c}",
		                "Authoritive NS": "{d}",
		                "Email Address": "{e}",
		                "Last Change": "{f}",
		                "Retry In Secs": "{g}",
		                "Expiry": "{h}",
		                "Slave Cache In Sec": "{i}"
		    }}]

	}}'''.format(a = m_name, b = ttl, c = class_, d = ns, e = email, f = serial, g = retry, h = expiry, i = minim)
	return value


def welcome(args):

	title = """
BBBBBBBBBBBBBBBBB  lllllll                       tttt
B::::::::::::::::B l:::::l                     ttt:::t
B::::::BBBBBB:::::Bl:::::l                     t:::::t
BB:::::B     B:::::l:::::l{0}               t:::::t
  B::::B     B:::::Bl::::luuuuuu    uuuuuttttttt:::::ttttttt      ooooooooooo
  B::::B     B:::::Bl::::lu::::u    u::::t:::::::::::::::::t    oo:::::::::::oo
  B::::BBBBBB:::::B l::::lu::::u    u::::t:::::::::::::::::t   o:::::::::::::::o
  B:::::::::::::BB  l::::lu::::u    u::::tttttt:::::::tttttt   o:::::ooooo:::::o
  B::::BBBBBB:::::B l::::lu::::u    u::::u     t:::::t         o::::o     o::::o
  B::::B     B:::::Bl::::lu::::u    u::::u     t:::::t         o::::o     o::::o
  B::::B     B:::::Bl::::lu::::u    u::::u     t:::::t         o::::o     o::::o
  B::::B     B:::::Bl::::lu:::::uuuu:::::u     t:::::t    ttttto::::o     o::::o
BB:::::BBBBBB::::::l::::::u:::::::::::::::uu   t::::::tttt:::::o:::::ooooo:::::o
B:::::::::::::::::Bl::::::lu:::::::::::::::u   tt::::::::::::::o:::::::::::::::o
B::::::::::::::::B l::::::l uu::::::::uu:::u     tt:::::::::::ttoo:::::::::::oo
BBBBBBBBBBBBBBBBB  llllllll   uuuuuuuu  uuuu       ttttttttttt    ooooooooooo
	""".format(colored("v" + args.VERSION_CONST, 'red'))

	desc = """{2} | {3} | {4} | {9}
    {8} | {7} | {10}
	    {11}  |  {12}
	        {0}  |  {1}
	            {5}""" . format (colored("Author: Darryl Lane", 'blue'),
	              colored("Twitter: @darryllane101", 'blue'),
	              colored("DNS Recon", 'green'),
	              colored("SubDomain Brute Forcer", 'green'),
	              colored("DNS Zone Transfers", 'green'),
	              colored("https://github.com/darryllane/Bluto", 'green'),
	              colored("v" + args.VERSION_CONST, 'red'),
	              colored("Email Enumeration", 'green'),
	              colored("Staff Enumeration", 'green'),
	              colored("DNS Wild Card Checks", 'green'),
	              colored("DNS Wild Card Brute Forcer", 'green'),
	              colored("Compromised Account Enumeration", 'green'),
	              colored("MetaData Mining", 'green'))

	print(title)
	print(desc)
