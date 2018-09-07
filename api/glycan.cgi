#!/usr/bin/python
import os,sys
import json


from wsgiref.handlers import CGIHandler

from glycan import app

#print "Content-type: application/json "
#print 
#print """"""

CGIHandler().run(app)


