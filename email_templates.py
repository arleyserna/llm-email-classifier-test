# email_templates.py

# Templates for automated responses by category

complaint_response_template = """\
Hello,

We’re truly sorry to hear about your experience. We take such issues seriously and appreciate you bringing it to our attention.

Our team is already looking into this and will follow up shortly to resolve the situation. If you have any additional information or photos, please reply to this message.

Sincerely,  
Customer Support Team
"""

inquiry_response_template = """\
Hi,

Thank you for reaching out! We appreciate your interest and are happy to assist.

Regarding your question: [Insert dynamic answer if needed].  
If you have more questions or need further clarification, feel free to reply.

Best regards,  
Customer Experience Team
"""

feedback_response_template = """\
Hello,

Thank you for your kind words and for taking the time to share your feedback. We’re thrilled to hear that you had a positive experience!

Your message has been shared with our team.

Warm regards,  
Customer Support Team
"""

support_request_response_template = """\
Hi,

Thanks for reaching out. We’re sorry you’re facing technical issues.

Our team has received your support request and is reviewing the problem. We’ll get back to you as soon as we have an update. Meanwhile, you can also check our Help Center for common solutions.

Best,  
Tech Support Team
"""

other_response_template = """\
Hello,

Thanks for getting in touch. Your message has been received and forwarded to the appropriate team.

We’ll follow up shortly.

Sincerely,  
Customer Care
"""

# Optional dictionary if you want centralized access
response_templates = {
    "complaint": complaint_response_template,
    "inquiry": inquiry_response_template,
    "feedback": feedback_response_template,
    "support_request": support_request_response_template,
    "other": other_response_template
}