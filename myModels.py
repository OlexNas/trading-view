from app import db


class NewAsset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assetTitle = db.Column(db.String(50), nullable=False)
    assetAmount = db.Column(db.Float, nullable=False)
    assetPrice = db.Column(db.Float, nullable=False)
    pricePrediction = db.Column(db.Float, nullable=False)
    stake = db.Column(db.Float, nullable=False)
    addDate = db.Column(db.Date, nullable=False)



    def getStake(self):
        self.stake = self.assetPrice * self.assetAmount
        return self.stake

    def addStake(self, newStake):
        if newStake.assetTitle == self.assetTitle:
            stake1 = self.stake
            print("mself=", stake1)
            stake2 = newStake.stake
            print("mnewstake=", stake2)
            newAmount = self.assetAmount + newStake.assetAmount
            self.assetPrice = (stake1 + stake2)/newAmount
            self.stake = stake1 + stake2
            print(self.stake)
            return self.stake