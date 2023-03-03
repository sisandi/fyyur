from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from app import db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# Association table - composite primary key
show = db.Table('Show',
  db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
  db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
  db.Column('start_time', db.DateTime, primary_key=True)
)

class Venue(db.Model):
  __tablename__ = 'Venue'

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
  shows = db.relationship(
    'Artist',
    secondary=show,
    backref='Venue',
    lazy=True,
    cascade = 'save-update' #keep past shows data
  )

class Artist(db.Model):
  __tablename__ = 'Artist'

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
  shows = db.relationship(
    'Venue',
    secondary=show,
    backref='Artist',
    lazy=True,
    cascade = 'save-update'
  )
