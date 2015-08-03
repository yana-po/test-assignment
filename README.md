## Project Overview
This is a Python script which returns a list of all uncountable English nouns from Wiktionary.

## Code Implementation
Basically the implemented solution breaks the task into several smaller steps:
- create a URL that tells the English Wiktionary's web service API
to send us the content of the [English uncountable nouns](https://en.wiktionary.org/wiki/Category:English_uncountable_nouns) page.
With all query paramaters specified, the following URL is generated:
https://en.wiktionary.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:English_uncountable_nouns&cmprop=title&cmlimit=max&cmcontinue=&format=json
- make an HTTP GET request for this URL and obtain a JSON response
- iterate over the parsed content and yield titles (nouns) within the category
- update 'continue' and 'cmcontinue' parameters and repeat the request until it reaches the end of the category
- write the yielded nouns in a file.

```python
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
```
For information on methods and functionalities of Requests HTTP library, see
[Requests](http://docs.python-requests.org/en/latest/) documentation.
For details on MediaWiki API web service usage, see
[MediaWiki API](https://www.mediawiki.org/wiki/API:Main_page) documentation.

## Requirements
- Python 2.7
- Requests library

## Requests Installation
    pip install -r requirements.txt