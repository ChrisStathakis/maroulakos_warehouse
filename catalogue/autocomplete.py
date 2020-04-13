from dal.autocomplete import Select2QuerySetView

from .models import Product


class ProductAutocomplete(Select2QuerySetView):

    def get_queryset(self):
        print('wtf')
        if not self.request.user.is_authenticated:
            print('here`')
            return Product.objects.none()
        return Product.filters_data(self.request, Product.objects.filter(product_class__have_ingredient=False, product_class__is_service=False))