from .models import SchoolClass

def school_classes(request):
    if hasattr(request, 'user') and request.user.is_authenticated and request.user.role != 'user':
        classes = SchoolClass.objects.filter(customuser=request.user)
        print("Classes from explicit query:", [c.name for c in classes])
        return {'school_classes': classes}
    return {'school_classes': []}