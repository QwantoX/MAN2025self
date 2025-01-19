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
#             # Якщо користувач звичайний, дозволяємо лише 1 клас
#             self.fields['assigned_classes'].widget = forms.Select()
#         else:
#             # Для модератора чи адміна дозволяємо множинний вибір
#             self.fields['assigned_subjects'].widget = forms.SelectMultiple()
#             self.fields['assigned_classes'].widget = forms.SelectMultiple()
