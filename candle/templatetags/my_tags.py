import random
from django import template

register = template.Library()

@register.simple_tag
def random_reviews():
    num = random.randint(1, 50)
    return num