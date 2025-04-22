from fastapi import APIRouter, Depends, Path, HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Optional
from sqlalchemy.orm import Session
from Schemas.orderSchema import OrderOut, OrderItemOut, SingleProductOrder
from models.orderModel import OrderItem, Order
from models.userModel import User
from models.productModel import Product
from database import get_db
from utils import get_current_user, get_token_from_header


router = APIRouter()

@router.get("/", response_model=list[OrderOut])
def get_all_orders(request: Request, db: Session = Depends(get_db)):
    try:
        #token, credentials_exception = get_token_from_header(request)
        user = get_current_user(request, db, User)
        orders = db.query(Order).filter(Order.user_id == user.id).all()
        if not orders:
            return JSONResponse(status_code=404, content={"message": "No orders found"})
        
        return orders
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
    

@router.post("/create-order")
def create_order(request: Request, order: SingleProductOrder, db: Session = Depends(get_db)):
    try:
         #token, credentials_exception = get_token_from_header(request)
        user = get_current_user(request, db, User)

        total_price = 0.0

        product = db.query(Product).filter(Product.id == order.product_id).first()
        if not product:
            return JSONResponse(status_code=404, content={"message": f"Product with id {order.product_id} not found"})
            
        item_total = order.quantity * product.price
        total_price += item_total

        new_order = Order(user_id=user.id, total_price=total_price, quantity=order.quantity)

        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        
        return new_order
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})