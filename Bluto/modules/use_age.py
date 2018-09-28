import json

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

def soa_build():
	value = """
	{
		"soa_data": [
		    {
		                "Main Name In Zone": "{{a}}",
		                "Cache TTL": "{{b}}",
		                "Class": "{{c}}",
		                "Authoritive NS": "{{d}}",
		                "Email Address": "{{e}}",
		                "Last Change": "{{f}}",
		                "Retry In Secs": "{{g}}",
		                "Expiry": "{{h}}",
		                "Slave Cache In Sec": "{{i}}"
		    }
		],
	}""".format(a = m_name, b = ttl, c = class_, d = ns, e = str(email).replace('\\', ''), f = serial, g = retry, h = expiry, i = minim)

	return value

def debug_out(value):
	if isinstance(value, dict):
		print (json.dumps(value, indent=4, sort_keys=True))
	if isinstance(value, list):
		clean_dump = {'key': [item for item in value] }
		print (json.dumps(clean_dump, indent=4, sort_keys=True))


def bluto_use():
	now = datetime.datetime.now()
	try:
		link = "http://darryllane.co.uk/bluto/log_use.php"
		payload = {'country': countryID, 'Date': now}
		requests.post(link, data=payload)
	except Exception:
		info('An Unhandled Exception Has Occured, Please Check The Log For Details' + INFO_LOG_FILE)
		pass