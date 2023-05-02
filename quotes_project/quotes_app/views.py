from django.core.paginator import Paginator
from django.db.models import Count, Max
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .forms import AddAuthorForm, AddQuoteForm

from .models import Quote, Author, Tag


class PageNotAnInteger(Exception):
    ...


class EmptyPage(Exception):
    ...


# Create your views here.
def quote_page(request):
    quotes = Quote.objects.all()


    p = Paginator(quotes, 10)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
        
    tags = Tag.objects.annotate(num_quotes = Count('quote'), font_size = Max('quote')).order_by('-num_quotes')[:10]
        
    for tag in tags:
        font_size = tag.num_quotes * 28 / tags[0].num_quotes // 1
        if font_size < 8:
            font_size = 8   
        tag.font_size = str(font_size)        
            
        
    context = {
        'paginator': p,
        'page_obj': page_obj,
        'tags': tags,
    }
    # sending the page object to index.html
    return render(request, 'quotes_app/index.html', context)


def tag_page(request, tag_name):
    quotes = Quote.objects.filter(tags__name=tag_name)

    p = Paginator(quotes, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
        
    tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
        
    for tag in tags:
        font_size = tag.num_quotes * 28 / tags[0].num_quotes // 1
        if font_size < 8:
            font_size = 8   
        tag.font_size = str(font_size)        
            
        
    context = {
        'paginator': p,
        'page_obj': page_obj,
        'tags': tags,
        'tag': tag_name,
    }

    return render(request, 'quotes_app/tag_list.html', context)

def author_list(request):
    authors = Author.objects.order_by('fullname').all()
    return render(request, 'quotes_app/author_list.html', {'authors': authors})


def author_detail(request, author_name):
    author = get_object_or_404(Author, fullname=author_name)
    quotes = Quote.objects.filter(author=author)
    return render(request, 'quotes_app/author_detail.html', {'author': author, 'quotes': quotes})

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AddAuthorForm(request.POST, instance=Author())
        if form.is_valid():
            # сохраняем данные автора в базу данных
            author = form.save()
            return redirect(to='quotes_app:author_detail', author_name=author.fullname)
    else:
        form = AddAuthorForm(instance=Author())
    return render(request, 'quotes_app/add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = AddQuoteForm(request.POST)
        if form.is_valid():
            quote = form.save()
            return redirect(to='quotes_app:quote')
    else:
        form = AddQuoteForm()
        form.fields['author'].queryset = Author.objects.order_by('fullname').all()
    return render(request, 'quotes_app/add_quote.html', {'form': form})