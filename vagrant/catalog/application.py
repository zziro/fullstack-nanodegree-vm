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


# Show all Categories


@app.route('/')
@app.route('/categories/')
def showCategories():
    categories = session.query(Category).all()        
    return render_template('categories.html', categories=categories)

    # return "This page will show all my categories"


# Create a new Category


@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newcategory.html')

    # return "This page will be for making a new category"

# Edit a Category


@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']

        session.add(editedCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('editcategory.html', category=editedCategory)

    # return 'This page will be for editing category %s' % category_id

# Delete a Category

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
            'deletecategory.html', category=categoryToDelete)

    # return 'This page will be for deleting category %s' % category_id


# Show a Category Item


@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/item/')
def showItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by(
        category_id=category_id).all()
    return render_template('categoryitems.html', items=items, category=category)

    # return 'This page is the item for category %s' % category_id

# Create a new Category Item


@app.route('/category/<int:category_id>/item/new/', methods=['GET', 'POST'])
def newCategoryItem(category_id):
    if request.method == 'POST':
        newItem = CategoryItem(name=request.form['name'], 
                            description=request.form['description'],
                            category_id=category_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('newcategoryitem.html', category_id=category_id)

    # return render_template('newcategoryitem.html', category=category)
    # return 'This page is for making a new category item for category %s'
    # %category_id

# Edit a Category Item


@app.route('/category/<int:category_id>/item/<int:item_id>/edit', methods=['GET', 'POST'])
def editCategoryItem(category_id, item_id):
    editedItem = session.query(CategoryItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']

        session.add(editedItem)
        session.commit()        
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('editcategoryitem.html', category_id=category_id, item_id=item_id, item=editedItem)

    # return 'This page is for editing category item %s' % item_id

# Delete a Category Item


@app.route('/category/<int:category_id>/item/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteCategoryItem(category_id, item_id):
    itemToDelete = session.query(CategoryItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deletecategoryitem.html', item=itemToDelete)

    # return "This page is for deleting category item %s" % item_id

# Show Category Item Detail


@app.route('/category/<int:category_id>/detail/<int:item_id>/show', methods=['GET', 'POST'])
def showCategoryItemDetail(category_id, item_id):
    editedItem = session.query(CategoryItem).filter_by(id=item_id).one()
    return render_template('showcategoryitemdetail.html', category_id=category_id, item_id=item_id, item=editedItem)   

    # return 'This page is for editing category item detail %s' % item_id

# Edit a Category Item Detail


@app.route('/category/<int:category_id>/detail/<int:item_id>/edit', methods=['GET', 'POST'])
def editCategoryItemDetail(category_id, item_id):
    editedItem = session.query(CategoryItem).filter_by(id=item_id).one()
    if request.method == 'POST':        
        if request.form['description']:
            editedItem.description = request.form['description']

        session.add(editedItem)
        session.commit()        
        return redirect(url_for('showCategoryItemDetail', category_id=category_id, item_id=item_id))
    else:
        return render_template('editcategoryitemdetail.html', category_id=category_id, item_id=item_id, item=editedItem)

    # return 'This page is for editing category item %s' % item_id

# Delete a Category Item Detail


@app.route('/category/<int:category_id>/detail/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteCategoryItemDetail(category_id, item_id):
    itemToDelete = session.query(CategoryItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showCategoryItemDetail', category_id=category_id, item_id=item_id))
    else:
        return render_template('deletecategoryitemdetail.html', item=itemToDelete)

    # return "This page is for deleting category item %s" % item_id


if __name__ == '__main__':
    app.debug = True
    #app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
