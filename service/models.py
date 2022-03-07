"""
Models for Shopcart

All of the models are stored in this module

Attributes Explanations:

item_id: an item id
user_id: a user id, primary key for shopcart
user_id + item_id serves as the compound primary key in our Shopcart-Item table
item_name: name of an item
quantity: quantity of an item
price: price of an item
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass

    


class Shopcart(db.Model):
    """
    Class that represents a shopcart
    """

    app = None

    # Shopcart-Item Table Schema
    user_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(63))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)


    def __repr__(self):
        return "<Shopcart for user %s>" % self.user_id

    def create(self):
        """
        Creates a Shopcart to the database
        """
        logger.info("Creating shopcart for user %s", self.user_id)
        db.session.add(self)
        db.session.commit()
    
    def save(self):
        """
        Updates a Shopcart to the database
        """
        logger.info("Saving shopcart for user %s", self.user_id)
        db.session.commit()

    def delete(self):
        """ Removes a Shopcart from the data store """
        logger.info("Deleting shopcart for user %s", self.user_id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Shopcart into a dictionary """
        return {"user_id": self.user_id, 
        "item_id": self.item_id,
        "item_name": self.item_name,
        "quantity": self.quantity,
        "price": self.price
        }

    def deserialize(self, data):
        """
        Deserializes a Shopcart from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.user_id = data["user_id"]
            self.item_id = data["item_id"]
            self.item_name = data["item_name"] + ""
            self.quantity = data["quantity"]
            self.price = data["price"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid Shopcart: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid Shopcart: body of request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Shopcarts in the database """
        logger.info("Processing all Shopcarts")
        return cls.query.all()

    @classmethod
    def find(cls, user_id, item_id):
        """ Finds an item by user_id and item_id """
        logger.info("Processing lookup for user id %s item id %s...", user_id, item_id)
        return cls.query.filter((cls.user_id == user_id) & (cls.item_id == item_id))


    @classmethod
    def find_or_404(cls, uid, iid):
        """ Find an item by user_id and item_id """
        logger.info("Processing lookup or 404 for user id %s item id %s...", uid, iid)
        return cls.query.get_or_404(uid, iid)

