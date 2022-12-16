from django.contrib import admin
from projects.models.articles import BlogArticlePage
from projects.models.about import AboutPage
from projects.models.blogs import BlogPage
from projects.models.categories import CategoryPage
from projects.models.contact import ContactPage
from projects.models.home import HomePage
from projects.models.products import ProductPage
from projects.models.websites import Website


admin.site.register(AboutPage)
admin.site.register(BlogPage)
admin.site.register(CategoryPage)
admin.site.register(ContactPage)
admin.site.register(HomePage)
admin.site.register(ProductPage)
admin.site.register(Website)
