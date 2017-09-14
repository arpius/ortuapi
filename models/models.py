from db import db


season = db.Table('season', db.metadata)


class SeasonModel(db.Model):
    __tablename__ = 'season'
    __table_args__ = (db.UniqueConstraint('vegetable_id', 'month_id'),
                      {'extend_existing': True})

    vegetable_id = db.Column(db.Integer, db.ForeignKey('vegetables.id'),
                             primary_key=True)
    month_id = db.Column(db.Integer, db.ForeignKey('months.id'),
                         primary_key=True)

    def __init__(self, vegetable_id, month_id):
        self.vegetable_id = vegetable_id
        self.month_id = month_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class MonthModel(db.Model):
    __tablename__ = 'months'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))

    vegetables_month = db.relationship('VegetableModel', secondary=season,
                                       backref=db.backref('months',
                                                          lazy='dynamic'))

    def __init__(self, name):
        self.name = name

    def to_json(self):
        vegetables = VegetableModel.query.filter(VegetableModel.months.any(
                                                 name=self.name)).all()
        return {'month': self.name, 'vegetables': [vegetable.name for vegetable
                                                   in vegetables]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class VegetableModel(db.Model):
    __tablename__ = 'vegetables'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    season = db.relationship('MonthModel', secondary=season,
                             backref=db.backref('vegetables', lazy='dynamic'))

    def __init__(self, name):
        self.name = name

    def to_json(self):
        season = MonthModel.query.filter(MonthModel.vegetables.any(
                                         name=self.name)).all()
        return {'vegetable': self.name, 'season': [month.name for month
                                                   in season]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
