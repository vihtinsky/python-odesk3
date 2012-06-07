import odesk
#oAuth key
PUBLIC_KEY = None
SECRET_KEY = None


def web_based_app(public_key, secret_key):
    print ("Emulating web-based app")
    #Instantiating a client without an auth token
    client = odesk.Client(public_key, secret_key, auth='oauth')

    print ("Please to this URL (authorize the app if necessary):")
    print (client.auth.get_authorize_url())

    print ("After that you should be redirected back to your app URL with " + \
          "additional ?oauth_verifier= parameter")
    verifier = input('Enter oauth_verifier: ')

    oauth_access_token, oauth_access_token_secret = client.auth.get_access_token(verifier)

    #Instantiating a new client, now with a token.
    #Not strictly necessary here (could just set `client.oauth_access_token`
    #and `client.oauth_access_token_secret`), but typical for web apps,
    #which wouldn't probably keep client instances between requests

    client = odesk.Client(public_key, secret_key, auth='oauth',
                        oauth_access_token=oauth_access_token,
                        oauth_access_token_secret=oauth_access_token_secret)

    try:
        print ("Tasks list:")
        print (client.task.get_user_tasks('company_id', 'team_id', 'user_id'))
        #Post new task
        print(client.task.post_user_task(company_id='company',
                team_id='team', user_id='provider', code='TEST_TASK',
                description='Test api task', url='http://task_url.py'
            ))
        #Update task
        print(client.task.post_user_task(company_id='company',
                team_id='team', user_id='provider', code='TEST_TASK',
                description='Test api updated', url='http://task_url.py'
            ))
        #Should be list of task_codes. If one task list of 1 element
        print(client.task.delete_user_task(company_id='company',
                team_id='team', user_id='provider', task_codes=["TEST_TASK", "TASK_2"]
            ))

    except Exception as e:
        print ("Exception at %s %s" % (client.last_method, client.last_url))
        raise e



if __name__ == '__main__':
    public_key = PUBLIC_KEY or input('Enter public key: ')
    secret_key = SECRET_KEY or input('Enter secret key: ')

    web_based_app(public_key, secret_key)

