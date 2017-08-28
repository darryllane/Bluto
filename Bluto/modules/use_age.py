import json

def des():
	value = """

Description:

    Filler

    Author:  Darryl Lane
    Twitter: @darryllane101
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
		print json.dumps(value, indent=4, sort_keys=True)
	if isinstance(value, list):
		clean_dump = {'key': [item for item in value] }
		print json.dumps(clean_dump, indent=4, sort_keys=True)
