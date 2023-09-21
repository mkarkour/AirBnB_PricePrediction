# Airbnb Price Prediction

## Project Overview

The aim of this project is to provide a Gradio application that allows Airbnb landlords to receive price predictions for their properties. The predictions are based on data collected for different European cities and various property characteristics. The goal is to help landlords set competitive and attractive prices for their Airbnb listings.

### Data Source

The dataset used for this project is sourced from Kaggle and can be found at the following link: [Airbnb Prices in European Cities](https://www.kaggle.com/datasets/thedevastator/airbnb-prices-in-european-cities).

### Project Features

The dataset consists of several columns, each providing valuable information for predicting Airbnb prices. Here's a brief description of the key columns:

* `realSum`: The total price of the Airbnb listing (Numeric).
* `room_type`: The type of room being offered (e.g., private, shared, etc.) (Categorical).
* `room_shared`: Indicates whether the room is shared or not (Boolean).
* `room_private`: Indicates whether the room is private or not (Boolean).
* `person_capacity`: The maximum number of people that can stay in the room (Numeric).
* `host_is_superhost`: Indicates whether the host is a superhost or not (Boolean).
* `multi`: Indicates whether the listing is for multiple rooms or not (Boolean).
* `biz`: Indicates whether the listing is for business purposes or not (Boolean).
* `cleanliness_rating`: The cleanliness rating of the listing (Numeric).
* `guest_satisfaction_overall`: The overall guest satisfaction rating of the listing (Numeric).
* `bedrooms`: The number of bedrooms in the listing (Numeric).
* `dist`: The distance from the city center (Numeric).
* `metro_dist`: The distance from the nearest metro station (Numeric).
* `lng`: The longitude of the listing (Numeric).
* `lat`: The latitude of the listing (Numeric).

### Project Output

The output of this project is an Airbnb price prediction based on the provided features. Users, specifically Airbnb landlords, can input the relevant property characteristics into the Gradio application, and the model will generate a predicted price. This prediction serves as a valuable tool for landlords to make informed pricing decisions and maximize the attractiveness of their listings on Airbnb.

Feel free to explore the code and the Gradio application to see how the price prediction model works and how it can benefit Airbnb landlords.

## Usage

To use the Gradio application for Airbnb price prediction, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies as specified in the `requirements.txt` file.
3. Run the Gradio application script.
4. Input the property characteristics for which you want to receive a price prediction.
5. Receive the predicted Airbnb price based on the provided data.

## Dependencies

The project relies on the following libraries and packages:

- NumPy
- Pandas
- Scikit-Learn
- Gradio

Make sure to install these dependencies using `pip` before running the Gradio application.

## Questions or Issues

If you have any questions or encounter any issues while using the application or exploring the project, please don't hesitate to reach out to the project maintainers or open an issue in the repository. We are here to assist you and improve the project.

Enjoy using the Airbnb Price Prediction application!
