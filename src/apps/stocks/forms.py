from django import forms


class InvestmentPortfolioCreateForm(forms.Form):
    name = forms.CharField(
        label="Enter value",
        max_length=100,
        widget=forms.TextInput(attrs={'style': 'color: white;'})
    )
