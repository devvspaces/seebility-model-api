from chat.models import CartItem
import cuid


def add_cart_to_db(user_id, product, name, price, quantity):
    """
    Add product to cart in db
    """
    cart_item = CartItem.objects.using('api_db').create(
        id=cuid.cuid(),
        user_id=user_id,
        product_id=product,
        name=name,
        price=price,
        quantity=quantity,
    )
    return cart_item


def update_cart(cart_id, quantity):
    """
    Update cart in db
    """
    try:
        cart_item = CartItem.objects.using('api_db').get(id=cart_id)
    except CartItem.DoesNotExist:
        return None
    cart_item.quantity = quantity
    cart_item.save(using="api_db")
    return cart_item


def delete_cart(cart_id):
    """
    Delete cart from db
    """
    try:
        cart_item = CartItem.objects.using('api_db').get(id=cart_id)
    except CartItem.DoesNotExist:
        return None
    cart_item.delete(using="api_db")
    return cart_item


def get_cart_from_db(user_id):
    """
    Get cart from db
    """
    cart_items = CartItem.objects.using('api_db').filter(user_id=user_id)
    return cart_items
