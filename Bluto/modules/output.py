#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from termcolor import colored
import traceback
import collections
import datetime
import webbrowser
import shutil
import os
from search import action_pwned
from bluto_logging import info, INFO_LOG_FILE, LOG_DIR


def action_output_vuln_zone(google_results, bing_results, linkedin_results, time_spent_email, time_spent_total, clean_dump, sub_intrest, domain, report_location, company, data_mine):
    info('Output action_output_vuln_zone: Start')
    linkedin_evidence_results = []
    email_evidence_results = []
    email_results = []
    email_seen = []
    url_seen = []
    person_seen = []
    final_emails = []

    for email, url in google_results:
        try:
            e1, e2 = email.split(',')
            if url not in email_seen:
                email_seen.append(url)
                email_evidence_results.append((str(e2).replace(' ',''),url))
                email_evidence_results.append((str(e1).replace(' ',''),url))
                email_results.append((str(e2).replace(' ','')))
                email_results.append((str(e1).replace(' ','')))

        except ValueError:
            if url not in email_seen:
                email_seen.append(url)
                email_evidence_results.append((str(email).replace(' ',''),url))
                email_results.append(str(email).replace(' ',''))

    for e, u in bing_results:
        email_results.append(e)
        if u not in url_seen:
            email_evidence_results.append((e, u))

    for url, person, description in linkedin_results:
        if person not in person_seen:
            person_seen.append(person)
            linkedin_evidence_results.append((url, person, description))

    linkedin_evidence_results.sort(key=lambda tup: tup[1])
    sorted_email = set(sorted(email_results))
    for email in sorted_email:
        if email == '[]':
            pass
        elif email == '@' + domain:
            pass
        else:
            final_emails.append(email)
    email_count = len(final_emails)
    staff_count = len(person_seen)
    f_emails = sorted(final_emails)
    pwned_results = action_pwned(f_emails)
    c_accounts = len(pwned_results)

    print '\n\nEmail Addresses:\n'
    write_html(email_evidence_results, linkedin_evidence_results, pwned_results, report_location, company, data_mine)
    if f_emails:
        for email in f_emails:

            print str(email).replace("u'","").replace("'","").replace('[','').replace(']','')
    else:
        print '\tNo Data To Be Found'

    print '\nCompromised Accounts:\n'
    if pwned_results:
        sorted_pwned = sorted(pwned_results)
        for account in sorted_pwned:
            print 'Account: \t{}'.format(account[0])
            print 'Domain: \t{}'.format(account[1])
            print 'Date: \t{}\n'.format(account[3])
    else:
        print '\tNo Data To Be Found'

    print '\nLinkedIn Results:\n'

    sorted_person = sorted(person_seen)
    if sorted_person:
        for person in sorted_person:
            print person
    else:
        print '\tNo Data To Be Found'

    if data_mine is not None:
        user_names = data_mine[0]
        software_list = data_mine[1]
        download_count = data_mine[2]
        download_list = data_mine[3]
        username_count = len(user_names)
        software_count = len(software_list)

        print '\nData Found In Document MetaData'
        print '\nPotential Usernames:\n'
        if user_names:
            for user in user_names:
                print '\t' + colored(user, 'red')
        else:
            print '\tNo Data To Be Found'

        print '\nSoftware And Versions Found:\n'
        if software_list:
            for software in software_list:
                print '\t' + colored(software, 'red')
        else:
            print '\tNo Data To Be Found'
    else:
        user_names = []
        software_list = []
        download_count = 0
        username_count = len(user_names)
        software_count = len(software_list)

    target_dict = dict((x.split(' ') for x in clean_dump))
    clean_target = collections.OrderedDict(sorted(target_dict.items()))
    print "\nProcessed Dump\n"

    bruted_count = len(clean_target)
    for item in clean_target:
        if item in sub_intrest:
            print colored(item, 'red'), colored("\t" + clean_target[item], 'red')
        else:
            print item, "\t" + target_dict[item]

    time_spent_email_f = str(datetime.timedelta(seconds=(time_spent_email))).split('.')[0]
    time_spent_total_f = str(datetime.timedelta(seconds=(time_spent_total))).split('.')[0]

    print '\nHosts Identified: {}' .format(str(bruted_count))
    print 'Potential Emails Found: {}' .format(str(email_count))
    print 'Potential Staff Members Found: {}' .format(str(staff_count))
    print 'Compromised Accounts: {}' .format(str(c_accounts))
    print 'Potential Usernames Found: {}'.format(username_count)
    print 'Potential Software Found: {}'.format(software_count)
    print 'Documents Downloaded: {}'.format(download_count)
    print "Email Enumeration:", time_spent_email_f
    print "Total Time:", time_spent_total_f

    info('Hosts Identified: {}' .format(str(bruted_count)))
    info("Total Time:" .format(str(time_spent_total_f)))
    info("Email Enumeration: {}" .format(str(time_spent_email_f)))
    info('Compromised Accounts: {}' .format(str(c_accounts)))
    info('Potential Usernames Found: {}'.format(username_count))
    info('Potential Software Found: {}'.format(software_count))
    info('Documents Downloaded: {}'.format(download_count))
    info('Potential Staff Members Found: {}' .format(str(staff_count)))
    info('Potential Emails Found: {}' .format(str(email_count)))
    info('DNS Vuln Run completed')
    info('Output action_output_vuln_zone: Complete')

    domain_r = domain.split('.')
    docs = os.path.expanduser('~/Bluto/doc/{}/'.format(domain_r[0]))
    answers = ['no','n','y','yes']
    while True:
        answer = raw_input("\nWould you like to keep all local data?\n(Local Logs, Downloded Documents, HTML Evidence Report)\n\nYes|No:").lower()
        if answer in answers:
            if answer == 'y' or answer == 'yes':
                domain
                print '\nThe documents are located here: {}'.format(docs)
                print 'The logs are located here: {}.'.format(LOG_DIR)
                print "\nAn evidence report has been written to {}\n".format(report_location)
                while True:
                    answer = raw_input("Would you like to open this report now? ").lower()
                    if answer in answers:
                        if answer == 'y' or answer == 'yes':
                            print '\nOpening {}' .format(report_location)
                            webbrowser.open('file://' + str(report_location))
                            break
                        else:
                            break
                    else:
                        print 'Your answer needs to be either yes|y|no|n rather than, {}' .format(answer)
                break
            else:
                shutil.rmtree(docs)
                shutil.rmtree(LOG_DIR)
                os.remove(report_location)
                break
        else:
            print '\tYour answer needs to be either yes|y|no|n rather than, {}' .format(answer)


def action_output_vuln_zone_hunter(google_results, bing_results, linkedin_results, time_spent_email, time_spent_total, clean_dump, sub_intrest, domain, emailHunter_results, args, report_location, company, data_mine):
    info('Output action_output_vuln_zone_hunter: Start')
    linkedin_evidence_results = []
    email_evidence_results = []
    email_results = []
    email_seen = []
    url_seen = []
    person_seen = []
    final_emails = []

    if emailHunter_results is not None:
        for email in emailHunter_results:
            email_results.append(email[0])
            email_evidence_results.append((email[0],email[1]))

    for email, url in google_results:
        try:
            e1, e2 = email.split(',')
            if url not in email_seen:
                email_seen.append(url)
                email_evidence_results.append((str(e2).replace(' ',''),url))
                email_evidence_results.append((str(e1).replace(' ',''),url))
                email_results.append((str(e2).replace(' ','')))
                email_results.append((str(e1).replace(' ','')))

        except ValueError:
            if url not in email_seen:
                email_seen.append(url)
                email_evidence_results.append((str(email).replace(' ',''),url))
                email_results.append(str(email).replace(' ',''))

    for e, u in bing_results:
        email_results.append(e)
        if u not in url_seen:
            email_evidence_results.append((e, u))

    for url, person, description in linkedin_results:
        if person not in person_seen:
            person_seen.append(person)
            linkedin_evidence_results.append((url, person, description))

    linkedin_evidence_results.sort(key=lambda tup: tup[1])
    sorted_email = set(sorted(email_results))
    for email in sorted_email:
        if email == '[]':
            pass
        elif email == '@' + domain:
            pass
        else:
            final_emails.append(email)
    email_count = len(final_emails)
    staff_count = len(person_seen)
    f_emails = sorted(final_emails)
    pwned_results = action_pwned(f_emails)
    c_accounts = len(pwned_results)

    print '\n\nEmail Addresses:\n'
    write_html(email_evidence_results, linkedin_evidence_results, pwned_results, report_location, company, data_mine)
    if f_emails:
        for email in f_emails:
            print str(email).replace("u'","").replace("'","").replace('[','').replace(']','')
    else:
        print '\tNo Data To Be Found'

    print '\nCompromised Accounts:\n'
    if pwned_results:
        sorted_pwned = sorted(pwned_results)
        for account in sorted_pwned:
            print 'Account: \t{}'.format(account[0])
            print 'Domain: \t{}'.format(account[1])
            print 'Date: \t{}\n'.format(account[3])
    else:
        print '\tNo Data To Be Found'

    print '\nLinkedIn Results:\n'

    sorted_person = sorted(person_seen)
    if sorted_person:
        for person in sorted_person:
            print person
    else:
        print '\tNo Data To Be Found'

    if data_mine is not None:
        user_names = data_mine[0]
        software_list = data_mine[1]
        download_count = data_mine[2]
        download_list = data_mine[3]
        username_count = len(user_names)
        software_count = len(software_list)

        print '\nData Found In Document MetaData'
        print '\nPotential Usernames:\n'
        if user_names:
            for user in user_names:
                print '\t' + colored(user, 'red')
        else:
            print '\tNo Data To Be Found'

        print '\nSoftware And Versions Found:\n'
        if software_list:
            for software in software_list:
                print '\t' + colored(software, 'red')
        else:
            print '\tNo Data To Be Found'
    else:
        user_names = []
        software_list = []
        download_count = 0
        username_count = len(user_names)
        software_count = len(software_list)

    target_dict = dict((x.split(' ') for x in clean_dump))
    clean_target = collections.OrderedDict(sorted(target_dict.items()))

    print "\nProcessed Dump\n"
    bruted_count = len(clean_target)
    for item in clean_target:
        if item in sub_intrest:
            print colored(item, 'red'), colored("\t" + clean_target[item], 'red')
        else:
            print item, "\t" + target_dict[item]

    time_spent_email_f = str(datetime.timedelta(seconds=(time_spent_email))).split('.')[0]
    time_spent_total_f = str(datetime.timedelta(seconds=(time_spent_total))).split('.')[0]

    print '\nHosts Identified: {}' .format(str(bruted_count))
    print 'Potential Emails Found: {}' .format(str(email_count))
    print 'Potential Staff Members Found: {}' .format(str(staff_count))
    print 'Compromised Accounts: {}' .format(str(c_accounts))
    print 'Potential Usernames Found: {}'.format(username_count)
    print 'Potential Software Found: {}'.format(software_count)
    print 'Documents Downloaded: {}'.format(download_count)
    print "Email Enumeration:", time_spent_email_f
    print "Total Time:", time_spent_total_f

    info('Hosts Identified: {}' .format(str(bruted_count)))
    info("Total Time:" .format(str(time_spent_total_f)))
    info("Email Enumeration: {}" .format(str(time_spent_email_f)))
    info('Compromised Accounts: {}' .format(str(c_accounts)))
    info('Potential Usernames Found: {}'.format(username_count))
    info('Potential Software Found: {}'.format(software_count))
    info('Documents Downloaded: {}'.format(download_count))
    info('Potential Staff Members Found: {}' .format(str(staff_count)))
    info('Potential Emails Found: {}' .format(str(email_count)))
    info('DNS Vuln Run completed')
    info('Output action_output_vuln_zone_hunter: Completed')

    domain_r = domain.split('.')
    docs = os.path.expanduser('~/Bluto/doc/{}/'.format(domain_r[0]))
    answers = ['no','n','y','yes']
    while True:
        answer = raw_input("\nWould you like to keep all local data?\n(Local Logs, Downloded Documents, HTML Evidence Report)\n\nYes|No:").lower()
        if answer in answers:
            if answer == 'y' or answer == 'yes':
                domain
                print '\nThe documents are located here: {}'.format(docs)
                print 'The logs are located here: {}.'.format(LOG_DIR)
                print "\nAn evidence report has been written to {}\n".format(report_location)
                while True:
                    answer = raw_input("Would you like to open this report now? ").lower()
                    if answer in answers:
                        if answer == 'y' or answer == 'yes':
                            print '\nOpening {}' .format(report_location)
                            webbrowser.open('file://' + str(report_location))
                            break
                        else:
                            break
                    else:
                        print 'Your answer needs to be either yes|y|no|n rather than, {}' .format(answer)
                break
            else:
                shutil.rmtree(docs)
                shutil.rmtree(LOG_DIR)
                os.remove(report_location)
                break
        else:
            print '\tYour answer needs to be either yes|y|no|n rather than, {}' .format(answer)


def action_output_wild_false(brute_results_dict, sub_intrest, google_results, bing_true_results, linkedin_results, check_count, domain, time_spent_email, time_spent_brute, time_spent_total, report_location, company, data_mine):
    info('Output action_output_wild_false: Start')
    linkedin_evidence_results = []
    email_evidence_results = []
    email_results = []
    email_seen = []
    url_seen = []
    person_seen = []
    final_emails = []

    for email, url in google_results:
        try:
            e1, e2 = email.split(',')
            if url not in email_seen:
                email_seen.append(url)
                email_evidence_results.append((str(e2).replace(' ',''),url))
                email_evidence_results.append((str(e1).replace(' ',''),url))
                email_results.append((str(e2).replace(' ','')))
                email_results.append((str(e1).replace(' ','')))

        except ValueError:
            if url not in email_seen:
                email_seen.append(url)
                email_evidence_results.append((str(email).replace(' ',''),url))
                email_results.append(str(email).replace(' ',''))

    for e, u in bing_true_results:
        email_results.append(e)
        if u not in url_seen:
            email_evidence_results.append((e, u))

    for url, person, description in linkedin_results:
        if person not in person_seen:
            person_seen.append(person)
            linkedin_evidence_results.append((url, person, description))

    linkedin_evidence_results.sort(key=lambda tup: tup[1])
    sorted_email = set(sorted(email_results))
    for email in sorted_email:
        if email == '[]':
            pass
        elif email == '@' + domain:
            pass
        else:
            final_emails.append(email)
    email_count = len(final_emails)
    staff_count = len(person_seen)
    f_emails = sorted(final_emails)
    pwned_results = action_pwned(f_emails)
    c_accounts = len(pwned_results)

    print '\n\nEmail Addresses:\n'
    write_html(email_evidence_results, linkedin_evidence_results, pwned_results, report_location, company, data_mine)
    if f_emails:

        for email in f_emails:

            print str(email).replace("u'","").replace("'","").replace('[','').replace(']','')
    else:
        print '\tNo Data To Be Found'

    print '\nCompromised Accounts:\n'
    if pwned_results:
        sorted_pwned = sorted(pwned_results)
        for account in sorted_pwned:
            print 'Account: \t{}'.format(account[0])
            print 'Domain: \t{}'.format(account[1])
            print 'Date: \t{}\n'.format(account[3])
    else:
        print '\tNo Data To Be Found'

    print '\nLinkedIn Results:\n'

    sorted_person = sorted(person_seen)
    if sorted_person:
        for person in sorted_person:
            print person
    else:
        print '\tNo Data To Be Found'

    if data_mine is not None:
        user_names = data_mine[0]
        software_list = data_mine[1]
        download_count = data_mine[2]
        download_list = data_mine[3]
        username_count = len(user_names)
        software_count = len(software_list)

        print '\nData Found In Document MetaData'
        print '\nPotential Usernames:\n'
        if user_names:
            for user in user_names:
                print '\t' + colored(user, 'red')
        else:
            print '\tNo Data To Be Found'

        print '\nSoftware And Versions Found:\n'
        if software_list:
            for software in software_list:
                print '\t' + colored(software, 'red')
        else:
            print '\tNo Data To Be Found'
    else:
        user_names = []
        software_list = []
        download_count = 0
        username_count = len(user_names)
        software_count = len(software_list)

    sorted_dict = collections.OrderedDict(sorted(brute_results_dict.items()))
    bruted_count = len(sorted_dict)
    print "\nBluto Results: \n"
    for item in sorted_dict:
        if item in sub_intrest:
            print colored(item + "\t", 'red'), colored(sorted_dict[item], 'red')
        else:
            print item + "\t",sorted_dict[item]


    time_spent_email_f = str(datetime.timedelta(seconds=(time_spent_email))).split('.')[0]
    time_spent_brute_f = str(datetime.timedelta(seconds=(time_spent_brute))).split('.')[0]
    time_spent_total_f = str(datetime.timedelta(seconds=(time_spent_total))).split('.')[0]

    print '\nHosts Identified: {}' .format(str(bruted_count))
    print 'Potential Emails Found: {}' .format(str(email_count))
    print 'Potential Staff Members Found: {}' .format(str(staff_count))
    print 'Compromised Accounts: {}' .format(str(c_accounts))
    print 'Potential Usernames Found: {}'.format(username_count)
    print 'Potential Software Found: {}'.format(software_count)
    print 'Documents Downloaded: {}'.format(download_count)
    print "Email Enumeration:", time_spent_email_f
    print "Requests executed:", str(check_count) + " in ", time_spent_brute_f
    print "Total Time:", time_spent_total_f

    info('Hosts Identified: {}' .format(str(bruted_count)))
    info("Email Enumeration: {}" .format(str(time_spent_email_f)))
    info('Compromised Accounts: {}' .format(str(c_accounts)))
    info('Potential Staff Members Found: {}' .format(str(staff_count)))
    info('Potential Emails Found: {}' .format(str(email_count)))
    info('Potential Usernames Found: {}'.format(username_count))
    info('Potential Software Found: {}'.format(software_count))
    info('Documents Downloaded: {}'.format(download_count))
    info("Total Time:" .format(str(time_spent_total_f)))
    info('DNS No Wild Cards + Email Hunter Run completed')
    info('Output action_output_wild_false: Completed')

    domain_r = domain.split('.')
    docs = os.path.expanduser('~/Bluto/doc/{}/'.format(domain_r[0]))
    answers = ['no','n','y','yes']
    while True:
        answer = raw_input("\nWould you like to keep all local data?\n(Local Logs, Downloded Documents, HTML Evidence Report)\n\nYes|No:").lower()
        if answer in answers:
            if answer == 'y' or answer == 'yes':
                domain
                print '\nThe documents are located here: {}'.format(docs)
                print 'The logs are located here: {}.'.format(LOG_DIR)
                print "\nAn evidence report has been written to {}\n".format(report_location)
                while True:
                    answer = raw_input("Would you like to open this report now? ").lower()
                    if answer in answers:
                        if answer == 'y' or answer == 'yes':
                            print '\nOpening {}' .format(report_location)
                            webbrowser.open('file://' + str(report_location))
                            break
                        else:
                            break
                    else:
                        print 'Your answer needs to be either yes|y|no|n rather than, {}' .format(answer)
                break
            else:
                shutil.rmtree(docs)
                shutil.rmtree(LOG_DIR)
                os.remove(report_location)
                break
        else:
            print '\tYour answer needs to be either yes|y|no|n rather than, {}' .format(answer)


def action_output_wild_false_hunter(brute_results_dict, sub_intrest, google_results, bing_true_results, linkedin_results, check_count, domain, time_spent_email, time_spent_brute, time_spent_total, emailHunter_results, args, report_location, company, data_mine):
    info('Output action_output_wild_false_hunter: Start')
    linkedin_evidence_results = []
    email_evidence_results = []
    email_results = []
    email_seen = []
    url_seen = []
    person_seen = []
    final_emails = []

    if emailHunter_results is not None:
        for email in emailHunter_results:
            email_results.append(email[0])
            email_evidence_results.append((email[0],email[1]))

    for email, url in google_results:
        try:
            e1, e2 = email.split(',')
            if url not in email_seen:
                email_seen.append(url)
                email_evidence_results.append((str(e2).replace(' ',''),url))
                email_evidence_results.append((str(e1).replace(' ',''),url))
                email_results.append((str(e2).replace(' ','')))
                email_results.append((str(e1).replace(' ','')))

        except ValueError:
            if url not in email_seen:
                email_seen.append(url)
                email_evidence_results.append((str(email).replace(' ',''),url))
                email_results.append(str(email).replace(' ',''))

    for e, u in bing_true_results:
        email_results.append(e)
        if u not in url_seen:
            email_evidence_results.append((e, u))

    for url, person, description in linkedin_results:
        if person not in person_seen:
            person_seen.append(person)
            linkedin_evidence_results.append((url, person, description))

    linkedin_evidence_results.sort(key=lambda tup: tup[1])
    sorted_email = set(sorted(email_results))
    for email in sorted_email:
        if email == '[]':
            pass
        elif email == '@' + domain:
            pass
        else:
            final_emails.append(email)
    email_count = len(final_emails)
    staff_count = len(person_seen)
    f_emails = sorted(final_emails)
    pwned_results = action_pwned(f_emails)
    c_accounts = len(pwned_results)

    print '\n\nEmail Addresses:\n'
    write_html(email_evidence_results, linkedin_evidence_results, pwned_results, report_location, company, data_mine)
    if f_emails:

        for email in f_emails:

            print '\t' + str(email).replace("u'","").replace("'","").replace('[','').replace(']','')
    else:
        print '\tNo Data To Be Found'

    print '\nCompromised Accounts:\n'
    if pwned_results:
        sorted_pwned = sorted(pwned_results)
        for account in sorted_pwned:
            print 'Account: \t{}'.format(account[0])
            print ' Domain: \t{}'.format(account[1])
            print '   Date: \t{}\n'.format(account[3])
    else:
        print '\tNo Data To Be Found'

    print '\nLinkedIn Results:\n'

    sorted_person = sorted(person_seen)
    if sorted_person:
        for person in sorted_person:
            print person
    else:
        print '\tNo Data To Be Found'

    if data_mine is not None:
        user_names = data_mine[0]
        software_list = data_mine[1]
        download_count = data_mine[2]
        download_list = data_mine[3]
        username_count = len(user_names)
        software_count = len(software_list)

        print '\nData Found In Document MetaData'
        print '\nPotential Usernames:\n'
        if user_names:
            for user in user_names:
                print '\t' + colored(user, 'red')
        else:
            print '\tNo Data To Be Found'

        print '\nSoftware And Versions Found:\n'
        if software_list:
            for software in software_list:
                print '\t' + colored(software, 'red')
        else:
            print '\tNo Data To Be Found'
    else:
        user_names = []
        software_list = []
        download_count = 0
        username_count = len(user_names)
        software_count = len(software_list)

    sorted_dict = collections.OrderedDict(sorted(brute_results_dict.items()))
    bruted_count = len(sorted_dict)
    print "\nBluto Results: \n"
    for item in sorted_dict:
        if item is not '*.' + domain:
            if item is not '@.' + domain:
                if item in sub_intrest:
                    print colored(item + "\t", 'red'), colored(sorted_dict[item], 'red')
                else:
                    print item + "\t",sorted_dict[item]

    time_spent_email_f = str(datetime.timedelta(seconds=(time_spent_email))).split('.')[0]
    time_spent_brute_f = str(datetime.timedelta(seconds=(time_spent_brute))).split('.')[0]
    time_spent_total_f = str(datetime.timedelta(seconds=(time_spent_total))).split('.')[0]

    print '\nHosts Identified: {}' .format(str(bruted_count))
    print 'Potential Emails Found: {}' .format(str(email_count))
    print 'Potential Staff Members Found: {}' .format(str(staff_count))
    print 'Compromised Accounts: {}' .format(str(c_accounts))
    print 'Potential Usernames Found: {}'.format(username_count)
    print 'Potential Software Found: {}'.format(software_count)
    print 'Documents Downloaded: {}'.format(download_count)
    print "Email Enumeration:", time_spent_email_f
    print "Requests executed:", str(check_count) + " in ", time_spent_brute_f
    print "Total Time:", time_spent_total_f

    info('Hosts Identified: {}' .format(str(bruted_count)))
    info("Email Enumeration: {}" .format(str(time_spent_email_f)))
    info('Compromised Accounts: {}' .format(str(c_accounts)))
    info('Potential Staff Members Found: {}' .format(str(staff_count)))
    info('Potential Emails Found: {}' .format(str(email_count)))
    info("Total Time:" .format(str(time_spent_total_f)))
    info('Documents Downloaded: {}'.format(download_count))
    info('DNS No Wild Cards + Email Hunter Run completed')
    info('Output action_output_wild_false_hunter: Completed')

    domain_r = domain.split('.')
    docs = os.path.expanduser('~/Bluto/doc/{}/'.format(domain_r[0]))
    answers = ['no','n','y','yes']
    while True:
        print colored("\nWould you like to keep all local data?\n(Local Logs, Downloded Documents, HTML Evidence Report)\n\nYes|No:", "red")
        answer = raw_input("").lower()
        if answer in answers:
            if answer == 'y' or answer == 'yes':
                domain
                print '\nThe documents are located here: {}'.format(docs)
                print 'The logs are located here: {}.'.format(LOG_DIR)
                print "\nAn evidence report has been written to {}\n".format(report_location)
                while True:
                    answer = raw_input("Would you like to open this report now? ").lower()
                    if answer in answers:
                        if answer == 'y' or answer == 'yes':
                            print '\nOpening {}' .format(report_location)
                            webbrowser.open('file://' + str(report_location))
                            break
                        else:
                            break
                    else:
                        print 'Your answer needs to be either yes|y|no|n rather than, {}' .format(answer)
                break
            else:
                shutil.rmtree(docs)
                shutil.rmtree(LOG_DIR)
                os.remove(report_location)
                break
        else:
            print '\tYour answer needs to be either yes|y|no|n rather than, {}' .format(answer)


def write_html(email_evidence_results, linkedin_evidence_results, pwned_results, report_location, company, data_mine):
    info('Started HTML Report')
    if data_mine is not None:
        user_names = data_mine[0]
        software_list = data_mine[1]
        download_count = data_mine[2]
        download_list = data_mine[3]
        username_count = len(user_names)
        software_count = len(software_list)
    header = '''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table {{
        style="width:75%"
        border-collapse: separate;
        border-spacing: 5px;
        *border-collapse: expression('separate', cellSpacing = '10px');
    }}
    th {{
        text-align: left;
    }}
    header {{
        background-color:black;
        color:white;
        text-align:center;
        padding:5px;
    }}
    section {{
        width:75%;
        float:left;
        padding:10px;
    }}
    footer {{
        background-color:black;
        color:white;
        clear:both;
        text-align:center;
        padding:5px;
    }}
    div {{
        width: 100%;
    }}
    </style>
    </head>
    <body>

    <header>
    <h1>Bluto Evidence Report</h1>
    <h2>{a}</h2>
    </header>
    '''.format(a=company)
    footer = '''

        <footer>
            <p>Bluto</p>
            <p>Author: Darryl Lane</p>
            <p>Twitter: @darryllane101</p>
        </footer>
    </body>
    </html>
    '''

    emailDescription ='''

        <H2>Email Evidence:</H2>
        <th>
            <div>
                <p>
                 Email evidence includes the email address and the location it was found, this allows for potential remediation.
                 If corporate emails are to be utilised in the public domain, it is recommended that they are generic in nature and are not able to
                 authenticate to any public corporate services such as VPN, or similare remote control services.

                 This data can also be used in further attack vectors such as potential targets for Social Engineering and Phishing attacks.
                </p>
            </div>
        </th>
    '''
    metaDescription ='''

            <H2>MetaData Evidence:</H2>
            <th>
                <div>
                    <p>
                     Various techniques were used to gather potentially useful information on the scoped domain. The consultant
                     identified multiple documents available for download from the scoped domains website/s. These documents could hold potentially
                     sensitive data such as usernames, email addresses, folder structures, printers, operating system version information and
                     software version information. This information can prove to be very useful to an attacker when targeting various vectors
                     such as Social Engineering, password attacks and to expose further attack vectors.

                     It is recommended that all document metadata is sanitised before being published into the public domain.
                    </p>
                </div>
            </th>
        '''

    linkedinDescription ='''

            <H2>LinkedIn Evidence:</H2>
            <th>
                <div>
                    <p>
                     Staff names, job roles and associations can be gathered from social media sites such as LinkedIn. This information can be used
                     to attempt futher information gathering via vectors such as Social Engineering techniques, phone attacks, and phishing attacks. This data can also be used to try determine more
                     information such as potential email addresses.
                    </p>
                </div>
            </th>
        '''

    compromisedDescription ='''

                <H2>Compromised Account Evidence:</H2>
                <th>
                    <div>
                        <p>
                         This data was made publicly available due to a breach, this means that these account passwords and any portals that are utilised by these accounts
                         could be compromised. It is recommedned that all account passwords are modified and made to adhere to company policy.
                        </p>
                    </div>
                </th>
            '''

    try:
        with open(report_location, 'w') as myFile:
            myFile.write(header)
            myFile.write('<section>')
            if email_evidence_results:
                myFile.write(emailDescription)
                myFile.write('<table>')
                myFile.write('<tr>')
                myFile.write('<th>Email Address</th>')
                myFile.write('<th>URL Address</th>')
                myFile.write('</tr>')
                for email, url in email_evidence_results:
                    myFile.write('<tr>')
                    myFile.write('<td>{}</td>'.format(email))
                    myFile.write('<td>{}</td>'.format(url))
                    myFile.write('</tr>')
                myFile.write('</table>')
            if linkedin_evidence_results:
                myFile.write(linkedinDescription)
            if linkedin_evidence_results:
                for url, person, clean in linkedin_evidence_results:
                    myFile.write('<table style="width:60%">')
                    myFile.write('<p><tr><td><b>Person:</b> {}</td>'.format(person))
                    myFile.write('</tr>')
                    myFile.write('<tr><td><b>Role</b>: {}</td>'.format(clean))
                    myFile.write('</tr>')
                    myFile.write('<tr><td><b>Url</b>: {}</td>'.format(url))
                    myFile.write('</tr></p>')
                    myFile.write('</table>')
            if pwned_results:
                myFile.write(compromisedDescription)
                myFile.write('<table>')
            if pwned_results:
                for result in pwned_results:
                    myFile.write('<p><tr><td>Email: {}</td>'.format(result[0]))
                    myFile.write('</tr>')
                    myFile.write('<tr><td>Domain: {}</td>'.format(result[1]))
                    myFile.write('</tr>')
                    myFile.write('<tr><td>Data: {}</td>'.format(result[2]))
                    myFile.write('</tr>')
                    myFile.write('<tr><td>Compromise Date: {}</td>'.format(result[3]))
                    myFile.write('</tr>')
                    myFile.write('<tr><td>Date Added: {}</td>'.format(result[4]))
                    myFile.write('</tr>')
                    myFile.write('<tr><td>Description: <p>{}</p></td>'.format(result[5]))
                    myFile.write('</tr></p>')
                myFile.write('</table>')
            if data_mine:
                myFile.write(metaDescription)
                myFile.write('<table>')
                if data_mine:
                    myFile.write('<tr>')
                    if software_count:
                        myFile.write('<th>Software Count</th>')
                    if username_count:
                        myFile.write('<th>Username Count</th>')
                    if download_count:
                        myFile.write('<th>Download Count</th>')
                    myFile.write('</tr>')
                    myFile.write('<tr>')
                    if software_count:
                        myFile.write('<td>{}</td>'.format(software_count))
                    if username_count:
                        myFile.write('<td>{}</td>'.format(username_count))
                    if download_count:
                        myFile.write('<td>{}</td>'.format(download_count))
                    myFile.write('</tr>')
                myFile.write('</table>')
                myFile.write('<table>')
                myFile.write('<br>')
            if user_names:
                myFile.write('<tr>')
                myFile.write('<th>Usernames</th>')
                myFile.write('</tr>')
                for username in user_names:
                    myFile.write('<tr>')
                    myFile.write('<td>{}</td>'.format(username))
                    myFile.write('<tr>')
                myFile.write('</table>')
                myFile.write('<table style="width:75">')
                myFile.write('<br>')
            if software_list:
                myFile.write('<tr>')
                myFile.write('<th>Software</th>')
                myFile.write('</tr>')
                for software in software_list:
                    myFile.write('<tr>')
                    myFile.write('<td>{}</td>'.format(software))
                    myFile.write('<tr>')
                myFile.write('</table>')
                myFile.write('<table style="width:100%">')
            if download_list:
                myFile.write('<tr>')
                myFile.write('<th>Document</th>')
                myFile.write('</tr>')
                for doc in download_list:
                    myFile.write('<tr>')
                    myFile.write('<td>{}</td>'.format(doc))
                    myFile.write('<tr>')
                myFile.write('</table>')
            myFile.write('</section>')
            myFile.write(footer)
            myFile.write('</body>')
            myFile.write('</html>')
            myFile.close()
            info('Completed HTML Report')
    except IOError,e:
        info('IOError', exc_info=True)
    except Exception:
        info('An Unhandled Exception Occured', exc_info=True)
