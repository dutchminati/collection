import urllib, json, re, urllib2, requests

## A Function to crawl through 4chan
def crawl_4chan(thread):

    ## Defining the URL for the JSON file
    url = "https://boards.4chan.org/pol/thread/" + str(thread) + ".json"

    ## Download the JSON file
    resp = urllib.urlopen( url )

    ## Get HTTP response code
    check = resp.getcode()

    ## If JSON doesn't return 404
    if check != 404:

        ## Load the JSON file
        data = json.loads(resp.read())

        ## Save JSON to list
        posts = data['posts']

        ## Reiterate list for filtering
        for i in posts:

            ## If 'com' key is in list, start filtering
            if 'com' in i:

                ## Some basic filtering
                text = i['com'].encode('utf-8').replace('&quot;', '"').replace('&#039;', "'").replace('<title>','').replace('</title>', '').replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("<br>", "").replace("<s>", "").replace("</br>", "").replace("</s>", "")
                final = re.sub('<[^>]*>', '', text).replace('>>', '')

                ## Final result displays a basic text output
                print final

## Display the JSON output from entered thread
crawl_4chan(68897565)
