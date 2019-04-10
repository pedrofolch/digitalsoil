from django import forms
from .models import Recipe


class RecipeCreateForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = [
            'producer',
            "pile_name",
            'image',
            "content",
            "observation",
            "user",
            "ready_to_use",
            "recipe_name",
            "public",
            "draft",
            "category",
            "category_value",
            "nitrogen_material",
            "type_of_bucket_nitrogen",
            "amount_nitrogen",
            "nitrogen_material_two",
            "type_of_bucket_nitrogen_two",
            "amount_nitrogen_two",
            "nitrogen_material_three",
            "type_of_bucket_nitrogen_three",
            "amount_nitrogen_three",
            "high_nitrogen_material",
            "type_of_bucket_high_nitrogen",
            "amount_high_nitrogen",
            "high_nitrogen_material_two",
            "type_of_bucket_high_nitrogen_two",
            "amount_high_nitrogen_two",
            "high_nitrogen_material_three",
            "type_of_bucket_high_nitrogen_three",
            "amount_high_nitrogen_three",
            "carbon_material",
            "type_of_bucket_carbon",
            "amount_carbon",
            "carbon_material_two",
            "type_of_bucket_carbon_two",
            "amount_carbon_two",
            "carbon_material_three",
            "type_of_bucket_carbon_three",
            "amount_carbon_three",
            "wide",
            "length",
            "tall"
        ]

    def __init__(self, user=None, *args, **kwargs):
        # print(kwargs.pop('user'))
        # print(user)
        # print(kwargs)
        super(RecipeCreateForm, self).__init__(*args, **kwargs)
        self.fields['recipe_name'].queryset = Recipe.objects.filter(user=user)
