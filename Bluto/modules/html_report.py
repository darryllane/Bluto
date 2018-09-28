import json
import os
import traceback
from .logger_ import info, error

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
					url = user['image']
					address = user['location']
					email = 'FILLER'

					myFile.write('<div class="row">')
					myFile.write('<div class="column">')
					myFile.write('<div class="card">')
					myFile.write('<img src="{url}" style="width:100%">'.format(url=url))
					myFile.write('<div class="container">')
					myFile.write('<h2>{name}</h2>'.format(name=name))
					myFile.write('<p class="title">{job}</p>'.format(job=job))
					myFile.write('<p>{address}</p>'.format(address=address))
					myFile.write('<p>{email}</p>'.format(email=email))
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
