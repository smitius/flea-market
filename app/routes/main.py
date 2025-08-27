from flask import Blueprint, render_template
from app.models import Item

main = Blueprint('main', __name__)

@main.route('/')
def index():
    items = Item.query.order_by(Item.created_at.desc()).all()
    return render_template('index.html', items=items)
