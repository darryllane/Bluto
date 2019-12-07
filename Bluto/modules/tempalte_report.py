from bs4 import BeautifulSoup
import os

class Dashboard():
	def __init__(self, data):
		"filler"


class DNSEnumeration():
	def __init__(self, data):
		"filler"
		

class StaffEnumeration():

	def __init__(self, data, args):
		
		self.args = args
		LOG_ROOT = os.path.expanduser('~/Bluto/')
		COMPANY_LOC = LOG_ROOT+'{}'.format(str(self.args.domain).split('.', 1)[0])
		self.COMPANY_LOC = COMPANY_LOC
		
		if not os.path.exists(self.COMPANY_LOC):
			os.makedirs(self.COMPANY_LOC)
			os.chmod(self.COMPANY_LOC, 0o700)			
		
		self.data = data
		
		start_html = self.start()
		dashboard_html = self.dashboard()
		datatable_html = self.datatable()
		end_html = self.end()
		
		page = dashboard_html + datatable_html + end_html
		
		soup = BeautifulSoup(page, 'lxml')
		
		page = soup.prettify()
		page = start_html.decode('utf-8') + page
	
		
		
		with open(self.COMPANY_LOC + '/profiles.html', 'a') as myFile:

			myFile.write(page)		
			myFile.close()
			
	
	def blank_user(self):
		obj = 'data:image/png;base64,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'
		return obj	
	
	def start(self):
		start = """
		<!-- START -->
		<!DOCTYPE html>
		<html lang="en">
		<head>
		<!-- Required meta tags -->
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<title>Bluto Report</title>
		
		<!-- Cards style -->
		<link rel="stylesheet" href="css/cards-style.css" type="text/css">
		
		<!-- Common Styles-->
		<link href="css/all.css" rel="stylesheet">
		<link rel="stylesheet" href="css/bootstrap.min.css" type="text/css">
		<link href="lib/Ionicons/css/ionicons.css" rel="stylesheet">
		<link rel="stylesheet" href="css/bracket.css">
		<link rel="stylesheet" href="css/blutoface_style.css">
		<style>
		.table > tbody > tr > td {
			vertical-align: middle;
		}
		.dataTables_filter {
			float: left !important;
		}
		div.dt-buttons {
			position: relative;
			padding-top: 11px;
			padding-left: 5px;
		}
		</style>
		</head>
		
		<body>
		<!-- ########## START: LEFT PANEL ########## -->
		<div class="br-logo">
		<div class="glyph" style="font-size: 140px; margin-left: 20px; margin-top: 150px; margin-bottom: 10px;">
			<div> <span class="icon-blutoface"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span><span class="path7"></span><span class="path8"></span><span class="path9"></span><span class="path10"></span><span class="path11"></span><span class="path12"></span><span class="path13"></span><span class="path14"></span><span class="path15"></span><span class="path16"></span><span class="path17"></span><span class="path18"></span><span class="path19"></span><span class="path20"></span><span class="path21"></span><span class="path22"></span><span class="path23"></span><span class="path24"></span><span class="path25"></span><span class="path26"></span><span class="path27"></span><span class="path28"></span><span class="path29"></span><span class="path30"></span><span class="path31"></span><span class="path32"></span><span class="path33"></span><span class="path34"></span><span class="path35"></span><span class="path36"></span><span class="path37"></span><span class="path38"></span><span class="path39"></span><span class="path40"></span><span class="path41"></span><span class="path42"></span><span class="path43"></span><span class="path44"></span><span class="path45"></span><span class="path46"></span><span class="path47"></span><span class="path48"></span><span class="path49"></span><span class="path50"></span></span> </div>
		  </div>
		</div>
		<div class="br-sideleft overflow-y-auto">
		  <label class="sidebar-label pd-x-15 mg-t-20"><br>
			<br>
			<br>
			<br>
			<br>
			<br>
			</label>
		  <div class="br-sideleft-menu"> 
			  <a href="index.html" class="br-menu-link">
				<div class="br-menu-item"> <i class="menu-item-icon icon ion-ios-home tx-24"></i> <span class="menu-item-label">Dashboard</span> </div>
			  </a>
			  
			  <a href="dns_enumeration.html" class="br-menu-link">
				  <div class="br-menu-item"> <span  class="icon-crate-apple tx-20"></span> <span class="menu-item-label">DNS Enumeration</span> </div>
			  </a>
			  <a href="profiles.html" class="br-menu-link active">
				<div class="br-menu-item"> <i class="icon ion-person-stalker tx-24"></i> <span class="menu-item-label">Staff Enumeration</span> </div>
			  </a> 
			 
			  <a href="breach_data.html" class="br-menu-link">
				<div class="br-menu-item"> <span  class="icon-anon tx-24"></span> <span class="menu-item-label">Breach Data</span> </div>
			  </a>
			  
			  <br>
			  
		  </div>
		  <br>
		</div>
		<!-- ########## END: LEFT PANEL ########## --> 
		
		<!-- ########## START: HEAD PANEL ########## -->
		<div class="br-header">
		  <div class="br-header-left">
			<div class="navicon-left hidden-lg-up"> <a id="btnLeftMenuMobile" href=""> <i class="icon ion-navicon-round"></i> </a> </div>
		  </div>
		</div>
		<!-- ########## END: HEAD PANEL ########## -->
		<div class="br-mainpanel">
		  <div class="pd-30">
			<h4 class="tx-gray-800 mg-b-20">Profiles</h4>
			<p class="mg-b-0">Staff names, job roles and associations can be gathered from social media sites such as LinkedIn. This data can be used to build potential target lists for other vectors such as Social Engineering.</p>
			<p class="mg-b-0">&nbsp;</p>
			<p class="mg-b-0">The enumeration processes gathers all potential staff members, cross references any identified emails in an attempt to try understand the naming scheme being used by any given business and generates possible email addresses for each individual. These values are then queried against known breach databases to validate the address. </p>
			<p class="mg-b-0">&nbsp;</p>
			<p class="mg-b-0">All associated breaches are referenced in the "BreachData" section of this report.</p>
		  </div> 
		  <div class="br-pagebody mg-t-5 pd-x-30">
		"""
		return start.encode('utf-8')
	
	def dashboard(self):
		
		confirmed_true = 0
		confirmed_false = 0
		emails = 0
		breached = 0
		staff_identified = len(self.data['person'])
		
		for person in self.data['person']:
			if person['email'] != 'none':
				emails += 1
			if person['confirmed'].strip() == 'True':
				confirmed_true += 1
			else:
				confirmed_false += 1
				
			if not person['pwn_data'] == '[]':
				breached += 1
				
		
		dashboard = """
		<div class="row row-sm">
			  <div class="col-xl-3">
				<div class="bg-info rounded overflow-hidden">
				  <div class="pd-25 d-flex align-items-center"><i class="fas fa-users" style="font-size: 48px; color: white;"></i>
					<div class="mg-l-20">
					  <p class="tx-10 tx-spacing-1 tx-mont tx-medium tx-uppercase tx-white-8 mg-b-10">Staff Identified</p>
					  <p class="tx-24 tx-white tx-lato tx-bold mg-b-2 lh-1">{staff_identified}</p>
					  <span class="tx-11 tx-roboto tx-white-6"></span> <!-- LEFT BLANK --> 
					</div>
				  </div>
				</div>
			  </div>
			  <!-- col-3 -->
			  <div class="col-xl-3">
				<div class="bg-warning rounded overflow-hidden">
				  <div class="pd-25 d-flex align-items-center"><i class="far fa-frown" style="font-size: 48px; color: white;"></i>
					<div class="mg-l-20">
					  <p class="tx-10 tx-spacing-1 tx-mont tx-medium tx-uppercase tx-white-8 mg-b-10">Accounts Breached</p>
					  <p class="tx-24 tx-white tx-lato tx-bold mg-b-2 lh-1">{breached}</p>
					  <span class="tx-11 tx-roboto tx-white-6"></span> <!-- LEFT BLANK --> 
					</div>
				  </div>
				</div>
			  </div>
			  <!-- col-3 -->
			  <div class="col-xl-3">
				<div class="bg-danger rounded overflow-hidden">
				  <div class="pd-25 d-flex align-items-center"><i class="far fa-envelope" style="font-size: 48px; color: white;"></i>
					<div class="mg-l-20">
					  <p class="tx-10 tx-spacing-1 tx-mont tx-medium tx-uppercase tx-white-8 mg-b-10">Validated Emails</p>
					  <p class="tx-24 tx-white tx-lato tx-bold mg-b-2 lh-1">{confirmed_true}</p>
					  <span class="tx-11 tx-roboto tx-white-6"></span> <!-- LEFT BLANK --> 
					</div>
				  </div>
				</div>
			  </div>
			</div>
		""".format(staff_identified=staff_identified, breached=breached, confirmed_true=confirmed_true)
	
		return dashboard.encode('utf-8')
		
	def datatable(self):
		
		table_start = """
		<div class="card-container" style="margin-top: 15px;">
		  <table id="dataTable" class="table table-dark">
			<thead>
			  <tr>
				<th style="color: white;">Image</th>
				<th style="color: white;">Name</th>
				<th style="color: white;">Title</th>
				<th style="color: white;">Email</th>
				<th style="color: white;">Location</th>
				<th style="color: white;">Confirmed</th>
				<th style="color: white;">Breached</th>
			  </tr>
			</thead>
			<tbody>
		"""
		tabledata = ''
		
		for person in self.data['person']:
			
			img = person['image']
			if img.lower() == 'none':
				img = self.blank_user()
				
			email = person['email']
			name = person['name']
			role = person['role'].split('|')[0].strip()
			location = person['location']
			
			if person['confirmed'] == 'True':
				confirmed = '<button type="button" class="btn bg-success btn-rounded btn-sm m-0 text-light" style="font-size: 11px;">CONFIRMED'
			else:
				confirmed = '<button type="button" class="btn btn-secondary btn-rounded btn-sm m-0 text-light" style="font-size: 11px;">UNCONFIRMED</button>'
			
			if not person['pwn_data'] == '[]':
				breached = '<button type="button" class="btn bg-danger btn-rounded btn-sm m-0 text-light" style="font-size: 11px;">BREACHED</button>'
			else:
				breached = '<button type="button" class="btn btn-secondary btn-rounded btn-sm m-0 text-light" style="font-size: 11px;">NOT BREACHED</button>'
			
			html = """<tr>
				<td><img src="{img}" class="wd-60 rounded-circle" alt="">
				  <p style="display:none">{img}</p></td>
				<td>{name}</td>
				<td>{role}</td>
				<td>{email}</td>
				<td>{location}</td>
				<td>{confirmed}</td>
				<td>{breached}</td>
				</tr>
			""".format(img=img, name=name, role=role, email=email, location=location, confirmed=confirmed, breached=breached)
			
			tabledata = tabledata + html
			
		table_end = """  
				</tbody>
			  </table>
			</div>
			"""
		
		staff_table = table_start + tabledata + table_end
		
		return staff_table.encode('utf-8')
		
		
	def end(self):
		footer = """
				</div>
		  <footer class="br-footer">
			<div class="footer-left">
			  <div class="mg-b-2">Copyright &copy; 2019. Bluto. All Rights Reserved.</div>
			  <div>Attentively and carefully made by Darryl Lane.</div>
			</div>
		  </footer>
		</div>
		<!-- ########## END: MAIN PANEL ########## --> 

		<script src="js/font-awsome-kit-code.js"></script> 
		<script src="js/bracket.js"></script> 
		<script type="text/javascript" src="js/jquery-3.4.1.min.js"></script> 
		<script type="text/javascript" charset="utf8" src="DataTables/datatables.js"></script> 
		<script>
			$(document).ready(function() {
			var table = $('#dataTable').DataTable( {
				dom: 'Bfrtip',
				lengthChange: false,
				paging: false,
				
				buttons: [
				{
					extend: 'csv',
					title: 'Staff_Table',
					text: 'Export'
				}
					]

			} );
			table.buttons().container()
				.appendTo( '#example_wrapper .col-md-6:eq(0)' );
		} );

		</script>
		</body>
		</html>
		"""
		
		return footer.encode('utf-8')

class BreachData():
	def __init__(self, data):
		"filler"	
		