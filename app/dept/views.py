from flask import Blueprint, render_template
from . import dept

@dept.route('/<dept>')
def departmentlist(dept):
  return dept

@dept.route('/<dept>/class/<classnum>')
def classthing(dept, classnum):
    return dept + classnum
