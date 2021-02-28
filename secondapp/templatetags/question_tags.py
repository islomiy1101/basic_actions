from django import template
from ..models import PartQuestion, Question


register = template.Library()


@register.inclusion_tag('secondapp/savollar.html')
def savollar(id):
    data = Question.objects.filter(partquestion_id__id=id)
    return {'data': data}