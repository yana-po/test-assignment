import requests, json, codecs, os

# A generator function that iterates over and returns available nouns
def nouns():
    """
    Fetch nouns (titles of category members) listed in
    the respective Wiktionary category with an HTTP-GET request
    """
    # Providing parameters of a query string wrapped up
    # in a dictionary as its key-value pairs
    query_data = {
        'action':'query',
        'list':'categorymembers',
        'cmtitle':'Category:English_uncountable_nouns',
        'cmprop':'title',
        'cmlimit':'max',
        'format':'json',
        'continue':'',
        'cmcontinue':''
    }
    
    response = {'continue':''}
    # Setting a condition for the generator function: while
    # 'continue' section appears in the query response, its values
    # are used to update the query parameters.
    while 'continue' in response:
        # Sending a query in the URL and calling Wiktionary API
        # to obtain a response object parsed in the json format
        # https://www.mediawiki.org/wiki/API:Main_page
        response = requests.get('https://en.wiktionary.org/w/api.php', params=query_data).json()
        categorymembers = response['query']['categorymembers']
        # Yielding every title from the 'category members' section of the response
        for cm in categorymembers:
            yield cm['title']
        if 'continue' in response: 
            # Updating parameters of the original query with the values returned
            # in the 'continue' and 'cmcontinue' sections of the last iteration
            query_data['continue'] = response['continue']['continue']
            query_data['cmcontinue'] = response['continue']['cmcontinue']

if __name__ == "__main__":
    # Creating new file
    with codecs.open('nouns.txt', 'w', encoding='UTF-8') as f:
        # Launching the iterator for the "nouns()" function
        for noun in nouns():
            # Writing words in the "nouns.txt" file
            f.write(noun + os.linesep)