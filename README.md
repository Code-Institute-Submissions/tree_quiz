Practical Python: Tree Quiz
============================
 
This is the Milestone Project in Practical Python module for the Code Institutes Diploma in Software Development.
The porject shows my understanding and capabilities in developing web applications using Python, HTML, CSS and JavaScript.

The Tree Quiz is a pictorial quiz, where the user is asked to identify the native Irish trees shown in 10 pictures. 
The user and the users game playing history is stored, so that the user can leave the game and return at any stage by simply signing in with the same username. 
This allows for multiple users to play at the same time so long as they are signed into different browsers using different usernames. 
A leaderboard of the top 5 scores is also maintained.

UX
----
This application was developed with an educational end use in mind. 
The user in mind would use this application to test their knowledge of Irish tree species and by repeating learn to identify all of the trees.

__User Stories__

User stories were developed to guide game play and desired functions.

* As a site visitor I expect to have a access to instruction before deciding to sign in and play. 
* As a site visitor I expect to be able to view the leaderboard without having to sign in.
* As a player I should be able to enter my username before starting the game.
* As a player I expect that only valid username entries will be accepted.
* As a player I expect that I will be informed of if the username entered has already been used and if so what is the users playing status.
* As a player I should to have each tree image presented to me one at a time, with a form to enter my answer.
* As a player I should be informed if my answer was right or wrong before moving on to the next image. 
* As a player I should expect to have two attempts at answering each question, scoring higher marks for submitting a correct answer on the first attempt.
* As a player I should see my progress at each question in the quiz, with the question number, attempt and current score clearly shown.
* As a player on completing the game I expect to have my scores validated against other players and my own past scores, and be shown the leaderboard.
* As a player after seeing the leader board I should be given the option to exit or play again.

__Mockups__

Mockups were developed using a free online mockup tool, FluidUI. The mockup wireframes allowed for greater visualisation of the how the application should look before starting creating the HTML templates. 
JPGs of the mockups can be found at GitHub repository for the project at:

https://github.com/dcasey720/tree_quiz/tree/master/mockups.

Features
-----------------

__Existing Features__
* The home page greats the user with a brief intro, provides a text box to sign in, as well as links to the leaderboard and game instructions
* Players.json file stores the game data for all players as a list of dictionaries. In the format of:  
        
          [{"cur_score": 0,  
            "attempt": 2,   
            "name": "name1"  
            "cur_question": 5,  
            "high_score": 60,  
            "game_num": 2}]

* If the player signs in with a username already used it will load up the players data on record.
* The username must be of the form "^[a-zA-Z0-9]+$". This requirement is set in the html code.
* Once the player enters a username a brief welcome message is displayed, informing the player of their current game status. This allows the user to enter in a different username if they are a new player, before playing the game.
* Each questions data is stored in a tree_lib.json as a list of dictionaries. in the format of:
       
         [{"question": 1,  
         "tree_image": "/static/img/arbutus.jpg",  
         "tree_name": "arbutus"}]

* As the game progresses the question number is incremented by one and the relevant image and tree_name/answer are retrieved using the question number.
* The player is presented with the image of a tree, a brief request to enter the tree name, along with an input box for the answer and submit button.
* The answer may not contain any spaces and must be of form "^[a-zA-Z0-9]+$". This requirement is set in the html code.
* The player can keep track of their game with the progress states displayed on screen, current question, attempt number and current score are displayed. The attempt number is hidden in smaller screen resolutions.
* Once the player submits an answer the answer is processed, there data is updated in the players.json file and a feedback message is displayed on the screen.
* If the player answers correctly a green tick and  congratulatory message is displayed and 'Next Question' button is made visible.
* If the player answers incorrectly on their first attempt at the question, a red x with a message stating that their answer was incorrect and they have another attempt, is displayed,
* If the player answers incorrectly on their second attempt at the question, a red x with a message stating the correct answer is displayed, along with the 'Next Question' button.
* The player gets 10 points for every question answer correctly on their first attempt and 5 points for answered correctly on their second attempt.
* Once the 10th question has been submitted the player is presented with a Game Over screen, displayed their final score and a a game feedback message. 
* The feedback message compares the players current score to their high score on record as well as to the leaderboard and displays an appropriate message.
* The a 5 ranked leaderboard is also displayed. The leaderboard data is stored in leaderboard.json. To be included in the leaderboard the player must score higher than their high score on record and higher than the lowest score on the leaderboard.
* If the player scores the same as their high score it does not make any changes, but if the score is the same as the lowest score on the leaderboard it knocks out the older player.
* From the Game Over screen the player can play the game again without having to reenter the username.

__Features Left to Implement__
* Develop code so that the images are not shown in the same sequence during each game. Some use of the random function, should be used.
* Include more trees, make the game longer.
* Display a hint for the second attempt at a question.
* On the Game Over screen show all the pictures, displaying which ones were answered correctly and which ones were wrong. Use a list to save if the user got each question wrong of right.

Technologies Used
-----------------------

* __FluidUI__ (https://www.fluidui.com) was used to develop wireframes for the initial UI design mockups.
* __Python3__ (https://docs.python.org/3/) was used to develop all back-end code.
* __HTML5__ (https://www.w3.org/TR/html5/) was used to develop front-end templates.
* __CSS__ (https://www.w3.org/Style/CSS/) was used for styling of front-end templates.
* __Flask__ (http://flask.pocoo.org/) microframework was used throughout the project in interacting between the back-end code and front-end templates, rendering templates and acquiring data.
* __json__ (http://www.json.org/) was used to store and access game play data.
* __Bootstrap 3.3.7__ (https://stackpath.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css) was used for more effective CSS layout styling. 
    - __Boostrap Grid__ system was used for content arrangement and responsive behavour when moving between different screen sizes
    - __Boostrap Navbar__ was used for the main navigation. Collapsible menu was utilised for lower screen resolutions.
    - __Bootstrap Forms Controls__ were used for the user actions.
* __Font-Awesome 5.3.1__ (https://use.fontawesome.com/releases/v5.3.1/css/all.css) was for the icons in the header, footer and quiz template.
* __Unittest__ (https://docs.python.org/3/library/unittest.html) unit testing framework was used for the testing of none template rendering functions.

Testing
-----------------------

__Code Validation__

* __Python__ was validated using http://pep8online.com/. Both run.py and test_quiz.py are pep8 compliant.
* __HTML__ was validated using https://validator.w3.org/. Due to the python code embedded in the HTML templates there were a number of errors.
* __CSS__ was validated using https://jigsaw.w3.org/css-validator/validator. No  errors were found.
* __Spelling and Grammar__ was validated using Google Docs.


__Automated Testing__

Throughout the development of this project a 'Test After - Automated Testing' approach was taken. After deciding what was needed, the function was written, manually tested 
while developing. Once a basic function was built, an automated test was written in test_quiz.py using unittest testing framework for each of the possible conditions.
As functions became more complex and interacted with other functions, these automated tests insured that the functions all maintained their required functionality. 
The tests are written quite explicitly, to ensure it is clear as to what each test is testing. This resulted in a very long repetitive testing code, but made troubleshooting simpler.

In run.py there are 10 functions that do not render html templates. 8 of these have automated tests written in test_quiz.py. The other 2 use text book code to read and write to .json files.
As the .json files would be constantly changing, these were manually tested. For all template rendering functions manual testing was performed.

The automated test_quiz.py file can be found at: 

https://github.com/dcasey720/tree_quiz/blob/master/test_quiz.py

__Visual Testing__

The dev tool within Google Chrome was used to test that the pages were displaying correctly (alignment, spacing, position etc) across different screen widths.


|                                    | Galaxy S5 | Pixel 2 | Pixel 2XL | iPhone 5/SE |	iPhone 6/7/8  | iPhone 6/7/8 + | iPhone X | iPad  | iPad Pro   | Responsive 1366 x 768 | Responsive 1680 x 1050 |  
| ---------------------------------- | --------- | ------- | --------- | ----------- | -------------- | -------------- | -------- | ------| ---------- | --------------------- | ---------------------- |
| index.html (sign-in)               | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 
| index.html (play game)             | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 
| leaderboard.html                   | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 
| instructions.html                  | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 
| quiz.html (ask question)           | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 
| quiz.html (wrong, go again)        | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 
| quiz.html (wrong, next question)   | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 
| quiz.html (correct, next question) | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 
| game_over.html                     | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 



__Manual Testing__

The following test were performed manually. Care was taken that all relevant messages were correctly displayed.
During initial testing it was noted that if the user refreshed the page during game play that questions could be skipped, 
and even increment the users score without entering an answer. The function was changed in run.py to corrrect this bug.


|                                   | Chrome (Desktop) | Edge (Desktop) | Chrome (Mobile) | Samsung Internet (Mobile)|
| ----------------------------      | ---------------- | -------------- | --------------- | ------------------------ |
| __index.html__                                                                                                     |                                                                                
| Sign in Btn (blank name)          | OK               | OK             | OK              | OK                       |
| Sign in Btn (new name)            | OK               | OK             | OK              | OK                       |
| Sign in Btn (old name)            | OK               | OK             | OK              | OK                       |
| Play Game Btn                     | OK               | OK             | OK              | OK                       |
| Refresh (reloads index.html with blank input box) | OK | OK           | OK              | OK                       |
| __quiz.html__                                                                                                      |                                                                                
| Submit Btn (blank answer)         | OK               | OK             | OK              | OK                       |
| Submit Btn (attempt 1, correct)   | OK               | OK             | OK              | OK                       |
| Submit Btn (attempt 1, incorrect) | OK               | OK             | OK              | OK                       |
| Submit Btn (attempt 2, incorrect) | OK               | OK             | OK              | OK                       |
| Submit Btn (attempt 2, correct)   | OK               | OK             | OK              | OK                       |
| Next Question Btn                 | OK               | OK             | OK              | OK                       |
| players.json updating             | OK               | OK             | OK              | OK                       |
| Refresh before submit (reloads quiz.html with same question) | OK |OK | OK              | OK                       |
| Refresh after submit (warning that form data will be re-entered, submitted answer will continue to be submitted for the next question) | OK | OK  | OK| OK|
| __game_over.html__                                                                                                 |                                                                                
| leaderboard.json up to date       | OK               | OK             | OK              | OK                       |
| players.json up to date           | OK               | OK             | OK              | OK                       |
| Play Again Btn                    | OK               | OK             | OK              | OK                       |
| Refresh (loads quiz.html with new game)| OK          | OK             | OK              | OK                       |
| __leaderboard.html__                                                                                               |                                                                                
| Sign in Btn                       | OK               | OK             | OK              | OK                       |
| matches leaderboard,json          | OK               | OK             | OK              | OK                       |
| Refresh (reloads leaderboard.html | OK               | OK             | OK              | OK                       |
| __instructions.html__                                                                                              |                                                                                
| Sign in Btn                       | OK               | OK             | OK              | OK                       |
| Refresh (reloads instructions.html| OK               | OK             | OK              | OK                       |

Multiplayer paralelel play was tested by signing in with the two usernames in different browsers (Chrome & Edge) and answering questions at the same time.
Players.json updated correctly without the seperate games conflicting.
It was also tested if the same username was playing on two different browsers at the same time. The player would be unaware except that questions would be skipped as they are already been answered by the other browser.

Deployment
------------------------

To deploy the app requires flask to be installed on the machine and the machine should be running python 3.4.3.
All requirements can be found in https:  
//github.com/dcasey720/tree_quiz/blob/master/requirements.txt
It was noted in development that if python verion was set to the newer python 3.6, that the flask framwork could not be acceessed.

__Data Folder__

The data folder contains the dynamic .json files to store game play. 
Leaderboard.json and players.json are updated with every game. 
For the the initial game both these must be occupied with an empty list [].

https://github.com/dcasey720/tree_quiz/blob/master/data/tree_lib.json
 

__Static Folder__

Contains the main.css file for styling within the css folder, all the images for the quiz as well as template images.
The static folder also contains tree_lib.json, a list of dictionaries of the questions and address to the respectful images.

Static folder can be found at:  
https://github.com/dcasey720/tree_quiz/tree/master/static

__Templates Folder__

The templates folder contains all the html templates for the front end of the application. It can be found at:  
https://github.com/dcasey720/tree_quiz/tree/master/templates

__Hosting__

The application is hosted on Heroku and can be accessed at:

https://irish-tree-quiz.herokuapp.com/

A Procfile is required by Heroku to know what language to launch the application as. 
In Heroku the config variables were set:

IP: 0.0.0.0  
Port: 5000

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