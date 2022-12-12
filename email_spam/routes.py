from email_spam import app
from flask import render_template, redirect, url_for, flash
from email_spam.form import EmailForm
import imaplib
import email
from email.header import decode_header
import joblib
import os

# Load the Multinomial Naive Bayes' pkl model and TF | IDF vectorizer using joblib

# classifier = joblib.load(os.path.expanduser('~') + '/PycharmProjects/halogen/email_spam/Detection_Model.pkl')
# cv = joblib.load(os.path.expanduser('~') + '/PycharmProjects/halogen/email_spam/TF_IDF.pkl')

classifier = joblib.load('/app/email_spam/Detection_Model.pkl')
cv = joblib.load('/app/email_spam/TF_IDF.pkl')

# Spam check result variable
result = []


@app.route('/', methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():

    form = EmailForm()
    prediction = []

    if form.validate_on_submit():
        email_address = form.email.data
        app_password = form.password.data

        # Imap server
        imap_server = "imap.gmail.com"

        try:
            # create an IMAP4 class with SSL
            imap = imaplib.IMAP4_SSL(imap_server)
        except:
            flash("Please check your internet connection and try again.", category='danger')

        # authenticate
        try:
            imap.login(email_address, app_password)

            status, messages = imap.select("Inbox")

            # number of recent emails to fetch
            n = 50

            # total number of emails
            messages = int(messages[0])

            # loop through the messages
            for i in range(messages, messages - n, -1):

                # fetch the email message by ID
                res, msg = imap.fetch(str(i), "(RFC822)")

                # loop through the response in messages
                for response in msg:
                    if isinstance(response, tuple):
                        # parse a bytes email into a message object
                        msg = email.message_from_bytes(response[1])
                        # decode the email subject
                        subject, encoding = decode_header(msg["Subject"])[0]
                        try:
                            if isinstance(subject, bytes):
                                # if it's a bytes, decode to str
                                subject = subject.decode(encoding)
                        except TypeError:
                            pass

                        # decode email sender
                        sender, encoding = decode_header(msg.get("From"))[0]
                        try:
                            if isinstance(sender, bytes):
                                sender = sender.decode(encoding)
                        except TypeError:
                            pass

                        # decode date sent
                        date, encoding = decode_header(msg.get("Date"))[0]
                        try:
                            if isinstance(date, bytes):
                                date = date.decode(encoding)
                        except TypeError:
                            pass
                        new_date = date[:16]

                        # if the email message is multipart
                        if msg.is_multipart():
                            # iterate over email parts
                            for part in msg.walk():
                                # extract content type of email
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    # get the email body
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    pass

                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    content = body

                                    # Transform email body to array using TF | IDF vectorizer
                                    data = [content]
                                    vectorized = cv.transform(data).toarray()

                                    # Predict using multinomial Bayes' model classifier
                                    my_prediction = classifier.predict(vectorized)
                                    prediction.append(my_prediction[0])

                                elif "attachment" in content_disposition:
                                    # skip attachment
                                    continue
                        else:
                            # extract content type of email
                            content_type = msg.get_content_type()
                            # get the email body
                            try:
                                body = msg.get_payload(decode=True).decode()
                            except:
                                pass

                            if content_type == "text/plain":
                                content = body

                                # Transform email body to array using TF | IDF vectorizer
                                data = [content]
                                vectorized = cv.transform(data).toarray()

                                # Predict using multinomial Bayes' model classifier
                                my_prediction = classifier.predict(vectorized)
                                prediction.append(my_prediction[0])

                        if content_type == "text/html":
                            # skip HTML
                            continue

                    if len(prediction) == 0:
                        prediction.append(0)

                result.insert(-1, {'date': new_date, 'sender': sender, 'subject': subject, 'prediction': prediction[-1]})
                # close the connection and logout

            imap.close()
            imap.logout()

            return redirect(url_for('result_page'))

        except:
            flash("Invalid email or application password", category='danger')

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg[0], category='danger')

    return render_template("home.html", form=form)


@app.route("/result", methods=['GET', 'POST'])
def result_page():
    return render_template("result.html", result=result[-50:])


@app.errorhandler(404)
def invalid_route(e):
    return render_template("error_404.html")
