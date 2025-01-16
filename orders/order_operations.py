from datetime import datetime
from typing import List, Dict
from fastapi import HTTPException
from orders.order_validations import OrderCreate
from database import Orders, Products


# Function to create an order
async def create_order_logic(order: OrderCreate, current_user: dict) -> Dict:
    """
    Creates a new order for the current authenticated user.
    """
    user_id = current_user["id"]  # Extract user ID from current_user dict
    
    # Step 1: Extract product IDs and fetch product details
    product_ids = [item.product_id for item in order.products]
    products = Products.objects(id__in=product_ids, status=True)

    if len(products) != len(order.products):
        raise HTTPException(status_code=400, detail="One or more products are invalid or unavailable.")

    # Step 2: Map product details and calculate total price
    products_map = {str(product.id): product for product in products}
    total_price = 0
    order_items = []

    for item in order.products:
        product = products_map.get(item.product_id)
        if not product:
            raise HTTPException(status_code=400, detail=f"Product ID {item.product_id} not found.")

        item_total_price = product.price * item.quantity
        total_price += item_total_price

        order_items.append({
            "product_id": str(product.id),
            "product_name": product.product_name,
            "quantity": item.quantity,
            "price": product.price,
            "total_price": item_total_price,
        })

    # Step 3: Create the Order document
    new_order = Orders(
        user_id=user_id,
        order_status="pending",
        total_price=total_price,
        products=order_items,
        time_stamp=datetime.utcnow(),
        status=True
    )
    new_order.save()

    return {
        "order_id": str(new_order.id),
        "order_status": new_order.order_status,
        "total_price": total_price,
        "products": order_items
    }


# Function to get all orders for a user
async def get_user_orders_logic(current_user: dict) -> List[Dict]:
    """
    Fetches all orders belonging to the authenticated user.
    """
    user_id = current_user["id"]  # Extract user ID

    user_orders = Orders.objects(user_id=user_id, status=True)

    if not user_orders:
        raise HTTPException(status_code=404, detail="No orders found for this user.")

    return [
        {
            "order_id": str(order.id),
            "order_status": order.order_status,
            "total_price": order.total_price,
            "products": order.products,
            "time_stamp": order.time_stamp
        }
        for order in user_orders
    ]


# Function to get a specific order by ID
async def get_order_by_id_logic(order_id: str, current_user: dict) -> Dict:
    """
    Fetches a specific order by its ID for the authenticated user.
    """
    user_id = current_user["id"]  # Extract user ID
    
    order = Orders.objects(id=order_id, user_id=user_id, status=True).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found or does not belong to the user.")

    return {
        "order_id": str(order.id),
        "order_status": order.order_status,
        "total_price": order.total_price,
        "products": order.products,
        "time_stamp": order.time_stamp
    }
