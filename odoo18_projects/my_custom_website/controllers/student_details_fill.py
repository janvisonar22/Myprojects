from odoo import http
from odoo.http import request

class StudentWebsite(http.Controller):

	# Show Form Page
	@http.route('/student/profile', type='http', auth="user", website=True)
	def student_profile_form(self, **kw):
		return request.render("my_custom_website.student_profile_form", {})

	# Handle Form Submission
	@http.route('/student/profile/submit', type='http', auth="user", website=True, csrf=True, methods=['POST'])
	def student_form_submit(self, **post):
		# extract fields from post
		name = post.get('name')
		roll_number = post.get('roll_number')
		class_name = post.get('class_name')
		dob = post.get('dob')
		gender = post.get('gender')
		email = post.get('email')
		phone = post.get('phone')
		address = post.get('address')

		# save into custom model
		request.env['student.profile'].sudo().create({
			'name': name,
			'roll_number': roll_number,
			'class_name': class_name,
			'dob': dob,
			'gender': gender,
			'email': email,
			'phone': phone,
			'address': address,
		})

		# return thank you page
		return request.render("my_custom_website.student_profile_thanks", {'name': name})
