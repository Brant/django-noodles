"""
custom list fitlers
"""
from django.db.models import Q
from django.contrib.admin import SimpleListFilter


class HasTextListFilter(SimpleListFilter):
    """
    Custom list filter to determine
        whether or not a field has text in it
        
    Accounts for NULL and '' values (null and blank string)
    """
    def lookups(self, request, model_admin):
        """
        Offer a yes and a no
        """
        return (
            ('y', 'Yes'),
            ('n', 'No')
        )
        
    def queryset(self, request, queryset):
        """
        Filter the queryset dynamically, based on self.parameter_name
        """
        if self.value() == 'y':
            query = Q(~Q(**{self.parameter_name: ""}) & Q(**{"%s__isnull" % self.parameter_name: False}))
            return queryset.filter(query)
        
        if self.value() == 'n':
            query = Q(Q(**{self.parameter_name: ""}) | Q(**{"%s__isnull" % self.parameter_name: True}))
            return queryset.filter(query)
