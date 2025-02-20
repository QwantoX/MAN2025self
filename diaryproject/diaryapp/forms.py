from django import forms
from .models import CustomUser, Subject, SchoolClass

# class CustomUserAdminForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'username', 'role', 'assigned_subjects', 'assigned_classes']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.fields['assigned_subjects'].queryset = Subject.objects.all()
#         self.fields['assigned_classes'].queryset = SchoolClass.objects.all()

#         instance = kwargs.get('instance')
#         if instance and instance.role == 'user':
#             self.fields['assigned_classes'].widget = forms.Select()
#         else:
#             self.fields['assigned_subjects'].widget = forms.SelectMultiple()
#             self.fields['assigned_classes'].widget = forms.SelectMultiple()


from django import forms
from .models import Grade, CustomUser, Subject, SchoolClass

from datetime import date

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'school_class', 'grade', 'date']
        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date', 'value': date.today().strftime('%Y-%m-%d')}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(GradeForm, self).__init__(*args, **kwargs)
 
        self.fields['date'].initial = date.today()
        
        if user and user.role != 'user':
            if user.assigned_classes.exists():
                self.fields['school_class'].queryset = user.assigned_classes.all()
            if user.assigned_subjects.exists():
                self.fields['subject'].queryset = user.assigned_subjects.all()