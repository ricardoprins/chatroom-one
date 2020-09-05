import motor
from motor import motor_tornado

client = motor_tornado.MotorClient(
    "mongodb+srv://sampleAdmin:samplePassword@cluster0.qvjxl.mongodb.net/test?retryWrites=true&w=majority")

db = client.test
