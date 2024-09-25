from flask import g, render_template, request, redirect, make_response, url_for, render_template_string, flash, current_app
from flask import Blueprint
import os

from tranq.models.models import User, Token, Trip, Flight
from tranq.utils.utils import DateFormatter
from tranq.api.apisnippet import FlightDataRequest

from openai import OpenAI
from pypdf import PdfReader


emails = Blueprint('emails', __name__)
date_formatter = DateFormatter()


client = OpenAI(api_key='sk-svcacct-JOkFYQH_RUWl7Km6JsdZsZDXJw-3ob85a67c5W9OIw43nHvu39w6ghLKURd_v6mLnWe_zQ-nwAQ6KT3BlbkFJ5RhObYx684fdMfO-uYXUd0lZUUrhipq-BORwKWbJdYaih-PiHsK4W9lEW2lBtJfdBle1xsYM97uAA')


def get_chat_completion(prompt, model="gpt-4o-mini"):

    # Creating a message as required by the API
    messages = [{"role": "user", "content": prompt}]

    # Calling the ChatCompletion API
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=0)

    return response.choices[0].message.content


def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    number_of_pages = len(reader.pages)
    text = ""
    for page_num in range(number_of_pages):
        page = reader.pages[page_num]
        text += page.extract_text()
    breakpoint()
    return text


#################################################################################################
@emails.before_request
def before_request():
    g.user_model = User(g.db)
    g.token_model = Token(g.db)
    g.trip_model = Trip(g.db)
    g.flight_model = Flight(g.db)


@emails.get("/process_email")
def email_text_input():
    return render_template("process_email.html")


#################################################################################################
#################################################################################################
@emails.post("/process_email")
def process_email():
    print("********************************************************************************")

    # if 'pdf_file' not in request.files:
        # flash("No file part", "error")
        # return redirect(url_for('db_views.emails.process_email'))

    file = request.files['pdf_file']
    print(file, "************************************************************************************************************")

    # if user selected a file before submitting
    # if file.filename == '':
        # flash("No selected file", "error")
        # return redirect(url_for('db_views.emails.process_email'))

    if file and file.filename.endswith('.pdf'):
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

    print(file.filename, filepath, "********************************************************************************")
    print("********&&%$^$%^%&*^%&^%$&^$%&************************************************************************")

    #     flash(f"File {file.filename} uploaded successfully!", "success")
    # else:
    #     flash("Invalid file format. Only PDF files are allowed.", "error")

    pdf_to_text = extract_text_from_pdf(filepath)
    response = process_pdf_text(pdf_to_text)

    # process the email here, then render the template and showcase the output
    return render_template_string("<pre>{{response}}</pre>", response=response)


def process_pdf_text(pdf_to_text):
    req = f"""
        From the following html retrieve the information I will ask for. DO NOT infer anything, WRITE EVERYTHING AS IT IS EXACTLY ON THE HTML. 
        The date format as well as the overall shall be the same as in my example. Date format -> dd-M-Y Be sure not to infer any information if it is not provided, it is preferred to stay blank like, for example below, departure terminal was left blank:
        “ Departure Terminal: "
        The same rule applies to all other entries, if not provided, is left empty.
        Example scheme of the information needed below:
        Passenger Information: 
        - Name: Poghosyan Larisa Ms (ADT) 
        - Booking Reference: UJIGV7
        - Ticket Number: 080 2420057290
        - Issuing Office: LOT.COM, UNITED KINGDOM, LONDON
        - Telephone: +44 2037888001 

        Flight 'all the flights one by one':
        - Flight Number: LO279 
        - Airline: LOT POLISH AIRLINES
        - Departure City: WARSAW
        - Departure Airport: FREDERIC CHOPIN 
        - Departure Terminal:
        - Departure Date: 22-10-2024
        - Departure Time: 15:30
        - Arrival City: LONDON
        - Arrival Airport: HEATHROW
        - Arrival Terminal: 2
        - Arrival Date: 22-10-2024
        - Arrival Time: 17:20
        - Seat: 13D
        - Baggage Allowance: 1PC
        - Duration: 02:50
        - Class: STANDARD, T
        - Booking Status: OK
        Text:
        {pdf_to_text}
        """

    response = get_chat_completion(req)
    return response







# @emails.post("/process_email")
# def process_email():
#     user_text = request.form['text']
#     # user_text = f'<p>{user_text}</p>'

#     response = get_chat_completion(f"Translate into German: {user_text}")

#     email_html = """
#         <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title></title>
#     </head>
#     <body>
#         <div>
#             <h1>Processing Emails</h1>
#             <p>{{ response }}</p>
#         </div>
#     </body>
#     </html>
    # """
    # # process the email here, then render the template and showcase the ourput
    # return render_template_string(
    #     email_html,
    #     response=response
    # )
