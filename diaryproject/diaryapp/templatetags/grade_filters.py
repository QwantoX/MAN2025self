from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def school_classes(request):
    if hasattr(request, 'user') and request.user.is_authenticated and request.user.role != 'user':
        # Отримати класи, призначені користувачу
        classes = request.user.assigned_classes.all()
        print("Classes assigned to user:", [c.name for c in classes])
        return {'school_classes': classes}
    return {'school_classes': []}



