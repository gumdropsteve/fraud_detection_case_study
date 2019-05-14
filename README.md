# Fraud Detection Case Study

### Premise
You are a contract data scientist/consultant hired by a new e-commerce site to try to weed out fraudsters. The company unfortunately does not have much data science expertise... so you must properly scope and present your solution to the manager before you embark on your analysis. Also, you will need to build a sustainable software project that you can hand off to the companies engineers by deploying your model in the cloud. Since others will potentially use/extend your code you NEED to properly encapsulate your code and leave plenty of comments.

### Overview
- The Team's slideshow presentation can be found [here](https://docs.google.com/presentation/d/18Cjmb0vYKc3gODhvI9Pd0EpG34irc41pNJ-zUGMSC64/edit?usp=sharing)
- For an understanding of the project, see the [overview](https://github.com/gumdropsteve/fraud_detection_case_study/blob/master/overview_from_gschool.md) provided by Galvanize

### Model
- We applied Gradient Boosting to predict the probability of any event being fraud
- As a baseline, we attempted predicting fraud probability based on  total fraud rate.  
  - This resulted in a log loss of 0.33 
- Our model  achieved a log loss of 0.06

- Predicted chance of fraud Thresholds
  - Low: up to 0.5% 
  - Med: 0.5% to 70% 
  - High: x > 70%
- Fraud detection
  - Medium Threshold:
    - Model detects 99% of fraud
    - 44% FPR
  - High Threshold:
    - Model Detects 78% of Fraud
    - 0.4% FPR




Fraud Detection in Event Postings (Galvanize g88 - Spring 2019)
