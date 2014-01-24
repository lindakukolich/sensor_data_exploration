#Team: Girs & Buoyrs

###Milestone 2

###Did any of your answers to Milestone 1 change (particularly the Additional Questions, your idea for your site, or team members)? Write the numbers for the questions whose answers have changed, and their new answers.
Team is now:
+ Caroline Meeks MIT ‘85 carolineroos@alum.mit.edu
+ Linda Kukolich MIT ‘86 lindakukolich@alum.mit.edu
+ Elizabeth Brooks MIT ‘84 lizbrooks@alum.mit.edu

###Which features are implemented. To what extent are they complete?
From our MVP List the following are complete
* Data from at least 2 sensor  sources (wunderground, nortek))
* One month of data
* Ability to create multiple line graphs on a page choosing data from these two sources
* At least 2 time frames or the ability to change the date range
* Link that can be clicked that displays some information about the data source and its sensors.
* Look and Feel that matches the Thompson Island site

From our full vision list the following are complete:
* Ability to save png of the graphs
* A third data source

###Are there any features you wanted to include in your MVP from Milestone 1 that are not complete? If so, which are they?
The following is not complete:
* Ability to view data in table format

We spoke to Thompson Island staff today and we decided to download the data instead of viewing because there is so much of it.


###What additional features do you wish to implement? How far along on those features are you?
High Priority:
* Load more data
* Automatically update with current data
* Custom date picker
* Downlaod CSV of data

Next priority:
* Sync zoom of graphs
* Crosshairs that move together like on the wunderground beta
* Image storage and display

###What technologies are you using for the back-end? Include any frameworks if relevant.
Django/Python
###What technologies are you using for the front-end? Include Javascript frameworks such as jQuery, templating frameworks such as Handlebars.js, and other client-side frameworks such as Ember.js or Backbone.js.
Jquery, Bootstrap, Highcharts
###What is the main browser you are targeting? Must be one of our supported browsers.
Chrome, Firefox
###What implementation unknown / risks are you still facing? Consider this an exercise of imagination, not a test of confidence.
* We are currently struggling with the date picker.
* Getting current data from sites that require login
* Hosting! We have already blown well past Heroku's free database row limit
* Speed - Will this be too slow when all the data is loaded and on old computers?