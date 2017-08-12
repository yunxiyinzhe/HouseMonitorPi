#!/usr/bin/env python
import os
from app import create_app
from flask_script import Manager

application  = create_app(__name__)
manager = Manager(application)

if __name__ == '__main__':
    manager.run()
