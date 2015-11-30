# Spot My School

Spot My School makes it easy for aspiring law students to identify the perfect law schools for them. Created by Eileen Conner, this app compares each user's GPA and LSAT score against a SQLite database of law school statistics to produce a list of great potential law school choices.

## Table of Contents
* [Welcome to Spot My School](#spotmyschool)
* [Technologies Used](#technologiesused)
* [Version 2.0](#v2)
* [Author](#author)

## <a name="spotmyschool"></a>Welcome to Spot My School

#### Introduction

Spot My School analyzes admission data from [the American Bar Association’s 2013 questionnaire](http://www.americanbar.org/groups/legal_education/resources/statistics.html), compares it to each user’s GPA and LSAT score, dynamically generates individualized lists of recommended law schools, and categorizes the results by likelihood of admission. 

![Spot My School homepage](/static/images/screenshots/spot_my_school_screenshot.png)

#### School matches

User results are produced via SQLAlchemy queries and organized by closeness to each school's GPA and LSAT statistics. Law schools are classified as safety schools (user stats at or above the 75th percentile), match schools (user stats between the 75th and 50th percentile), stretch schools (user stats between the 50th and 25th percentile), and split schools (one user stat above the 75th percentile and one below the 50th percentile), all via a series of class methods on the Python back end. Users can then create a well-rounded group of school choices and use it to manage their application process.

![School matches](/static/images/screenshots/match_query_screenshot.png)

#### School profile

Users can learn more about each law school through individual school profiles, which are dynamically generated through database queries. These pages display a Google Maps location map, Chart.js bar charts comparing the user's GPA and LSAT to admitted student statistics at the 25th, 50th, and 75th percentile, and tuition and living expense numbers. They also include a link to each school's website for further research. 

![School profile](/static/images/screenshots/school_profile_screenshot.png)

#### User profile

Users can quickly and easily add chosen law schools to their personalized list via AJAX buttons throughout the app. This list is displayed on the user's profile page. There users can ensure they have chosen a good distribution of schools, change their stats as needed, and keep track of their submitted applications. An integrated Google Map shows the location of each school, while color-coded pins correspond to the user's likelihood of admission. A Chart.js doughnut chart shows the distribution of selected schools.

![User profile](/static/images/screenshots/user_profile_screenshot.png)

## <a name="technologiesused"></a>Technologies used
* [Python](https://www.python.org/) - back-end code models, seeds, and accesses database, manages incoming data, and dynamically serves data to webpages.
* [Flask](http://flask.pocoo.org/) - web framework that serves pages dynamically according to user actions.
* [Jinja](http://jinja.pocoo.org/docs/dev/) - Python templating language that allows use of variables to create webpages from database data.
* Javascript - front-end dynamic web design.
* [JQuery](https://jquery.com/) - JavaScript library allowing simplified, easily readable DOM manipulation and event handling.
* AJAX/JSON - used for buttons throughout app, letting users quickly add or change their information in the database without interrupting their experience.
* [SQLite](https://www.sqlite.org/) - database containing complex law school data from ABA 2013 questionnaire.
* [SQLAlchemy](http://www.sqlalchemy.org/) - streamlines database queries in Python codebase.
* HTML5/CSS - displays and styles webpages.
* [Bootstrap](http://getbootstrap.com/2.3.2/) - UI framework that allows responsive website design.
* [Google Maps](https://developers.google.com/maps/) - displays maps on law school profile pages and user profiles.
* [Chart.js](http://www.chartjs.org/) - displays charts dynamically comparing user stats to school stats and noting number of student school picks from each admission chance category.
* [GeoPy](https://pypi.python.org/pypi/geopy) - back-end implementation generates latitude and longitude points on seeding of database, taking load time off front end and ensuring API limits are respected.

## <a name="v2"></a>Version 2.0
* Increase user security: hash passwords before saving to database, possibly implement OAuth or other login system.
* Update database with new statistics when 2014 ABA questionnaire becomes available.
* Improve test coverage.
* Add application management tools to help users manage deadlines; possible integration with Google Calendar.

## <a name="author"></a>Author

Eileen Conner is a software engineer from Mountain View, CA.