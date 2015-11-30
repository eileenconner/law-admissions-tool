# Spot my School

Spot my School makes it easy for aspiring law students to identify the perfect law schools for them. Created by Eileen Conner, this app compares each user's GPA and LSAT score against a sqlite database of law school statistics to produce a list of great potential law school choices.

## Table of Contents
* [Welcome to Spot my School](#spotmyschool)
* [Technologies Used](#technologiesused)
* [Version 2.0](#v2)
* [Author](#author)

## <a name="spotmyschool"></a>Welcome to Spot my School

![Spot my School homepage](/static/images/screenshots/spot_my_school_screenshot.png)

#### Introduction

This app analyzes admission data from the American Bar Association’s 2013 questionnaire, compares it to each user’s GPA and LSAT score, dynamically generates individualized lists of recommended law schools, and categorizes the results by likelihood of admission. 

![School matches](/static/images/screenshots/match_query_screenshot.png)

#### School matches

User results are organized by closeness to each school's GPA and LSAT statistics. Law schools are dynamically classified as safety schools (user stats at or above the 75th percentile), match schools (user stats between the 75th and 50th percentile), stretch schools (user stats between the 50th and 25th percentile), and split schools (one user stat above the 75th percentile and one below the 50th percentile). This helps users create a well-rounded group of school choices, which they can then use to manage their application process.

![School profile](/static/images/screenshots/school_profile_screenshot.png)

#### School profile

Users can learn more about each law school through dynamically created school profiles. These pages provide a location map, charts comparing user GPA and LSAT to admitted student statistics, and tuition and living expense numbers. 

![User profile](/static/images/screenshots/user_profile_screenshot.png)

#### User profile

Users can easily add chosen law schools to a personalized list, accessed via their individual profile. There they can ensure they have chosen a good distribution of schools, change their stats as needed, and keep track of their submitted applications.

## <a name="technologiesused"></a>Technologies used
* [Python](https://www.python.org/)
* [Flask](http://flask.pocoo.org/)
* [Jinja](http://jinja.pocoo.org/docs/dev/)
* Javascript
* [JQuery](https://jquery.com/)
* AJAX/JSON
* [SQLite](https://www.sqlite.org/)
* [SQLAlchemy](http://www.sqlalchemy.org/)
* HTML/CSS
* [Bootstrap](http://getbootstrap.com/2.3.2/)
* [Google Maps](https://developers.google.com/maps/)
* [Chart.js](http://www.chartjs.org/)
* [GeoPy](https://pypi.python.org/pypi/geopy)

## <a name="v2"></a>Version 2.0
* Increase user security: hash passwords before saving to database
* Add application management tools to help users manage deadlines; possible integration with Google Calendar

## <a name="author"></a>Author

Eileen Conner is a software engineer from Mountain View, CA.