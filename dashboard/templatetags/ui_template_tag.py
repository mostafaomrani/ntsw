
from django.template import Library
from django.urls import reverse_lazy

register = Library()


@register.inclusion_tag('dashboard/template_tags/section_title.html')
def section_title(title):
    return {'title': title}


@register.inclusion_tag('dashboard/template_tags/breadcrumb.html')
def breadcrumbs(*args, **kwargs):
    breadcrumbs_list = []
    for a, b in zip(args[::2], args[1::2]):
        url = reverse_lazy(b) if ':' in b else b
        breadcrumbs_list.append(
            {
                'text': a,
                'url': url,
            }
        )
    return {'breadcrumb_list': breadcrumbs_list}


@register.inclusion_tag('dashboard/template_tags/input_box.html')
def input_box(lable, value, disabled=True, field_type='text', div_with='', name='', input_id=''):
    d = 'disabled' if disabled else ''
    v = value if value else ''
    context = {
        'label': lable,
        'value': v,
        'disabled': d,
        'type': field_type,
        'class': div_with,
        'name': name,
        'input_id': input_id,

    }
    return context


@register.inclusion_tag('dashboard/template_tags/widget_tweak_field.html')
def widget_tweaks_field(field, width='col-12 col-md-6 col-lg-3', *args, **kwargs):
    context = {
        'field': field,
        'width': width,
    }
    attr = [
        'required',
        'placeholder',
        'control_class',
        'invalid_feedback',
    ]
    for a in attr:
        attr = kwargs.get(a, None)
        if attr:
            context[a] = attr
        # add bootstrap form control class for all field
        context['control_class'] = f"form-control {context.get('control_class', '').strip()}"
    return context


@register.inclusion_tag('dashboard/template_tags/business_intro_box.html')
def business_intro_box(icon, color_class_suffix, count, title, main_link="#", *args, **kwargs):
    context = {
        'icon': icon,
        'color_class_suffix': color_class_suffix,
        'count': count,
        'title': title,
        'links': kwargs['links'],
        'main_link': main_link,
    }
    return context


@register.inclusion_tag('dashboard/template_tags/error.html')
def show_error(field):
    return {
        'errors': field.errors
    }
