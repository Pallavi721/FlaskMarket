from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

# it's a decorator which tells the application which URL should call the associated function. 
# means when you open the url inside route the following function will be called
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
@app.route('/home')
def home_page():
    return render_template('home.html')

# displays registered users
@app.route('/users')
def all_users():
    users = User.query.all()
    return '<br>'.join([f'{user.id} - {user.username} - {user.email_address}' for user in users])


@app.route('/market', methods=['GET','POST'])
@login_required
def market_page() :
    purchase_form = PurchaseItemForm()
    
    '''if purchase_form.validate_on_submit():
        # 'request' stores all the data that is sent by client to the server.
        print(request.form.get('purchased_item'))   '''
    
    selling_form = SellItemForm()

    if request.method == 'POST':
        # purchased item logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object :
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f'Congratulations! You purchased {p_item_object.name} for {p_item_object}', category='success')
            else:
                flash(f'Unfortunately you dont have enough money to purchase {p_item_object.name}', category='danger')
        
        # selling item logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f'Congratulations! You sold {s_item_object.name} back to market!', category='success')
            else:
                flash(f'Something went wrong with selling {s_item_object.name}', category='danger')
        
        return redirect(url_for('market_page'))
    
    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner = current_user.id)
        return render_template('market.html', item_name = items, purchase_form = purchase_form, owned_items = owned_items, selling_form = selling_form)
        '''items = [
        {'id' : 1, 'name' : 'pallavi', 'barcode' : 225267281053, 'price' : '500$'},
        {'id' : 2,'name' : 'pragathi', 'barcode' : 299121098545, 'price' : '250$'},
        {'id' : 3,'name' : 'kowshik', 'barcode' : 109876513548, 'price' : '380$'}
        ]'''

@app.route('/register', methods=['GET','POST'])
def register_page() :
    # create an object
    form = RegisterForm()
    if form.validate_on_submit():
        # Link to Model: The form fields → model fields mapping happens when you do this
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        #Flask-Login library; It tells Flask-Login: “This is the user who just authenticated successfully, now treat them as logged in.”
        login_user(user_to_create)
        flash(f'Account created successfully!! You are now logged in as {user_to_create.username}', category='success')
        return redirect(url_for('market_page'))
    
    if form.errors:  # If there are any validation errors
        for field_errors in form.errors.values():
            for err_msg in field_errors:
                flash(f'There was an error creating user: {err_msg}', category='danger')

    return render_template('register.html', form = form)

@app.route('/login', methods = ['GET','POST'])
def login_page():
    # create an object
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password = form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username} ', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match!! Try again', category='danger')

    return render_template('login.html', form = form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out!,', category='info')
    return redirect(url_for('home_page'))
