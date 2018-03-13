from .b_classes import linkedin_class


def linkedIn(args):
	people = []
	obj = linkedin_class.FindPeople(args, page_limits='5:100', company_details='', company='', company_number='')
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
		print(people)
	else:
		print('No Data')
