from django.shortcuts import render

# Create your views here.
from Inventory.models import InventoryItems, Inventory


def inventory_logs(request):
    return render(request, 'logs.html', {'context':Inventory.objects.all()})


def add(request):
    return render(request, 'additems.html', {'context': InventoryItems.objects.all()})


def new(request):
    return render(request, 'newitem.html')


def view_items(request):
    return  render(request, 'customitem.html', {'context':InventoryItems.objects.all()})


def new_item(request):
    category = request.POST['category']
    item = request.POST['item']

    New_item = InventoryItems()
    New_item.category = category
    New_item.name = item
    New_item.save()
    return render(request, 'adminindex.html', {'Message':'New Item Added Successfully!!!'})


def add_items(request):
    item_id1 = request.POST['item'].split()[0]
    quantity = request.POST['quantity']
    price = request.POST['price']
    unit = request.POST['unit']
    desc = request.POST['desc']
    if item_id1!= 'None':
        [item]=InventoryItems.objects.filter(item_id=item_id1)

    Item_object = Inventory()
    Item_object.item = item
    Item_object.quantity = quantity
    Item_object.price = price
    Item_object.unit = unit
    Item_object.description = desc
    Item_object.save()

    return render(request, 'index.html', {'Message':'Item Added Successfully!!!'})


def update_items(request):
    return