from fastapi import FastAPI
#import uvicorn

from dotenv import load_dotenv
import os

from models.productModel import Product
from database import engine
# from inventory_data import inventory_item_data as inventory_data
# from apis import  get_all_items, get_item_by_id, get_item_by_name, create_new_product, router
from routes import productRoutes, userRoutes, adminRoutes, cartRoutes, orderRoutes

load_dotenv()

#create DB and table
Product.metadata.create_all(bind=engine)

app = FastAPI()

#     return create_new_product(item, db)
# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=8080)

app.include_router(productRoutes.router, prefix="/api/v1", tags=["Inventory"])
app.include_router(userRoutes.router, prefix="/users", tags=["Users"])
app.include_router(adminRoutes.router, prefix="/admin", tags=["Admin"])
app.include_router(cartRoutes.router, prefix="/cart", tags=["Cart"])
app.include_router(orderRoutes.router, prefix="/orders", tags=["Orders"])