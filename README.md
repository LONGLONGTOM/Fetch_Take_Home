# Fetch_Take_Home
Hi, thank you for the opportunity and welcome!
To run my program, you con do the following:
1. Download the code from github, run web.py. You will see the link for a webpage. Copy the link to a brower and see the webpage.
2. Download the code from github, run this command:
   
   docker build -t my-flask-app .
   
   docker run -p 5000:5000 my-flask-app
   
   Copy the link generated to the browser and see the webpage.
3. run the follwing command:
   
   docker pull harveyyliu/my-flask-app:tag
   
   docker run -p 5000:5000 harveyyliu/my-flask-app:tag
   
   Copy the link generated to the browser and see the webpage.

Here is my explantion for my work.


In Model_Train.ipynb, I perform data visualizations, stationary and seasonlity check to examine structures of the data, and decisde SARIMA to be the ideal model. Therefore, I trained and fined the model using data_daily.csv and save the model to sarima_result.pkl. When building the mode, I decide to let the model predict each day of 2022 and aggregate the prediction results for every month, because this way is much more accurate and we do not lose information.


In web.py, I built a small webpage using Flask to do model inference for result of each month and each day in 2022.
The templates folder conatins corresponding html file. 


Thank you so much for your consideration!
