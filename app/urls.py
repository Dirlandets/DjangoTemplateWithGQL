from decouple import config
from graphene_django.views import GraphQLView

from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]

if config('DEBUGTOOLBAR', default=False):
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
