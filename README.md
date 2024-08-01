# Weather API Wrapper Service

## Overview

This project is a weather API wrapper service that integrates with a third-party weather API - [Visual Crossing weather API](https://www.visualcrossing.com/weather-api), implements caching using Django's built-in cache framework, and utilizes environment management strategies.

## Features

* Consumes external weather API services
* Implements caching using Django's built-in cache framework for quick in-memory storage
* Allows users to request weather data for a specific city, caching the response for similar requests

## App Logic

1. User requests weather data for a city
2. API checks cache for existing data
3. If cached data exists, returns cached response
4. If no cached data exists, requests data from external weather API
5. Caches response for future requests