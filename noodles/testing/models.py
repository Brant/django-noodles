from noodles.models import TitleDateSlug, ActiveToggler

class TitleDateSlugConcrete(TitleDateSlug):
    """
    Concreate class to test against
    """
    class Meta:
        """
        Django metadata
        """
        app_label = "noodles"

class ActiveTogglerConcrete(ActiveToggler):
    """
    Concrete class to test against
    """
    class Meta:
        """
        Django metadata
        """
        app_label = "noodles"