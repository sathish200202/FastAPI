from fastapi import APIRouter, Depends, Path, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from Schemas.productsSchema import ProductCreate, ProductOut
from models.productModel import Product
from models.orderModel import Order
from models.userModel import User
from database import get_db
from utils import admin_required


router = APIRouter()

@router.get("/dashboard")
def get_admin_dashboard(db: Session = Depends(get_db), admin: User = Depends(admin_required)):
    #user = admin_required(request, db, User)
    if admin:
       users = db.query(User).all()
       products = db.query(Product).all()
       orders = db.query(Order).all()

       total_users = len(users)
       total_products = len(products)
       total_orders = len(orders)

       return {
           "total_users": total_users,
              "total_products": total_products,
                "total_orders": total_orders,
       }
    else:
        return JSONResponse(status_code=401, content={"message": "Unauthorized access"})

@router.get("/get-all-products")
def get_all_products(db: Session = Depends(get_db), admin: User = Depends(admin_required)):
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
def update_product(product_id: int, updateProduct: ProductCreate, db: Session = Depends(get_db), admin: User = Depends(admin_required)):
    product = db.query(Product).filter(Product.id == product_id).first()
    print(updateProduct)
    if_updated = False
    if product:
        if updateProduct.product_name is not None:
            product.product_name = updateProduct.product_name
            if_updated = True

        if updateProduct.price is not None:
            product.price = updateProduct.price
            if_updated = True

        if updateProduct.category is not None:
            product.category = updateProduct.category
            if_updated = True

        if updateProduct.quantity is not None:
            product.quantity = updateProduct.quantity
            if_updated = True

        if not if_updated:
            return JSONResponse(status_code=400, content={"message": "No changes made"})
            
        db.commit()
        db.refresh(product)
        return product
    else:
        return JSONResponse(status_code=404, content={"message": "Product not found"})
    

@router.delete("/inventory/delete-product/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db),  description: str = "Delete a product by ID", admin: User = Depends(admin_required)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return JSONResponse(status_code=404, content={"message": "Product not found"})
    
    db.delete(product)
    db.commit()
    
    return JSONResponse(status_code=200, content={"message": "Product deleted successfully"})


#Users controller
@router.get("/get-users", )
def get_all_users(db: Session = Depends(get_db), admin: User = Depends(admin_required)):
    all_users = db.query(User).all()
    if all_users:
        return all_users
    else:
        return JSONResponse(status_code=404, content={"message": "No users"})
    

@router.delete("/delete-user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), description: str = "Delete a user by ID", admin: User = Depends(admin_required)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    
    db.delete(user)
    db.commit()

    return JSONResponse(status_code=200, content={"message": "User deleted successfully"})



#view all orders
@router.get("/get-orders")
def get_all_orders(db: Session = Depends(get_db), admin: User = Depends(admin_required)):
    all_orders = db.query(Order).all()
    if all_orders:
        return all_orders
    else:
        return JSONResponse(status_code=404, content={"message": "No orders"})
    
@router.get("/get-orders/{order_id}")
def get_order_by_id(order_id: int, db: Session = Depends(get_db), admin: User = Depends(admin_required)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        return order
    else:
        return JSONResponse(status_code=404, content={"message": "Order not found"})
    
@router.put("update-order-status/{order_id}")
def update_order_status(Order_id: int, status: str, db: Session = Depends(get_db), admin: User = Depends(admin_required)):
    order = db.query(Order).filter(Order.id == Order_id).first()
    if order:
        order.status = status
        db.commit()
        db.refresh(order)
        return order
    else:
        return JSONResponse(status_code=404, content={"message": "Order not found"})