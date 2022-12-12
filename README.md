
# A Multi-Model based BERT-embedded system for spam detection

* The output dataset is an extension of the existing input dataset retrieved from the [SMS Spam Collection Dataset](https://www.kaggle.com/uciml/sms-spam-collection-dataset).

* This repo stores the input dataset, the dataset with the embeddings and the code used to generate this dataset.

## Architecture
![Capture](https://user-images.githubusercontent.com/47308654/206814161-0e9e918f-ee51-4cf1-9b80-87bfe33e92da.PNG)

## Overview
* This project implements a fully functional flask interfaced app written in python for spam filtering
* It employs multi-model blocks consisting of a BERT Model, Light GBM classifier and a Naive Bayes classifier 
* It reads email messages via the Google gmail API then runs it through our classifier to evaluate its content
* The result of evaluation is then presented on the front-end in three columns each containing the `Date`, `Sender`, `Subject` and `Prediction`

## Live Preview
##### Check out this [link](https://halogen-esd.herokuapp.com) to test the application with your own email
![](https://github.com/Simileholluwa/halogen-esd/blob/master/email_spam/live_preview.gif)

## Project Walkthrough
* Exploratory Data Analysis (EDA)
* Data Cleaning
* Data Manipulation
* Feature Engineering
* Applied Stemming and Lemmatization techniques (Snowball Stemmer, Porter Stemmer, and Wordnet Lemmatizer)
* Implemented Bag of Words model on the dataset
* Implemented TF | IDF 
* Model Building - Used Multinomial Naive Bayes and Light GBM Classifier
* Exported Multinomial Naive Bayes Classifier model using Joblib library
* Implemented DistilBERT - a hugging face transformer model
* Fine Tuned DistilBERT
* Developed Front End using flask
* Deployed flask app to Heroku
* Project is available for live testing via this [link](https://halogen-esd.herokuapp.com)

## Models employed
* Bidirectional Encoder Representations from Transformers (BERT)
* Light GBM (Gradient Boosting machine) Classifier
* Multinomial Naive Bayes

## Input Dataset Structure
##### The original dataset contains 5574 english messages each labelled as *spam* or *ham*. This dataset contains 4 columns:

* `v1` -> Target column specifying if the message is *spam* or *ham*
* `v2` -> The original unprocessed messages
* `Unnamed_col_1` & `Unnamed_col_2` -> Columns with mostly missing values (around 99%) that are discarded

## Encoded Dataset Structure

##### The output encoded dataset contains the same information as the input dataset plus the additional DistilBERT classification embeddings. This results in a dataset with 770 columns:

* `spam` -> Target column specifying if the message is *spam* or *ham*
* `original_message` -> The original unprocessed messages
* `0` up to `768` -> columns containing the DistilBERT classification embeddings for the message, after it being processed

## Libraries Used
* HTML
* CSS
* Bootstrap
* JavaScript
* Flask
* gunicorn
* itsdangerous
* Jinja2
* MarkupSafe
* Werkzeug
* Pillow
* Pickle
* NLTK
* Numpy
* Scikit-learn
* Pandas
* Seaborn
* Joblib
* Matplotlib
* Click
* Dnspython
* Email-validator
* Flask-WTF
* Idna
* Threadpoolctl
* WTForms

## Limitations
* Only Google email server is currently supported
* Only analyses plain texts contained in the email body

## Future implementations
* Support for multiple email servers such as yahoo and outlook
* Analysis of email html content type
* Analysis of email attachments content
* Integration with companies and businesses email servers for spam filtering

## Developers
* [Ajanaku Oluwatosin Ezekiel](https://github.com/simileholluwa)
* [Adegoke Israel](https://github.com/adegokeisrael)

## References
* [Almeida, T.A., Gómez Hidalgo, J.M., Yamakami, A. Contributions to the Study of SMS Spam Filtering: New Collection and Results.  Proceedings of the 2011 ACM Symposium on Document Engineering (DOCENG'11), Mountain View, CA, USA, 2011](https://dl.acm.org/doi/abs/10.1145/2034691.2034742)
