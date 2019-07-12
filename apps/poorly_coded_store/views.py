from django.shortcuts import render, redirect
from .models import Order, Product

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):

    if "spendingTotal" not in request.session:
        request.session["spendingTotal"] = 0

    quantity_from_form = int(request.POST["quantity"])
    price = Product.objects.get(id = request.POST["product"]).price## this is the line we had to change to prevent price from being manipulated
    total_charge = quantity_from_form * price                           ## originally, this was price_from_form, and grabbed the value from there
    print("Charging credit card...")                                    ## but we had to change the syntax to grab price from the database AND
                                                                        ## account for users manipulating the product, and still charging them the right price
    thisOrder = Order.objects.create(                                                  ## which this equation allows for
        quantity_ordered = quantity_from_form,
        total_price = total_charge
    )
    thisOrder.save()

    return redirect(f"/process/{thisOrder.id}")
    
def process(request, orderId):
    orders = Order.objects.all()
    sum = 0
    for order in orders:
        sum += order.total_price

    checkoutDict = {
        "order" : Order.objects.get(id=orderId),
        "spendingTotal" : sum
    }
    
    return render(request, "store/checkout.html", checkoutDict)