from django import template

register = template.Library()

@register.filter(is_safe=True)
def label_with_css(value, arg):
    return value.label_tag(attrs={'class': arg})
    
@register.filter(is_safe=True)
def with_css(value, arg):
    return value.as_widget(attrs={'class': arg})
    