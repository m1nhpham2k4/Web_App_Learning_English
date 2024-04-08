from app import db

class vocab(db.Model):
    vocab = db.Column(db.String(1024), primary_key=True)
    phonetic_vocab = db.Column(db.String(1024))
    phonetic_example = db.Column(db.String(1024))
    mean = db.Column(db.String(1024))
    example = db.Column(db.String(1024))
    audio_vocab = db.Column(db.String(1024))
    audio_example = db.Column(db.String(1024))