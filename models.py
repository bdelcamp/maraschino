from sqlalchemy import Column, Integer, String, Boolean
from database import Base

# IMPORTANT!
# VALID MODULES:

# applications
# library         [mandatory static]
# recently_added
# sabnzbd
# synopsis        [mandatory static]
# trakt           [mandatory static]

class Module(Base):
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    static = Column(Boolean)
    column = Column(Integer)
    position = Column(Integer)
    poll = Column(Integer)
    delay = Column(Integer)

    def __init__(self, name=None, static=0, column=None, position=None, poll=None, delay=None):
        self.name = name
        self.static = static
        self.column = column
        self.position = position
        self.poll = poll
        self.delay = delay

    def __repr__(self):
        return '<Module %r>' % (self.name)