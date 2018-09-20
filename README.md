Practical Python: Tree Quiz
============================
This project’s goal is to prove my understanding and capabilities in developing web applications using Python, HTML, CSS and JavaScript. It is the Milestone Project in Practical Python module for the Code Institutes Diploma in Software Development.

The Tree Quiz is a pictorial quiz, where the user is asked to identify the native Irish trees shown in 10 pictures. The user and the users game playing history is stored, so that the user can leave the game and return at any stage by simply signing in with the same username. This allows for multiple users to play at the same time so long as they are signed into different browsers using different usernames. A leaderboard of the top 5 scores is also maintained.

UX
----
This application was developed with an educational end use in mind. The user/s would use this application to be more familiar with the native flora of Ireland by repeating the quiz until they score 100%.  

__User Stories__

User stories were developed to guide game play and desired functions.

* As a site visitor I expect to have a access to instruction before deciding to sign in and play. 
* As a site visitor I expect to be able to view the leaderboard without having to sign in.
* As a player I should be able to enter my username before starting the game.
* As a player I expect that only valid username entries will be accepted.
* As a player I expect that I will be informed of if the username entered has already been used and if so what is the users playing status.
* As a player I should to have each tree image presented to me one at a time, with a form to enter my answer.
* As a player I should be informed if my answer was right or wrong before moving on to the next image. 
* As a player I should expect to have two attempts at answering each question, scoring higher marks for submitting a correct answer on the first attempt..
* As a player I should see my progress at each question in the quiz, with the question number, attempt and current score clearly shown.
* As a player on completing the game I expect to have my scores validated against other players and my own past scores, and be shown the leaderboard.
* As a player after seeing the leader board I should be given the option to exit or play again.

__Mockups__

Mockups were developed using a free online mockup tool, FluidUI. The mockup wireframes allowed for greater visualisation of the how the application should look before starting creating the HTML templates. 
JPGs of the mockups can be found at GitHub repository for the project at:

https://github.com/dcasey720/tree_quiz/tree/master/mockups.

Features
-----------------
In this section, you should go over the different parts of your project, and describe each in a sentence or so.

__Existing Features__



__Features Left to Implement__
* Include green/ read to indicate if the answers were wrong or right.
* Develop code so that the images are not shown in the same sequence during each game.
* Include more trees, make the game longer.
* Display a hint for the second attempt at a question.
* On the Game Over screen show all the pictures, displaying which ones were answered correctly and which ones were wrong. Use a list to save if the user got each question wrong of right.

Technologies Used
-----------------------

* __FluidUI__ (https://www.fluidui.com) was used to develop wireframes for the initial UI design mockups.
* __Python3__ (https://docs.python.org/3/) was used to develop all back-end code.
* __HTML5__ (https://www.w3.org/TR/html5/) was used to develop front-end templates.
* __CSS__ (https://www.w3.org/Style/CSS/) was used for styling of front-end templates.
* __Flask__ (http://flask.pocoo.org/) microframwork was used through out the project in interacting between the back-end code and front-end templates, rendering templates and aquiring data.
* __json__ (http://www.json.org/) was used to store and access game play data.
* __Bootstrap 3.3.7__ (https://stackpath.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css) was used for more effective CSS layout styling. 
    - __Boostrap Grid__ system was used for content arrangment and responsive behavour when moving between different screen sizes
    - __Boostrap Navbar__ was used for the main navigation. Collapsible menu was utilised for lower screen resolutions.
    - __Bootstrap Forms Controls__ were used for the user actions.
* __Font-Awesome 5.3.1__ (https://use.fontawesome.com/releases/v5.3.1/css/all.css) was for the icons in the header and footer.
* __Unittest__ (https://docs.python.org/3/library/unittest.html) unit testing framework was used for the testing of none template rendering functions.

Testing
-----------------------

Deployment
------------------------

__Hosting__

The application is hosted on Heroku and can be accessed at:

https://irish-tree-quiz.herokuapp.com/

__Deployed vs Development__

There is only one code difference between the deployed and development application version.

|       Code       | Deployed | Development |
| ---------------- | -------- | ----------- | 
| app.run(debug= ) |  False   |   True      |       

Leaderboard.json and players.json are updated during game play and so may differ between the development and deployed versions.

Credits
-----------------------------
__Media__

The photos used in this site were obtained from:

https://treecouncil.ie/tree-advice/native-species/