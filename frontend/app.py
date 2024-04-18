from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database models


class Band(db.Model):
    __tablename__ = 'band'
    band_id = db.Column(db.Integer, primary_key=True)
    band_name = db.Column(db.String, nullable=False)
    urls = db.relationship('BandURL', backref='band', lazy=True)


class BandURL(db.Model):
    __tablename__ = 'band_url'
    url_id = db.Column(db.Integer, primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey(
        'band.band_id'), nullable=False)
    url = db.Column(db.String, nullable=False)
    class_name = db.Column(db.String)
    hash_value = db.Column(db.String)
    date_added = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime)
    last_failed = db.Column(db.DateTime)

# API Routes


@app.route('/api/bands', methods=['GET', 'POST'])
def handle_bands():
    if request.method == 'POST':
        data = request.json
        new_band = Band(band_name=data['band_name'])
        db.session.add(new_band)
        db.session.commit()
        return jsonify({'band_id': new_band.band_id, 'band_name': new_band.band_name}), 201
    bands = Band.query.all()
    return jsonify([{ 
        'band_id': band.band_id, 
        'band_name': band.band_name,
        'urls': [{
            'url_id': url.url_id,
            'url': url.url,
            'class_name': url.class_name,
            'last_updated': url.last_updated.isoformat() if url.last_updated else None,
            'last_failed': url.last_failed.isoformat() if url.last_failed else None
        } for url in band.urls]
    } for band in bands])


@app.route('/api/bands/<int:band_id>', methods=['PUT', 'DELETE'])
def update_delete_band(band_id):
    band = Band.query.get_or_404(band_id)
    if request.method == 'PUT':
        data = request.json
        band.band_name = data.get('band_name', band.band_name)  # Update band name if provided
        db.session.commit()
        return jsonify({'band_id': band.band_id, 'band_name': band.band_name}), 200
    elif request.method == 'DELETE':
        db.session.delete(band)
        db.session.commit()
        return '', 204  # No content to signify successful deletion



@app.route('/api/urls', methods=['POST'])
def add_url():
    data = request.json
    band_id = data.get('band_id')
    url = data.get('url')
    # Default to None if not provided
    class_name = data.get('class_name', None)

    # Check if class_name is an empty string and convert it to None
    if not class_name:
        class_name = None

    new_url = BandURL(
        band_id=band_id,
        url=url,
        class_name=class_name
    )
    db.session.add(new_url)
    db.session.commit()
    return jsonify(new_url.url_id), 201


@app.route('/api/urls/<int:url_id>', methods=['PUT', 'DELETE'])
def update_delete_url(url_id):
    url = BandURL.query.get_or_404(url_id)
    if request.method == 'PUT':
        data = request.json
        url.url = data.get('url', url.url)
        url.class_name = data.get('class_name', url.class_name)  # Update class_name if provided, allow None
        db.session.commit()
        return jsonify({'url_id': url.url_id, 'url': url.url, 'class_name': url.class_name}), 200
    elif request.method == 'DELETE':
        db.session.delete(url)
        db.session.commit()
        return '', 204  # No content to signify successful deletion


# Main page route


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
