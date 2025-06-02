import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["jarvis_db"]
collection = db["commands"]

# Insert some predefined commands
commands = [
    {"command": "hi", "response": "Hello! How can I help you?"},
    {"command": "how are you", "response": "I am just a program, but I am functioning well!"},
    {"command": "bye", "response": "Goodbye! Have a nice day!"}
]

collection.insert_many(commands)
print("Commands added to database!")

image_commands = [
    {"command": "show me the cat picture", "image_path": "images/cat.jpg"},
    {"command": "show me the dog picture", "image_path": "images/dog.jpg"}
]

collection.insert_many(image_commands)
print("Image commands added to database!")
