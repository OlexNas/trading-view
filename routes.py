import forms
from app import app
from flask import render_template, url_for, redirect, request, flash
from myModels import db, NewAsset
from datetime import datetime
from pull import client, asset_names


@app.route('/')
@app.route('/main')
def started():
    asset_id = 0
    my_assets = NewAsset.query.all()
    bitcoin = getBitcoin()

    for i in range(len(my_assets)):

        my_assets[i].current_price = getCurrentPrice(my_assets[i].assetTitle)
        asset_id = my_assets[i].id
        new_asset = NewAsset.query.get(asset_id)
        new_asset.current_price = getCurrentPrice(new_asset.assetTitle)
        a = float(new_asset.current_price)
        b = float(new_asset.assetPrice)
        c = float(new_asset.assetAmount)
        new_asset.gain_loss = float("{:.2f}".format((a - b) / a * 100))
        my_assets[i].potentialGain = float("{:.2f}".format(a * c - b * c))

        if -5 < new_asset.gain_loss < 0:
            my_assets[i].cellColor = "yellow"
        elif new_asset.gain_loss > 0:
            my_assets[i].cellColor = "green"
        elif new_asset.gain_loss < -5:
            my_assets[i].cellColor = "red"

    return render_template('account.html', my_assets=my_assets, asset_id=asset_id, bitcoin=bitcoin)


def getBitcoin():
    tickersPulls = client.get_ticker()["ticker"]

    for i in tickersPulls:
        if i["symbol"] == "BTC-USDT":
            return i


def getCurrentPrice(tickersName):
    tickersPulls = client.get_ticker()["ticker"]

    for i in tickersPulls:
        if i["symbol"] == tickersName:
            return i["buy"]


@app.route('/addAsset', methods=["GET", "POST"])
def addNewAsset():
    form = forms.AddTokenForm()
    if request.method == "POST":
        asset = NewAsset(assetTitle=form.title.data,
                         assetAmount=form.amount.data,
                         assetPrice=form.tokenPrice.data,
                         pricePrediction=form.pricePrediction.data,
                         addDate=datetime.now())

        asset.stake = asset.getStake()
        db.session.add(asset)
        db.session.commit()
        flash("Asset added!")
        return redirect(url_for('started'))

    return render_template('addAsset.html', form=form, asset_names=asset_names)


@app.route('/asset')
def getasset():
    theId = request.args.get('id')
    new_asset = NewAsset.query.get(theId)
    new_asset.current_price = printingit1(new_asset.assetTitle)
    a = float(new_asset.current_price)
    b = float(new_asset.assetPrice)
    new_asset.gain_loss = float("{:.2f}".format((a - b) / a * 100))

    return render_template('asset.html', new_asset=new_asset)


def printingit1(tickersName):
    tickersPulls = client.get_ticker()["ticker"]

    for i in tickersPulls:
        if i["symbol"] == tickersName:
            return i["buy"]


@app.route('/edit/<int:asset_id>', methods=["GET", "POST"])
def edit(asset_id):
    new_asset = NewAsset.query.get(asset_id)
    form = forms.AddTokenForm()
    if new_asset:
        if request.method == "POST":
            new_asset.assetAmount = form.amount.data
            new_asset.assetPrice = form.tokenPrice.data
            new_asset.pricePrediction = form.pricePrediction.data
            db.session.commit()
            flash("Asset updated!")
            return redirect(url_for('started'))

        form.title.data = new_asset.assetTitle
        form.amount.data = new_asset.assetAmount
        form.tokenPrice.data = new_asset.assetPrice
        form.pricePrediction.data = new_asset.pricePrediction
        return render_template('edit.html', form=form, asset_id=asset_id)
    else:
        flash("Asset is not found.")
    return redirect(url_for('started'))


@app.route('/addstake/<int:asset_id>', methods=["GET", "POST"])
def addstake(asset_id):
    the_asset = NewAsset.query.get(asset_id)
    form = forms.AddTokenForm()
    form.title.data = the_asset.assetTitle

    if request.method == "POST":
        newStake = NewAsset(assetTitle=the_asset.assetTitle,
                            assetAmount=form.amount.data,
                            assetPrice=form.tokenPrice.data,
                            pricePrediction=the_asset.pricePrediction,
                            addDate=the_asset.addDate)
        newStake.stake = newStake.getStake()

        the_asset.addStake(newStake)
        print(the_asset.stake)



        db.session.commit()
        print()
        flash("Stake added.")
        return redirect(url_for('started'))

    return render_template('addstake.html', form=form, asset_id=asset_id)


@app.route('/delete/<int:asset_id>', methods=["GET", "POST"])
def delete(asset_id):
    new_asset = NewAsset.query.get(asset_id)
    form = forms.DeleteAssetForm()

    if request.method == "POST":
        db.session.delete(new_asset)

        db.session.commit()
        flash("Asset deleted")

        return redirect(url_for('started'))

    return render_template('delete.html', form=form, asset_id=asset_id, new_asset=new_asset)
