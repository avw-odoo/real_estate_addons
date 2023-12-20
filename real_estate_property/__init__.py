# -*- coding: utf-8 -*-

from . import models
from . import controllers
from odoo import models, fields, api

 
def _assign_property_folder(env):
    folder_demo_ref = 'real_estate_property.folder_demo_property_maison_1'
    parent_folder_ref = 'real_estate_property.documents_realestate_folder'
    
    folder_demo = env.ref(folder_demo_ref, raise_if_not_found=False)
    parent_folder = env.ref(parent_folder_ref, raise_if_not_found=False)
    
    if folder_demo and parent_folder:
        folder_demo.write({'parent_folder_id': parent_folder.id})
    
    folder_demo_ref = 'real_estate_property.folder_demo_property_maison_2'
    parent_folder_ref = 'real_estate_property.documents_realestate_folder'
    
    folder_demo = env.ref(folder_demo_ref, raise_if_not_found=False)
    parent_folder = env.ref(parent_folder_ref, raise_if_not_found=False)
    
    if folder_demo and parent_folder:
        folder_demo.write({'parent_folder_id': parent_folder.id})
    
    folder_demo_ref = 'real_estate_property.folder_demo_property_maison_3'
    parent_folder_ref = 'real_estate_property.documents_realestate_folder'
    
    folder_demo = env.ref(folder_demo_ref, raise_if_not_found=False)
    parent_folder = env.ref(parent_folder_ref, raise_if_not_found=False)
    
    if folder_demo and parent_folder:
        folder_demo.write({'parent_folder_id': parent_folder.id})
    
    folder_demo_ref = 'real_estate_property.folder_demo_property_maison_4'
    parent_folder_ref = 'real_estate_property.documents_realestate_folder'
    
    folder_demo = env.ref(folder_demo_ref, raise_if_not_found=False)
    parent_folder = env.ref(parent_folder_ref, raise_if_not_found=False)
    
    if folder_demo and parent_folder:
        folder_demo.write({'parent_folder_id': parent_folder.id})
    
    folder_demo_ref = 'real_estate_property.folder_demo_property_maison_5'
    parent_folder_ref = 'real_estate_property.documents_realestate_folder'
    
    folder_demo = env.ref(folder_demo_ref, raise_if_not_found=False)
    parent_folder = env.ref(parent_folder_ref, raise_if_not_found=False)
    
    if folder_demo and parent_folder:
        folder_demo.write({'parent_folder_id': parent_folder.id})