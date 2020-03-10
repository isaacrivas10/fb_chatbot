
from flask import Blueprint, render_template
from flask_login import current_user

main= Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated:
        return render_template('index.html', show=True, isauth=True)    
    return render_template('soon.html')

"""
@main.route("/privacy_policy", methods=['GET'])
def privacy_policy():
    return render_template('privacy_policy.html', title='Privacy Policy')
"""

@main.route('/<path:page>')
def anypage(page):
    return render_template('soon.html')