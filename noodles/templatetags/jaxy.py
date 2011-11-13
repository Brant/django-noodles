from django import template
from django.template.loader_tags import ExtendsNode
from django.template import TemplateSyntaxError
from django.template.loader import get_template

register = template.Library()

class JaxyExtend(ExtendsNode):
    
    def __init__(self, nodelist, parent_name, parent_name_expr, condition=None, parent_alt=None, template_dirs=None):
        
        self.condition = condition
        self.parent_alt = parent_alt
            
        super(JaxyExtend, self).__init__(nodelist, parent_name, parent_name_expr, template_dirs=None)       
            
        self.must_be_first = False
        
    def get_parent(self, context):
        if self.parent_name_expr:
            self.parent_name = self.parent_name_expr.resolve(context)
            
        parent = self.parent_name
        
        if self.condition:
            request = context['request']
            if hasattr(request, self.condition):
                if callable(getattr(request, self.condition)):
                    result = getattr(request, self.condition)()
                else:
                    result = getattr(request, self.condition)
                
                if result:
                    parent = self.parent_alt
            else:
                raise TemplateSyntaxError("HttpRequest has no attribute or method %s" % self.condition)
        
        if not parent:
            error_msg = "Invalid template name in 'extends' tag: %r." % parent
            if self.parent_name_expr:
                error_msg += " Got this from the '%s' variable." % self.parent_name_expr.token
            raise TemplateSyntaxError(error_msg)
        
        if hasattr(parent, 'render'):
            return parent # parent is a Template object
        return get_template(parent)
        
        
        
        
def do_jaxy_extends(parser, token):
    """
    Signal that this template extends a parent template.

    This tag may be used in two ways: ``{% extends "base" %}`` (with quotes)
    uses the literal value "base" as the name of the parent template to extend,
    or ``{% extends variable %}`` uses the value of ``variable`` as either the
    name of the parent template to extend (if it evaluates to a string) or as
    the parent tempate itelf (if it evaluates to a Template object).
    """
    bits = token.split_contents()
    if len(bits) != 2 and len(bits) != 4:
        raise TemplateSyntaxError("'%s' takes either 1 or 3 arguments" % bits[0])
    
    parent_name, parent_name_expr = None, None
    
    if len(bits) == 4:
        condition = bits[2]        
        parent_name = bits[1][1:-1]    
        parent_alt = bits[3][1:-1]
    else:
        if bits[1][0] in ('"', "'") and bits[1][-1] == bits[1][0]:
            parent_name = bits[1][1:-1]
        else:
            parent_name_expr = parser.compile_filter(bits[1])
    
    nodelist = parser.parse()
    
    if nodelist.get_nodes_by_type(ExtendsNode):
        raise TemplateSyntaxError("'%s' cannot appear more than once in the same template" % bits[0])
    
    return JaxyExtend(nodelist, parent_name, parent_name_expr, condition, parent_alt, template_dirs=None)

register.tag('jaxtends', do_jaxy_extends)