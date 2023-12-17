# -*- coding: utf-8 -*-

from . import models
from . import controllers


def _generate_templates(env):
    default_urban_template = env['res.company']._get_default_urban_planning_template()
    
    env['res.company'].search([]).write({
        'urban_planning_template': default_urban_template,
    })