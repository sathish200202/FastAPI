from fastapi import APIRouter, Depends, Path, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from Schemas.productsSchema import ProductCreate, ProductOut
from models.productModel import Product
from models.userModel import User
from database import get_db


router = APIRouter()

@router.get("/")
def get_all_products(db: Session = Depends(get_db)):
    all_products = db.query(Product).all()
    if all_products:
        return all_products
    else:
        return JSONResponse(status_code=404, content={"message": "No Products"})
    

@router.post("/add-product", response_model = ProductOut)
def add_item(item: ProductCreate, db:Session = Depends(get_db)):
   new_item = Product(**item.dict())
   db.add(new_item)
   db.commit()
   db.refresh(new_item)

   return new_item
   

@router.put("/update-product/{product_id}", response_model = ProductOut)
def update_product(product_id: int, updateProduct: ProductCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        for key, value in updateProduct.dict().items():
            setattr(product, key, value)
            
        db.commit()
        db.refresh(product)
        return product
    else:
        return JSONResponse(status_code=404, content={"message": "Product not found"})
    

@router.delete("/inventory/delete-product/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), description: str = "Delete a product by ID"):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return JSONResponse(status_code=404, content={"message": "Product not found"})
    
    db.delete(product)
    db.commit()
    
    return JSONResponse(status_code=200, content={"message": "Product deleted successfully"})


@router.get("/get-users")
def get_all_users(db: Session = Depends(get_db)):
    all_users = db.query(User).all()
    if all_users:
        return all_users
    else:
        return JSONResponse(status_code=404, content={"message": "No users"})
    

@router.delete("/delete-user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), description: str = "Delete a user by ID"):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    
    db.delete(user)
    db.commit()

    return JSONResponse(status_code=200, content={"message": "User deleted successfully"})