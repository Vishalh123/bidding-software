from django.forms import ModelForm
from bidding_app.models import AddProduct

# Create the form class.
class AddProductForm(ModelForm):
     class Meta:
         model = AddProduct
         fields = ['name', 'description', 'max_bid', 'image']
