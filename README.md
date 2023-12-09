# E-com

E-commerce platform selling fans

This project is full-fledged e-commerce platform designed for selling fans. It encompasses user authentication, a user-friendly interface, comprehensive product management, and a well-structured admin panel. 

FEATURES

## User Side

> User Authentication : User can register, login and manage their accounts.

> Home Page : A dynamic home page showcauses featured products, promotions and trending items.

> Cart : User can add item to their cart, manage their cart content and proceed to checkout.

> Checkout : A secure and streemlined checkout process enabled user to complete their purchases using Various payment methods(ie, razorpay, cod, wallet).

> Wishlist: Users can create and manage wishlists to save products they're interested in for future purchases.

> UserProfile Page :  User can view and edit their persional information, manage their orders and track their wishlist.




## Admin Side

> Dashboard : A comprehensive dashboard provides an overview of store performance, sales data, and user statistices.

> Coupon Management : Admin can create, manage and applay coupons to provide discount and promotions.

> User Management : Admin can view, edit and manage user accounts including user permissions.

> Product Management : Admin can add, edit and manage product information, including product image, discription, pricing and inventory.

> Category Management : Admin can create, edit and manage product categories to organize the product catelog effectively.

> Variant Management : Admin can mange product variants.




## Technology Stack

> Frontend : HTML, CSS, JS, Bootstrap

> Backend : Django

> Database : postgreSQL


## Installation and Setup

1. Clone the project repository from GitHub.

   Open the project forlder in the text editor (create a new folder and open it in the VS CODE)

   Open new terminal, then type

       git clone https://github.com/donxavier369/E-com.git

2. Install required dependencies

   1. create vertual env

    Navigete to project direactory( in this project ...\...\E-com)

    Run the following command to create vertual enviornment( replace env with your desired vertual enviornment name):

         python -m venv env

    2. Activate the vertual enviornment

       On Unix or MacOS:

           source  env/bin/activate

       On Windows:

            .\env\Scripts\activate

   3. Navigate to requirement.txt file then type (for install depnedencies)

             pip install -requirements.txt

3. Set up  DJANGO SECRET_KEY , Razorpay(RAZORPAY_KEY_ID) and Database(RAZORPAY_KEY_SECRET)

      > In settings.py file import DJANGO SECRET_KEY , Razorpay(RAZORPAY_KEY_ID) and Database(RAZORPAY_KEY_SECRET) using config

      > create .env file in the project diractory, in this project => in this project ...\...\E-com

      > whith in the .env file add,

           TWILIO_VERIFY_SERVICE_SID = Add your TWILIO_VERIFY_SERVICE_SID
           TWILIO_ACCOUNT_SID = Add your TWILIO_ACCOUNT_SID
           TWILIO_AUTH_TOKEN = Add your TWILIO_AUTH_TOKEN
         
         
           SECRET_KEY = 'django-insecure-mx_ng(%1p6qs5pv0ez_uvqyi6)w!v(=hux2vf+c3vxhcrbd&9k'
           
           RAZORPAY_KEY_ID = 'Add your AZORPAY_KEY_ID'
           RAZORPAY_KEY_SECRET = 'Add your AZORPAY_KEY_SECRET'
           
           
           DATABASE_NAME = Add your database name
           DATABASE_USER = Add database user 
           DATABASE_PASSWORD = Add database password


4. Perform migration and makemigration
  
         python manage.py makemigrations

         python manage.py migrate


5. Start the development server

        python manage.py runserver


## Usage

Detail view for User Side click 

Detail view for Admin Side click 



      
         


