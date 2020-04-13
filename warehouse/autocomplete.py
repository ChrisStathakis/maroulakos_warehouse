from .models import Vendor

from dal.autocomplete import Select2QuerySetView


class VendorAutocomplete(Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Vendor.objects.none()
        return Vendor.filters_data(self.request, Vendor.objects.filter(active=True))
