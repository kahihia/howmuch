from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter
def tagsformat(value, autoescape=None):
	result = ''
	if autoescape:
		esc = conditional_escape
	else:
		esc = lambda x: str(x)
	tags = value.split(',')
	for tag in tags[:len(tags)-1]:
		result += '<a class="item-tag tag blue" href="#">%s</a>' % (esc(tag))
	return mark_safe(result)

@register.filter(is_safe=True)
@stringfilter
def listtostring(value):
	return str(value)