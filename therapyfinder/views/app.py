"""
Therapistfinder - therapistfinder/views/app.py

Author/s: olel
Therapistfinder (thus this code) is public domain.
"""

from datetime import time
from therapyfinder.const.therapist import RESULT_TEXTS
from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import request

from datetime import datetime
from therapyfinder.models import therapist

from therapyfinder.util.user import requires_login
from therapyfinder.models.therapist import LogEntry, Therapist, Timeslot

from therapyfinder.const.time import weekdays_strings
from therapyfinder.util.time import filter_current_timeslots

# Create blueprint
app = Blueprint("app", "therapyfinder.views.app")


@app.route("/")
@requires_login
def index(user=None, user_error=None):
    return render_template("app/index.html")

@app.route("/call")
@requires_login
def call(user=None, user_error=None):
    now = datetime.now()
    timeslots = list(Timeslot.select().where(Timeslot.weekday == now.weekday()))
    timeslots = filter_current_timeslots(now.hour, now.minute, timeslots)
    result = []
    for slot in timeslots:
        if slot.therapist.enabled and slot.therapist.user == user:
            result.append(slot)
        

    return render_template("app/call.html", timeslots=result)

@app.route("/call/therapist/<int:therapist>")
@requires_login
def call_therapist(therapist=None, user=None, user_error=None):
    therapist_model = Therapist.get_or_none(Therapist.id == therapist)
    if therapist_model is None:
        flash("Invalid request")
        return redirect(url_for("app.call"))
    if therapist_model.user == user:
        return render_template("app/call_therapist.html", therapist=therapist_model)
    else:
        flash("You're not allowed to see this page", "danger")
        return redirect(url_for("index.index"))

@app.route("/therapists")
@requires_login
def therapists(user=None, user_error=None):
    therapists = Therapist.select().where(Therapist.user == user)
    return render_template("app/therapists.html", therapists=therapists)

@app.route("/therapists/editor/<int:new>", methods=["GET", "POST"])
@app.route("/therapists/editor/<int:new>/<int:therapist>", methods=["GET", "POST"])
@requires_login
def therapist_editor(new=True, therapist=None, user=None, user_error=None):
    if not new and therapist is None:
        flash("Invalid request")
        return redirect(url_for("app.index"))

    therapist_model = None
    if not new:
        therapist_model = Therapist.get_or_none(Therapist.user == user and Therapist.id == therapist)
        if therapist_model is None:
            flash("Invalid request")
            return redirect(url_for("app.index"))
        if therapist_model.user != user:
            flash("You're not allowed to see this page", "danger")
            return redirect(url_for("index.index"))


    if request.method == "GET":
        timeslots = None
        if not new:
            timeslots = Timeslot.select().where(Timeslot.therapist == therapist_model).order_by(Timeslot.weekday)
        return render_template("app/therapist_editor.html", therapist=therapist_model, new=new, timeslots=timeslots, weekdays=weekdays_strings)
    else:
        custom_id = request.form.get("custom_id", None)
        if custom_id is None:
            flash("Invalid form data")
            return redirect(url_for("app.therapist_editor", new=new, therapist=therapist))
        title = request.form.get("title", None)
        if title is None:
            flash("Invalid form data")
            return redirect(url_for("app.therapist_editor", new=new, therapist=therapist))
        name = request.form.get("name", None)
        if name is None:
            flash("Invalid form data")
            return redirect(url_for("app.therapist_editor", new=new, therapist=therapist))
        plz = request.form.get("plz", None)
        if plz is None:
            flash("Invalid form data")
            return redirect(url_for("app.therapist_editor", new=new, therapist=therapist))
        city = request.form.get("city", None)
        if city is None:
            flash("Invalid form data")
            return redirect(url_for("app.therapist_editor", new=new, therapist=therapist))
        street = request.form.get("street", None)
        if street is None:
            flash("Invalid form data")
            return redirect(url_for("app.therapist_editor", new=new, therapist=therapist))
        phone = request.form.get("phone", None)
        if phone is None:
            flash("Invalid form data")
            return redirect(url_for("app.therapist_editor", new=new, therapist=therapist))
        mobile = request.form.get("mobile", None)
        specialism = request.form.get("specialism", None)
        if specialism is None:
            flash("Invalid form data")
            return redirect(url_for("app.therapist_editor", new=new, therapist=therapist))
        comment = request.form.get("comment", "")
        enabled = request.form.get("enabled", None)
        if enabled is None: enabled = False
        else: enabled = True
        
        if new:
            therapist_model = Therapist(
                user = user,
                custom_id = custom_id,
                title = title,
                name = name,
                plz = plz,
                city = city,
                street = street,
                phone = phone,
                mobile = mobile,
                specialism = specialism,
                enabled = enabled,
                comment = comment
            )
            therapist_model.save()
        else:
            therapist_model.custom_id = custom_id
            therapist_model.title = title
            therapist_model.name = name
            therapist_model.plz = plz
            therapist_model.city = city
            therapist_model.street = street
            therapist_model.phone = phone
            therapist_model.mobile = mobile
            therapist_model.specialism = specialism
            therapist_model.enabled = enabled
            therapist_model.comment = comment
            
            therapist_model.save()

        return redirect(url_for("app.therapist_editor", new=0, therapist=therapist_model.id))

@app.route("/therapists/delete/<int:therapist>")
@requires_login
def delete_therapist(therapist=None, user=None, user_error=None):
    therapist_model = Therapist.get_or_none(Therapist.id == therapist)

    if therapist_model.user != user:
        flash("You're not allowed to see this page", "danger")
        return redirect(url_for("index.index"))

    for timeslot in Timeslot.select().where(Timeslot.therapist == therapist_model):
        timeslot.delete_instance()
    if therapist_model:
        therapist_model.delete_instance()
    return redirect(url_for("app.therapists"))

@app.route("/therapists/add_timeslot/<int:therapist>", methods=["POST"])
@requires_login
def therapist_add_timeslot(therapist=None, user=None, user_error=None):
    therapist_model = Therapist.get_or_none(Therapist.user == user and Therapist.id == therapist)
    if therapist_model is None:
        flash("Invalid request (no such therapist)")
        return redirect(url_for("app.therapist_editor", new=0, therapist=therapist))

    if therapist_model.user != user:
        flash("You're not allowed to see this page", "danger")
        return redirect(url_for("index.index"))
    
    day = request.form.get("day", None)
    if day is None:
        flash("Invalid request")
        return redirect(url_for("app.therapist_editor", new=0, therapist=therapist))
    
    start_hour = request.form.get("start_hour", None)
    if start_hour is None:
        flash("Invalid request")
        return redirect(url_for("app.therapist_editor", new=0, therapist=therapist))

    start_minute = request.form.get("start_minute", None)
    if start_minute is None:
        flash("Invalid request")
        return redirect(url_for("app.therapist_editor", new=0, therapist=therapist))

    end_hour = request.form.get("end_hour", None)
    if end_hour is None:
        flash("Invalid request")
        return redirect(url_for("app.therapist_editor", new=0, therapist=therapist))

    end_minute = request.form.get("end_minute", None)
    if end_minute is None:
        flash("Invalid request")
        return redirect(url_for("app.therapist_editor", new=0, therapist=therapist))
    
    timeslot = Timeslot(weekday = day,
        start_hour = start_hour,
        start_minute = start_minute, 
        end_hour = end_hour,
        end_minute = end_minute,
        therapist = therapist_model)
    timeslot.save()

    return redirect(url_for("app.therapist_editor", new=0, therapist=therapist))
    
@app.route("/remove_timeslot/<int:timeslot>")
@requires_login
def remove_timeslot(timeslot=None, user=None, user_error=None):
    timeslot_model = Timeslot.get_or_none(Timeslot.id == timeslot)
    
    if timeslot_model.therapist.user != user:
        flash("You're not allowed to see this page", "danger")
        return redirect(url_for("index.index"))

    therapist = timeslot_model.therapist.id
    timeslot_model.delete_instance()
    return redirect(url_for('app.therapist_editor', new=0, therapist=therapist))

@app.route("/settings")
@requires_login
def settings(user=None, user_error=None):
    return render_template("app/settings.html")

@app.route("/log/add/<after>", methods=["POST"])
@requires_login
def log_add(after=None, user=None, user_error=None):
    if after is None: after = "index.index"

    result = request.form.get("result", None)
    if result is None:
        flash("Invalid request")
        return redirect(url_for(after))
    result = int(result)

    comment = request.form.get("comment", None)
    if comment is None:
        comment = ""
    
    therapist_id = request.form.get("therapist", None)
    if therapist_id is None:
        flash("Invalid request")
        return redirect(url_for(after))

    therapist = Therapist.get_or_none(Therapist.id == therapist_id)
    if therapist is None:
        flash("Invalid request")
        return redirect(url_for(after))

    if therapist.user != user:
        flash("You're not allowed to see this page", "danger")
        return redirect(url_for("index.index"))

    entry = LogEntry(
        therapist = therapist,
        user = user,
        result = result,
        comment = comment
    )

    entry.save()

    return redirect(url_for(after))

@app.route("/log")
@requires_login
def log(user=None, user_error=None):
    entries = LogEntry.select().where(LogEntry.user == user).order_by(LogEntry.time.desc())
    return render_template("app/log.html", entries=entries, result_texts=RESULT_TEXTS)

@app.route("/timegrid")
@requires_login
def timegrid(user=None, user_error=None):

    timeslots = []
    for i in range(7, 18): # 7 - 18 Uhr
        for j in range(0, 2):
            start_hour = i
            start_minute = 30 * j

            if start_minute == 30:
                end_hour = start_hour + 1
                end_minute = 0
            else:
                end_hour = start_hour
                end_minute = 30

            timeslots.append({
                "time": "%02d:%02d - %02d:%02d" % (start_hour, start_minute, end_hour, end_minute),
                "days": []
            })

            for d in range(0, 7): # days
                slot_models = Timeslot.select().where(
                    Timeslot.weekday == d
                )
                day = []
                start_time = (100 * start_hour + start_minute)
                end_time = (100 * end_hour + end_minute)
                for slot in slot_models:
                    slot_start = (100 * slot.start_hour + slot.start_minute)
                    slot_end = (100 * slot.end_hour + slot.end_minute)

                    if not slot_end <= start_time and not slot_start >= end_time:
                        if slot.therapist.enabled and slot.therapist.user == user:
                            day.append(slot.therapist)

                timeslots[-1]["days"].append(day)

    return render_template("app/timegrid.html", timeslots=timeslots)