
import MySQLdb.cursors # Imports 'cursors' allows you to interect with MySQL database. Also used to execute SQL queries and fetch data from database.
import re # Provide support for regular expressions, searches and manipulates strings, it helps with a lot of tasks like validation.

from flask import Flask, render_template, request, redirect, session, url_for, flash #imported flask and other things here
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import hashlib
import uuid



c_str = "mysql://root:cyber241@localhost/ecomm"
engine = create_engine(c_str, echo=True)


app = Flask(__name__)
app.secret_key = 'hola'

conn = engine.connect()




# displays the home page
@app.route('/')
def home():
    return render_template('/index.html')

# ------------------------------------------------ Start of Register - Vee

# function to hash the password when it is entered by the user and add it to the db
def hash_password(inputpw):
    return hashlib.sha3_256(inputpw.encode())

# check to see if user already exists
def Checkexist(user_name):
     user_name = str(user_name)
     account = conn.execute(text("SELECT USER_NAME FROM USER WHERE USER_NAME = :USER_NAME"), {'USER_NAME': user_name})
     result = account.fetchone()
     if result:
         return True
     else:
        return False

# displays the sign up page
@app.route('/register', methods=['GET'])
def showRegister():
    return render_template('/register.html')

# actual sign up function
@app.route('/register', methods=['POST', 'GET'])
def registerUser():
    msg = ''
    if request.method == 'POST':
        user_name = request.form.get('USER_NAME')
        name = request.form.get('NAME')
        email = request.form.get('EMAIL')
        password = request.form.get('PASSWORD')
        acc_type = request.form.get('ACCOUNT_TYPE')
        # hashing the password value from the form
        hashed_password = hash_password(password).hexdigest()

        if Checkexist(user_name):
            flash('This Account Already Exists!', 'error')
            return redirect(url_for('showRegister'))
        else:
            conn.execute(text(f'INSERT INTO USER (USER_NAME, NAME, EMAIL, PASSWORD, ACCOUNT_TYPE) VALUES (\'{user_name}\', \'{name}\',\'{email}\',\'{hashed_password}\', \'{acc_type}\')'))
            conn.commit() #extra layer of protection
            session['loggedin'] = True
            session['USER_NAME'] = user_name
            session["NAME"] = f"{name}"  
            return redirect(url_for('showLogin'))   

# ------------------------------------------------ End of Register ------------------------------------------------------------

def generate_unique_cart_id():
    return str(uuid.uuid4())

def create_cart_for_user(username):
    cart_id = generate_unique_cart_id()
    conn.execute(text("INSERT INTO CART (CART_ID, CREATED_BY) VALUES (:cart_id, :username)"), {'cart_id': cart_id, 'username': username})
    return cart_id


# ------------------------------------------------ Start of Login - Jaiden
@app.route('/login', methods=['GET'])
# function uses session to display errors when there is a bad login attempt
def showLogin():
  return render_template('/login.html')


@app.route('/login', methods=['POST', 'GET'])
# actual login function 

def loginUser():
    msg = ''
    if request.method == 'POST' and 'USER_NAME' in request.form and 'PASSWORD' in request.form:
        username_or_email = request.form.get('USER_NAME') or request.form.get('EMAIL')
        password = request.form.get('PASSWORD')

        hashed_password = hash_password(password).hexdigest()

        account = conn.execute(text("SELECT * FROM User WHERE USER_NAME = :identifier OR EMAIL = :identifier"), {'identifier': username_or_email})
        user_data = account.fetchone()
        if user_data:     
            if user_data[3] == hashed_password:
                session['loggedin'] = True
                session['USER_NAME'] = user_data[0]
                session['NAME'] = f"{user_data[1]}"
                cart_id = create_cart_for_user(user_data[0])  # Assuming user_data[0] is the USER_NAME or user identifier
                session['cart_id'] = cart_id
                if user_data[4] == 'Administrator':
                     redirect(url_for('showAdmin'))
                elif user_data[4] == 'Vendor':
                    return redirect(url_for('showVendor'))
                else:
                    return redirect(url_for('home'))
            else:
                msg = 'Wrong username or password'
        else:
            msg = 'User not found'

    return render_template('/login.html', msg=msg)


# ------------------------------------------------ End of Login ----------------------------------------------------------------



# ------------------------------------------------ Start of Log out - Jaiden

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('USER_NAME', None)
    session.pop('NAME', None)
    return redirect(url_for('loginUser'))


# ------------------------------------------------ End of log out ---------------------------------------------------------------




# ------------------------------------------------ Start of User Accounts - Jaiden

@app.route('/my_account', methods=['GET'])
def account_info():
    username = str(session.get('USER_NAME'))
    if username:
        account = conn.execute(text("SELECT * FROM user WHERE USER_NAME = :USER_NAME"), {'USER_NAME': username})
        user_data = account.fetchone()
        if user_data:
            return render_template("/my_account.html", user_data=user_data)
    return redirect(url_for('loginUser'))

# ------------------------------------------------ End of User Accounts --------------------------------------------------------------





# ------------------------------------------------ Start of Admin accounts - Kishaun

# admin views all accounts
@app.route('/all_accounts', methods=['GET'])
def all_accounts():
    return render_template('all_accounts.html')


@app.route('/all_accounts', methods=['POST'])
def search_account():
    acc_type = request.form.get('acc_type')
    if acc_type == 'all':
        users = conn.execute(text('SELECT * FROM USER')).fetchall()
    else:
        users = conn.execute(text('SELECT * FROM USER WHERE ACCOUNT_TYPE = :acc_type'), {'acc_type': acc_type}).fetchall()
    conn.commit()
    print(users)
    return render_template('all_accounts.html', users=users)


# ------------------------------------------------ End of Admin --------------------------------------------------------------




# ------------------------------------------------ Start of Vendor accounts - Vee

# Shows the vendor page
@app.route('/vendor')
def showVendor():
    return render_template('/vendor.html')

# shows specific products on the Vendor page
@app.route('/vendorproducts')
def showVendor_Products():
    # getting username from session
    username = str(session.get('USER_NAME'))

    # getting products and images from the db
    # query that joins product and product imgs table together to get details and photos.
    items = conn.execute(text('Select * from product p join product_imgs p_img where p.PID = p_img.PID')).all()
    imgs = conn.execute(text('SELECT * FROM PRODUCT_IMGS')).all()

    # message to be displayed when vendor logs in but has no products
    no_products = "Looks like you don't have any products..."
    print(no_products)

    # getting all the products from the db for a specific vendor so that they will be displayed on the vendor page
    # query that joins product table and user table together to get products for a specific vendor
    vendor_products = conn.execute(text("SELECT * FROM PRODUCT prod join USER acc WHERE acc.ACCOUNT_TYPE = 'Vendor' AND acc.USER_NAME = :USER_NAME"), {'USER_NAME':username}).fetchall()

    return render_template('/vendor.html', items=items, imgs=imgs, no_products=no_products, vendor_products=vendor_products)

# ------------------------------------------------ End of Vendor --------------------------------------------------------------





# ------------------------------------------------ Start of Product page - Vee
# shows the actual page and products
@app.route('/view_products', methods=['GET', 'POST'])
def showProduct_page():
    # joining together the product table and product image table
    items = conn.execute(text('Select * from product p join product_imgs p_img where p.PID = p_img.PID')).all()

    # grabbing images from the db
    imgs = conn.execute(text('SELECT * FROM PRODUCT_IMGS')).all()

    # just checking to see if it's working in the terminal
    print(len(items))

    return render_template('/view_products.html', items=items, imgs=imgs)


# ------------------------------------------------ End of Product page ------------------------------------------------------------
 





# ------------------------------------------------ Start of checkout - Jaiden


# Add to Cart - Jaiden
@app.route('/add_to_cart/<int:product_id>', methods=['GET'])
def add_to_cart(product_id):
    try:
        product_id = int(product_id)
        cart_id = session.get('cart_id')
        if not cart_id:
            cart_id = generate_unique_cart_id()  # Function to generate a unique cart ID
            session['cart_id'] = cart_id
        
        conn.execute(text("INSERT INTO CART_HAS_PRODUCT (PID, CART_ID) VALUES (:pid, :cart_id)"), {'pid': product_id, 'cart_id': cart_id})
        flash('Item added to cart!')
        return redirect(url_for('showProduct_page'))
    
    except ValueError:
        return "Invalid product ID", 400
    
    except Exception as e:
        return f"Failed to add item to cart: {str(e)}", 500




# Remove from Cart - Jaiden
@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session and product_id in session['cart']:
        session['cart'].remove(product_id)
        flash('Item removed from cart!')
    return redirect(url_for('showCart'))


# A route to display the actual cart - Jaiden
@app.route('/cart')
def showCart():
    cart_items = []
    total = 0
    if 'cart' in session:
        product_ids = session['cart']
        for product_id in product_ids:
            product = conn.execute(text("SELECT * FROM PRODUCT WHERE PID = :pid"), {'pid': product_id}).fetchone()
            if product:
                image_url = conn.execute(text("SELECT IMAGE_URL FROM PRODUCT_IMGS WHERE PID = :pid"), {'pid': product_id}).fetchone()[0] #NEED TO CHANGE IMAGESURL TO IMAGE_URL, and product_images to product_imgs
                item_total = product[5] * product[4]
                cart_items.append({'pid': product[0], 'title': product[1], 'description': product[2], 'warranty_period': product[3], 'number_of_items': product[4], 'price': product[5], 'category': product[6], 'image_url': image_url, 'item_total': item_total})
                total += item_total
    return render_template('cart.html', cart_items=cart_items, total=total)





# ------------------------------------------------ End of checkout ---------------------------------------------------------------




# Start of Vendor add/delete/update functions ----------------------------------------------------------> Kishaun
@app.route('/add_products', methods=['GET'])
def add_products():
    return render_template('add_products.html')


@app.route('/add_products', methods=['POST'])
def add_products_post():
    created_by = session.get('USER_NAME')
    conn.execute(text('INSERT INTO PRODUCT (TITLE, DESCRIPTION, WARRANTY_PERIOD, NUMBER_OF_ITEMS, PRICE, CREATED_BY, CATEGORY) VALUES (:title, :description, :warranty_period, :number_of_items, :price, :created_by, :category)'), {'title': request.form['title'], 'description': request.form['description'], 'warranty_period': request.form['warranty_period'], 'number_of_items': request.form['number_of_items'], 'price': request.form['price'], 'created_by': created_by, 'category': request.form['category']})
    # Grabs the image from the add_product form and adds it to the database 
    conn.execute(text('INSERT INTO PRODUCT_IMGS (PID, IMAGE_URL) VALUES (LAST_INSERT_ID(), :IMAGE_URL)'), {'IMAGE_URL': request.form['IMAGE_URL']})
    conn.execute(text('INSERT INTO PRODUCT_COLOR (PID, color) VALUES (LAST_INSERT_ID(), :color)'), {'color': request.form['color']})
    conn.execute(text('INSERT INTO PRODUCT_SIZE (PID, size) VALUES (LAST_INSERT_ID(), :size)'), {'size': request.form['size']})
    conn.commit()
    flash('Product Added!')
    return redirect(url_for('add_products'))


@app.route('/add_more_images',methods=['POST'])
def add_more_images():
    PID = request.form['PID']
    imagesURL = request.form['imagesURL']
    conn.execute(text('INSERT INTO ProductImages (PID, imagesURL) VALUES (:PID, :imagesURL)'), {'PID': PID, 'imagesURL': imagesURL}) 
    conn.commit()  
    flash('Image added')
    return redirect(url_for('add_products'))


@app.route('/update', methods=['POST'])
def update_product():
    PID = request.form['PID']
    created_by = session['USER_NAME']
    
    # category = request.form['category']
    conn.execute(text('UPDATE PRODUCT SET TITLE = :title, DESCRIPTION = :description, WARRANTY_PERIOD = :warranty_period, NUMBER_OF_ITEMS = :number_of_items, PRICE = :price, Category = :category WHERE PID = :PID and ADDED_BY_USERNAME = :created_by'), {'title': request.form['title'], 'description': request.form['description'], 'warranty_period': request.form['warranty_period'], 'number_of_items': request.form['number_of_items'], 'price': request.form['price'],'category': request.form['category'], 'PID': PID,'created_by': created_by})
    conn.execute(text('UPDATE PRODUCT_IMGS SET IMAGE_URL = :IMAGE_URL WHERE PID = :PID'), {'IMAGE_URL': request.form['IMAGE_URL'], 'PID': PID})
    conn.execute(text('UPDATE PRODUCT_COLOR SET color = :color WHERE PID = :PID'), {'color': request.form['color'], 'PID': PID})
    conn.execute(text('UPDATE PRODUCT_SIZE SET size = :size WHERE PID = :PID'), {'size': request.form['size'], 'PID': PID})
    conn.commit()
    flash('Item Edited')
    return redirect(url_for('add_products'))



@app.route('/delete', methods=['POST'])
def delete_product():

    created_by = session['USER_NAME']

    PID = request.form['PID']
    conn.execute(text('DELETE FROM REVIEW WHERE PRODUCT = :PID'), {'PID': PID}) 
    conn.execute(text('DELETE FROM PRODUCT_IMGS WHERE PID = :PID'), {'PID': PID})
    conn.execute(text('DELETE FROM PRODUCT_COLOR WHERE PID = :PID'), {'PID': PID})
    conn.execute(text('DELETE FROM PRODUCT_SIZE WHERE PID = :PID'), {'PID': PID})
    conn.execute(text('DELETE FROM PRODUCT WHERE PID = :PID and CREATED_BY = :created_by'), {'PID': PID, 'created_by': created_by})
    conn.commit()
    flash('Item Deleted')
    return redirect(url_for('add_products'))

## End of Vendor functions ----------------------------------------------------------> Kishaun


## Start of admin add/delete/update functions----------------------------------------------------------> Kishaun
@app.route('/admin_add_products', methods=['GET'])
def admin_add_products():
    return render_template('admin_add_products.html')


@app.route('/admin_add_products', methods=['POST'])
def admin_add_products_post():
    created_by = session.get('USER_NAME')
    # Ensure the user exists in the USERS table
    user_exists = conn.execute(text('SELECT * FROM User WHERE USER_NAME = :username'), {'username': created_by}).fetchone() is not None
    if not user_exists:
        conn.execute(text('INSERT INTO User (USER_NAME, NAME) VALUES (:username, :name)'), {'username': created_by, 'name': 'Vendor'})
        conn.execute(text('INSERT INTO PRODUCT (TITLE, DESCRIPTION, WARRANTY_PERIOD, NUMBER_OF_ITEMS, PRICE, CREATED_BY, CATEGORY) VALUES (:title, :description, :warranty_period, :number_of_items, :price, :created_by, :category)'), {'title': request.form['title'], 'description': request.form['description'], 'warranty_period': request.form['warranty_period'], 'number_of_items': request.form['number_of_items'], 'price': request.form['price'], 'created_by': request.form['created_by'], 'category': request.form['category']})
        conn.execute(text('INSERT INTO PRODUCT_IMGS (PID, IMAGE_URL) VALUES (LAST_INSERT_ID(), :IMAGE_URL)'), {'IMAGE_URL': request.form['IMAGE_URL']})
        conn.execute(text('INSERT INTO PRODUCT_COLOR (PID, color) VALUES (LAST_INSERT_ID(), :color)'), {'color': request.form['color']})
        conn.execute(text('INSERT INTO PRODUCT_SIZE (PID, size) VALUES (LAST_INSERT_ID(), :size)'), {'size': request.form['size']})
        conn.commit()
        flash('Item added')
    return redirect('/admin_add_products')





@app.route('/all_accounts', methods=['POST'])
def search_account():
    acc_type = request.form.get('acc_type')
    if acc_type == 'all':
        users = conn.execute(text('SELECT * FROM USER')).fetchall()
    else:
        users = conn.execute(text('SELECT * FROM USER WHERE ACCOUNT_TYPE = :acc_type'), {'acc_type': acc_type}).fetchall()
    conn.commit()
    print(users)
    return render_template('admin.html', users=users)
  



@app.route('/admin_update', methods=['POST'])
def admin_update_product():
    created_by = request.form['vendor_username']
    PID = request.form['PID']
    # category = request.form['category']
    conn.execute(text('UPDATE PRODUCT SET TITLE = :title, DESCRIPTION = :description, WARRANTY_PERIOD = :warranty_period, NUMBER_OF_ITEMS = :number_of_items, PRICE = :price, Category = :category WHERE PID = :PID'), {'title': request.form['title'], 'description': request.form['description'], 'warranty_period': request.form['warranty_period'], 'number_of_items': request.form['number_of_items'], 'price': request.form['price'],'category': request.form['category'], 'PID': PID,})
    conn.execute(text('UPDATE PRODUCT_IMGS SET IMAGE_URL = :IMAGE_URL WHERE PID = :PID'), {'IMAGE_URL': request.form['IMAGE_URL'], 'PID': PID})
    conn.execute(text('UPDATE PRODUCT_COLOR SET color = :color WHERE PID = :PID'), {'color': request.form['color'], 'PID': PID})
    conn.execute(text('UPDATE PRODUCT_SIZE SET size = :size WHERE PID = :PID'), {'size': request.form['size'], 'PID': PID})
    conn.commit()
    return redirect(url_for('admin_add_products'))


@app.route('/admin_delete', methods=['POST'])
def admin_delete_product():
    PID = request.form['PID']
    created_by = request.form['vendor_username']
    conn.execute(text('DELETE FROM PRODUCT_IMGS WHERE PID = :PID'), {'PID': PID})
    conn.execute(text('DELETE FROM PRODUCT_COLOR WHERE PID = :PID'), {'PID': PID})
    conn.execute(text('DELETE FROM PRODUCT_SIZE WHERE PID = :PID'), {'PID': PID})
    conn.execute(text('DELETE FROM PRODUCT WHERE PID = :PID AND CREATED_BY = :username'), {'PID': PID, 'username': created_by})
    conn.commit()
    return redirect(url_for('admin_add_products'))
## End of admin functions--------------------------------------------------------------------> Kishaun


## Start of review section Kishaun--------------------------------------------------------------------> Kishaun
@app.route('/review',methods=['GET'])
def review_get():
    return render_template('review.html')


@app.route('/review',methods=['POST'])
def review_post():
    username = session['user_id']
    rating = request.form['rating']
    desc = request.form['desc']
    img = request.form['img']
    Product = request.form['Product']
    conn.execute(text('INSERT INTO REVIEW (RATING, `DESC`, IMG, REVIEW_USER_NAME, PRODUCT) VALUES (:rating, :desc, :img, :username, :Product)'), {'rating': rating, 'desc': desc, 'img': img, 'username': username, 'Product': Product})
    conn.commit()
    return redirect('/review')


@app.route('/view_reviews', methods=['GET'])
def view_reviews():
    return render_template('view_reviews.html')


@app.route('/view_reviews', methods=['POST'])
def view_reviews_post():
    Product = request.form.get('Product')  ## This is the product that the user is reviewed
    Rating = request.form.get('Rating')   ## This is the rating that the user gave
    if Product and Rating:
        reviews = conn.execute(text('SELECT * FROM REVIEW WHERE Product = :Product AND RATING = :Rating'), {'Product': Product, 'Rating': Rating}).fetchall() ## This is the SQL query that gets the reviews from the database
    elif Product:
        reviews = conn.execute(text('SELECT * FROM REVIEW WHERE Product = :Product'), {'Product': Product}).fetchall()   ## this sorts reviews based on the product
    elif Rating:
        reviews = conn.execute(text('SELECT * FROM REVIEW WHERE RATING = :Rating'), {'Rating': Rating}).fetchall()  ## this sorts reviews based on the rating
    else:
        reviews = conn.execute(text('SELECT * FROM REVIEW')).fetchall()       ## this gets all reviews
    conn.commit()
    return render_template('view_reviews.html', reviews=reviews)
## End of review section Kishaun-------------------------------------------------------------------------------------> 

## Start of complaint section Kishaun-------------------------------------------------------------------------------------> Kishaun
@app.route('/Customer_create_complaint', methods=['GET'])
def create_complaint():
    reviewUserName = session.get('USER_NAME') ## This is the username of the person who is logged in
    complaints_with_images = conn.execute(text('''
        SELECT COMPLAINT.*, COMPLAINTIMAGES.imageURL 
        FROM COMPLAINT 
        LEFT JOIN COMPLAINTIMAGES ON COMPLAINT.CID = COMPLAINTIMAGES.CID
        WHERE COMPLAINT.reviewUserName = :reviewUserName
    '''), {'reviewUserName': session.get('USER_NAME')}).fetchall()  ## This is the SQL query that gets the complaints and images from the database by joining the COMPLAINT and COMPLAINTIMAGES tables
    conn.commit()
    return render_template('Customer_create_complaint.html', complaints=complaints_with_images, reviewUserName=reviewUserName)  ## This is the page that the user sees when they want to create a complaint
## This app route is used to view the page and all of the complaints that the user has made

@app.route('/Customer_create_complaint', methods=['POST'])
def create_complaint_post():
    title = request.form['title']  # Add this line to define the variable "title"
    desc = request.form['desc']  # Add this line to define the variable "desc" which is the description of the complaint
    demand = request.form['demand']  #  this comes from the form on the page
    status = "Pending" ## This is the status of the complaint defualt is pending
    reviewUserName = session.get('USER_NAME')  ## This is the username of the person who is logged in

    # Use current date and time for the 'date' field
    from datetime import datetime
    now = datetime.now()  # Add this line to get the current date and time when creating a complaint

    
    conn.execute(text('INSERT INTO COMPLAINT (date, title, description, demand, status, reviewUserName) VALUES (:date, :title, :desc, :demand, :status, :reviewUserName)'), 
                     {'date': now, 'title': title, 'desc': desc, 'demand': demand, 'status': status, 'reviewUserName': reviewUserName}) ## This is the SQL query that inserts the complaint into the database
    conn.execute(text('INSERT INTO COMPLAINTIMAGES (CID, imageURL) VALUES (LAST_INSERT_ID(), :imagesURL)'), {'imagesURL': request.form['imagesURL']}) ## This is the SQL query that inserts the image into the database
    conn.commit()
    return redirect('/Customer_create_complaint')
    ## This app route lets the Customer create a complaint and add it to the database on the Customer_create_complaint page

## End of customer complaint section Kishaun-------------------------------------------------------------------------------------> Kishaun

## Start of admin complaint section Kishaun-------------------------------------------------------------------------------------> Kishaun
@app.route('/Admin_view_complaints', methods=['GET'])
def view_complaints():
    return render_template('Admin_view_complaints.html')
## This app route lets Admins view all complaints in the database on the Admin_view_complaints page

@app.route('/Admin_view_complaints', methods=['POST'])
def view_complaints_post():
    status = request.form.get('status')
    if status:
        complaints = conn.execute(text('''
        SELECT COMPLAINT.*, COMPLAINTIMAGES.imageURL
        FROM COMPLAINT 
        LEFT JOIN COMPLAINTIMAGES ON COMPLAINT.CID = COMPLAINTIMAGES.CID
        WHERE status = :status
        '''), {'status': status}).fetchall() ## This is the SQL query that gets the complaints and images from the database by joining the COMPLAINT and COMPLAINTIMAGES tables based on the status of the complaint
    else:
        complaints = conn.execute(text(
            'SELECT COMPLAINT.*, COMPLAINTIMAGES.imageURL FROM COMPLAINT LEFT JOIN COMPLAINTIMAGES ON COMPLAINT.CID = COMPLAINTIMAGES.CID'
        )).fetchall() ## This is the SQL query that gets the complaints and images from the database by joining the COMPLAINT and COMPLAINTIMAGES tables
    conn.commit()
    return render_template('Admin_view_complaints.html', complaints=complaints)
## This app route lets the admin sort complaints by status on the Admin_view_complaints page

@app.route('/update_complaint', methods=['POST'])
def update_complaint():
    complaint_id = request.form['complaint_id']  ## This is the complaint id that the admin wants to update
    status = request.form['status']  ## This is the status that the admin wants to update the complaint to
    conn.execute(text('UPDATE COMPLAINT SET status = :status WHERE CID = :complaint_id'), {'status': status, 'complaint_id': complaint_id}) ## This is the SQL query that updates the status of the complaint in the database
    conn.commit()
    return redirect('/Admin_view_complaints')
## This app route lets the admin update the status of a complaint on the Admin_view_complaints page

@app.route('/delete_complaint', methods=['POST'])
def delete_complaint():
    complaint_id = request.form['complaint_id']
    conn.execute(text('DELETE FROM COMPLAINTIMAGES WHERE CID = :complaint_id'), {'complaint_id': complaint_id}) ## This is the SQL query that deletes the image of the complaint from the database based on the complaint id
    conn.execute(text('DELETE FROM COMPLAINT WHERE CID = :complaint_id'), {'complaint_id': complaint_id}) ## This is the SQL query that deletes the complaint from the database based on the complaint id
    conn.commit()
    return redirect('/Admin_view_complaints')
## This app route lets the admin delete a complaint on the Admin_view_complaints page

## End of  Admin complaint section Kishaun-------------------------------------------------------------------------------------> Kishaun


# ------------------------------------------------ Start of Chat - Vee








# ------------------------------------------------ End of Chat ---------------------------------------------------------------





if __name__ == '__main__':
    app.run(debug=True)

