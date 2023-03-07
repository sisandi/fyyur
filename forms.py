from datetime import datetime
from flask_wtf import Form
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
)
from wtforms.validators import DataRequired, AnyOf, URL, Regexp, Optional


class FyyurBaseForm(Form):
    """Set a filter on all fields that strips leading and trailing spaces. This helps reduce duplicate records.
    Source: https://stackoverflow.com/questions/26232165/automatically-strip-all-values-in-wtforms
    """

    class Meta:
        def bind_field(self, form, unbound_field, options):
            filters = unbound_field.kwargs.get("filters", [])
            filters.append(my_strip_filter)
            return unbound_field.bind(form=form, filters=filters, **options)


def my_strip_filter(value):
    if value is not None and hasattr(value, "strip"):
        return value.strip()
    return value


class ShowForm(FyyurBaseForm):
    artist_id = StringField("artist_id")
    venue_id = StringField("venue_id")
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.today()
    )


class VenueForm(FyyurBaseForm):
    name = StringField("name", validators=[DataRequired()])
    city = StringField(
        "city",
        validators=[
            DataRequired(),
            Regexp(
                "^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$", message="Please enter valid city name"
            ),
        ],
    )
    state = SelectField(
        "state",
        validators=[DataRequired()],
        choices=[
            ("AL", "AL"),
            ("AK", "AK"),
            ("AZ", "AZ"),
            ("AR", "AR"),
            ("CA", "CA"),
            ("CO", "CO"),
            ("CT", "CT"),
            ("DE", "DE"),
            ("DC", "DC"),
            ("FL", "FL"),
            ("GA", "GA"),
            ("HI", "HI"),
            ("ID", "ID"),
            ("IL", "IL"),
            ("IN", "IN"),
            ("IA", "IA"),
            ("KS", "KS"),
            ("KY", "KY"),
            ("LA", "LA"),
            ("ME", "ME"),
            ("MT", "MT"),
            ("NE", "NE"),
            ("NV", "NV"),
            ("NH", "NH"),
            ("NJ", "NJ"),
            ("NM", "NM"),
            ("NY", "NY"),
            ("NC", "NC"),
            ("ND", "ND"),
            ("OH", "OH"),
            ("OK", "OK"),
            ("OR", "OR"),
            ("MD", "MD"),
            ("MA", "MA"),
            ("MI", "MI"),
            ("MN", "MN"),
            ("MS", "MS"),
            ("MO", "MO"),
            ("PA", "PA"),
            ("RI", "RI"),
            ("SC", "SC"),
            ("SD", "SD"),
            ("TN", "TN"),
            ("TX", "TX"),
            ("UT", "UT"),
            ("VT", "VT"),
            ("VA", "VA"),
            ("WA", "WA"),
            ("WV", "WV"),
            ("WI", "WI"),
            ("WY", "WY"),
        ],
    )
    address = StringField("address", validators=[DataRequired()])
    phone = StringField(
        "phone",
        validators=[
            Regexp(
                "^\d{3}-\d{3}-\d{4}", message="Phone format needs to be ###-###-####"
            )
        ],
    )
    image_link = StringField("image_link", validators=[Optional(), URL()])
    genres = SelectMultipleField(
        "genres",
        validators=[DataRequired()],
        choices=[
            ("Alternative", "Alternative"),
            ("Blues", "Blues"),
            ("Classical", "Classical"),
            ("Country", "Country"),
            ("Electronic", "Electronic"),
            ("Folk", "Folk"),
            ("Funk", "Funk"),
            ("Hip-Hop", "Hip-Hop"),
            ("Heavy Metal", "Heavy Metal"),
            ("Instrumental", "Instrumental"),
            ("Jazz", "Jazz"),
            ("Musical Theatre", "Musical Theatre"),
            ("Pop", "Pop"),
            ("Punk", "Punk"),
            ("R&B", "R&B"),
            ("Reggae", "Reggae"),
            ("Rock n Roll", "Rock n Roll"),
            ("Soul", "Soul"),
            ("Other", "Other"),
        ],
    )

    facebook_link = StringField(
        "facebook_link",
        validators=[
            Optional(),
            URL(message="Invalid facebook URL"),
            Regexp(
                "(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?",
                message="Please enter valid facebook link format",
            ),
        ],
    )

    website_link = StringField(
        "website_link", validators=[Optional(), URL(message="Invalid website URL")]
    )

    seeking_talent = BooleanField("seeking_talent")

    seeking_description = StringField("seeking_description")


class ArtistForm(FyyurBaseForm):
    name = StringField("name", validators=[DataRequired()])
    city = StringField(
        "city",
        validators=[
            DataRequired(),
            Regexp(
                "^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$", message="Please enter valid city name"
            ),
        ],
    )
    state = SelectField(
        "state",
        validators=[DataRequired()],
        choices=[
            ("AL", "AL"),
            ("AK", "AK"),
            ("AZ", "AZ"),
            ("AR", "AR"),
            ("CA", "CA"),
            ("CO", "CO"),
            ("CT", "CT"),
            ("DE", "DE"),
            ("DC", "DC"),
            ("FL", "FL"),
            ("GA", "GA"),
            ("HI", "HI"),
            ("ID", "ID"),
            ("IL", "IL"),
            ("IN", "IN"),
            ("IA", "IA"),
            ("KS", "KS"),
            ("KY", "KY"),
            ("LA", "LA"),
            ("ME", "ME"),
            ("MT", "MT"),
            ("NE", "NE"),
            ("NV", "NV"),
            ("NH", "NH"),
            ("NJ", "NJ"),
            ("NM", "NM"),
            ("NY", "NY"),
            ("NC", "NC"),
            ("ND", "ND"),
            ("OH", "OH"),
            ("OK", "OK"),
            ("OR", "OR"),
            ("MD", "MD"),
            ("MA", "MA"),
            ("MI", "MI"),
            ("MN", "MN"),
            ("MS", "MS"),
            ("MO", "MO"),
            ("PA", "PA"),
            ("RI", "RI"),
            ("SC", "SC"),
            ("SD", "SD"),
            ("TN", "TN"),
            ("TX", "TX"),
            ("UT", "UT"),
            ("VT", "VT"),
            ("VA", "VA"),
            ("WA", "WA"),
            ("WV", "WV"),
            ("WI", "WI"),
            ("WY", "WY"),
        ],
    )
    phone = StringField(
        "phone",
        validators=[
            Regexp(
                "^\d{3}-\d{3}-\d{4}", message="Phone format needs to be ###-###-####"
            )
        ],
    )
    image_link = StringField("image_link", validators=[Optional(), URL()])
    genres = SelectMultipleField(
        "genres",
        validators=[DataRequired()],
        choices=[
            ("Alternative", "Alternative"),
            ("Blues", "Blues"),
            ("Classical", "Classical"),
            ("Country", "Country"),
            ("Electronic", "Electronic"),
            ("Folk", "Folk"),
            ("Funk", "Funk"),
            ("Hip-Hop", "Hip-Hop"),
            ("Heavy Metal", "Heavy Metal"),
            ("Instrumental", "Instrumental"),
            ("Jazz", "Jazz"),
            ("Musical Theatre", "Musical Theatre"),
            ("Pop", "Pop"),
            ("Punk", "Punk"),
            ("R&B", "R&B"),
            ("Reggae", "Reggae"),
            ("Rock n Roll", "Rock n Roll"),
            ("Soul", "Soul"),
            ("Other", "Other"),
        ],
    )

    facebook_link = StringField(
        "facebook_link",
        validators=[
            Optional(),
            URL(message="Invalid facebook URL"),
            Regexp(
                "(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?",
                message="Please enter valid facebook link format",
            ),
        ],
    )

    website_link = StringField(
        "website_link", validators=[Optional(), URL(message="Invalid website URL")]
    )

    seeking_venue = BooleanField("seeking_venue")

    seeking_description = StringField("seeking_description")
