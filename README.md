Overview
Using machine learning model, this project analyzes the dataset of individual’s personal characteristics, daily activities and sleep/health habits to compare the factors influencing sleep disorder. A tool is created to identify behaviors or patterns of people who are deemed “at risk” to prevent them from developing sleep disorder.

Database
Data is stored as a Sleep_health_and_lifestyle_dataset csv file

Data Preprocessing:
*Split the “Blood Pressure” column into two columns “Systolic” and “Diastolic” to have two different numerical values to place the “Sleep Disorder” with a code for people with “Insomnia” as 1 and people with “Sleep Apnea” as 2 and fill in the blanks as 0.
*Define features of the machine learning model (all except for “Sleep Disorder”) and its output (“Sleep Disorder”)
*remove “Person ID” column
*convert categorical values to dummy columns
*split the datasets into training and test data
*define the scalar for numerical values with the xtrain set and transform using the scalar
*transform the sleep disorder features 0, 1, and 2 with output folder
[0, 1, 0] is insomnia
[1, 0, 0] is no disorder
[0, 0, 1] is sleep apnea

Keras Tuner Setting: 
*define the function to provide the best possible model for creation
*activation function, add first layer of model with initial inputs (number of features from x set)
*use softmax activation feature for output layer to have different values (one of the three categories)

Hyperparameter Evaluation and using optimized parameters for model
*find the best hyperparameter for the model through trial and error for keras tuner to work
Activation function: tanh
Start with 5 neurons
Add 2 extra hidden layers and 5 neurons each
Activation function: Softmax for output layer
*train 216 parameters based on parameter model
*compile with 100 epochs
*best accuracy ~93% based on train set
*accuracy ~89% based on test set so very effective

Prerequisites
*Pandas for data manipulation and transformation
*Tensor Flow for deep learning framework and neural networks

Summary of Results
*bar graph: average age of this diverse age group (27-59) dataset: 43 years old
*histogram of sleep duration records: majority sleep between 7.5-8 hours which is a healthy sign as Google says, “humans who sleep more than 7 hours is healthy”, but some people sleep less than 7 hours
*box plot to show how many of those who sleep less than 7 hours have sleep disorders: insomnia lower in the spectrum and sleep apnea covers the whole range
*box plot to compare gender: fairly consistent between male and female
*scatterplot to show sleep duration and sleep quality: scattered pretty high line of correlation so sleep quality increases as sleep duration increases
*heatmap to show strong relation between sleep quality and sleep duration: red color shows strong relation and other colors to show other comparisons such as stress level, heart rate
*bar graph to show impact of stress level on sleep quality: stress level decreases as sleep quality increases
*stacked bar chart to compare BMI types (normal vs overweight) impact on sleep disorders: people with normal BMI have not much sleep disorder while people with overweight BMI have more sleep apnea and insomnia.
*bar graph to compare BMI amongst genders: more overweight females than overweight males
*graph to show daily steps relation: not much correlation
*bar graph to show gender sleep disorder correlation: men typically have no sleep disorder while women tend to have more sleep disorder perhaps due to strong correlation between sleep order and BMI
*distribution plot to show occupation with similar sleep durations: nurses have lowest sleep duration as well as doctors and teachers have low sleep duration while engineers have fairly good sleep duration which could mean engineers do not have much sleep disorders

Summary of Gradio App
