from flask import Blueprint, render_template
from . import prof

@prof.route('/<professor>')
def stuff(professor):
  return professor
