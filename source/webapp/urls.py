from django.urls import path

from webapp.views import IndexView, AdCreateView, AdToDeleteView, DeactivatedListView, AdActivateView, AdListView, \
    AdToDeleteFromListView

app_name = 'webapp'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('ad_create/<str:type>/', AdCreateView.as_view(), name='ad_create'),
    path('ad_to_delete/<int:pk>/', AdToDeleteView.as_view(), name='ad_to_delete'),
    path('ad_to_delete_from_list/<int:pk>/<str:type>', AdToDeleteFromListView.as_view(), name='ad_to_delete_from_list'),
    path('ad_activate/<int:pk>/', AdActivateView.as_view(), name='ad_activate'),
    path('deactivated/', DeactivatedListView.as_view(), name='deactivated_list'),
    path('ad_list/<str:type>', AdListView.as_view(), name='ad_list'),

    # path('product/add/', ProductCreateView.as_view(), name='product_create'),
    # path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    # path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    # path('product_category/<int:pk>', ProductListView.as_view(), name='products_category'),
    # path('product_sub_category/<int:pk>', ProductSubCategoryListView.as_view(), name='products_sub_category'),
    # path('product_list/', ProductListGetView.as_view(), name='products_list_get'),
    # path('product/add-to-favorites/', AddToFavorites.as_view(), name='add_to_favorites'),
    # path('product/delete-from-favorites/', DeleteFromFavorites.as_view(), name='delete_from_favorites'),
    # path('products_favorites/', FavoritesList.as_view(), name='favorite_products'),
    # path('product/add-to-offer/', AddToOffer.as_view(), name='add_to_offer'),
    # path('product/delete-from-offer/', DeleteFromOffer.as_view(), name='delete_from_offer'),
    # path('products_in_offer/', ProductsOfferListView.as_view(), name='offer_products'),
]