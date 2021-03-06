"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""


from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import render_template, flash, url_for, redirect

from models import ExampleModel
from decorators import login_required, admin_required
from forms import ExampleForm

from api_keys import *
import api
import settings
import logging


def home():
    return redirect(url_for('list_examples'))


def say_hello(username):
    """Contrived example to demonstrate Flask's url routing capabilities"""
    return 'Hello %s' % username

def api_test():
    eveapi = api.get_api();

    result = eveapi.eve.AllianceList()

    return render_template('list_alliances.html', alliances=result.alliances)


def wallet_total():
    eveapi = api.get_api();

    corpDetails = eveapi.corp.CorporationSheet()
    walletNames = {}

    for accountKey,description in corpDetails.walletDivisions.Select("accountKey", "description"):
        walletNames[accountKey] = description

    logging.info(walletNames)

    wallet = eveapi.corp.AccountBalance(characterID=settings.API_CHARACTERID)
    walletBalances = {}

    for accountKey,balance in wallet.accounts.Select("accountKey", "balance"):
        walletBalances[accountKey] = balance

    logging.info(walletBalances)

    return render_template('wallets.html', walletNames=walletNames, walletBalances=walletBalances)



@login_required
def list_examples():
    """List all examples"""
    examples = ExampleModel.all()
    form = ExampleForm()
    if form.validate_on_submit():
        example = ExampleModel(
            example_name = form.example_name.data,
            example_description = form.example_description.data,
            added_by = users.get_current_user()
        )
        try:
            example.put()
            example_id = example.key().id()
            flash(u'Example %s successfully saved.' % example_id, 'success')
            return redirect(url_for('list_examples'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_examples'))
    return render_template('list_examples.html', examples=examples, form=form)


@login_required
def delete_example(example_id):
    """Delete an example object"""
    example = ExampleModel.get_by_id(example_id)
    try:
        example.delete()
        flash(u'Example %s successfully deleted.' % example_id, 'success')
        return redirect(url_for('list_examples'))
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')
        return redirect(url_for('list_examples'))


@admin_required
def admin_only():
    """This view requires an admin account"""
    return 'Super-seekrit admin page.'


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''
