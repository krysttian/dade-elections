import requests
import csv
import sys
from contextlib import closing
from django.utils import timezone
import datetime
from decimal import Decimal
from  contributions.models import Candidate, Contributor, Contribution

def get_candidate_number(string):
    name_list = string.split('-')
    if len(name_list) == 2:
        return name_list[1]
    elif len(name_list) == 0:
        return 'NO_NUMBER_FOUND'
    else:
        for potential_number in name_list:
            try:
                int(potential_number)
                return potential_number
            except ValueError:
                pass
def create_or_update_candidate(text):
    '''
    Ingests text from csv stream and generates model instance and saves it
    Terribly inefficent with the number of database hits being n * 2 of lines of text
    '''
    # TODO replace with bulk_create 
    candidate_number = get_candidate_number(text)
    candidate, created = Candidate.objects.update_or_create(defaults={"name": text, "date_created": timezone.now()},
                                                            candidate_number=(candidate_number))
    if created:
        candidate.save()
    return candidate

def zip_number_parser(text):
    zip_code = text.split('-')[0]
    try:
        int(zip_code)
        return int(zip_code)
    except ValueError:
        print(zip_code)
        return 99999

def create_or_update_contributor(contribution_object):
    contibutor_object = {
        "first_name" : contribution_object['first_name'],
        "last_name" : contribution_object['last_name'],
        "middle_name": contribution_object['middle_name'],
        "occupation": contribution_object['occupation'],
        "type": contribution_object['type'],
        "address1": contribution_object['address1'],
        "address2": contribution_object['address2'],
        "city": contribution_object['city'],
        "state": contribution_object['state'],
        "zip" : contribution_object['zip'],
        "zip_number": zip_number_parser(contribution_object['zip']),
    }
    contributor, created = Contributor.objects.update_or_create(defaults={"date_created": timezone.now()}, **contibutor_object)
    if created:
        contributor.save()
    return contributor

def create_or_update_contribution(contribution_object, candidate, contributor):
    date_of_contribution = datetime.datetime.strptime(contribution_object['date'], '%m/%d/%Y').date()
    print(type(candidate))
    contribution = {
        "type": contribution_object['type'],
        "date": date_of_contribution,
        "candidate_name": contribution_object['candidate'],
        "office": contribution_object['office'],
        "amount": Decimal(contribution_object['amount']),
        "contribution_type": contribution_object['contribution_type'],
        "amend": contribution_object['amend'],
        "first_name" : contribution_object['first_name'],
        "last_name" : contribution_object['last_name'],
        "middle_name": contribution_object['middle_name'],
        "occupation": contribution_object['occupation'],
        "type": contribution_object['type'],
        "address1": contribution_object['address1'],
        "address2": contribution_object['address2'],
        "city": contribution_object['city'],
        "state": contribution_object['state'],
        "zip" : contribution_object['zip'],
        "zip_number": zip_number_parser(contribution_object['zip']),
    }
    contribution, created = Contribution.objects.update_or_create(defaults={"date_created": timezone.now()},candidate=candidate, contributor=contributor, **contribution)
    if created:
        contribution.save()
    return contribution


def map_list_to_object(line):
    '''
    takes 1 line from csv, uses predefined hardcoded tuple to iterate and generte object with same name.
    if there is an error I want to bubble up and prevent 
    '''
    row_tuple = ('type', 'date', 'candidate', 'office', 'last_name', 'first_name', 'middle_name', 'address1', 'address2', 'amount', 'city', 'state', 'zip', 'contributor_type', 'contribution_type','occupation', 'amend')
    mapped_object = {}
    for i, field in enumerate(row_tuple):
        mapped_object[field] = line[i].strip()
    print(mapped_object)
    return mapped_object

def import_voter_focus_election_donations():
    url = "https://www.voterfocus.com/CampaignFinance/cand_srch.php"
    request_options = {
        'srch_tp': 'C',
        'c_lastname':'',
            'cand_name':'',
    'cand_fname':'',
    'cand_id':'',
    'b_month': 8,
    'b_day': 1,
    'b_year': 2018,
    'e_month': 12,
    'e_day': 1,
    'e_year': 2018,
    's_min':'',
    's_max':'',
    'c_item_type':'',
    'e_item_type':'',
    'contributor_tp':'',
    'c_occ':'',
    'srch_order': 'D',
    's_min_summary':'',
    'csv': 'on',
    'isSearch': 1,
    'c': 'miamidade'
    }
    try:
        r = requests.get(url, params=request_options, stream=True)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    if r is not None:
        with closing(line.decode('utf-8') for line in r.iter_lines()) as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            next(reader)
            counter = 0
            all_candidates = []
            all_contributions = []
            for line in reader:
                counter += 1
                contribution_object = map_list_to_object(line)
                candidate = create_or_update_candidate(contribution_object['candidate'])
                contributor = create_or_update_contributor(contribution_object)
                contributon = create_or_update_contribution(contribution_object, candidate, contributor)
                print(counter)
            # next(reader)
            # for line in reader:
            #     print(line)
            #     # candidate = create_or_update_candidate(line[2])
            #     # contributor = create_or_update_contributor(line)
            print('all done')
    else:
        print('some kind of error as occured')

if __name__ == '__main__':
    import_voter_focus_election_donations()
