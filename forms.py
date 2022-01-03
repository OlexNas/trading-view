from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextField, FloatField
from wtforms.validators import DataRequired



class AddTokenForm(FlaskForm):
    title = StringField("Toke Name", validators=[DataRequired()], id="tags")
    amount = FloatField("Amount", validators=[DataRequired()])
    tokenPrice = FloatField("Entry price", validators=[DataRequired()])
    pricePrediction = FloatField("Price Prediction", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CheckPriceForm(FlaskForm):

    tickerName = StringField("select", validators=[DataRequired()], id="tags")
    currentPrice = StringField("Current Price", validators=[DataRequired()])
    checkPrice = SubmitField("<-check current price->")

class DeleteAssetForm(FlaskForm):

    submit = SubmitField('Delete')