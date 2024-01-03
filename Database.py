from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

database = client.Agrifarm

product = database.Products
credentials = database.credentials
company = database.Companies
companyorders = database.companyorders
productsales = database.productsales
warehouses = database.warehouses
customer = database.customers

