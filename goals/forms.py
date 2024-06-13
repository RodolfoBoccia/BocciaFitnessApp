from django import forms

from .models import GoalModel


class GoalForm(forms.ModelForm):
    class Meta:
        model = GoalModel
        fields = ['goal_type', 'tempistica', 'descrizione', 'CaloriesGoal', 'is_selected']
        widgets = {
            'goal_type': forms.Select(attrs={'class': 'form-control'}),
            'tempistica': forms.Select(attrs={'class': 'form-control'}),
            'is_selected': forms.CheckboxInput(),
        }
