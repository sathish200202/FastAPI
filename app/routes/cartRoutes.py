from fastapi import APIRouter, Depends, Path, HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Optional
from sqlalchemy.orm import Session
from Schemas.cartSchema import CartCreate, updateQuantity
from models.cartModel import Cart
from models.userModel import User
from models.productModel import Product
from database import get_db
from utils import get_current_user, get_token_from_header

router = APIRouter()

@router.get("/")
def get_user_cart(request: Request, db: Session = Depends(get_db)):
    token, credentials_exception = get_token_from_header(request)

    user = get_current_user(token, credentials_exception, db, User)
    #print(f"cart route: {user.username}")
    user_cart = db.query(Cart).filter(Cart.user_id == user.id).all()

    total_cart = len(user_cart)
    if user_cart:
        #print(f"user cart: {user_cart}")
        return user_cart
    else:
        return JSONResponse(status_code=404, content={"message": "No items in your cart"})

@router.post("/add-to-cart")
def add_to_cart(cart: CartCreate, request: Request, db: Session = Depends(get_db)):
    try:
        token, credentials_exception = get_token_from_header(request)

        user = get_current_user(token, credentials_exception, db, User)
        # Get product and calculate total price
        product = db.query(Product).filter(Product.id == cart.product_id).first()
        if not product:
            return JSONResponse(status_code=404, content={"message": "Product not found"})

        total_price = product.price * cart.quantity
        #cart.user_id = user.id

        new_cart_item = Cart(
        user_id=user.id,
        product_id=cart.product_id,
        quantity=cart.quantity,
        total_price=total_price,
     )

        db.add(new_cart_item)
        db.commit()
        db.refresh(new_cart_item)

        return JSONResponse(status_code=200, content={
            "cart": {
                "id": new_cart_item.id,
                "product_id": new_cart_item.product_id,
                "user_id": new_cart_item.user_id,
                "quantity": new_cart_item.quantity,
                "total_price": new_cart_item.total_price,
            },
            "message": "Item added to cart successfully"
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal Server Error", "error": str(e)})



@router.put("/update-quantity/{cart_id}")
def update_quantity(request: Request, cart_id: int, quantity: updateQuantity, db: Session = Depends(get_db)):
    try:
        #print(f"quantity: {quantity.quantity}")
        token, credentials_exception = get_token_from_header(request)

        user = get_current_user(token, credentials_exception, db, User)
        cart_item = db.query(Cart).filter(Cart.id == cart_id, Cart.user_id == user.id).first()
        if not cart_item:
            return JSONResponse(status_code=404, content={"message": "Cart item not found"})
        
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if not product:
            return JSONResponse(status_code=404, content={"message": "Product not found"})

        # Update the quantity and total price
        cart_item.quantity = quantity.quantity
        cart_item.total_price = product.price * quantity.quantity
        #print(f"total: {product.price * quantity.quantity}")
        db.commit()
        db.refresh(cart_item)

        return cart_item
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal Server Error", "error": str(e)})


@router.delete("/remove-cart-item/{cart_id}")
def remove_cart_item(request: Request, cart_id: int, db: Session = Depends(get_db)):
    try:
        token, credentials_exception = get_token_from_header(request)

        user = get_current_user(token, credentials_exception, db, User)
        cart_item = db.query(Cart).filter(Cart.id == cart_id, Cart.user_id == user.id).first()
        if not cart_item:
            return JSONResponse(status_code=404, content={"message": "Cart item not found"})

        db.delete(cart_item)
        db.commit()

        return JSONResponse(status_code=200, content={"message": "Cart item deleted successfully"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal Server Error", "error": str(e)})



@router.delete("/clear-cart")
def clear_cart_items(request: Request, db: Session = Depends(get_db)):
    try:
        token, credentials_exception = get_token_from_header(request)
        user = get_current_user(token, credentials_exception, db, User)
        cart_item = db.query(Cart).filter(Cart.user_id == user.id).all()

        if not cart_item:
            return JSONResponse(status_code=404, content={"message": "Cart is already empty"})
        
        for item in cart_item:
            db.delete(item)
            db.commit()
        return JSONResponse(status_code=200, content={"message": "Cart cleared successfully"})
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal Server Error", "error": str(e)})

