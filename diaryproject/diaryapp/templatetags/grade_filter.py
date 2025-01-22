from django import template

register = template.Library()

@register.filter
def avg_grade(grades):
    if not grades:
        return 0
    return sum(grade.grade for grade in grades) / len(grades)