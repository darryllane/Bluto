import json
import os
import traceback
from .logger_ import info, error


def blank_user():
	obj = 'data:image/png;base64,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'
	return obj

def write_html(users, company_details, args):
	try:
		LOG_ROOT = os.path.expanduser('~/Bluto/')
		COMPANY_LOC = LOG_ROOT+'{}'.format(str(args.domain).split('.', 1)[0])
		args.COMPANY_LOC = COMPANY_LOC
		if not os.path.exists(COMPANY_LOC):
			os.makedirs(COMPANY_LOC)
			os.chmod(COMPANY_LOC, 0o700)
		
	except Exception:
		print('An Unhandled Exception Has Occured, Please Check The \'Error\' For Details')
		info('An Unhandled Exception Has Occured, Please Check The \'Error\' For Details')
		error(traceback.print_exc())

	info('HTML report initialised')
	head = '''
	    <!DOCTYPE html>
	    <html>
	    <head>
	<style>
			.card {
		  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
		  max-width: 250px;
		  text-align: center;
		  font-family: arial;
		}

		.title {
		  color: grey;
		  font-size: 18px;
		}

		button {
		  border: none;
		  outline: 0;
		  display: inline-block;
		  padding: 8px;
		  color: white;
		  background-color: #3399cc;
		  text-align: center;
		  cursor: pointer;
		  width: 100%;
		  font-size: 18px;
		}

		a {
		  text-decoration: none;
		  margin:auto;
		  font-size: 22px;
		  color: black;
		}

		button:hover, a:hover {
		  opacity: 0.7;
		}

	footer {
        background-color:black;
        color:white;
        clear:both;
        text-align:center;
        padding:5px;
    }
	</style>
    </head>
	'''

	header ='''
	    <header>
	        <h1>Bluto Evidence Report</h1>
	        <h2>{a}</h2>
	    </header>'''.format(a=company_details)


	footer = '''
        <footer>
            <p>Bluto</p>
            <p>Author: Darryl Lane</p>
            <p>Twitter: @darryllane101</p>
        </footer>'''

	body_end ='''
		</body>
        </html>
        '''

	try:
		
		with open(args.COMPANY_LOC + '/linkedin_report.html', 'w') as myFile:
			myFile.write(head)
			myFile.write(header)
			myFile.write('<body>')
			myFile.write('<h2>Staff Profiles</h2>')
			myFile.write('<p>Resize the browser window to affect sizes, may move to static structure.</p>')
			myFile.write('<br>')
			for key, value in dict.items(users):
				for user in value:
					name = user['name']
					job = user['role']
					confirmed = user['confirmed']
					url = user['image']
					if url == 'None':
						url = blank_user()
						
					address = user['location']
					email = user['email']

					myFile.write('<div class="row">')
					myFile.write('<div class="column">')
					myFile.write('<div class="card">')
					myFile.write('<img src="{url}" style="width:100%">'.format(url=url))
					myFile.write('<div class="container">')
					myFile.write('<h2>{name}</h2>'.format(name=name))
					myFile.write('<p class="title">{job}</p>'.format(job=job))
					myFile.write('<p>{address}</p>'.format(address=address))
					myFile.write('<p>{email}</p>'.format(email=email))
					myFile.write('<p>Confirmed: {confirmed}</p>'.format(confirmed=confirmed))
					myFile.write('<p><button class="button">Details</button></p>')
					myFile.write('</div>')
					myFile.write('</div>')
					myFile.write('</div>')

			myFile.write(footer)
			myFile.write(body_end)
			myFile.close()
			info('Completed HTML Report')
	except IOError:
		error('IOError', exc_info=True)
	except Exception:
		print('An Unhandled Exception Has Occured, Please Check The \'Error\' For Details')
		info('An Unhandled Exception Has Occured, Please Check The \'Error\' For Details')
		error(traceback.print_exc())
