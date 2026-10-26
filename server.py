import json
import os
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for,session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def loadClubs():
    path = os.path.join(BASE_DIR, 'clubs.json')
    with open(path) as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    path = os.path.join(BASE_DIR, 'competitions.json')
    with open(path) as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['GET','POST'])
def showSummary():
    if request.method == 'POST':
        email = request.form.get('email')
        matching_clubs = [club for club in clubs if club['email'] == email]
        if not matching_clubs:
            flash("Sorry, that email was not found.")
            return redirect(url_for('index'))
        club = matching_clubs[0]
        session['email'] = club['email']
        return render_template('welcome.html',club=club,competitions=competitions)

    email = session.get('email')
    if not email:
        flash("Please log in to access this page.")
        return redirect(url_for('index'))
    matching_clubs = [club for club in clubs if club['email'] == email]
    if not matching_clubs:
        flash("Sorry, that email was not found.")
        return redirect(url_for('index'))
    club = matching_clubs[0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClubs = [c for c in clubs if c['name'] == club]
    foundCompetitions = [c for c in competitions if c['name'] == competition]
    if not foundClubs or not foundCompetitions:
        flash("Something went wrong-please try again")
        return redirect(url_for('index'))
    foundClub = foundClubs[0]
    foundCompetition = foundCompetitions[0]
    if datetime.strptime(foundCompetition['date'], "%Y-%m-%d %H:%M:%S") < datetime.now():
        flash("This competition is already over.")
        return render_template('welcome.html', club=foundClub, competitions=competitions)
    return render_template('booking.html',club=foundClub,competition=foundCompetition)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    foundCompetitions = [c for c in competitions if c['name'] == request.form.get('competition')]
    foundClubs = [c for c in clubs if c['name'] == request.form.get('club')]
    if not foundCompetitions or not foundClubs:
        flash("Something went wrong-please try again")
        return redirect(url_for('index'))
    competition = foundCompetitions[0]
    club = foundClubs[0]
    if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") < datetime.now():
        flash("Cannot book places for a past competition.")
        return render_template('welcome.html', club=club, competitions=competitions)
    try:
        placesRequired = int(request.form.get('places', ''))
    except (ValueError, TypeError):
        flash("Invalid number of places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    if placesRequired <= 0:
        flash("Number of places must be at least 1.")
        return render_template('welcome.html', club=club, competitions=competitions)
    if placesRequired > 12:
        flash("You cannot book more than 12 places per competition.")
        return render_template('welcome.html', club=club, competitions=competitions)
    if placesRequired > int(competition['numberOfPlaces']):
        flash("You cannot book more places than available in the competition.")
        return render_template('welcome.html', club=club, competitions=competitions)
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club['points'] = int(club['points']) - placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/points')
def points():
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))