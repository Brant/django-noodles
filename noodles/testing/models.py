from noodles.models import TitleDateSlug, ActiveToggler


class TitleDateSlugConcrete(TitleDateSlug):
    """
    Concreate class to test against
    """
    pass

    class Meta:
        db_table = "noodles_titledateslugconcrete"

class ActiveTogglerConcrete(ActiveToggler):
    """
    Concrete class to test against
    """
    pass 
    
    class Meta:
        db_table = "noodles_activetogglerconcrete"