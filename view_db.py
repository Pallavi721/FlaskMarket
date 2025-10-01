from market import app, db, Item

# Run inside the Flask app context
with app.app_context():
    items = Item.query.all()
    
    if not items:
        print("No data found in 'Item' table.")
    else:
        print("Items in database:")
        for item in items:
            print(f"{item.id}: {item.name} - ${item.price} - {item.barcode}")
