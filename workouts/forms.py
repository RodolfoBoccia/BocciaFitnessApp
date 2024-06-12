from django import forms
from .models import Workout


class WorkoutForm(forms.ModelForm):
        class Meta:
            model = Workout
            fields = ['workout_type', 'distance', 'calories_burned','repetitions','weight','descrizione']
            widgets = {
                'workout_type': forms.Select(attrs={'class': 'form-control'}),
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['distance'].required = False

        def form_valid(self, form):
            form.instance.utente = self.request.user
            return super().form_valid(form)

        def clean(self):
            cleaned_data = super().clean()
            workout_type = cleaned_data.get('workout_type')

            if workout_type == 'pesi':
                cleaned_data['distance'] = None
            elif workout_type == 'altro':
                cleaned_data['repetitions'] = None
                cleaned_data['weight'] = None

            return cleaned_data
