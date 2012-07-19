#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json
import logging

import webapp2
from google.appengine.api import mail

from  models import BotResults
from models import Speakers

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Test Day Reporter')

class BotHandler(webapp2.RequestHandler):
    def post(self):
        logging.debug("BotHandler.post has been called")
        data = json.loads(self.request.body)
        logging.info(self.request.body)
        results = BotResults(testday=data['testday'],
                             greetedName = data['greetedName'],
                             greetedNumber = data['greetedNumber'],
                             firebotBugs = data['firebotBugs'],
                             )
        id = results.put()
        logging.info(data['usersTalked'])
        for k,v in data['usersTalked'].items():
            speaker = Speakers(botresults = id,
                               speaker=k,
                               spoke=v)
            speaker.put()

        self._send_email(data)

    def _send_email(self, data):
        message = mail.EmailMessage()
        message.sender = "david.burns@theautomatedtester.co.uk"
        message.to = "dburns@mozilla.com, ahughes@mozilla.com"
        message.subject = "Testday Stats for: %s " % data['testday'][29:]
        message.body = """The following stats were collected from the following testday:
            %s
            %s
        """ % (data['testday'], json.dumps(data))
        message.send()

app = webapp2.WSGIApplication([('/', MainHandler),
                              ('/bot', BotHandler)],
                              debug=True)

