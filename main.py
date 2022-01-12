from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, URL
from csv import writer 
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), URL(message="This is not a valid URL.")])
    open_time = StringField('Open Time (am)', validators=[DataRequired()])
    closing_time = StringField('Closing Time (pm)', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=["☕️", "☕️ ☕️", "☕️ ☕️ ☕️", "☕️ ☕️ ☕️ ☕️", "☕️ ☕️ ☕️ ☕️ ☕️"], validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Rating', choices=["💻", "💻 💻", "💻 💻 💻", "💻 💻 💻 💻", "💻 💻 💻 💻 💻"], validators=[DataRequired()])
    power_outlet_rating = SelectField('Power Outlet Rating', choices=["🔌", "🔌 🔌", "🔌 🔌 🔌", "🔌 🔌 🔌 🔌", "🔌 🔌 🔌 🔌 🔌"], validators=[DataRequired()])
    
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print(form.data)
        data_list = []
        for value in form.data.values():
            data_list.append(value)

        cleaned_data_list = []
        for n in range(len(data_list) - 2):   #To get rid of the submit=True and csrf_token
            cleaned_data_list.append(data_list[n])

        with open('cafe-data.csv', 'a+', newline='') as csv:
            csv_write = writer(csv)
            csv_write.writerow(cleaned_data_list)

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
