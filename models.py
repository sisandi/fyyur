from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import datetime

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = "Venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(300))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(300))
    shows = db.relationship("Show", backref=db.backref("Venue", lazy=True))

    def __repr__(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "state": self.state,
            "address": self.address,
            "phone": self.phone,
            "image_link": self.image_link,
            "genres": [i.strip() for i in self.genres.split(',')],
            "facebook_link": self.facebook_link,
            "website": self.website,
            "seeking_talent": self.seeking_talent,
            "seeking_description": self.seeking_description,
        }


class Artist(db.Model):
    __tablename__ = "Artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(300))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(300))
    shows = db.relationship("Show", backref=db.backref("Artist", lazy=True))

    def __repr__(self):
        return f"<Artist ID: {self.id}, name: {self.name}>"


# Composite primary key
class Show(db.Model):
    __tablename__ = "Show"

    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), primary_key=True)
    start_time = db.Column(db.DateTime, primary_key=True)

    def __repr__(self):
        return {
            "artist_id": self.artist_id,
            "venue_id": self.venue_id,
            "start_time": datetime.strftime(self.start_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        }
