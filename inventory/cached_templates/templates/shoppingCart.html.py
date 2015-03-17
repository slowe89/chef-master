# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1425761005.751362
_enable_loop = True
_template_filename = '/Users/spencerlowe/PycharmProjects/chef-master/inventory/templates/shoppingCart.html'
_template_uri = 'shoppingCart.html'
_source_encoding = 'ascii'
import os, os.path, re
_exports = ['content', 'extra_links']


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
    return runtime._inherit_from(context, '/base_app/templates/base_ajax.htm', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        def content():
            return render_content(context._locals(__M_locals))
        items = context.get('items', UNDEFINED)
        def extra_links():
            return render_extra_links(context._locals(__M_locals))
        __M_writer = context.writer()
        __M_writer('\n\n')
        __M_writer('\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'extra_links'):
            context['self'].extra_links(**pageargs)
        

        __M_writer('\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def content():
            return render_content(context)
        items = context.get('items', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n\n    <div>\n\n        <table class="table table-hover table-bordered">\n            <thead>\n                <tr>\n\n                    <th>\n                        Item Name\n                    </th>\n\n                    <th>\n                        Quantity\n                    </th>\n                    <th>\n                        Total Price\n                    </th>\n                    <th>\n                        Remove\n                    </th>\n                </tr>\n            </thead>\n            <tbody>\n\n        ')
        totalPrice = 0 
        
        __M_writer('\n')
        for item in items:
            __M_writer('            <tr>\n                <td>\n                    <span>')
            __M_writer(str( item.name ))
            __M_writer('</span>\n                </td>\n                <td>\n                    <span>')
            __M_writer(str( items[item] ))
            __M_writer('</span>\n                </td>\n                <td>\n                    <span>$')
            __M_writer(str( item.price * items[item] ))
            __M_writer('</span>\n                </td>\n                <td>\n                    <div align="center">\n                        <button class="btn btn-danger" data-id="')
            __M_writer(str( item.id ))
            __M_writer('" id="delete_item">Delete</button>\n                    </div>\n                </td>\n            </tr>\n            ')
            totalPrice += (item.price * items[item]) 
            
            __M_writer('\n')
        __M_writer('            <tr>\n                <td>\n                    <b>Total</b>\n                </td>\n                <td></td>\n                <td>\n                    <b>$')
        __M_writer(str( totalPrice ))
        __M_writer('</b>\n                </td>\n            </tr>\n            </tbody>\n\n         </table>\n        <div align="right">\n            <a href="/inventory/shopping_cart.checkOut/">\n                <button class="btn btn-warning" id="btn_purchase">Check Out</button>\n            </a>\n        </div>\n    </div>\n\n')
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
        __M_writer('\n    <link rel="stylesheet" type="text/css" href="')
        __M_writer(str( STATIC_URL ))
        __M_writer('homepage/styles/login.css">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "/Users/spencerlowe/PycharmProjects/chef-master/inventory/templates/shoppingCart.html", "uri": "shoppingCart.html", "source_encoding": "ascii", "line_map": {"64": 40, "65": 41, "66": 42, "67": 44, "68": 44, "69": 47, "70": 47, "71": 50, "72": 50, "73": 54, "74": 54, "75": 58, "77": 58, "78": 60, "79": 66, "80": 66, "86": 11, "27": 0, "93": 11, "94": 12, "95": 12, "101": 95, "38": 7, "39": 9, "44": 13, "54": 15, "61": 15, "62": 40}}
__M_END_METADATA
"""
