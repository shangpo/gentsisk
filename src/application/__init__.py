"""
Initialize Flask app

"""

from flask import Flask
from flaskext.gae_mini_profiler import GAEMiniProfiler
from inspect import getmembers, isfunction
import jinja_filters


app = Flask('application')
app.config.from_object('application.settings')

my_filters = {name: function
                for name, function in getmembers(jinja_filters)
                if isfunction(function)}

app.jinja_env.filters.update(my_filters)

# Enable profiler (enabled in non-production environ only)
GAEMiniProfiler(app)

# Pull in URL dispatch routes
import urls
