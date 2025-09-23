from django import forms
from .models import Task, Subject, LearningItem

# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ["title", "task_type", "subject", "due_date"]

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop("user")  # get the user from view
#         super().__init__(*args, **kwargs)
#         # Filter subjects to match user's semester
#         self.fields["subject"].queryset = Subject.objects.filter(semester=user.semester)
#         # Optional: add field class same as before
#         for field_name, field in self.fields.items():
#             field.widget.attrs.update({"class": field_name})
from django import forms
from .models import Task, Subject

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "task_type", "subject", "due_date", "status"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")  # extract user
        super().__init__(*args, **kwargs)

        # Filter subjects based on the logged-in user's semester
        self.fields["subject"].queryset = Subject.objects.filter(semester=user.semester)

        # Apply Bootstrap classes to fields
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["task_type"].widget.attrs.update({"class": "form-select"})
        self.fields["subject"].widget.attrs.update({"class": "form-select"})
        self.fields["due_date"].widget.attrs.update({"class": "form-control", "type": "date"})
        self.fields["status"].widget.attrs.update({"class": "form-control"})


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', "course_code"]


from django import forms
from .models import LearningItem, Subject

class LearningItemForm(forms.ModelForm):
    class Meta:
        model = LearningItem
        fields = ["subject", "title", "description"]  # exclude 'user'

    def __init__(self, *args, **kwargs):
        # Pop the user from kwargs (mandatory)
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        # Filter subjects for this user based on their semester
        self.fields["subject"].queryset = Subject.objects.filter(semester=self.user.semester)

        # Add CSS class same as field name
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": field_name})
