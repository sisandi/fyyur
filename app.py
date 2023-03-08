# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import logging
from logging import FileHandler, Formatter
from datetime import datetime

import babel
import dateutil.parser
from flask import Flask, Response, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from forms import *
from collections import defaultdict

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale="en")


app.jinja_env.filters["datetime"] = format_datetime

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#
from models import *

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("pages/home.html")


#  Venues
#  ----------------------------------------------------------------


@app.route("/venues")
def venues():
    group = defaultdict(list)
    data = []

    vens = Venue.query.order_by(Venue.state).all()
    for venue in vens:
        v = {
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": Show.query.filter(
                Show.venue_id == venue.id, Show.start_time > datetime.now()
            ).count(),
            "genres": venue.genres,
        }

        group[f"{venue.city},{venue.state}"].append(v)

    for city_state in group.keys():
        data.append(
            {
                "city": city_state.split(",")[0],
                "state": city_state.split(",")[1],
                "venues": group[city_state],
            }
        )

    return render_template("pages/venues.html", areas=data)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    response = {
        "count": 1,
        "data": [
            {
                "id": 2,
                "name": "The Dueling Pianos Bar",
                "num_upcoming_shows": 0,
            }
        ],
    }
    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    """Shows the venue page with the given venue_id"""
    
    venue = Venue.query.get(venue_id)
    shows = (
        db.session.query(
            Show.start_time.label("start_time"),
            Show.venue_id.label("venue_id"),
            Artist.id.label("artist_id"),
            Artist.name.label("artist_name"),
            Artist.image_link.label("artist_image"),
        )
        .join(Artist, Artist.id == Show.artist_id)
        
    )        

    data = venue.__repr__()
    data["past_shows"] = []
    data["upcoming_shows"] = []
    
    for show in shows:
        if show.venue_id == venue_id:
            
            show_data = {
                    "artist_id": show.artist_id,
                    "artist_name": show.artist_name,
                    "artist_image_link": show.artist_image,
                    "start_time": datetime.strftime(show.start_time, "%Y-%m-%dT%H:%M:%S.%fZ"),
            }
            
            if show.start_time >= datetime.now():
                data["upcoming_shows"].append(show_data)
            else:
                data["past_shows"].append(show_data)
    
    return render_template("pages/show_venue.html", venue=data)


#  Create Venue
#  ----------------------------------------------------------------


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    """Venue data add with address data all standardized to be uppercase"""

    form = VenueForm(request.form)

    if form.validate():
        if (
            Venue.query.filter(
                Venue.name == form.name.data,
                Venue.address == form.address.data.upper(),
                Venue.city == form.city.data.upper(),
                Venue.state == form.state.data,
            ).count()
            > 0
        ):
            flash(
                "Looks like this venue already exists. To edit venue information, see the venue's details page and click the 'edit' button"
            )
            return render_template("forms/new_venue.html", form=form)

        try:
            venue = Venue(
                name=form.name.data,
                city=form.city.data.upper(),
                state=form.state.data,
                address=form.address.data.upper(),
                phone=form.phone.data,
                image_link=form.image_link.data,
                genres=",".join(form.genres.data),
                facebook_link=form.facebook_link.data,
                website=form.website_link.data,
                seeking_talent=form.seeking_talent.data,
                seeking_description=form.seeking_description.data,
            )

            db.session.add(venue)
            db.session.commit()

            flash("Venue " + request.form["name"] + " was successfully listed!")
            return render_template("pages/home.html")

        except ValueError as e:
            flash(
                "An error occurred. Venue "
                + request.form["name"]
                + " could not be listed. Please try again."
            )
            db.session.rollback()
            return render_template("forms/new_venue.html", form=form)

        finally:
            db.session.close()

    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash("An error occurred. " + err)
                return render_template("forms/new_venue.html", form=form)

    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


#  Artists
#  ----------------------------------------------------------------
@app.route("/artists")
def artists():
    data = []

    artists = Artist.query.order_by(Artist.name).all()
    for artist in artists:
        data.append({"id": artist.id, "name": artist.name})

    return render_template("pages/artists.html", artists=data)


@app.route("/artists/search", methods=["POST"])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [
            {
                "id": 4,
                "name": "Guns N Petals",
                "num_upcoming_shows": 0,
            }
        ],
    }
    return render_template(
        "pages/search_artists.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    """Shows the artist page with the given artist_id"""

    artist = Artist.query.get(artist_id)
    shows = (
        db.session.query(
            Show.start_time.label("start_time"),
            Show.artist_id.label("artist_id"),
            Venue.id.label("venue_id"),
            Venue.name.label("venue_name"),
            Venue.image_link.label("venue_image"),
        )
        .join(Venue, Venue.id == Show.venue_id)
    )
            
    data = artist.__repr__()
    data["past_shows"] = []
    data["upcoming_shows"] = []
    
    for show in shows:
        if show.artist_id == artist_id:
            
            show_data = {
                    "venue_id": show.venue_id,
                    "venue_name": show.venue_name,
                    "venue_image_link": show.venue_image,
                    "start_time": datetime.strftime(show.start_time, "%Y-%m-%dT%H:%M:%S.%fZ"),
            }
            
            if show.start_time >= datetime.now():
                data["upcoming_shows"].append(show_data)
            else:
                data["past_shows"].append(show_data)
    
    return render_template("pages/show_artist.html", artist=data)    


#  Create Artist
#  ----------------------------------------------------------------


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    """Artist data add with address data all standardized to be upper case"""

    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Artist record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    form = ArtistForm(request.form)

    if form.validate():
        if (
            Artist.query.filter(
                Artist.name == form.name.data,
                Artist.phone == form.phone.data,
                Artist.city == form.city.data.upper(),
                Artist.state == form.state.data,
            ).count()
            > 0
        ):
            flash(
                "Looks like this artist already exists. To edit artist information, see the artist's details page and click the 'edit' button"
            )
            return render_template("forms/new_artist.html", form=form)

        try:
            artist = Artist(
                name=form.name.data,
                city=form.city.data.upper(),
                state=form.state.data,
                phone=form.phone.data,
                image_link=form.image_link.data,
                genres=",".join(form.genres.data),
                facebook_link=form.facebook_link.data,
                website=form.website_link.data,
                seeking_venue=form.seeking_venue.data,
                seeking_description=form.seeking_description.data,
            )

            db.session.add(artist)
            db.session.commit()

            flash("Artist " + request.form["name"] + " was successfully listed!")
            return render_template("pages/home.html")

        except ValueError as e:
            flash(
                "An error occurred. Artist "
                + request.form["name"]
                + " could not be listed. Please try again."
            )
            db.session.rollback()
            return render_template("forms/new_artist.html", form=form)

        finally:
            db.session.close()

    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash("An error occurred. " + err)
                return render_template("forms/new_artist.html", form=form)

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')


#  Update
#  ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template("forms/edit_artist.html", form=form, artist=artist)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for("show_artist", artist_id=artist_id))


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template("forms/edit_venue.html", form=form, venue=venue)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for("show_venue", venue_id=venue_id))


#  Shows
#  ----------------------------------------------------------------


@app.route("/shows")
def shows():
    data = []

    shows = (
        db.session.query(
            Show.start_time,
            Venue.id.label("venue_id"),
            Venue.name.label("venue_name"),
            Artist.id.label("artist_id"),
            Artist.name.label("artist_name"),
            Artist.image_link.label("artist_image"),
        )
        .join(Venue, Venue.id == Show.venue_id)
        .join(Artist, Artist.id == Show.artist_id).order_by(Show.start_time)
    )

    for show in shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue_name,
            "artist_id": Show.artist_id,
            "artist_name": show.artist_name,
            "artist_image_link": show.artist_image,
            "start_time": datetime.strftime(show.start_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        })

    return render_template("pages/shows.html", shows=data)


@app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    form = ShowForm(request.form)

    if form.validate():
        
        if (
            Show.query.filter(
                Show.artist_id == form.artist_id.data,
                Show.venue_id == form.venue_id.data,
                Show.start_time == form.start_time.data,
            ).count()
            > 0
        ):
            flash(
                "Looks like this show's already in the books! To edit show information, see the show's details page and click the 'edit' button"
            )
            return render_template("forms/new_show.html", form=form)

        try:
            show = Show(
                artist_id=form.artist_id.data,
                venue_id=form.venue_id.data.upper(),
                start_time=form.start_time.data
            )

            db.session.add(show)
            db.session.commit()

            flash("Show was successfully listed!")
            return render_template("pages/home.html")

        except ValueError as e:
            flash(
                "An error occurred. Your show could not be listed at this time. Please try again."
            )
            db.session.rollback()
            return render_template("forms/new_show.html", form=form)

        finally:
            db.session.close()

    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash("An error occurred. " + err)
                return render_template("forms/new_show.html", form=form)

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
