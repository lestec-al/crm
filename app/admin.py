from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User # to settings.py ???
from app.models import Product, Sale, ProductQuantity, AdditionalField


class ProductsInline(admin.TabularInline):
    model = Sale.products.through
    extra = 0
    autocomplete_fields = ('product',)


class AdditionalInline(admin.TabularInline):
    model = AdditionalField
    extra = 0


class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'stage', 'manager', 'date_created', 'date_updated')
    search_fields = ('id', 'stage', 'manager__username')
    autocomplete_fields = ('manager',)
    readonly_fields = ('total_price', 'date_created', 'date_updated')
    inlines = (AdditionalInline, ProductsInline)
    exclude = ('products',)
    actions = ('change_manager', 'change_stage')

    @admin.action(description='Change stage of selected sales')
    def change_stage(self, request, queryset):
        context = {}
        context['sales'] = queryset
        context['stages'] = Sale.SALE_STAGES_CHOICES
        if 'apply' in request.POST:
            stage = request.POST["stage"]
            queryset.update(stage=stage)
            return HttpResponseRedirect(request.get_full_path())
        return render(request,'admin/admin_plus.html', context=context)

    @admin.action(description='Change manager of selected sales')
    def change_manager(self, request, queryset):
        context = {}
        context['sales'] = queryset
        context['users'] = User.objects.all()
        if 'apply' in request.POST:
            manager = request.POST["manager"]
            if manager == "":
                manager = request.POST.get("user")
            users = User.objects.filter(username=manager)
            if users.exists():
                user = users.first()
                queryset.update(manager=user)
                return HttpResponseRedirect(request.get_full_path())
        return render(request,'admin/admin_plus.html', context=context)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('id', 'name')


admin.site.register(Sale, SaleAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductQuantity)
admin.site.register(AdditionalField)
admin.site.site_title = 'ACRM'
admin.site.site_header = 'ACRM administration'