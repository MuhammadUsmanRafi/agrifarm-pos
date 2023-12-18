from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

database = client.Agrifarm

product = database.Products
