from kiosk import app, db
from kiosk.models import User, Session, Orders, Food

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Session': Session, 'Orders': Orders, 'Food': Food}
