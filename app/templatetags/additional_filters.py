from django import template

register = template.Library()

def cut_underscores(value):
    return value.replace("_", " ")

register.filter('cut_underscores', cut_underscores)