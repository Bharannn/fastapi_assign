from database import User, Orders

async def fetch_all_users():
    """
    Fetch all user data from the database.
    """
    users = User.objects.all()
    if not users:
        return {"message": "No users found"}

    user_data = [
        {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role_id.role_name,
            "time_stamp": user.time_stamp.strftime("%Y-%m-%d %H:%M:%S"),
            "status": user.status,
        }
        for user in users
    ]
    return {"users": user_data}


async def fetch_all_orders():
    """
    Fetch all order data from the database.
    """
    orders = Orders.objects.all()
    if not orders:
        return {"message": "No orders found"}

    order_data = [
        {
            "order_id": str(order.id),
            "user_id": str(order.user_id.id),
            "order_status": order.order_status,
            "total_price": order.total_price,
            "products": order.products,
            "time_stamp": order.time_stamp.strftime("%Y-%m-%d %H:%M:%S"),
            "status": order.status,
        }
        for order in orders
    ]
    return {"orders": order_data}
