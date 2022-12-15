from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User # to settings.py ???
from app.models import Sale, Product, ProductQuantity, AdditionalField
from settings.utils import get_fields_names
from app.forms import SaleForm


@login_required
def sale_list_view(request, stage=None):
    if stage == None:
        return HttpResponseRedirect(reverse("sale_stages", args=['r']))
    else:
        context = {}
        stage = stage.lower()
        if stage in [i[0] for i in Sale.SALE_STAGES_CHOICES]:
            if request.user.is_staff:
                qs = Sale.objects.filter(stage=stage)
            else:
                qs = Sale.objects.filter(stage=stage, manager=request.user)
            if qs.exists():
                context["sales"] = qs
            context["sale_fields"] = get_fields_names(request.user)
            return render(request, 'home.html', context)
        raise Http404


@login_required
def search_view(request):
    str_search = request.GET.get("search", False)
    if str_search:
        # Better search ???
        if request.user.is_staff:
            q1 = Sale.objects.filter(client_name__contains=str_search)
            q2 = Sale.objects.filter(manager__username__contains=str_search)
            q3 = Sale.objects.filter(id__contains=str_search)
            qs = q1 | q2 | q3
        else:
            q1 = Sale.objects.filter(client_name__contains=str_search, manager=request.user)
            qs = q1
        context = {"sales":qs, "sale_fields":get_fields_names(request.user)}
    return render(request, "home.html", context)


@login_required
def sale_detail_view(request, id):
    sale = Sale.objects.get(id=id)
    if request.user.is_staff or sale.manager == request.user:
        # Unedited page for Delivery and Finished stages for non staff users
        if not request.user.is_staff and sale.manager == request.user and sale.stage.lower() in ('d','f'): # Settings for admin ???
            return render(request, 'detail_no_edit.html', context={"sale":sale, "additional":AdditionalField.objects.filter(sale=sale)})

        form = SaleForm(request.POST or None, instance=sale)
        if request.method == "POST":
            # Remove additional field
            for d_id in request.POST.getlist("remove_additional"):
                AdditionalField.objects.filter(id=d_id).delete()
            # Add / Update additional field
            for id,title,text in zip(request.POST.getlist("add_additional_id"), request.POST.getlist("add_additional_title"), request.POST.getlist("add_additional_text")):
                if len(title) > 100:
                    messages.error(request, "Additional field title length over 100 characters")
                else:
                    if id == "new":
                        AdditionalField.objects.create(sale=sale, title=title, text=text)
                    else:
                        AdditionalField.objects.filter(id=id).update(title=title, text=text)
            # Remove products
            for d_id in request.POST.getlist("remove_products"):
                pr = Product.objects.get(id=d_id)
                sale.products.remove(pr)
            # Add products
            for idx,i in enumerate(request.POST.getlist("add_products")):
                pr = Product.objects.get(id=i)
                if pr not in sale.products.all():
                    try:
                        new_quantity = float(request.POST.getlist("add_quantitys")[idx])
                        ProductQuantity.objects.create(product=pr, sale=sale, quantity=new_quantity)
                    except:
                        messages.error(request, "Products quantity must be a number")
                else:
                    messages.error(request, "The product is already in sale")
            if form.is_valid():
                form.save()

        context = {"sale":sale, "form":form, "products":Product.objects.all(), "additional":AdditionalField.objects.filter(sale=sale)}
        if request.user.is_staff:
            context["users"] = User.objects.all() if request.user.is_staff else None
        return render(request, 'detail.html', context)
    raise Http404


@login_required
def sale_create_view(request):
    products = Product.objects.all()
    form = SaleForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            sale = form.save(commit=False)
            sale.manager = request.user
            sale.save()
            # Add additional field to Sale
            for id,title,text in zip(request.POST.getlist("add_additional_id"), request.POST.getlist("add_additional_title"), request.POST.getlist("add_additional_text")):
                if id == "new":
                    AdditionalField.objects.create(sale=sale, title=title, text=text)
            # Add products to Sale
            for idx,i in enumerate(request.POST.getlist("add_products")):
                pr = Product.objects.get(id=i)
                new_quantity = float(request.POST.getlist("add_quantitys")[idx])
                ProductQuantity.objects.create(product=pr, sale=sale, quantity=new_quantity)
            # Redirect
            return HttpResponseRedirect(reverse("sale_detail", args=[sale.id]))
    context = {"form":form, "products":products}
    return render(request, "detail.html", context)