from flask import Blueprint, render_template
from app.models import Item
from flask import current_app as app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    items = Item.query.order_by(Item.created_at.desc()).all()
    return render_template(
        'index.html', 
        items=items,
        site_name=app.config.get('SITE_NAME', 'Personal Flea Market'),
        whatsapp_number=app.config.get('WHATSAPP_NUMBER', ''),
        apartment_address=app.config.get('APARTMENT_ADDRESS', '')
    )