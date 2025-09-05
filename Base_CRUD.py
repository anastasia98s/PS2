
class BaseCRUD:
    @classmethod
    def create(cls, session, **kwargs):
        """Erstellt eine neue Instanz und fügt sie zur Session hinzu."""
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    @classmethod
    def read(cls, session, **filters):
        """Liest Objekte mit bestimmten Filtern aus der Datenbank."""
        return session.query(cls).filter_by(**filters).all()

    @classmethod
    def read_one(cls, session, **filters):
        """Liest ein einzelnes Objekt aus der Datenbank."""
        return session.query(cls).filter_by(**filters).first()

    @classmethod
    def update(cls, session, id, **kwargs):
        """Aktualisiert ein Objekt mit den angegebenen Feldern."""
        obj = session.query(cls).filter_by(id=id).first()
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            session.commit()
            session.refresh(obj)
            return obj
        return None

    @classmethod
    def delete(cls, session, id):
        """Löscht ein Objekt mit der angegebenen ID."""
        obj = session.query(cls).filter_by(id=id).first()
        if obj:
            session.delete(obj)
            session.commit()
            return True
        return False
