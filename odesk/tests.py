# -*- coding: utf-8 -*-
"""
Python bindings to odesk API
python-odesk version 0.4
(C) 2010 oDesk
"""
from odesk import Client, BaseClient, utils, get_version, signed_urlencode
from odesk.exceptions import *
from odesk.namespaces import *
from odesk.auth import Auth
from odesk.oauth import OAuth
from odesk.routers.team import Team

from mock import Mock, patch
import urllib2, urllib

try:
    import json
except ImportError:
    import simplejson as json


def test_signed_urlencode():
    secret_data = {
    'some$ecret': {'query': {},
                   'result':
                   'api_sig=5da1f8922171fbeffff953b773bcdc7f'},
    'some$ecret': {'query': {'spam': 42, 'foo': 'bar'},
                   'result':
                   'api_sig=11b1fc2e6555297bdc144aed0a5e641c&foo=bar&spam=42'},
    'som[&]234e$ecret': {'query': {'spam': 42, 'foo': 'bar'},
                   'result':
                   'api_sig=ac0e1b26f401dd4a5ccbaf7f4ea86b2f&foo=bar&spam=42'},
               }
    for key in list(secret_data.keys()):
        result = signed_urlencode(key, secret_data[key]['query'])
        assert secret_data[key]['result'] == result, \
            " %s returned and should be %s" % (result, \
                                                secret_data[key]['result'])


def test_http_request():
    request_methods = [('POST', 'POST'), ('GET', 'GET'),
                       ('PUT', 'POST'), ('DELETE', 'POST')]

    for method in request_methods:
        request = HttpRequest(url="http://url.com", data=None, method=method[0])
        assert request.get_method() == method[1], (request.get_method(), \
                                                   method[1])


def test_base_client():
    public_key = 'public'
    secret_key = 'secret'

    bc = BaseClient(public_key, secret_key)

    #test urlencode
    urlresult = bc.urlencode({'spam': 42, 'foo': 'bar'})
    encodedkey = 'api_sig=8a0da3cab1dbf7451f38fb5f5aec129c&api_key=public&foo=bar&spam=42'
    assert urlresult == encodedkey, urlresult

sample_json_dict = {'glossary':
                    {'GlossDiv':
                     {'GlossList':
                      {'GlossEntry':
                       {'GlossDef':
                        {'GlossSeeAlso': ['GML', 'XML'],
                         'para': 'A meta-markup language'},
                         'GlossSee': 'markup',
                         'Acronym': 'SGML',
                         'GlossTerm': 'Standard Generalized Markup Language',
                         'Abbrev': 'ISO 8879:1986',
                         'SortAs': 'SGML',
                         'ID': 'SGML'}},
                         'title': 'S'},
                         'title': 'example glossary'}}


def return_sample_json():
    return json.dumps(sample_json_dict).encode("utf-8")


def patched_urlopen(request, *args, **kwargs):
    request.read = return_sample_json
    return request


@patch('urllib2.urlopen', patched_urlopen)
def test_base_client_urlopen():
    public_key = 'public'
    secret_key = 'secret'

    bc = BaseClient(public_key, secret_key)

    #test urlopen
    data = [{'url': 'http://test.url',
             'data': {'foo': 'bar'},
             'method': 'GET',
             'result_data': None,
             'result_url': 'http://test.url?api_sig=ddbf4b10a47ca8300554441dc7c9042b&api_key=public&foo=bar',
             'result_method': 'GET'},
             {'url': 'http://test.url',
             'data': {},
             'method': 'POST',
             'result_data': b'api_sig=ba343f176db8166c4b7e88911e7e46ec&api_key=public',
             'result_url': 'http://test.url',
             'result_method': 'POST'},
             {'url': 'http://test.url',
             'data': {},
             'method': 'PUT',
             'result_data': b'api_sig=52cbaea073a5d47abdffc7fc8ccd839b&api_key=public&http_method=put',
             'result_url': 'http://test.url',
             'result_method': 'POST'},
             {'url': 'http://test.url',
             'data': {},
             'method': 'DELETE',
             'result_data': b'api_sig=8621f072b1492fbd164d808307ba72b9&api_key=public&http_method=delete',
             'result_url': 'http://test.url',
             'result_method': 'POST'},
             ]

    for params in data:
        result = bc.urlopen(url=params['url'],
                            data=params['data'],
                            method=params['method'])
        assert isinstance(result, HttpRequest), type(result)
        assert result.get_data() == params["result_data"], (result.get_data(),
                                                        params["result_data"])
        assert result.get_full_url() == params["result_url"], \
                                                         (result.get_full_url(),
                                                          params["result_url"])
        assert result.get_method() == params["result_method"], \
                                                         (result.get_method(),
                                                          params["result_method"])


def patched_urlopen_error(request, code=400, *args, **kwargs):
    raise urllib2.HTTPError(url=request.get_full_url(),
                            code=code, msg=str(code), hdrs='', fp=None)


def patched_urlopen_400(request, *args, **kwargs):
    return patched_urlopen_error(request, 400, *args, **kwargs)


def patched_urlopen_401(request, *args, **kwargs):
    return patched_urlopen_error(request, 401, *args, **kwargs)


def patched_urlopen_403(request, *args, **kwargs):
    return patched_urlopen_error(request, 403, *args, **kwargs)


def patched_urlopen_404(request, *args, **kwargs):
    return patched_urlopen_error(request, 404, *args, **kwargs)


def patched_urlopen_500(request, *args, **kwargs):
    return patched_urlopen_error(request, 500, *args, **kwargs)


@patch('urllib2.urlopen', patched_urlopen_400)
def base_client_read_400(bc, url):
    return bc.read(url)


@patch('urllib2.urlopen', patched_urlopen_401)
def base_client_read_401(bc, url):
    return bc.read(url)


@patch('urllib2.urlopen', patched_urlopen_403)
def base_client_read_403(bc, url):
    return bc.read(url)


@patch('urllib2.urlopen', patched_urlopen_404)
def base_client_read_404(bc, url):
    return bc.read(url)


@patch('urllib2.urlopen', patched_urlopen_500)
def base_client_read_500(bc, url):
    return bc.read(url)


@patch('urllib2.urlopen', patched_urlopen)
def test_base_client_read():
    """
    test cases:
      method default (get) - other we already tested
      format json|yaml ( should produce error)
      codes 200|400|401|403|404|500
    """
    public_key = 'public'
    secret_key = 'secret'

    bc = BaseClient(public_key, secret_key)
    test_url = 'http://test.url'

    #produce error on format other then json
    class NotJsonException(Exception):
        pass

    try:
        bc.read(url=test_url, format='yaml')
        raise NotJsonException()
    except NotJsonException as e:
        assert 0, "BaseClient.read() doesn't produce error on yaml format"
    except:
        pass

    #test get, all ok
    result = bc.read(url=test_url)
    assert result == sample_json_dict, result

    #test get, 400 error
    try:
        result = base_client_read_400(bc=bc, url=test_url)
    except HTTP400BadRequestError as e:
        pass
    except Exception as e:
        assert 0, "Incorrect exception raised for 400 code: " + str(e)

    #test get, 401 error
    try:
        result = base_client_read_401(bc=bc, url=test_url)
    except HTTP401UnauthorizedError as e:
        pass
    except Exception as e:
        assert 0, "Incorrect exception raised for 401 code: " + str(e)

    #test get, 403 error
    try:
        result = base_client_read_403(bc=bc, url=test_url)
    except HTTP403ForbiddenError as e:
        pass
    except Exception as e:
        assert 0, "Incorrect exception raised for 403 code: " + str(e)

    #test get, 404 error
    try:
        result = base_client_read_404(bc=bc, url=test_url)
    except HTTP404NotFoundError as e:
        pass
    except Exception as e:
        assert 0, "Incorrect exception raised for 404 code: " + str(e)

    #test get, 500 error
    try:
        result = base_client_read_500(bc=bc, url=test_url)
    except urllib2.HTTPError as e:
        if e.code == 500:
            pass
        else:
            assert 0, "Incorrect exception raised for 500 code: " + str(e)
    except Exception as e:
        assert 0, "Incorrect exception raised for 500 code: " + str(e)


def get_client():
    public_key = 'public'
    secret_key = 'secret'
    api_token = 'some_token'
    return Client(public_key, secret_key, api_token)


@patch('urllib2.urlopen', patched_urlopen)
def test_client():
    c = get_client()
    test_url = "http://test.url"

    result = c.get(test_url)
    assert result == sample_json_dict, result

    result = c.post(test_url)
    assert result == sample_json_dict, result

    result = c.put(test_url)
    assert result == sample_json_dict, result

    result = c.delete(test_url)
    assert result == sample_json_dict, result


@patch('urllib2.urlopen', patched_urlopen)
def test_namespace():
    ns = Namespace(get_client())
    test_url = "http://test.url"

    #test full_url
    full_url = ns.full_url('test')
    assert full_url == 'https://www.odesk.com/api/Nonev1/test', full_url

    result = ns.get(test_url)
    assert result == sample_json_dict, result

    result = ns.post(test_url)
    assert result == sample_json_dict, result

    result = ns.put(test_url)
    assert result == sample_json_dict, result

    result = ns.delete(test_url)
    assert result == sample_json_dict, result


def setup_auth():
    return Auth(get_client())


def test_auth():

    au = setup_auth()

    #test full_url
    full_url = au.full_url('test')
    assert full_url == 'https://www.odesk.com/api/auth/v1/test', full_url

    auth_url = au.auth_url('test')
    auth_url_result = 'https://www.odesk.com/services/api/auth/?frob=test&api_key=public&api_sig=42b7f18cbc5c16b1f037dbad241f2a6b&api_token=some_token'
    assert 'frob=test' in auth_url, auth_url
    assert 'api_key=public' in auth_url, auth_url
    assert 'api_sig=42b7f18cbc5c16b1f037dbad241f2a6b' in auth_url, auth_url


frob_dict = {'frob': 'test'}


def return_frob_json():
    return json.dumps(frob_dict).encode("utf-8")


def patched_urlopen_frob(request, *args, **kwargs):
    request.read = return_frob_json
    return request


@patch('urllib2.urlopen', patched_urlopen_frob)
def test_auth_get_frob():
    #test get_frob
    au = setup_auth()
    assert au.get_frob() == frob_dict['frob']


token_dict = {'token': 'testtoken', 'auth_user': 'test_auth_user'}


def return_token_json():
    return json.dumps(token_dict).encode("utf-8")


def patched_urlopen_token(request, *args, **kwargs):
    request.read = return_token_json
    return request


@patch('urllib2.urlopen', patched_urlopen_token)
def test_auth_get_token():
    #test get_frob
    au = setup_auth()
    token, auth_user = au.get_token('test_token')
    assert token == token_dict['token'], token
    assert auth_user == token_dict['auth_user'], auth_user


@patch('urllib2.urlopen', patched_urlopen_token)
def test_check_token_true():
    #check if ok
    au = setup_auth()
    try:
        au.check_token()
    except:
        pass
    else:
        assert "Not Raised"


@patch('urllib2.urlopen', patched_urlopen_token)
def test_revoke_token_true():
    #check if ok
    au = setup_auth()
    assert au.revoke_token(), au.revoke_token()


@patch('urllib2.urlopen', patched_urlopen_403)
def test_check_token_false():
    #check if denied
    au = setup_auth()
    try:
        au.check_token()
    except:
        pass
    else:
        assert "Not Raised"


teamrooms_dict = {'teamrooms':
                  {'teamroom':
                   {'team_ref': '1',
                    'name': 'oDesk',
                    'recno': '1',
                    'parent_team_ref': '1',
                    'company_name': 'oDesk',
                    'company_recno': '1',
                    'teamroom_api': '/api/team/v1/teamrooms/odesk:some.json',
                    'id': 'odesk:some'}},
                  'teamroom': {'snapshot': 'test snapshot'},
                  'snapshots': {'user': 'test', 'snapshot': 'test'},
                  'snapshot': {'status': 'private'}
                 }


def return_teamrooms_json():
    return json.dumps(teamrooms_dict).encode("utf-8")


def patched_urlopen_teamrooms(request, *args, **kwargs):
    request.read = return_teamrooms_json
    return request


@patch('urllib2.urlopen', patched_urlopen_teamrooms)
def test_team():
    te = Team(get_client())

    #test full_url
    full_url = te.full_url('test')
    assert full_url == 'https://www.odesk.com/api/team/v1/test', full_url

    #test get_teamrooms
    assert te.get_teamrooms() == [teamrooms_dict['teamrooms']['teamroom']], \
         te.get_teamrooms()

    #test get_snapshots
    assert te.get_snapshots(1) == [teamrooms_dict['teamroom']['snapshot']], \
         te.get_snapshots(1)

    #test get_snapshot
    assert te.get_snapshot(1, 1) == teamrooms_dict['snapshot'], te.get_snapshot(1, 1)

    #test update_snapshot
    assert te.update_snapshot(1, 1, memo='memo') == teamrooms_dict, te.update_snapshot(1, 1, memo='memo')

    #test update_snapshot
    assert te.delete_snapshot(1, 1) == teamrooms_dict, te.delete_snapshot(1, 1)

    #test get_workdiaries
    assert te.get_workdiaries(1, 1, 1) == (teamrooms_dict['snapshots']['user'], \
        [teamrooms_dict['snapshots']['snapshot']]), te.get_workdiaries(1, 1, 1)

userroles = {'userrole':
             [{'parent_team__reference': '1',
              'user__id': 'testuser', 'team__id': 'test:t',
              'reference': '1', 'team__name': 'te',
              'company__reference': '1',
              'user__reference': '1',
              'user__first_name': 'Test',
              'user__last_name': 'Development',
              'parent_team__id': 'testdev',
              'team__reference': '1', 'role': 'manager',
              'affiliation_status': 'none', 'engagement__reference': '',
              'parent_team__name': 'TestDev', 'has_team_room_access': '1',
              'company__name': 'Test Dev',
              'permissions':
                {'permission': ['manage_employment', 'manage_recruiting']}}]}

engagement = {'status': 'active',
              'buyer_team__reference': '1', 'provider__reference': '2',
              'job__title': 'development', 'roles': {'role': 'buyer'},
              'reference': '1', 'engagement_end_date': '',
              'fixed_price_upfront_payment': '0',
              'fixed_pay_amount_agreed': '1.00',
              'provider__id': 'test_provider',
              'buyer_team__id': 'testteam:aa',
              'engagement_job_type': 'fixed-price',
              'job__reference': '1', 'provider_team__reference': '',
              'engagement_title': 'Developer',
              'fixed_charge_amount_agreed': '0.01',
              'created_time': '0000', 'provider_team__id': '',
              'offer__reference': '',
              'engagement_start_date': '000', 'description': ''}

engagements = {'lister':
               {'total_items': '10', 'query': '',
                'paging': {'count': '10', 'offset': '0'}, 'sort': ''},
               'engagement': [engagement, engagement],
               }

offer = {'provider__reference': '1',
         'signed_by_buyer_user': '',
         'reference': '1', 'job__description': 'python',
         'buyer_company__name': 'Python community',
         'engagement_title': 'developer', 'created_time': '000',
         'buyer_company__reference': '2', 'buyer_team__id': 'testteam:aa',
         'interview_status': 'in_process', 'buyer_team__reference': '1',
         'signed_time_buyer': '', 'has_buyer_signed': '',
         'signed_time_provider': '', 'created_by': 'testuser',
         'job__reference': '2', 'engagement_start_date': '00000',
         'fixed_charge_amount_agreed': '0.01', 'provider_team__id': '',
         'status': '', 'signed_by_provider_user': '',
         'engagement_job_type': 'fixed-price', 'description': '',
         'provider_team__name': '', 'fixed_pay_amount_agreed': '0.01',
         'candidacy_status': 'active', 'has_provider_signed': '',
         'message_from_provider': '', 'my_role': 'buyer',
         'key': '~~0001', 'message_from_buyer': '',
         'buyer_team__name': 'Python community 2',
         'engagement_end_date': '', 'fixed_price_upfront_payment': '0',
         'created_type': 'buyer', 'provider_team__reference': '',
         'job__title': 'translation', 'expiration_date': '',
         'engagement__reference': ''}

offers = {'lister':
          {'total_items': '10', 'query': '', 'paging':
           {'count': '10', 'offset': '0'}, 'sort': ''},
           'offer': [offer, offer]}

job = {'subcategory': 'Development', 'reference': '1',
       'buyer_company__name': 'Python community',
       'job_type': 'fixed-price', 'created_time': '000',
       'created_by': 'test', 'duration': '',
       'last_candidacy_access_time': '',
       'category': 'Web',
       'buyer_team__reference': '169108', 'title': 'translation',
       'buyer_company__reference': '1', 'num_active_candidates': '0',
       'buyer_team__name': 'Python community 2', 'start_date': '000',
       'status': 'filled', 'num_new_candidates': '0',
       'description': 'test', 'end_date': '000',
       'public_url': 'http://www.odesk.com/jobs/~~0001',
       'visibility': 'invite-only', 'buyer_team__id': 'testteam:aa',
       'num_candidates': '1', 'budget': '1000', 'cancelled_date': '',
       'filled_date': '0000'}

jobs = [job, job]

task = {'reference': 'test', 'company_reference': '1',
          'team__reference': '1', 'user__reference': '1',
          'code': '1', 'description': 'test task',
          'url': 'http://url.odesk.com/task', 'level': '1'}

tasks = [task, task]

auth_user = {'first_name': 'TestF', 'last_name': 'TestL',
             'uid': 'testuser', 'timezone_offset': '0',
             'timezone': 'Europe/Athens', 'mail': 'test_user@odesk.com',
             'messenger_id': '', 'messenger_type': 'yahoo'}

user = {'status': 'active', 'first_name': 'TestF',
        'last_name': 'TestL', 'reference': '0001',
        'timezone_offset': '10800',
        'public_url': 'http://www.odesk.com/users/~~000',
        'is_provider': '1',
        'timezone': 'GMT+02:00 Athens, Helsinki, Istanbul',
        'id': 'testuser'}

team = {'status': 'active', 'parent_team__reference': '0',
         'name': 'Test',
         'reference': '1',
         'company__reference': '1',
         'id': 'test',
         'parent_team__id': 'test_parent',
         'company_name': 'Test', 'is_hidden': '',
         'parent_team__name': 'Test parent'}

company = {'status': 'active',
             'name': 'Test',
             'reference': '1',
             'company_id': '1',
             'owner_user_id': '1', }

candidacy_stats = {'job_application_quota': '20',
                   'job_application_quota_remaining': '20',
                   'number_of_applications': '2',
                   'number_of_interviews': '3',
                   'number_of_invites': '0',
                   'number_of_offers': '0'}

hr_dict = {'auth_user': auth_user,
           'server_time': '0000',
           'user': user,
           'team': team,
           'company': company,
            'teams': [team, team],
            'companies': [company, company],
            'users': [user, user],
            'tasks': task,
            'userroles': userroles,
            'engagements': engagements,
            'engagement': engagement,
            'offer': offer,
            'offers': offers,
            'job': job,
            'jobs': jobs,
            'candidacy_stats': candidacy_stats}


def return_hr_json():
    return json.dumps(hr_dict).encode("utf-8")


def patched_urlopen_hr(request, *args, **kwargs):
    request.read = return_hr_json
    return request


@patch('urllib2.urlopen', patched_urlopen_hr)
def test_get_hrv2_user():
    hr = get_client().hr

    #test get_user
    assert hr.get_user(1) == hr_dict['user'], hr.get_user(1)


@patch('urllib2.urlopen', patched_urlopen_hr)
def test_get_hrv2_companies():
    hr = get_client().hr
    #test get_companies
    assert hr.get_companies() == hr_dict['companies'], hr.get_companies()

    #test get_company
    assert hr.get_company(1) == hr_dict['company'], hr.get_company(1)


@patch('urllib2.urlopen', patched_urlopen_hr)
def test_get_hrv2_company_teams():
    hr = get_client().hr
    #test get_company_teams
    assert hr.get_company_teams(1) == hr_dict['teams'], hr.get_company_teams(1)


@patch('urllib2.urlopen', patched_urlopen_hr)
def test_get_hrv2_company_users():
    hr = get_client().hr
    #test get_company_users
    assert hr.get_company_users(1) == hr_dict['users'], hr.get_company_users(1)
    assert hr.get_company_users(1, False) == hr_dict['users'], \
         hr.get_company_users(1, False)

@patch('urllib2.urlopen', patched_urlopen_hr)
def test_get_hrv2_teams():
    hr = get_client().hr
    #test get_teams
    assert hr.get_teams() == hr_dict['teams'], hr.get_teams()

    #test get_team
    assert hr.get_team(1) == hr_dict['team'], hr.get_team(1)


@patch('urllib2.urlopen', patched_urlopen_hr)
def test_get_hrv2_team_users():
    hr = get_client().hr
    #test get_team_users
    assert hr.get_team_users(1) == hr_dict['users'], hr.get_team_users(1)
    assert hr.get_team_users(1, False) == hr_dict['users'], \
         hr.get_team_users(1, False)


@patch('urllib2.urlopen', patched_urlopen_hr)
def test_get_hrv2_jobs():
    hr = get_client().hr
    #test get_jobs
    assert hr.get_jobs() == hr_dict['jobs'], hr.get_jobs()
    assert hr.get_job(1) == hr_dict['job'], hr.get_job(1)
    assert hr.update_job(1, {'status': 'filled'}) == hr_dict, hr.update_job(1, {'status': 'filled'})
    assert hr.delete_job(1, 41) == hr_dict, hr.delete_job(1, 41)


@patch('urllib2.urlopen', patched_urlopen_hr)
def test_get_hrv2_offers():
    hr = get_client().hr
    #test get_offers
    assert hr.get_offers() == hr_dict['offers'], hr.get_offers()
    assert hr.get_offer(1) == hr_dict['offer'], hr.get_offer(1)


@patch('urllib2.urlopen', patched_urlopen_hr)
def test_get_hrv2_engagements():
    hr = get_client().hr
    #test get_engagements
    assert hr.get_engagements() == hr_dict['engagements'], hr.get_engagements()
    assert hr.get_engagement(1) == hr_dict['engagement'], hr.get_engagement(1)


adjustments = {'adjustment': {'reference': '100'}}


def return_hradjustment_json():
    return json.dumps(adjustments).encode("utf-8")


def patched_urlopen_hradjustment(request, *args, **kwargs):
    request.read = return_hradjustment_json
    return request


@patch('urllib2.urlopen', patched_urlopen_hradjustment)
def test_hrv2_post_adjustment():
    hr = get_client().hr

    result = hr.post_team_adjustment(1, 2, 100000, 'test', 'test note')
    assert result == adjustments['adjustment'], result


@patch('urllib2.urlopen', patched_urlopen_hr)
def test_get_hrv2_candidacy_stats():
    hr = get_client().hr
    #test get_candidacy_stats
    result = hr.get_candidacy_stats()
    assert result == hr_dict['candidacy_stats'], result


provider_dict = {'profile':
                 {'response_time': '31.0000000000000000',
                  'dev_agency_ref': '',
                  'dev_adj_score_recent': '0',
                  'dev_ui_profile_access': 'Public',
                  'dev_portrait': '',
                  'dev_ic': 'Freelance Provider',
                  'certification': '',
                  'dev_usr_score': '0',
                  'dev_country': 'Ukraine',
                  'dev_recent_rank_percentile': '0',
                  'dev_profile_title': 'Python developer',
                  'dev_groups': '',
                  'dev_scores':
                  {'dev_score':
                   [{'description': 'competency and skills for the job, understanding of specifications/instructions',
                     'avg_category_score_recent': '',
                     'avg_category_score': '',
                     'order': '1', 'label': 'Skills'},
                     {'description': 'quality of work deliverables',
                      'avg_category_score_recent': '',
                      'avg_category_score': '', 'order': '2', 'label': 'Quality'},
                      ]
                   }},
                   'providers': {'test': 'test'},
                   'jobs': {'test': 'test'},
                   'otherexp': 'experiences',
                   'skills': 'skills',
                   'tests': 'tests',
                   'certificates': 'certificates',
                   'employments': 'employments',
                   'educations': 'employments',
                   'projects': 'projects',
                   'quick_info': 'quick_info'}


def return_provider_json():
    return json.dumps(provider_dict).encode("utf-8")


def patched_urlopen_provider(request, *args, **kwargs):
    request.read = return_provider_json
    return request


@patch('urllib2.urlopen', patched_urlopen_provider)
def test_provider():
    pr = get_client().provider

    #test full_url
    full_url = pr.full_url('test')
    assert full_url == 'https://www.odesk.com/api/profiles/v1/test', full_url

    #test get_provider
    assert pr.get_provider(1) == provider_dict['profile'], pr.get_provider(1)

    #test get_provider_brief
    assert pr.get_provider_brief(1) == provider_dict['profile'], \
        pr.get_provider_brief(1)

    #test get_providers
    assert pr.get_providers(data={'a': 1}) == provider_dict['providers'], \
        pr.get_providers(data={'a': 1})

    #test get_jobs
    assert pr.get_jobs(data={'a': 1}) == provider_dict['jobs'], \
        pr.get_jobs(data={'a': 1})

    assert pr.get_skills(1) == provider_dict['skills'], \
        pr.get_skills(1)

    assert pr.get_quickinfo(1) == provider_dict['quick_info'], \
        pr.get_quickinfo(1)

    assert pr.update_quickinfo(1, {'quickinfo': 'quickinfo'}) == provider_dict, \
        pr.update_quickinfo(1, {'quickinfo': 'quickinfo'})

    result = pr.get_affiliates(1)
    assert result == provider_dict['profile']


trays_dict = {'trays': [{'unread': '0',
              'type': 'sent',
              'id': '1',
              'tray_api': '/api/mc/v1/trays/username/sent.json'},
              {'unread': '0',
               'type': 'inbox',
               'id': '2',
               'tray_api': '/api/mc/v1/trays/username/inbox.json'},
              {'unread': '0',
               'type': 'notifications',
               'id': '3',
               'tray_api': '/api/mc/v1/trays/username/notifications.json'}]}


def return_trays_json():
    return json.dumps(trays_dict).encode("utf-8")


def patched_urlopen_trays(request, *args, **kwargs):
    request.read = return_trays_json
    return request


@patch('urllib2.urlopen', patched_urlopen_trays)
def test_get_trays():
    mc = get_client().mc

    #test full_url
    full_url = mc.full_url('test')
    assert full_url == 'https://www.odesk.com/api/mc/v1/test', full_url

    #test get_trays
    assert mc.get_trays(1) == trays_dict['trays'], mc.get_trays(1)
    assert mc.get_trays(1, paging_offset=10, paging_count=10) ==\
         trays_dict['trays'], mc.get_trays(1, paging_offset=10, paging_count=10)


tray_content_dict = {"current_tray": {"threads": '1'}}


def return_tray_content_json():
    return json.dumps(tray_content_dict).encode("utf-8")


def patched_urlopen_tray_content(request, *args, **kwargs):
    request.read = return_tray_content_json
    return request


@patch('urllib2.urlopen', patched_urlopen_tray_content)
def test_get_tray_content():
    mc = get_client().mc

    #test get_tray_content
    assert mc.get_tray_content(1, 1) ==\
         tray_content_dict['current_tray']['threads'], mc.get_tray_content(1, 1)
    assert mc.get_tray_content(1, 1, paging_offset=10, paging_count=10) ==\
         tray_content_dict['current_tray']['threads'], \
         mc.get_tray_content(1, 1, paging_offset=10, paging_count=10)


thread_content_dict = {"thread": {"test": '1'}}


def return_thread_content_json():
    return json.dumps(thread_content_dict).encode("utf-8")


def patched_urlopen_thread_content(request, *args, **kwargs):
    request.read = return_thread_content_json
    return request


@patch('urllib2.urlopen', patched_urlopen_thread_content)
def test_get_thread_content():
    mc = get_client().mc

    #test get_provider
    assert mc.get_thread_content(1, 1) ==\
         thread_content_dict['thread'], mc.get_thread_content(1, 1)
    assert mc.get_thread_content(1, 1, paging_offset=10, paging_count=10) ==\
         thread_content_dict['thread'], \
         mc.get_thread_content(1, 1, paging_offset=10, paging_count=10)


read_thread_content_dict = {"thread": {"test": '1'}}


def return_read_thread_content_json():
    return json.dumps(read_thread_content_dict).encode("utf-8")


def patched_urlopen_read_thread_content(request, *args, **kwargs):
    request.read = return_read_thread_content_json
    return request


@patch('urllib2.urlopen', patched_urlopen_read_thread_content)
def test_put_threads_read_unread():
    mc = get_client().mc

    read = mc.put_threads_read('test', [1, 2, 3])
    assert read == read_thread_content_dict, read

    unread = mc.put_threads_read('test', [5, 6, 7])
    assert unread == read_thread_content_dict, unread

    read = mc.put_threads_unread('test', [1, 2, 3])
    assert read == read_thread_content_dict, read


@patch('urllib2.urlopen', patched_urlopen_read_thread_content)
def test_put_threads_starred_unstarred():
    mc = get_client().mc

    starred = mc.put_threads_starred('test', [1, 2, 3])
    assert starred == read_thread_content_dict, starred

    unstarred = mc.put_threads_unstarred('test', [5, 6, 7])
    assert unstarred == read_thread_content_dict, unstarred


@patch('urllib2.urlopen', patched_urlopen_read_thread_content)
def test_put_threads_deleted_undeleted():
    mc = get_client().mc

    deleted = mc.put_threads_deleted('test', [1, 2, 3])
    assert deleted == read_thread_content_dict, deleted

    undeleted = mc.put_threads_undeleted('test', [5, 6, 7])
    assert undeleted == read_thread_content_dict, undeleted


@patch('urllib2.urlopen', patched_urlopen_read_thread_content)
def test_post_message():
    mc = get_client().mc

    message = mc.post_message('username', 'recepient1,recepient2', 'subject',
                              'body')
    assert message == read_thread_content_dict, message

    message = mc.post_message('username', ('recepient1@sss',\
        'recepient`іваівsss'), 'subject',
                              'body')
    assert message == read_thread_content_dict, message

    message = mc.post_message('username',\
        'recepient1@sss,1%&&|-!@#recepient`іваівsss', 'subject',
                              'body')
    assert message == read_thread_content_dict, message

    reply = mc.post_message('username', 'recepient1,recepient2', 'subject',
                              'body', 123)
    assert reply == read_thread_content_dict, reply


timereport_dict = {'table':
     {'rows':
      [{'c':
        [{'v': '20100513'},
         {'v': 'company1:team1'},
         {'v': '1'},
         {'v': '1'},
         {'v': '0'},
         {'v': '1'},
         {'v': 'Bug 1: Test'}]}],
         'cols':
         [{'type': 'date', 'label': 'worked_on'},
          {'type': 'string', 'label': 'assignment_team_id'},
          {'type': 'number', 'label': 'hours'},
          {'type': 'number', 'label': 'earnings'},
          {'type': 'number', 'label': 'earnings_offline'},
          {'type': 'string', 'label': 'task'},
          {'type': 'string', 'label': 'memo'}]}}


def return_read_timereport_json(*args, **kwargs):
    return json.dumps(timereport_dict).encode("utf-8")


def patched_urlopen_timereport_content(request, *args, **kwargs):
    request.read = return_read_timereport_json
    return request


@patch('urllib2.urlopen', patched_urlopen_timereport_content)
def test_get_provider_timereport():
    tc = get_client().timereport

    read = tc.get_provider_report('test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == timereport_dict, read

    read = tc.get_provider_report('test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)),
                                                hours=True)
    assert read == timereport_dict, read


@patch('urllib2.urlopen', patched_urlopen_timereport_content)
def test_get_company_timereport():
    tc = get_client().timereport

    read = tc.get_company_report('test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == timereport_dict, read

    read = tc.get_company_report('test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)),
                                  hours=True)
    assert read == timereport_dict, read


@patch('urllib2.urlopen', patched_urlopen_timereport_content)
def test_get_agency_timereport():
    tc = get_client().timereport

    read = tc.get_agency_report('test', 'test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == timereport_dict, read

    read = tc.get_agency_report('test', 'test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)),
                                  hours=True)
    assert read == timereport_dict, read

fin_report_dict = {'table':
     {'rows':
      [{'c':
        [{'v': '20100513'},
         {'v': 'odesk:odeskps'},
         {'v': '1'},
         {'v': '1'},
         {'v': '0'},
         {'v': '1'},
         {'v': 'Bug 1: Test'}]}],
         'cols':
         [{'type': 'date', 'label': 'worked_on'},
          {'type': 'string', 'label': 'assignment_team_id'},
          {'type': 'number', 'label': 'hours'},
          {'type': 'number', 'label': 'earnings'},
          {'type': 'number', 'label': 'earnings_offline'},
          {'type': 'string', 'label': 'task'},
          {'type': 'string', 'label': 'memo'}]}}


def return_read_fin_report_json(*args, **kwargs):
    return json.dumps(fin_report_dict).encode("utf-8")


def patched_urlopen_fin_report_content(request, *args, **kwargs):
    request.read = return_read_fin_report_json
    return request


@patch('urllib2.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_billings():
    fr = get_client().finreport

    read = fr.get_provider_billings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib2.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_teams_billings():
    fr = get_client().finreport

    read = fr.get_provider_teams_billings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib2.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_companies_billings():
    fr = get_client().finreport

    read = fr.get_provider_companies_billings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib2.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_earnings():
    fr = get_client().finreport

    read = fr.get_provider_earnings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib2.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_teams_earnings():
    fr = get_client().finreport

    read = fr.get_provider_teams_earnings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib2.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_companies_earnings():
    fr = get_client().finreport

    read = fr.get_provider_companies_earnings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib2.urlopen', patched_urlopen_fin_report_content)
def test_get_buyer_teams_billings():
    fr = get_client().finreport

    read = fr.get_buyer_teams_billings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib2.urlopen', patched_urlopen_fin_report_content)
def test_get_buyer_companies_billings():
    fr = get_client().finreport

    read = fr.get_buyer_companies_billings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib2.urlopen', patched_urlopen_fin_report_content)
def test_get_buyer_teams_earnings():
    fr = get_client().finreport

    read = fr.get_buyer_teams_earnings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib2.urlopen', patched_urlopen_fin_report_content)
def test_get_buyer_companies_earnings():
    fr = get_client().finreport

    read = fr.get_buyer_companies_earnings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib2.urlopen', patched_urlopen_fin_report_content)
def test_get_financial_entities():
    fr = get_client().finreport

    read = fr.get_financial_entities('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib2.urlopen', patched_urlopen_fin_report_content)
def test_get_financial_entities_provider():
    fr = get_client().finreport

    read = fr.get_financial_entities_provider('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


def test_get_version():
    import odesk
    odesk.VERSION = (1, 2, 3, 'alpha', 2)

    assert get_version() == '1.2.3 alpha 2', get_version()

    odesk.VERSION = (1, 2, 3, 'alpha', 0)
    assert get_version() == '1.2.3 pre-alpha', get_version()


task_dict = {'tasks': 'task1'
     }


def return_task_dict_json(*args, **kwargs):
    return json.dumps(task_dict).encode("utf-8")


def patched_urlopen_task(request, *args, **kwargs):
    request.read = return_task_dict_json
    return request


@patch('urllib2.urlopen', patched_urlopen_task)
def test_get_company_tasks():
    task = get_client().task

    assert task.get_company_tasks(1) == task_dict['tasks'], \
     task.get_company_tasks(1)


@patch('urllib2.urlopen', patched_urlopen_task)
def test_get_team_tasks():
    task = get_client().task

    assert task.get_team_tasks(1, 1) == task_dict['tasks'], \
     task.get_team_tasks(1, 1)


@patch('urllib2.urlopen', patched_urlopen_task)
def test_get_user_tasks():
    task = get_client().task

    assert task.get_user_tasks(1, 1, 1) == task_dict['tasks'], \
     task.get_user_tasks(1, 1, 1)


@patch('urllib2.urlopen', patched_urlopen_task)
def test_company_tasks_full():
    task = get_client().task

    assert task.get_company_tasks_full(1) == task_dict['tasks'], \
     task.get_company_tasks_full(1)


@patch('urllib2.urlopen', patched_urlopen_task)
def test_get_team_tasks_full():
    task = get_client().task

    assert task.get_team_tasks_full(1, 1) == task_dict['tasks'], \
     task.get_team_tasks_full(1, 1)


@patch('urllib2.urlopen', patched_urlopen_task)
def test_get_user_tasks_full():
    task = get_client().task

    assert task.get_user_tasks_full(1, 1, 1) == task_dict['tasks'], \
     task.get_user_tasks_full(1, 1, 1)


@patch('urllib2.urlopen', patched_urlopen_task)
def test_get_company_specific_tasks():
    task = get_client().task

    assert task.get_company_specific_tasks(1, [1, 1]) == task_dict['tasks'], \
     task.get_company_specific_tasks(1, [1, 1])


@patch('urllib2.urlopen', patched_urlopen_task)
def test_get_team_specific_tasks():
    task = get_client().task

    assert task.get_team_specific_tasks(1, 1, [1, 1]) == task_dict['tasks'], \
     task.get_team_specific_tasks(1, 1, [1, 1])


@patch('urllib2.urlopen', patched_urlopen_task)
def test_get_user_specific_tasks():
    task = get_client().task

    assert task.get_user_specific_tasks(1, 1, 1, [1, 1]) == task_dict['tasks'], \
     task.get_user_specific_tasks(1, 1, 1, [1, 1])


@patch('urllib2.urlopen', patched_urlopen_task)
def test_post_company_task():
    task = get_client().task

    assert task.post_company_task(1, 1, '1', 'ttt') == task_dict, \
     task.post_company_task(1, 1, '1', 'ttt')


@patch('urllib2.urlopen', patched_urlopen_task)
def test_post_team_task():
    task = get_client().task

    assert task.post_team_task(1, 1, 1, '1', 'ttt') == task_dict, \
     task.post_team_task(1, 1, 1, '1', 'ttt')


@patch('urllib2.urlopen', patched_urlopen_task)
def test_post_user_task():
    task = get_client().task

    assert task.post_user_task(1, 1, 1, 1, '1', 'ttt') == task_dict, \
     task.post_user_task(1, 1, 1, 1, '1', 'ttt')


@patch('urllib2.urlopen', patched_urlopen_task)
def test_put_company_task():
    task = get_client().task

    assert task.put_company_task(1, 1, '1', 'ttt') == task_dict, \
     task.put_company_task(1, 1, '1', 'ttt')


@patch('urllib2.urlopen', patched_urlopen_task)
def test_put_team_task():
    task = get_client().task

    assert task.put_team_task(1, 1, 1, '1', 'ttt') == task_dict, \
     task.put_team_task(1, 1, 1, '1', 'ttt')


@patch('urllib2.urlopen', patched_urlopen_task)
def test_put_user_task():
    task = get_client().task

    assert task.put_user_task(1, 1, 1, 1, '1', 'ttt') == task_dict, \
     task.put_user_task(1, 1, 1, 1, '1', 'ttt')


@patch('urllib2.urlopen', patched_urlopen_task)
def test_delete_company_task():
    task = get_client().task

    assert task.delete_company_task(1, [1, 1]) == task_dict, \
     task.delete_company_task(1, [1, 1])


@patch('urllib2.urlopen', patched_urlopen_task)
def test_delete_team_task():
    task = get_client().task

    assert task.delete_team_task(1, 1, [1, 1]) == task_dict, \
     task.delete_team_task(1, 1, [1, 1])


@patch('urllib2.urlopen', patched_urlopen_task)
def test_delete_user_task():
    task = get_client().task

    assert task.delete_user_task(1, 1, 1, [1, 1]) == task_dict, \
     task.delete_user_task(1, 1, 1, [1, 1])


@patch('urllib2.urlopen', patched_urlopen_task)
def test_delete_all_company_tasks():
    task = get_client().task

    assert task.delete_all_company_tasks(1) == task_dict, \
     task.delete_all_company_tasks(1)


@patch('urllib2.urlopen', patched_urlopen_task)
def test_delete_all_team_tasks():
    task = get_client().task

    assert task.delete_all_team_tasks(1, 1) == task_dict, \
     task.delete_all_team_tasks(1, 1)


@patch('urllib2.urlopen', patched_urlopen_task)
def test_delete_all_user_tasks():
    task = get_client().task

    assert task.delete_all_user_tasks(1, 1, 1) == task_dict, \
     task.delete_all_user_tasks(1, 1, 1)


@patch('urllib2.urlopen', patched_urlopen_task)
def test_update_batch_tasks():
    task = get_client().task

    assert task.update_batch_tasks(1, "1;2;3") == task_dict, \
     task.update_batch_tasks(1, "1;2;3")


def test_gds_namespace():
    from odesk.namespaces import GdsNamespace
    gds = GdsNamespace(get_client())

    assert gds.urlopen('test.url', {}, 'POST') == None, \
        gds.urlopen('test.url', {}, 'POST')


oconomy_dict = {'table':
                {'rows':
                  [{'c': [{'v': 'Administrative Support'},
                        {'v': '2787297.31'}]},
                   {'c': [{'v': 'Business Services'},
                        {'v': '1146857.51'}]},
                   {'c': [{'v': 'Customer Service'},
                        {'v': '1072926.55'}]},
                   {'c': [{'v': 'Design & Multimedia'},
                        {'v': '1730094.73'}]},
                   {'c': [{'v': 'Networking & Information Systems'},
                        {'v': '690526.57'}]},
                   {'c': [{'v': 'Sales & Marketing'},
                        {'v': '3232511.54'}]},
                   {'c': [{'v': 'Software Development'},
                        {'v': '6826354.60'}]},
                   {'c': [{'v': 'Web Development'},
                        {'v': '15228679.46'}]},
                   {'c': [{'v': 'Writing & Translation'},
                        {'v': '2257654.76'}]}],
                 'cols':
                  [{'type': 'string', 'label': 'category'},
                   {'type': 'number', 'label': 'amount'}]}}


def return_read_oconomy_json(*args, **kwargs):
    return json.dumps(oconomy_dict).encode("utf-8")


def patched_urlopen_oconomy_content(request, *args, **kwargs):
    request.read = return_read_oconomy_json
    return request


@patch('urllib2.urlopen', patched_urlopen_oconomy_content)
def test_get_monthly_summary():
    oconomy = get_client().nonauth_oconomy

    read = oconomy.get_monthly_summary('201011')
    assert read == oconomy_dict, read


@patch('urllib2.urlopen', patched_urlopen_oconomy_content)
def test_get_hours_worked_by_locations():
    oconomy = get_client().oconomy

    read = oconomy.get_hours_worked_by_locations()
    assert read == oconomy_dict, read


@patch('urllib2.urlopen', patched_urlopen_oconomy_content)
def test_get_hours_worked_by_weeks():
    oconomy = get_client().oconomy

    read = oconomy.get_hours_worked_by_weeks()
    assert read == oconomy_dict, read


@patch('urllib2.urlopen', patched_urlopen_oconomy_content)
def test_get_top_countries_by_hours():
    oconomy = get_client().oconomy

    read = oconomy.get_top_countries_by_hours()
    assert read == oconomy_dict, read


@patch('urllib2.urlopen', patched_urlopen_oconomy_content)
def test_get_earnings_by_categories():
    oconomy = get_client().nonauth_oconomy

    read = oconomy.get_earnings_by_categories()
    assert read == oconomy_dict, read


@patch('urllib2.urlopen', patched_urlopen_oconomy_content)
def test_get_most_requested_skills():
    oconomy = get_client().oconomy

    read = oconomy.get_most_requested_skills()
    assert read == oconomy_dict, read


def get_oauth_client():
    key = '56adf4b66aaf61444a77796c17c0da53'
    secret = 'e5864a0bcbed2085'
    return Client(key, secret, auth='oauth')

def setup_oauth():
    return OAuth(get_oauth_client())

def test_oauth_full_url():
    oa = setup_oauth()
    request_token_url = oa.full_url('oauth/token/request')
    access_token_url = oa.full_url('oauth/token/access')
    assert request_token_url == oa.request_token_url, request_token_url
    assert access_token_url == oa.access_token_url, access_token_url

def patched_httplib2_request(*args, **kwargs):
    return {'status': '200'},\
        b'oauth_callback_confirmed=1&oauth_token=709d434e6b37a25c50e95b0e57d24c46&oauth_token_secret=193ef27f57ab4e37'

@patch('httplib2.Http.request', patched_httplib2_request)
def test_oauth_get_request_token():
    oa = setup_oauth()
    assert oa.get_request_token() == (b'709d434e6b37a25c50e95b0e57d24c46',\
                                    b'193ef27f57ab4e37')

@patch('httplib2.Http.request', patched_httplib2_request)
def test_oauth_get_authorize_url():
    oa = setup_oauth()
    assert oa.get_authorize_url() ==\
        'https://www.odesk.com/services/api/auth?oauth_token=709d434e6b37a25c50e95b0e57d24c46'
    assert oa.get_authorize_url('http://example.com/oauth/complete') ==\
        'https://www.odesk.com/services/api/auth?oauth_token=709d434e6b37a25c50e95b0e57d24c46&oauth_callback=http%3A%2F%2Fexample.com%2Foauth%2Fcomplete'

def patched_httplib2_access(*args, **kwargs):
    return {'status': '200'},\
        b'oauth_token=aedec833d41732a584d1a5b4959f9cd6&oauth_token_secret=9d9cccb363d2b13e'

@patch('httplib2.Http.request', patched_httplib2_access)
def test_oauth_get_access_token():
    oa = setup_oauth()
    oa.request_token = '709d434e6b37a25c50e95b0e57d24c46'
    oa.request_token_secret = '193ef27f57ab4e37'
    assert oa.get_access_token('9cbcbc19f8acc2d85a013e377ddd4118') ==\
     (b'aedec833d41732a584d1a5b4959f9cd6', b'9d9cccb363d2b13e')
