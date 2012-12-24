Gentlemen's Agreement ISK Tracking
==================================

This app runs the Gentlemen's Agreement ISK Tracking website on Google App Engine.


Installation
============

* Clone this repo
* Get the Google App Engine [https://developers.google.com/appengine/downloads]
* Install the development requirements
<pre class="console">
    sudo apt-get install build-essential python-dev python-pip
    sudo pip install -r requirements_dev.txt
</pre>
* Create the secret\_keys.py file for CSRF protection
<pre class="console">
    cd src/application
    python generate_keys.py
</pre>
* Create the api\_keys.py file for storing the API KEY details in
<pre class="console">
    cd src/application
    vim api_keys.py
</pre>
* Put the following within the api\_keys.py file placing the appropriate key details in each constant.
<pre>
    # API Keys
    API_KEYID = ''
    API_VCODE = ''
</pre>
* Start the GAE dev\_server.py
<pre class="console">
    ~/google_appengine/dev_appserver.py src/ -a <ipaddress> --high_replication --use_sqlite
</pre>
* Visit page http://<ipaddress>:8080/

