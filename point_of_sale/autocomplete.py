from dal import autocomplete

from .models import Costumer


class CostumerAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Costumer.objects.none()
        return Costumer.filters_data(self.request, Costumer.objects.filter(active=True))