class Config:
    SECRET_KEY = "5b1043ca39770af2b3086c74c2c53f74115c63b4bb8be17b98e92138928daf14"
    JWT_SECRET_KEY = "52be6f8543e522f24263a65cba17a3d2ba7f9a9e9d05806aed8c4704cbf96e1e"
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False