## Inspiration
As college students,budget constraints has always been a reality we have to face.Not a day goes by without borrowing or lending money to your friends.In such context splitwise has become an integral part in campus life.Fampay as we all know,is the neobank for genz students.Our idea aims to unlock the true potential of Fampay by integrating it with splitwise making it the ultimate e-wallet for the genz students.
## What it does
1. College students can now lend and borrow money with their peers in an organized fashion keeping an account of their balances on Fampay.
2. It adds a fun gamified element in the form of spinning wheel.The one whose name pops pays for the treat!
3. Provides a peer to peer lending deliquency predictor so that you can now find out who is never going to pay you back :)
## How we built it
- The backbone of the website is made with Django framework.
- We integrated it with open source splitwise API's.
- A randomizer was also made in the form of a wheel using the view functions and rendering html files.
- The frontend was based on html,css,javascript 
- lending club dataset was used which contains information about peer to peer lending.The original datasaet was tailored to match and create an appropriate analog so as to provide a proof of concpt for the problem statement.
- data cleaning and pre processing was carrried out using standard scaler one hot encoding and pca
- a ridge regression model is used with cross validation to make predictions.
## Challenges we ran into
- understanding the documentation and fetching the api's of splitwise was a task to do as we were new to it
- The html and css of spinning wheel was quite hectic and took great time to build
- an appropriate dataset to train the data was challenging to find
## Accomplishments that we're proud of
-The time limit was a challenge and we are proud to build the website in just 48 hours.
-Not giving up despite of the challenges
## What's next for Paymate
- We plan to add fun stats about friends which will make it more fun experience in group payments
- Plan to use our model as an api integrated on the fampay app which utilizes data from fampay and splitwise to make predictions on peer to peer lending deliquencies and to display a so-called credit score in a gameified fashion.
## Contributions
Thanks to Cognizance team,IIT Roorkee for organizing the hackathon
- PrakharMundra
- adityadeshpande04
- nishant-singh4
