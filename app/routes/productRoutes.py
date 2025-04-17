from fastapi import APIRouter, Depends, Path, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from Schemas.productsSchema import ProductCreate, ProductOut
from models.productModel import Product
from database import get_db
    


router = APIRouter()

@router.get("/")
def Home():
    return {"message": "Hello, world! welcome to the page"}


@router.get("/inventory", response_model = list[ProductOut])
def get_inventory(db: Session = Depends(get_db)):
    all_products = db.query(Product).all()
    if all_products:
        return all_products
    else:
        return JSONResponse(status_code=404, content={"message": "No Products"})
     


@router.get("/inventory/get-item/{product_id}", response_model = ProductOut)
def get_product_by_id(product_id: int = Path(..., description= "The Id of the product you want to view", gt=0, lt=4), db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        return product
    else:
        return JSONResponse(status_code=404, content={"message": "Product not found"})
    
    
@router.get("/inventory/get-by-category", response_model = list[ProductOut])
def get_by_name(product_category: str, db: Session = Depends(get_db)):
   products = db.query(Product).filter(Product.category == product_category).all()
   if products:
       return products
   else:
       return JSONResponse(status_code=404, content={"message": "Product not found"})
   
