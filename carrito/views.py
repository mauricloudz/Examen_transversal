#from django.shortcuts import render, redirect
#from django.contrib.auth.decorators import login_required
#from .models import CarritoCompras, ItemCarrito
#from .forms import AgregarAlCarritoForm
#from repuestos.models import Repuesto
#
#@login_required
#def agregar_al_carrito(request, repuesto_id):
#    repuesto = Repuesto.objects.get(id=repuesto_id)
#    carrito, created = CarritoCompras.objects.get_or_create(user=request.user)
#    if request.method == 'POST':
#        form = AgregarAlCarritoForm(request.POST)
#        if form.is_valid():
#            item = form.save(commit=False)
#            item.repuesto = repuesto
#            item.save()
#            carrito.repuestos.add(item)
#            return redirect('catalogo_repuestos')
#    else:
#        form = AgregarAlCarritoForm()
#    return render(request, 'carrito/agregar_al_carrito.html', {'form': form, 'repuesto': repuesto})
#
#@login_required
#def ver_carrito(request):
#    carrito, created = CarritoCompras.objects.get_or_create(user=request.user)
#    return render(request, 'carrito/ver_carrito.html', {'carrito': carrito})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .cart import Cart
from repuestos.models import Repuesto
from .forms import AgregarAlCarritoForm, EliminarDelCarritoForm

@login_required
def agregar_al_carrito(request, repuesto_id):
    cart = Cart(request)
    repuesto = get_object_or_404(Repuesto, id=repuesto_id)
    if request.method == 'POST':
        form = AgregarAlCarritoForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(repuesto=repuesto, quantity=cd['cantidad'])
            return redirect('catalogo_repuestos')
    else:
        form = AgregarAlCarritoForm()
    return render(request, 'carrito/agregar_al_carrito.html', {'form': form, 'repuesto': repuesto})

@login_required
def eliminar_del_carrito(request, repuesto_id):
    cart = Cart(request)
    repuesto = get_object_or_404(Repuesto, id=repuesto_id)
    if request.method == 'POST':
        form = EliminarDelCarritoForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.remove(repuesto=repuesto, quantity=cd['cantidad'])
            return redirect('ver_carrito')
    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    cart = Cart(request)
    return render(request, 'carrito/ver_carrito.html', {'cart': cart})