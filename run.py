from app import app
from db import db
from models.models import MonthModel

db.init_app(app)

enero = MonthModel('enero')
febrero = MonthModel('febrero')
marzo = MonthModel('marzo')
abril = MonthModel('abril')
mayo = MonthModel('mayo')
junio = MonthModel('junio')
julio = MonthModel('julio')
agosto = MonthModel('agosto')
septiembre = MonthModel('septiembre')
octubre = MonthModel('octubre')
noviembre = MonthModel('noviembre')
diciembre = MonthModel('diciembre')


@app.before_first_request
def create_tables():
    db.create_all()

    if db.session.query(MonthModel).count() == 0:
        db.session.add_all([enero, febrero, marzo, abril, mayo, junio, julio,
                            agosto, septiembre, octubre, noviembre, diciembre])
        db.session.commit()
