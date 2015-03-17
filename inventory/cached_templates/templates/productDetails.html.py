# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1425761864.220115
_enable_loop = True
_template_filename = '/Users/spencerlowe/PycharmProjects/chef-master/inventory/templates/productDetails.html'
_template_uri = 'productDetails.html'
_source_encoding = 'ascii'
import os, os.path, re
_exports = ['tab_title', 'content', 'paper_elements_import', 'extra_links']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, '/base_app/templates/base.htm', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        product = context.get('product', UNDEFINED)
        def paper_elements_import():
            return render_paper_elements_import(context._locals(__M_locals))
        def tab_title():
            return render_tab_title(context._locals(__M_locals))
        def content():
            return render_content(context._locals(__M_locals))
        def extra_links():
            return render_extra_links(context._locals(__M_locals))
        __M_writer = context.writer()
        __M_writer('\n')
        __M_writer('\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'tab_title'):
            context['self'].tab_title(**pageargs)
        

        __M_writer('\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'paper_elements_import'):
            context['self'].paper_elements_import(**pageargs)
        

        __M_writer('\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'extra_links'):
            context['self'].extra_links(**pageargs)
        

        __M_writer('\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        return ''
    finally:
        context.caller_stack._pop_frame()


def render_tab_title(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def tab_title():
            return render_tab_title(context)
        __M_writer = context.writer()
        __M_writer('\n  Edit Item\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def content():
            return render_content(context)
        product = context.get('product', UNDEFINED)
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n\n\t<div class="page_title">\n\t\t<h1>Details: ')
        __M_writer(str( product.name ))
        __M_writer('</h1>\n\t</div>\n\n')
        __M_writer('\t<div class="row">\n\n')
        __M_writer('\t <div class="col-md-12 text-center">\n         <br>\n         <img src="')
        __M_writer(str( STATIC_URL ))
        __M_writer('inventory/media/')
        __M_writer(str( product.id ))
        __M_writer('.jpg" class="imgsize" />\n         <br>\n         <br>\n         <br>\n         <div>\n            <b>Price:</b> $')
        __M_writer(str( product.price ))
        __M_writer('\n         </div>\n         <div>\n            <b>Condition:</b> ')
        __M_writer(str( product.condition ))
        __M_writer('\n         </div>\n         <div>\n            <b>In Stock:</b> ')
        __M_writer(str( product.quantity_on_hand ))
        __M_writer('\n         </div>\n         <div>\n            <b>Description:</b> ')
        __M_writer(str( product.note ))
        __M_writer('\n         </div>\n         <br>\n         <table align="center">\n             <tr>\n                 <td>\n                     <input type="number" class="form-control" placeholder="Qty" id="qty" value="1">\n                 </td>\n                 <td>\n                     <button class="btn btn-warning" data-pid="')
        __M_writer(str( product.id ))
        __M_writer('" id="cart_button">Add To Cart</button>\n                 </td>\n             </tr>\n         </table>\n\n\t </div>\n')
        __M_writer('\n\t</div>\n')
        __M_writer('\n')
        __M_writer('\t<div class="spacer"></div>\n\t<div class="spacer"></div>\n\t<div class="spacer"></div>\n')
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_paper_elements_import(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def paper_elements_import():
            return render_paper_elements_import(context)
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n\t<link rel="import" href="')
        __M_writer(str( STATIC_URL ))
        __M_writer('base_app/styles/bower_components/paper-input/paper-input.html">\n\t<link rel="import" href="')
        __M_writer(str( STATIC_URL ))
        __M_writer('base_app/styles/bower_components/paper-button/paper-button.html">\n\t<link rel="import" href="')
        __M_writer(str( STATIC_URL ))
        __M_writer('base_app/styles/bower_components/paper-radio-group/paper-radio-group.html">\n\t<link rel="import" href="')
        __M_writer(str( STATIC_URL ))
        __M_writer('base_app/styles/bower_components/paper-radio-button/paper-radio-button.html">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extra_links(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        def extra_links():
            return render_extra_links(context)
        __M_writer = context.writer()
        __M_writer('\n\t<link rel="stylesheet" type="text/css" href="')
        __M_writer(str( STATIC_URL ))
        __M_writer('base_admin/styles/Edit.css">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "/Users/spencerlowe/PycharmProjects/chef-master/inventory/templates/productDetails.html", "uri": "productDetails.html", "source_encoding": "ascii", "line_map": {"128": 11, "129": 11, "130": 12, "131": 12, "137": 15, "144": 15, "145": 16, "146": 16, "152": 146, "27": 0, "42": 1, "43": 2, "48": 6, "53": 13, "58": 17, "68": 4, "74": 4, "80": 19, "88": 19, "89": 22, "90": 22, "91": 26, "92": 29, "93": 31, "94": 31, "95": 31, "96": 31, "97": 36, "98": 36, "99": 39, "100": 39, "101": 42, "102": 42, "103": 45, "104": 45, "105": 54, "106": 54, "107": 61, "108": 64, "109": 66, "110": 70, "116": 8, "123": 8, "124": 9, "125": 9, "126": 10, "127": 10}}
__M_END_METADATA
"""
