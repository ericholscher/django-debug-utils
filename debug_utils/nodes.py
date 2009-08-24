"""
from http://www.djangosnippets.org/snippets/1689/

Tag to inspect template context, filter to inspect variable.

Originally by denis, http://www.djangosnippets.org/snippets/1550/.

This just extracts variables from the context to locals for quicker access and autocompletion (When using ipdb).

Additionally, 'vars' holds context keys for quick reference to whats available in the template. 
"""
from django.template import Library, Node

register = Library()

try:
    import ipdb as pdb
except ImportError:   
    import pdb

class PdbNode(Node):
    def render(self, context):
        # Access vars at the prompt for an easy reference to
        # variables in the context
        vars = []
        for dict in context.dicts:
            for k, v in dict.items():
                vars.append(k)
                locals()[k] = v
        pdb.set_trace()
        return ''

@register.tag("pdbdebug")
def pdbdebug_tag(parser, token):
    """Tag that inspects template context.

    Usage: 
    {% pdb_debug %}

    You can then access your context variables directly at the prompt.

    The vars variable additonally has a reference list of keys
    in the context.
    """
    return PdbNode()

@register.filter("pdbdebug")
def pdbdebug_filter(value, arg=None):
    """Filter that inspects a specific
    variable in context.

    Usage:
    {{ variable|pdbdebug }}
    """
    pdb.set_trace();  
    return ''

