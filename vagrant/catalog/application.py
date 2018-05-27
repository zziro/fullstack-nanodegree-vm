from flask import Flask, render_template, request, redirect, jsonify, url_for, flash


from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Category Item Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login', methods=['GET', 'POST'])
def showLogin():    
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)  


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']    
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Category Information
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
@app.route('/category/')
def showCategories():
    categories = session.query(Category).all()        
    return render_template('categories.html', categories=categories)

    # return "This page will show all my Categories"


# Create a new Category


@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)        
        session.commit()
        flash('New Category %s Successfully Created' % newCategory.name)
        return redirect(url_for('showCategories'))
    else:
        return render_template('newcategory.html')

    # return "This page will be for making a new Category"

# Edit a Category


@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']

        session.add(editedCategory)        
        session.commit()
        flash('Category %s Successfully Edited' % editedCategory.name)
        return redirect(url_for('showCategories'))
    else:
        return render_template('editcategory.html', category=editedCategory)

    # return 'This page will be for editing Category %s' % category_id

# Delete a Category

@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    categoryToDelete = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)        
        session.commit()        
        flash('Category  %s Successfully Deleted' % categoryToDelete.name)
        return redirect(
            url_for('showCategories', category_id=category_id))
    else:
        return render_template(
            'deletecategory.html', category=categoryToDelete)

    # return 'This page will be for deleting Category %s' % category_id


# Show a Category Item


@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/item/')
def showItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by(
        category_id=category_id).all()
    return render_template('categoryitems.html', items=items, category=category)

    # return 'This page is for showing Category Items'

# Create a new Category Item


@app.route('/category/<int:category_id>/item/new/', methods=['GET', 'POST'])
def newCategoryItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')  
    if request.method == 'POST':
        newItem = CategoryItem(name=request.form['name'], 
                            description=request.form['description'],
                            category_id=category_id)
        session.add(newItem)
        session.commit()
        flash('New Category Item %s Successfully Created' % (newItem.name))            
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('newcategoryitem.html', category_id=category_id)

    # return 'This page is for making a new Category Item %s' % category_id
     

# Edit a Category Item


@app.route('/category/<int:category_id>/item/<int:item_id>/edit', methods=['GET', 'POST'])
def editCategoryItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(CategoryItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']

        session.add(editedItem)
        session.commit()
        flash('Category Item %s Successfully Edited' % (editedItem.name))
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('editcategoryitem.html', category_id=category_id, item_id=item_id, item=editedItem)

    # return 'This page is for editing Category Item %s' % item_id

# Delete a Category Item


@app.route('/category/<int:category_id>/item/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteCategoryItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(CategoryItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Category Item %s Successfully Deleted' % (itemToDelete.name))
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deletecategoryitem.html', item=itemToDelete)

    # return "This page is for deleting category item %s" % item_id

# Show Category Item Detail


@app.route('/category/<int:category_id>/detail/<int:item_id>/show', methods=['GET', 'POST'])
def showCategoryItemDetail(category_id, item_id):
    item = session.query(CategoryItem).filter_by(id=item_id).one()
    return render_template('showcategoryitemdetail.html', category_id=category_id, item_id=item_id, item=item)   

    # return 'This page is for showing Category Item Detail'

# Edit a Category Item Detail


@app.route('/category/<int:category_id>/detail/<int:item_id>/edit', methods=['GET', 'POST'])
def editCategoryItemDetail(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(CategoryItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['description']:
            editedItem.description = request.form['description']

        session.add(editedItem)
        session.commit()
        flash('Category Item Detail %s Successfully Edited' % (editedItem.name))
        return redirect(url_for('showCategoryItemDetail', category_id=category_id, item_id=item_id))
    else:
        return render_template('editcategoryitemdetail.html', category_id=category_id, item_id=item_id, item=editedItem)

    # return 'This page is for editing Category Item Detail %s' % item_id

# Delete a Category Item Detail


@app.route('/category/<int:category_id>/detail/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteCategoryItemDetail(category_id, item_id):   
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(CategoryItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        #flash('Category Item Detail %s Successfully Deleted' % (itemToDelete.name))
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deletecategoryitemdetail.html', item=itemToDelete)

    # return "This page is for deleting Category Item  Detail %s" % item_id


if __name__ == '__main__':
    app.debug = True
    app.secret_key = '<S\xa5#\x95\xe4A\x10\x81\xe1X\xf4\xbf\xb1\xce\xf8\x83y4zK\xdf\xc5\t'
    app.run(host='0.0.0.0', port=5000)
