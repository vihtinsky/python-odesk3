.. _how_to:


***************
How to
***************

..
.. _authenticate:

Authenticate
-----------------

http://developers.odesk.com/Authentication

To authenticate your web application with the python-odesk3, use next code::

    client = odesk.Client('your public key', 'your secret key')
    #redirect your user to the client.auth.auth_url()

    #catch frob from the oDesk response to callback
    frob = raw_input('Enter frob: ')

    #you can authenticate now
    auth_token, user = client.auth.get_token(frob)

    #Initiating a new client, now with a token.
    #Not strictly necessary here (could just set `client.auth_token`), but
    #typical for web apps, which wouldn't probably keep client instances
    #between requests
    client = odesk.Client('your public key', 'your secret key', auth_token)

..
.. _provider_information:

Get provider's information
--------------------------

http://developers.odesk.com/Provider-Profile

To get information about provider, use::

    client.provider.get_provider(provider_ciphertext)
    client.provider.get_provider_brief(provider_ciphertext)

To search provider(http://developers.odesk.com/search-providers) by the query string, use::

    client.provider.get_providers(data={})

To search jobs(http://developers.odesk.com/search-jobs) by the query string, use::

    client.provider.get_jobs(data={})

..
.. _team_information:

Get teams` information
----------------------

http://developers.odesk.com/Team-API

After authentication, you can get teams' information from client instance you have::

    client.team.get_teamrooms()

To get snapshots::

    client.team.get_snapshots(team_id, online='now')

To get user's workdiaries inside the team::

    client.team.get_workdiaries(team_id, username, date=None)


..
.. _get_messages:

Get trays and messages
-----------------------

http://developers.odesk.com/Message-Center-API

Get user's trays (if user not provided, authenticated user will be taken)::

    client.mc.get_trays(username=None, paging_offset=0, paging_count=20)

Get content of the tray::

    client.mc.get_tray_content(username, tray, paging_offset=0, paging_count=20)

Get content of the thread::

    client.mc.get_thread_content(username, thread_id, paging_offset=0, paging_count=20)



..
.. _send_message:

Send message
----------------------

http://developers.odesk.com/Message-Center-API

To send message::

    client.mc.post_message(username, recipients, subject, body, thread_id=None)

Where:

* username = user who is sending message
* recipients = should be python list or tuple of the usernames of recipients
* subject = subject of the message
* body = body of the message
* thread_id = should be id of the thread if you want your message be a reply inside existing thread

..
.. _get_timereports:

Get timereports
----------------------

http://developers.odesk.com/Time-Reports-API

To get timereports, use, based on the level of the timereports you need::

    client.timereport.get_provider_report(provider_id, query, hours=False):
    client.timereport.get_company_report(company_id, query, hours=False):
    client.timereport.get_agency_report(company_id, agency_id, query, hours=False):

Where:
 * query - is the odesk.Query object
 * hours = Limits the query to hour specific elements and hides all financial details.

For example::

    client.timereport.get_provider_report('user1',
           odesk.utils.Query(select=odesk.utils.Query.DEFAULT_TIMEREPORT_FIELDS,
                        where=(odesk.utils.Q('worked_on') <= date.today()) &\
                                (odesk.utils.Q('worked_on') > '2010-05-01')))


    client.timereport.get_provider_report('user1',
           odesk.utils.Query(select=odesk.utils.Query.DEFAULT_TIMEREPORT_FIELDS,
                        where=(odesk.utils.Q('worked_on') <= date.today()) &\
                                (odesk.utils.Q('worked_on') > '2010-05-01')), hours=True)

    client.timereport.get_agency_report('company1', 'agency1',
           odesk.utils.Query(select=odesk.utils.Query.DEFAULT_TIMEREPORT_FIELDS,
                        where=(odesk.utils.Q('worked_on') <= date.today()) &\
                                (odesk.utils.Q('worked_on') > '2010-05-01')), hours=True)


..
.. _get_finreports:

Get finreports
----------------------

*TODO*

..
.. _work_with_tasks:

Work with tasks
----------------------

http://developers.odesk.com/oTasks-API

To work with tasks you should use client.otask wrapper::

    tasks = client.otask.get_company_tasks('company_id')

Methods to get tasks::

    client.task.get_team_tasks(company_id, team_id)
    client.task.get_user_tasks(company_id, team_id, user_id)
    client.task.get_company_tasks_full(company_id)
    client.task.get_team_tasks_full(company_id, team_id)
    client.task.get_user_tasks_full(company_id, team_id, user_id)
    client.task.get_company_specific_tasks(company_id, task_codes)
    client.task.get_team_specific_tasks(company_id, team_id, task_codes)
    client.task.get_user_specific_tasks(company_id, team_id, user_id, task_codes)

Create and update tasks::

    client.task.post_company_task(company_id, code, description, url)
    client.task.post_team_task(company_id, team_id, code, description, url)
    client.task.post_user_task(company_id, team_id, user_id, code, description, url)
    client.task.put_company_task(company_id, code, description, url)
    client.task.put_team_task(company_id, team_id, code, description, url)
    client.task.put_user_task(company_id, team_id, user_id, code, description, url)

Delete tasks::

    client.task.delete_company_task(company_id, task_codes)
    client.task.delete_team_task(company_id, team_id, task_codes)
    client.task.delete_user_task(company_id, team_id, user_id, task_codes)
    client.task.delete_all_company_tasks(company_id)
    client.task.delete_all_team_tasks(company_id, team_id)
    client.task.delete_all_user_tasks(company_id, team_id, user_id)

Batch update of tasks::

    client.task.update_batch_tasks(company_id, csv_data)

Where csv_data - is the raw csv data for tasks to be updated. Example::

    "acmeinc","","","ABC","Project ABC","https://www.acmeinc.com/project/abc"<br>"acmeinc","acmeinc:dev","b42","123","Task 123","https://www.acmeinc.com/task/123"


