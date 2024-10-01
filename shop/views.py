from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View

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
        }
        return render(request,'shop/product_detail.html', context)


class CommentView(View):
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

