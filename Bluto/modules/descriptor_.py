def des():
	value = """

Description:
    DNS Recon | Brute Forcer | DNS Zone Transfer | DNS Wild Card Checks | DNS Wild Card Brute Forcer
    Email Enumeration | Staff Enumeration | Compromised Account Enumeration | MetaData Harvesting
	                                  Web Inspection

    Author:  Darryl Lane
    Twitter: @darryllane101

Required Arguments:
	bluto -d, --domain Target Domain

Optional Arguments:
	bluto -t,  --timeo Set DNS Timeout value | Default 5
	bluto -ts, --top   Set value for top Subdomains, eg --top 100
	bluto -b,  --brute Enable Subdomain BruteForcing (This includes WildCard Checks and ZoneTrafer Checks)
	bluto -dns, --dsn  Carry out DNS enumeration
"""
	return value

def soa_build(data):
	m_name, ttl, class_, ns, email, serial, refresh, retry, expiry, minim = data
	value = '''{{
		"soa_data": [
		    {{
		                "Main Name In Zone": "{a}",
		                "Cache TTL": "{b}",
		                "Class": "{c}",
		                "Authoritive NS": "{d}",
		                "Email Address": "{e}",
		                "Last Change": "{f}",
		                "Retry In Secs": "{g}",
		                "Expiry": "{h}",
		                "Slave Cache In Sec": "{i}"
		    }}
		]
	}}'''.format(a = m_name, b = ttl, c = class_, d = ns, e = email, f = serial, g = retry, h = expiry, i = minim)
	value = value.replace(' ', '').replace('\t', '').replace('\n', '')
	print value
	return value
