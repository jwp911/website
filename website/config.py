class Config:
    SECRET_KEY = '65468A4D1H654FDSG64SFD65'
    uri_string = 'mysql+mysqlconnector://mysqladmin:GreenEnergy2024!@192.168.0.4:3306/db'
    SQLALCHEMY_DATABASE_URI = uri_string
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'email@email.com'
    MAIL_PASSWORD = 'password'

