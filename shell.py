#!/usr/bin/env python
import os
from pprint import pprint
import readline

from app import create_app as _create_app
from config import Dev as _Dev


os.environ['PYTHONINSPECT'] = 'True'
__ANCHOR_APP__ = _create_app(_Dev)
__ANCHOR_APP__.app_context().push()
