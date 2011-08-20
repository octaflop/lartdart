from django.views.generic import DetailView, ListView
from models import Gallery

class GalleryIndexView(ListView):
    queryset = Gallery.objects.all()
    model = Gallery()
home_view = GalleryIndexView.as_view()

class GalleryObjectView(DetailView):
    queryset = Gallery.objects.all()
    model = Gallery()
    context_object_name = 'gallery'
gallery_object_view = GalleryObjectView.as_view()
