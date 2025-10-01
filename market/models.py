from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin

# this decorator When a user logs in, Flask-Login stores their user ID in the session, 
# The user_loader decorator is used to tell Flask-Login how to get a user object from a user ID
# LoginManager is a class from Flask-Login that handles user authentication
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # returns the User object from DB


class User(db.Model, UserMixin) :
    __tablename__ = 'user'  # ctable name is 'User'
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(length=30), nullable = False, unique = True)
    email_address = db.Column(db.String(length=50), nullable = False, unique = True)
    password_hash = db.Column(db.String(length=60), nullable = False)
    budget = db.Column(db.Integer(), nullable = False, default = 1000)
    items = db.relationship('Item', backref = 'owned_user', lazy = True)
    # it's not a column , it's a relationship

    # lets you access it like an attribute. 
    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4 :
            return f'{str(self.budget)[ : -3]}, {str(self.budget)[-3:]}$'
        else:
            return f'{self.budget}$'

    @property
    def password(self) :
        return self.password_hash
    
    @password.setter
    def password(self, plain_text_password) :
        # Instead of storing "mypassword" in DB, it hashes it with bcrypt and saves the result into password_hash.
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password ):   # attempted_password is the plain text password the user types.
        # self.password_hash → the hashed password stored in the database.
        # bcrypt.check_password_hash() → hashes attempted_password internally and compares it with self.password_hash. Returns True if they match.
        return bcrypt.check_password_hash(self.password_hash, attempted_password)  # compares the stored hashed password with the entered password in login form

    def can_purchase(self, item_obj ):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(length=30), nullable = False, unique = True)
    price = db.Column(db.Integer(), nullable = False)
    barcode = db.Column(db.String(length = 12), nullable = False, unique = True)
    description = db.Column(db.String(length = 1024), nullable = False, unique = True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self) :
        return f'Item {self.name}'
    
    def buy(self, user) :
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()