from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm
from django.conf import settings
from django.utils.text import slugify
import os
import fitz

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books, 'BASE_URL': settings.BASE_URL})

def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    file_name = str(book.pdf).split('/')[-1].split('.')[0]
    folder = 'media/books/' + file_name
    images = os.listdir(folder)
    return render(request, 'books/book_detail.html', {'book':book, 'folder': folder, 'images':images, 'BASE_URL': settings.BASE_URL})

def book_preview(request, slug):
    book = get_object_or_404(Book, slug=slug)
    file_name = str(book.pdf).split('/')[-1].split('.')[0]
    folder = 'media/books/' + file_name
    images = os.listdir(folder)
    return render(request, 'books/book_preview.html', {'book':book, 'folder': folder, 'images':images, 'BASE_URL': settings.BASE_URL})

def book_edit(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_date = request.POST.get('date')
        category = request.POST.get('category')
        description = request.POST.get('description')
        status = request.POST.get('status')
        score = request.POST.get('score')
        pdf = request.FILES.get('book_pdf')
        cover_image = request.FILES.get('book_cover')

        book.title = title
        book.author = author
        book.publication_date = publication_date
        book.category = category
        book.description = description
        book.status = status
        book.score = score

        if pdf and pdf.size > 0:
            base_slug = slugify(title)
            slug = base_slug
            pdf_extension = os.path.splitext(pdf.name)[1]
            save_path = os.path.join('media/pdfs/', f"{slug}{pdf_extension}")
            counter = 1

            while Book.objects.filter(slug=slug).exists() and os.path.exists(save_path):
                slug = f"{base_slug}-{counter}"
                save_path = os.path.join('media/pdfs/', f"{slug}{pdf_extension}")
                print(slug)
                counter += 1
            
            pdf.name = f"{slug}{pdf_extension}"
            book.pdf = pdf
            book.slug = slug

        if cover_image and cover_image.size > 0:
            book.cover_image = cover_image
        
        book.save()
        if pdf:
            convert_pdf_to_jpg(book)
        return redirect('book_list')
    else:
        file_name = str(book.pdf).split('/')[-1].split('.')[0]
        folder = 'media/books/' + file_name
        images = os.listdir(folder)
    return render(request, 'books/book_form.html', {'book':book, 'folder': folder, 'images':images, 'BASE_URL': settings.BASE_URL})

def book_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_date = request.POST.get('date')
        category = request.POST.get('category')
        description = request.POST.get('description')
        status = request.POST.get('status')
        score = request.POST.get('score')
        pdf = request.FILES.get('book_pdf')
        cover_image = request.FILES.get('book_cover')

        if pdf:
            base_slug = slugify(title)
            slug = base_slug
            pdf_extension = os.path.splitext(pdf.name)[1]
            save_path = os.path.join('media/pdfs/', f"{slug}{pdf_extension}")
            counter = 1

            while Book.objects.filter(slug=slug).exists() and os.path.exists(save_path):
                slug = f"{base_slug}-{counter}"
                save_path = os.path.join('media/pdfs/', f"{slug}{pdf_extension}")
                print(slug)
                counter += 1
            
            pdf.name = f"{slug}{pdf_extension}"

        book = Book(
            title=title,
            author=author,
            publication_date=publication_date,
            category=category,
            description=description,
            status=status,
            score=score,
            pdf=pdf,
            cover_image=cover_image,
            slug=slug,
        )
        book.save()
        if pdf:
            convert_pdf_to_jpg(book)
        return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})

def book_update(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})

def book_delete(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

def convert_pdf_to_jpg(book):
    file_name = str(book.pdf).split('/')[-1].split('.')[0]
    print(file_name)
    pdf_document = fitz.open(book.pdf.path)
    output_folder = f"media/books/{file_name}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()
        output_path = f"media/books/{file_name}/page_{page_number + 1}.png"
        pix.save(output_path)
    pdf_document.close()

def book_search(request):
    query = request.GET.get('search')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})
