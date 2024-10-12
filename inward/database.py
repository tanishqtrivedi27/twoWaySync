# from sqlalchemy import create_engine, Column, String
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
# DATABASE_URL="postgresql://postgres:password@postgres:5432/mydb"
# engine = create_engine(DATABASE_URL)
# Session = sessionmaker(bind=engine)
# Base = declarative_base()
#
# class Customer(Base):
#     __tablename__ = 'customers'
#
#     id = Column(String, primary_key=True)
#     email = Column(String, nullable=False)
#     name = Column(String, nullable=False)
#
# Base.metadata.create_all(engine)
