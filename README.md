# Gallery Tracking Optimizer

Most of the e-commerces have a product gallery on their website, where they show their products to the customers trying
to sell them but showing how other buyers are using/consuming it.

Despite that, most of the companies that offer these services (creating a gallery from the e-commerce catalogue) has a 
very weak and poor technology behind. So, we want to create an amazing API where the companies can 
create a gallery for their website and optimize it based on user interest. 

## How it works?

The aim of this API is to **load a dataset of images**, provided by the company, and 
**sort them regarding a calculated weight**. To be able to calculate these weights, the client of this API will inform 
us every time a user `view` or `click` over any of the images showed on the gallery.

### Order algorithm 

We have 2 type of events:
* `view` → When the image is rendered on the user's screen. So, if the gallery has a pagination and the user is 
 scrolling down, every time an image is rendered, this event will be dispatched.
* `click` → When any user clicks on the image to see the product behind, or anywhere that the company wants to redirect 
 the user, this event will be triggered.

When a user `click` on an image, the level of interest on this image/product is way higher than just a 
view. In our case **the `click` will perform 7 times better than a `view`**.

The algorithm will take this into account to calculate the `weight` of every image and specify an optimized order.

### Workflow

The workflow of this API is as follows:
1. **Collect the data**, synchronously, and store them in terms of being able to track the events later and optimize the
grid. By default, the order would be based on the creation timestamp (the most recently first).
2. **Start receiving events** and calculating the weight for the image where the event has been dispatched. At this 
point, you should **optimize the order of the images**. Choose the best algorithm to sort the entire dataset, taking 
into account the time and complexity of your implementation. 
3. **Serve the images** with the expected order. 

## Using the API

1. Add the .env file
2. Make sure Docker is installed. `docker -v`
3. Build the image with: `docker-compose build`
4. Start the container with: `docker-compose up -d`
5. Once container is running, by default, your app's URL will be: `http://localhost:8009`
6. To run automatic tests, run: `docker-compose exec gallery poetry run python -m pytest`
