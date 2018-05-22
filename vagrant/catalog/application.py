from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Fake Restaurants
# category = {'name': 'The CRUDdy Crab', 'id': '1'}

# categorys = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


# Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}
# items = []


@app.route('/category/<int:category_id>/menu/JSON')
def categoryMenuJSON(category_id):
    category = session.query(Restaurant).filter_by(id=category_id).one()
    items = session.query(MenuItem).filter_by(
        category_id=category_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


#@app.route('/category/<int:category_id>/menu/<int:menu_id>/JSON')
#def categoryItemJSON(category_id, menu_id):
#    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
#    return jsonify(Menu_Item=Menu_Item.serialize)


#@app.route('/category/JSON')
#def categoriesJSON():
#    categories = session.query(Category).all()
#    return jsonify(categories=[r.serialize for r in categories])


# Show all categories


@app.route('/')
@app.route('/categories/')
def showCategories():
    categories = session.query(Category).all()    
    # return "This page will show all my categories"
    return render_template('categories.html', categories=categories)


# Create a new category


@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')
        
    # return "This page will be for making a new category"

# Edit a category


@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            return redirect(url_for('showCategories'))
    else:
        return render_template(
            'editCategory.html', category=editedCategory)

    # return 'This page will be for editing category %s' % category_id

# Delete a category

@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        return redirect(
            url_for('showCategories', category_id=category_id))
    else:
        return render_template(
            'deleteCategory.html', category=categoryToDelete)
    # return 'This page will be for deleting category %s' % category_id


# Show a category menu


@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/menu/')
def showMenu(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by(
        category_id=category_id).all()
    return render_template('menu.html', items=items, category=category)
    # return 'This page is the menu for category %s' % category_id

# Create a new menu item


@app.route('/category/<int:category_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(category_id):
    if request.method == 'POST':
        newItem = CategoryItem(name=request.form['name'], description=request.form['description'], category_id=category_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showMenu', category_id=category_id))
    else:
        return render_template('newcategoryitem.html', category_id=category_id)

    return render_template('newMenuItem.html', category=category)
    # return 'This page is for making a new menu item for category %s'
    # %category_id

# Edit a menu item


"""@app.route('/category/<int:category_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(category_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showMenu', category_id=category_id))
    else:

        return render_template(
            'editmenuitem.html', category_id=category_id, menu_id=menu_id, item=editedItem)"""

    # return 'This page is for editing menu item %s' % menu_id

# Delete a menu item


"""@app.route('/category/<int:category_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(category_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showMenu', category_id=category_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete)
    # return "This page is for deleting menu item %s" % menu_id"""


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
