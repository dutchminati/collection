from urllib2 import Request, urlopen, URLError
import requests, time, json, random

word_list = 'words2.txt'
retry_count = 1
debug = True

class Mailinraper:

  def __init__(self, wordlist, retry_count=3, debug=True):
    self.wordlist = wordlist
    self.max_retry_count = retry_count
    self.retry_count = 0
    self.debug = debug

    # read in wordlist
    file = open(wordlist, 'r')
    self.words = file.readlines()
    file.close()

    if self.debug:
      print len(self.words)

  def do_request(self, url):

    headers = {'User-Agent' : 'Googlebot/2.1 (+http://www.google.com/bot.html)'}
    request = Request(url, None, headers)

    if (self.retry_count < self.max_retry_count):

      try:

        response = urlopen(request).read()

        if response:
          self.retry_count = 0
          return response
        else:
          self.retry_count += 1

          if self.debug:
            print "do_request: Invalid Response: Retry " + str(self.retry_count)

          self.do_request(url)

      except URLError as e:
        self.retry_count += 1

        if self.debug:
          print e.reason

        self.do_request(url)

    else:
      self.retry_count = 0
      return None

  def get_addr(self, username):

    url = "http://mailinator.com/settttt?box=" + username

    if (self.retry_count < self.max_retry_count):

      response = self.do_request(url)

      if response:

        json_object = json.loads(response)

        if json_object and json_object.has_key('address'):

          if json_object['address'] is not None:
            self.retry_count = 0

            return json_object['address']
          else:
            self.retry_count += 1
            self.get_addr(username)

        else:
          self.retry_count += 1

          if self.debug:
            print "get_addr: Response did not contain the address"

          self.get_addr(username)


      else:

        if self.debug:
          print "get_addr: Hit Max Retry Count"

        return None

    else:
      return None


    if response:

      json_object = json.loads(response)

    else:
      return None

  def get_mail(self, username):

    if (self.retry_count < self.max_retry_count):
      address = self.get_addr(username)

      if address is not None:

        url = "http://mailinator.com/grab?inbox=" + username + "&address=" + address

        response = self.do_request(url)

        if response:

          json_object = json.loads(response)

          if json_object and json_object.has_key('maildir'):
            self.retry_count = 0
            return json_object['maildir']
          else:
            self.retry_count += 1
            self.get_mail(username)
        else:

          if self.debug:
            print "get_mail: No response"

          self.get_mail(username)

      else:
        self.retry_count = 0

        if self.debug:
          print "get_mail: Failed to get the address for: " + username

        return None
    else:
      self.retry_count = 0
      return None

  def search_mail(self, username):

    maildir = self.get_mail(username)

    if maildir is not None:

      if len(maildir) > 0:
        found_any = 0
        found_twitter = 0
        found_facebook = 0
        found_linkedin = 0
        found_okcupid = 0

        for message in maildir:

          if message and message.has_key('fromfull'):

            if "twitter" in message['fromfull'] and found_twitter == 0:

              print "Found Twitter Account"
              print "Account: " + username + "@mailinator.com"
              print "Subject: " + message['subject']
              print "Link: http://mailinator.com/rendermail.jsp?msgid="+ str(message['id'])

              with open("twitter.txt", "a") as file:
                account = username + "@mailinator.com\n"
                file.write(account)

              found_any = 1
              found_twitter = 1

            if "facebook" in message['fromfull'] and found_facebook == 0:

              print "Found Facebook Account"
              print "Account: " + username + "@mailinator.com"
              print "Subject: " + message['subject']
              print "Link: http://mailinator.com/rendermail.jsp?msgid="+ str(message['id'])

              with open("facebook.txt", "a") as file:
                account = username + "@mailinator.com\n"
                file.write(account)

              found_any = 1
              found_facebook = 1

            if "linkedin" in message['fromfull'] and found_linkedin == 0:

              print "Found LinkedIn Account"
              print "Account: " + username + "@mailinator.com"
              print "Subject: " + message['subject']
              print "Link: http://mailinator.com/rendermail.jsp?msgid="+ str(message['id'])

              with open("linkedin.txt", "a") as file:
                account = username + "@mailinator.com\n"
                file.write(account)

              found_any = 1
              found_linkedin = 1

            if "okcupid" in message['fromfull'] and found_okcupid == 0:

              print "Found OKCupid Account"
              print "Account: " + username + "@mailinator.com"
              print "Subject: " + message['subject']
              print "Link: http://mailinator.com/rendermail.jsp?msgid="+ str(message['id'])

              with open("okcupid.txt", "a") as file:
                account = username + "@mailinator.com\n"
                file.write(account)

              found_any = 1
              found_okcupid = 1

        if found_any == 0:
          print "Couldn't find anything using: " + username

      else:
        print "Emty Mailbox for: " + username
    else:
      print "Maildir returned None for: " + username

  def pwn(self):

    for word in self.words:

      username = word.rstrip()
      self.search_mail(username)
      #time.sleep(2)


Mailinraper(word_list, retry_count, debug).pwn()