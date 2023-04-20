from django.contrib import admin
from projects.models.articles import BlogArticlePage
from projects.models.blogs import BlogPage
from projects.models.categories import CategoryPage
from projects.models.products import ProductPage
from projects.models.websites import Website


admin.site.register(BlogPage)
admin.site.register(BlogArticlePage)
admin.site.register(CategoryPage)
admin.site.register(ProductPage)
admin.site.register(Website)
