from .linkedin_class import FindPeople
from ..html_report import write_html
from ..logger_ import info
import json
from termcolor import colored

def linkedIn(params):
	print ('\nActive LinkedIn Check:\n')
	info('active linkedin initialised')
	args = params[0][0]
	q1 = params[0][1]
	people = []
	obj = FindPeople(args, page_limits='5:101', company_details='', company='', company_number='')
	obj.company()
	obj.people()
	results = obj.output.get()


	if results:
		for tup in results:
			tempDict = {}
			for elem in tup:
				elem = elem.split(";")
				tempDict.update({elem[0]:elem[1]})
			people.append(tempDict)
		people = {'person':people}
		people = str(people).replace("'", '"')

		write_html(people, 'company name', args)
		output = json.dumps(str(people))
		parsed = json.loads(output)
		print (colored('\n\nOutput To HTML Module', 'magenta', attrs=['blink']))
		data = json.dumps(parsed, indent=6, sort_keys=True)
		print (colored(data, 'blue'))

	else:
		print('No Data')
