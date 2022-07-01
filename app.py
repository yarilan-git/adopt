
from forms import Add_pet
from flask  import Flask, render_template, request, flash, jsonify, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet, Specie


app = Flask(__name__)

app.config['SECRET_KEY'] = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def show_pets():
    """ Show all pets in the database """

    pets = Pet.get_all_pets()
    return render_template('pet_list.html', title='Pet list', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def show_add_pet_form():
    """ If reached via a GET mothod, shows a form that allows the user to add 
        a new pet. If reached via a POST method, validates the data provided
        by the user. If the validation passes, adds the pet to the database.
        Otherwise, re-renders the form with error messages."""

    pet_form=Add_pet()
    pet_form.species.choices=[(specie.id, specie.name) for specie in Specie.query.all()]  
    if pet_form.validate_on_submit():
        pet=Pet(name=pet_form.name.data,
                specie_id=pet_form.species.data,
                photo_url=pet_form.photo.data,
                age=pet_form.age.data,
                notes=pet_form.notes.data,
                available=pet_form.available.data
                )   
        db.session.add(pet)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('pet_form.html', title='Add a pet', pet_form=pet_form)

@app.route('/<int:id>', methods=['GET', 'POST'])
def pet_info(id):
    """ Show a pet's information """
    pet=Pet.get_pet_info(id)
    return render_template('pet_info.html', title='Pet info', pet=pet)

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_pet_info(id):
    """ If reached via a GET mothod, shows a form that allows the user to edit 
        a pet's information. If reached via a POST method, validates the data provided by the user. If the validation passes, updates the pet's data in the database.Otherwise, re-renders the form with error messages."""

    pet=Pet.get_pet_info(id)
    pet_form=Add_pet(obj=pet)
    pet_form.species.choices=Specie.bring_selected_to_top(pet.specie_id)  
    if pet_form.validate_on_submit():
        pet.name=pet_form.name.data
        pet.specie_id=pet_form.species.data
        pet.photo_url=pet_form.photo.data
        pet.age=pet_form.age.data
        pet.notes=pet_form.notes.data
        pet.available=pet_form.available.data
        db.session.add(pet)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit_pet_form.html', title='Edit pet details', pet_form=pet_form, pet=pet)








    





    


