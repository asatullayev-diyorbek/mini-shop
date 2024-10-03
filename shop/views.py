from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse

from .models import Category, Product, Comment
from .forms import CommentForm


class HomeView(View):
    def get(self, request):
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)[:8]
        context = {
            'title': 'Bosh sahifa',
            'categories': categories,
            'products': products,
        }
        return render(request, 'shop/index.html', context)


class ProductDetailView(View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        categories = Category.objects.all()

        comment_form = CommentForm()
        context = {
            'title': product.name,
            'product': product,
            'categories': categories,
            'comment_form': comment_form,
            'product_cart': request.session.get('cart', {}).get(str(product.id), 0)
        }
        return render(request,'shop/product_detail.html', context)


class CommentView(LoginRequiredMixin, View):
    def post(self, request, slug):
        product = Product.objects.get(slug=slug)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            Comment.objects.create(
                content=comment_form.cleaned_data['content'],
                rating=comment_form.cleaned_data['rating'],
                user=request.user,
                product=product,
            )
            messages.success(request, "Thank you for a comment")
            return redirect('shop:product_detail', slug=slug)
        messages.error(request, "Izoh saqlanmadi.")
        return redirect('shop:product_detail', slug=slug)


class CartListView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        products = Product.objects.filter(id__in=cart.keys())
        full_price = 0
        for product in products:
            product.quantity = cart[str(product.id)]
            product.total_price = float(product.current_price()) * cart[str(product.id)]
            full_price += product.total_price
        context = {
            'title': 'Savat',
            'products': products,
            'full_price': full_price,
        }
        return render(request,'shop/cart.html', context)


class CartAddView(View):
    def get(self, request, pk):
        cart = request.session.get('cart', {})
        p_id = str(pk)

        if cart.get(p_id):
            cart[p_id] += 1
            message = "Cart yangilandi"
        else:
            cart[p_id] = 1
            message = "Cartga qo'shildi"

        request.session['cart'] = cart
        return JsonResponse({'status': 'success', 'cart': cart, 'message': message})


class CartRemoveView(View):
    def get(self, request, pk):
        cart = request.session.get('cart', {})
        p_id = str(pk)
        p = cart.get(p_id)
        if p:
            if p > 1:
                cart[p_id] -= 1
                message = "Cart yangilandi"
            elif p == 1:
                del cart[p_id]
                message = "Cartdan o'chirildi"
            else:
                message = "Mavjud emas"
        else:
            message = "Cartda mavjud emas"
        print("Remove ****************************")
        request.session['cart'] = cart
        return JsonResponse({'status': 'success', 'cart': cart, 'message': message})


class CartDeleteView(View):
    def get(self, request, pk):
        cart = request.session.get('cart', {})
        p_id = str(pk)
        if p_id in cart:
            del cart[p_id]
        request.session['cart'] = cart
        return redirect('shop:cart_list')
