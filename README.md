# Shopify Backend Developer Challenge - Winter 2022 #
* Submission for Shopify challenge!

# Project Features # 

This project uses Python (Flask), MongoDB, and Stripe. This was my first time using Flask and Stripe - I had a lot of fun learning these technologies!

* Inserting/adding images
* Deleting images
* Updating image details
* Searching image by image name or tags
* Inventory management
* Purchasing images through Stripe

# Setup
This repo uses Python 3.9.7. Ensure that you have a MongoDB database set up.

1. Clone the project
2. Create a ```.env``` file in the root directory and request these environment variables from me.

``` 
MONGO_API_KEY=
PUBLISHABLE_KEY=
SECRET_KEY=
```
3. Install dependencies using ```pip install -r requirements.txt```
4. Run the server with ```flask run```

# Next Steps
I would like add front end components and integrate with the existing backend. Also, I would like to add user-based access control and authentication.
