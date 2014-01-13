
#Team: Girls & Buoys

###Milestone 1
 http://6.470.scripts.mit.edu/2014/contest/milestones

##Summary
We are creating a site that allows Boston area residents, especially Boston Public School (BPS) children and teachers to learn about the environment at Thompson Island.  

Located in the Boston Harbor Islands National Park area, Thompson Island is just one mile from downtown Boston.  Over 4000 BPS students visit the island for educational programs each year.

Over the years Thompson Island Outward Bound, the National Park Service, and UMass Boston have all placed environmental sensors on the island.  There are weather stations, buoys, a hydraulic sensor in the salt pond, cameras, and more!  However, each instrument has its own data access, typically a vendor website, often requiring a username and password.  In practice, it is almost impossible for teachers and students to use this data or compare information from different sources.

Our site will bring all the data together in one place and make it exciting and fun to explore.

##User Research
###1. What problem does your application address, and how does your application address it?
Only a mile from Boston, but a million miles from the consciousness of its urban residents lies Thompson Island.  A natural environment, being preserved, studied and used as a classroom, there is only one piece missing.  The educational programs being done on the island are not using the rich collection of data gathered there.  Thompson Island knows that good access to data would infuse more math and greater scientific rigor into their curriculum.  The data would both inspire and answer questions, and deepen thinking about the island and the environment.

Lots of fascinating environmental data is being collected but it is not in an accessible or usable format.


###2. What are the killer features of your application?
Data exploration of a rich, varied data set, from a place where students already go and have first-hand experiences.
Giving teachers and students agency by allowing them to choose which datasets to view and compare.
###3. Identify and briefly describe your target demographic. Who do you envision using your site?
The primary users are middle school (5th to 8th grade) students and their educators (teachers, Thompson Island instructors).
Additional users include, Thompson Island Staff, UMass Boston researchers, visitors to Thompson Island (the Island is used for conferences and is open to the public on weekends).  Thompson Island plans to hire a student intern to expand the site.  We also plan to design the codebase so that other environmental centers could use it as a starting point for a site that explores their data.
###4. Develop at least one use case for your site. This should be a list or table demonstrating a sequence of user actions and website responses that occur when a user attempts to complete a core task on your site. Make sure to indicate the task the user is trying to complete.
####Primary Use case: Supporting classroom instruction
Before or after their class trip to Thompson Island, the teacher and students brainstorm questions about the environment at Thompson Island that align with their science class’ studies of Weather and Water.  They choose some questions that they think the sensors on Thompson Island might help them answer.  
For this example we will use “What affects the algae levels in the salt pond?”  This graph from the hydrology sensor website gives some hints as to why this is an interesting question.

Right now all you can see is last weeks data, there is not a UI to graph other time frames. There is also no way to graph the tides, the weather, the water temperature etc.
Users will go to our site and select:
* The date range
* Data they want to display.  In this use case it might include:
   * Chlorophyll
   * Salinity
   * Tides
   * Air Temp, water temp at 3 depths
   * Wind speed and direction
   * Percent cloud cover
   * Precipitation
   * Dissolved Oxygen
   * Photosynthetically available radiation (PAR)
   * Images of an Inlet on the island automatically taken several times each day.
Users will get a page where they can add as many graphs as they want to view on one page.
While viewing graphs users can:
* View data in tabular form
* Download graphs in image form
* Download data in CSV format
* Save a graph to “MyGraphs”
* View statistics for each graph such as Min, Max, Mean, STD
* Make a prediction about the measurement for some time in the future (what will the average chlorophyll level be tomorrow?) and check how they did when the data is collected.
###Personas
Middle School Student: Bobby is a 6th grade student at Orchard Gardens K8 school.

Teacher: Mr. Orchard teaches math and science at Orchard Gardens

Thompson Island Employee: Paul creates curriculum, trains Thompson Island Educators and some days leads groups himself on Thompson Island.

UMass Boston Researcher: Ben is a grad student at UMass Boston and is using some of the data from the island for his research projects.

UMass Boston Intern: Bondi is a undergraduate at UMass Boston and has been hired with funds from the National Park Service, as an intern, to work on a data site for Thompson Island.

Non Boston High-Schooler doing a programming project:  Phyllis is a high school student in Philadelphia.  She has been to educational programs at John Heinz at Tinicum environmental center.  For her high school service project and as an independent study in computer science she wants to create a data exploration site for John Heinz, which has some of the same monitoring sensors as Thompson Island.

5th grader at Orchard Gardens BPS Student: Sam is an active 5th grader, reading slightly below grade level, going to Thompson Island for the first time.

10th grader from Orchard Gardens now attending Boston Latin: Samantha has been going to programs at Thompson Island since 5th grade. 

##Design Philosophy:

A design principle in childrens software made popular by One Laptop per Child and Sugar Labs  is “Low Floor, No Ceiling” this means it should be very easy to get started but that the design should not keep the students from moving to complex ideas. 

Our “Low Floor” user would be, Sam, a fifth grader, reading below grade level with a short attention span.  Our “high ceiling user” is Samantha a 9th grader who has been out to Thompson Island several times and now wants to use the data as part of her science fair project.  

When Sam first comes to the graphing page it should already have 2 or 3 graphs of interesting and easy to understand data.  Other interesting things to graph should be one click away from being shown.  The page should default to an interesting time range with other time ranges one click away.

Samantha needs to be able to find all the data, even things like the voltage level on the bird song recorder.  Samantha needs to be able to set custom date ranges and download the data into a spreadsheet for further analysis.

###“Competitive Landscape”

We looked at a few sites and discussed them with the Thompson Island leadership.  

Many of our ideas are inspired by Weather Underground, especially their new Beta site.

http://preview.wunderground.com/cgi-bin/findweather/getForecast?query=zmw:02101.1.99999

Note that WUnderground focuses on forecast and we are focusing on historical data, however there are still many things to like about this page.

Things to like and emulate:
* Small graphs, stacked on top and synced up by time.
* The line that moves across the graph.
* The light grey that shows day vs night
* Clicking one button puts in new data, no choices on color etc.  They decide if line or bar is better
* Ability to get to a tabular view of the data
* Love the wind speed visualization.
* In general we may want to match their colors as student may also use this site.

Things to change:
* We want one line per graph as that is easier to understand. (This is a recommendation from the client)
* We want the buttons to add graphs, at least some of them, immediately visible not behind a Configure menu
* We want to easily change time frames
* We need download buttons for graphs and data
* We need what is shown in the graph to be easier to see/understand because we will have a lot more variety they WU does.  For instance a graph of wind and current will look a lot alike. We could have Temp from different devices, and water temp etc.

Another site working with this type of data is NERACOOS:

http://www.neracoos.org/datatools/historical/graphing_download

The user interface at this URL is just way too hard.  Sam is never going to get to the end of all these steps.  Which of these features might Samantha find useful?

* Ability to set a custom date
* Ability to choose an averaging period (daily, hourly averages) versus getting all the data points.
* Ability to choose when to combine data onto a single graph

A simpler graph from NERACOOS:

http://www.neracoos.org/datatools/climatologies_display

In this graph, I like how the range of data is displayed as an area on the graph. It also has just a few options inviting exploration.

However, a serious issue is that when you change the location via the drop down menu nothing happens for several seconds while it computes the new graph. Our site definitely needs to have a “Loading” icon pop up as soon as the user clicks a button.  

###Design Iterations

See image files.







###Design Pro’s and Cons


####Design 1 (Black board)
Pros:
1. One chart, allowing easy comparison of data
2. Data is all in one place
3. Allows various ways to access the data (visual, numeric, downloads)
Cons:
1. One chart, confusing younger users about what each line is and what it means
2. Date selectors hard to work with
3. ComboBoxes to select data to display disorganized


####Design 2 (Balsamiq mockup)
Pros:
1. One graph per data stream
2. Less confusing than previous mockup
3. Cleaner design
Cons:
1. Drop downs hide info from naive users, making it hard for them to find the data sources they want
2. Options are so limited that experienced users may not be able to quickly meet their goals
3. Date selectors still hard to work with


####Design 3 (White board)
Pros:
1. Graphing new data sources is now just one click.
2. Starts with graphs shown for instant gratification
3. Date range radio buttons simplify selection of time spans
Cons:
1.  May be very difficult to implement
2. There is a limit to the number of data sources that can be displayed simultaneously with comprehension
3. Use of greek letter Sigma will obscure the meaning 

##Minimum Viable Product


###1. the proper functioning of your application?
* Data from at least 2 sensor  sources (wunderground, nortek))
* One month of data
* Ability to create multiple line graphs on a page choosing data from these two sources
* Ability to view data in table format
* At least 2 time frames or the ability to change the date range
* Link that can be clicked that displays some information about the data source and its sensors.
* Look and Feel that matches the Thompson Island site

We feel this MVP would be valuable to Thompson Island and that nothing critical is missing.

###2. What features do you plan to leave out of the MVP? How critical are they to the proper functioning of your application?
* Data from other sensors and external websites (we have a list of about 8 potential data sources right now, here are a few specifics:
   * Still images from cameras on the island the ability to display them and compare them with data.
   * Sound files from the birdsong monitor
   * Video from videos camera
* More the one month’s data
* Graphs that compare the same data over different year
* Graphs that show live conditions, fetch new data and change with javascript as you watch
* User Login and features that depend on login
   * Save to mycharts
   * Predictions
      * Gamification of prediction.
   * Integration with Google Apps for login
   * Ability for students to create accounts without revealing or having our site store any personally identifiable information (PII)
* Statistical information on the data
   * Click on a statistic and see it visualized on the graph
      * Show a line for Average and Median
      * Highlight the point for Max, Min
      * Show a range for St. Deviation
* Specialized charts for wind and current (wind roseish probably)
* Maps that show where all the sensors are.Ability to drag and drop graphs to rearrange
* Ability to save png of the graphs and CSV of the data
* Greater control over date ranges
* Ability to put two variables on the same graph.
   * With the same Y axis
   * With different Y Axis
   * Provide statistics about correlation
As you can see, there are many good and important ideas.  We know we will not get to all of them in this project so we will prioritize using agile methodologies. 
###3. Are there any other aspects of your application that are reduced in your MVP? Examples including limited fake datasets, stylistic concerns, security concerns, etc.
We will use real data from our first two data sources.  We may not completely match the Thompson Island style but we should be recognizably close in our MVP.  The MVP does not include login so we won’t have security concerns yet.  However, as we start to add login and personalization we will start to have security concerns about student PII making that a potentially expensive set of features to add.
##Additional Questions:
###Who is in your team? 

Caroline Meeks MIT ‘85 carolineroos@alum.mit.edu
Linda Kukolich MIT ‘86 lindakukolich@alum.mit.edu
Jan Gunther MIT ‘85 jan@gunther.com
Max Gunther RIT CE undergrad mdg1547@rit.edu
Elizabeth Brooks MIT ‘84 lizbrooks@alum.mit.edu

Note: We know we have too many people on our team. Only Caroline and Linda can commit for the whole time period. Also since we aren’t competing and we do have a real world use, we are working together.
###Which of the themes does your application match best?

Our site fits both Urban Living, Exploration, and Transportation and Environmental Sustainability.  We allow Boston residents to explore Thompson Island, which is within the city limits of Boston and a mile from downtown giving them a greater awareness of their local natural environment. 
###3. What technology do you plan to use for your server-side programming (e.g. PHP, Ruby on Rails, etc)?
Python and Django

###4. What risks do you envision preventing you from successfully implementing your idea? 

* We are planning on using High Charts. One risk is that our javascript won’t work well enough across browsers and platforms and on older computers.  It might also be too slow to usable.
* We are concerned that hosting will be too expensive for our nonprofit.  We are also concerned about storing and serving the images and audio files.
* We may not be able to get our UI to work.
* Adding user login, to meet the class requirements, may create issues because its not really needed for the project.

###5. Competition

We are not eligible for the competition. However a number of the people on this team are job hunting so we wouldn’t mind exposure to the judges. ;)
