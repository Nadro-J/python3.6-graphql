import json

# possibly move functions except handler() into separate .py file then import and call where necessary.
def getArticles():
    query = '''
        query GetArticles {
            articles {
            nodes {
                image
                id
                ownerId
            }
            }
        }
    '''
    return query

def getUsers():
    query = '''
        query GetUsers {
          users {
            nodes {
              username
              id
            }
          }
        }
    '''
    return query

def handle(params, context):
    """handle a request to the function
    Args:
        params (json): request body
        context (json): context, including GraphQL client
    """
    if params.decode('utf-8') == "getArticles":
        result = context.client.execute(getArticles())
    elif params.decode('utf-8') == "getUsers":
        result = context.client.execute(getUsers())

    return {
        'function': 'ok',
        'params': params,
        'result': json.loads(result)}

