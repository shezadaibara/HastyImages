# Interview challenge - Hasty Backend Engineer

## 1) Appliaction with HTTP REST API

Write an application with HTTP REST API for uploading images via an invitation link. You should implement at least these endpoints:
- **Generate upload link** - which accepts a secret token and expiration time, and produces an expirable link to the endpoint that can be used for image upload;
- **Upload image** - an expirable one, which accepts one or many images and returns back some identifier(s). The logic of uploading multiple images until the link is expired is up to you. Images, which will be persisted at service side and service should recognize duplicates and store them just once. Also, the image metadata data should be parsed and stored in a database (dimensions, camera model, location, etc.)
- **Get image** - accepts image identifier and returns back an image.
- **Get service statistics** - which expects a secret token and returns service statistics, among which:
- the most popular image format;
- the top 10 most popular camera models;
- image upload frequency per day for the past 30 days.

Application should be packed in one or multiple docker containers. Technologies and language choice is up to you.

A link to a repository or an archive with code is expected back from you.


## 2) Service scalability and performance

Imagine a thousand of users that constantly upload images to the service from the first task. You have to set up an infrastructure that can handle this traffic. The architecture should contain an asynchronous batch processing, as well as a real-time processing layer.

For instance, batch processing could be used to train and update a predictive model for each of the uploaded images. On the other hand, real-time processing could be used to apply simple data processing (e.g. aggregations over time, data cleaning etc.) or to generate predictions for uploaded images.

How could such an architecture look like? Please provide us with a brief sketch and textual description, and mention *anything* that might seem important to you, for instance:
- What kind of technologies would you use for the service and its respective infrastructure?
- Where and how would you store data?
- On top of what is mentioned above, what would you use the batch/real-time pipeline for?
- What kind of questions would you need to have answered in order to solve this task more concretely or in order to make better decisions on architecture and technologies?

# Evaluation
Your challenge results will be evaluated based on the following criteria
- code cleanliness,
- queries correctness,
- level of creativity / ingenuity of your solution.

# Questions?
Feel free to [email us](mailto:herbert@hasty.ai) with any questions you might have about the challenge.
