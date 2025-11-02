from odoo import models, fields

class TextToSpeech(models.Model):
	_name = "text.to.speech"
	_description = "Text to Speech Demo"

	name = fields.Char("Text")
	def action_speak(self):
		# Dummy method just to avoid XML validation error
		# You won’t actually use this in backend
		return True
