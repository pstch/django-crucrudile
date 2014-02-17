from django_filters.views import FilterView

class FilterMixin(FilterView):
    template_name_suffix = "_list_filtered"
