# -*- coding: utf-8 -*-
# from odoo import http


# class TextToSpeech(http.Controller):
#     @http.route('/text_to_speech/text_to_speech', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/text_to_speech/text_to_speech/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('text_to_speech.listing', {
#             'root': '/text_to_speech/text_to_speech',
#             'objects': http.request.env['text_to_speech.text_to_speech'].search([]),
#         })

#     @http.route('/text_to_speech/text_to_speech/objects/<model("text_to_speech.text_to_speech"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('text_to_speech.object', {
#             'object': obj
#         })

