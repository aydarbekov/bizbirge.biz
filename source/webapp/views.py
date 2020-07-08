from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView

from webapp.forms import AdForm, SimpleSearchForm
from webapp.models import Ad


class IndexView(ListView):
    template_name = 'index.html'
    model = Ad
    context_object_name = "ads"

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['ads_sorted'] = Ad.objects.filter(status='active', ad_type='need_help').order_by('-date')[:5]
        context['ads_sorted_can_help'] = Ad.objects.filter(status='active', ad_type='can_help').order_by('-date')[:5]
        context['ads_sorted_can_consult'] = Ad.objects.filter(status='active', ad_type='can_consult').order_by('-date')[:5]
        context['form'] = self.form
        return context


class AdCreateView(CreateView):
    model = Ad
    template_name = 'ad_create.html'
    form_class = AdForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['ad_type'] = self.kwargs.get('type')
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid_for_full(form)
        return self.form_invalid_for_full(form)

    def form_valid_for_full(self, form):
        self.object = form.save(commit=True)
        self.object.ad_type = self.request.POST.get('ad_type')
        print(self.object.ad_type)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid_for_full(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('webapp:index')


class AdToDeleteView(View):
    def get(self, *args, **kwargs):
        ad = Ad.objects.get(pk=int(self.kwargs.get('pk')))
        ad.status = 'deactivated'
        ad.save()
        return redirect('webapp:index')


class AdToDeleteFromListView(View):
    def get(self, *args, **kwargs):
        ad = Ad.objects.get(pk=int(self.kwargs.get('pk')))
        ad.status = 'deactivated'
        ad.save()
        return redirect('webapp:ad_list', type=self.kwargs.get('type'))


class AdActivateView(View):
    def get(self, *args, **kwargs):
        ad = Ad.objects.get(pk=int(self.kwargs.get('pk')))
        ad.status = 'active'
        ad.save()
        return redirect('webapp:deactivated_list')


class DeactivatedListView(LoginRequiredMixin, ListView):
    context_object_name = 'ad'
    model = Ad
    template_name = 'index.html'
    paginate_by = 10
    paginate_orphans = 3

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['ads_sorted'] = Ad.objects.filter(status='deactivated').order_by('-date')
        return context


class AdListView(ListView):
    context_object_name = 'ad'
    template_name = 'ad_list.html'
    paginate_by = 20
    paginate_orphans = 0
    ordering = '-date'

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        ad_type = self.kwargs.get('type')

        if ad_type != 'search':
            queryset = Ad.objects.filter(ad_type=ad_type, status='active').order_by('-date')
            return queryset
        elif ad_type == 'search':
            descr = self.search_value['descr']
            city = self.search_value['city']
            type = self.search_value['type']
            group = self.search_value['group']
            print(descr, city, type, group)
            if city != '' and descr == '' and group == '---':
                queryset = Ad.objects.filter(ad_type=type, status='active', city__icontains=city).order_by('-date')
                return queryset
            elif city == '' and descr != '' and group == '---':
                queryset = Ad.objects.filter(ad_type=type, status='active', description__icontains=descr).order_by('-date')
                return queryset
            elif city == '' and descr == '' and group != '---':
                queryset = Ad.objects.filter(ad_type=type, status='active', group__icontains=group).order_by('-date')
                return queryset
            elif city != '' and descr != '' and group == '---':
                queryset = Ad.objects.filter(ad_type=type, status='active', city__icontains=city, description__icontains=descr).order_by('-date')
                return queryset
            elif city != '' and descr == '' and group != '---':
                queryset = Ad.objects.filter(ad_type=type, status='active', city__icontains=city, group__icontains=group).order_by('-date')
                return queryset
            elif city == '' and descr != '' and group != '---':
                queryset = Ad.objects.filter(ad_type=type, status='active', descr__icontains=descr, group__icontains=group).order_by('-date')
                return queryset
            elif city != '' and descr != '' and group != '---':
                queryset = Ad.objects.filter(ad_type=type, status='active', city__icontains=city, description__icontains=descr, group__icontains=group).order_by('-date')
                return queryset
            elif city == '' and descr == '' and group == '---':
                queryset = Ad.objects.filter(ad_type=type, status='active').order_by('-date')
                return queryset


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        ad_type = self.kwargs.get('type')
        context['ads_sorted'] = Ad.objects.filter(ad_type=ad_type).order_by('-date')
        context['form'] = self.form
        return context

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        search = {}
        if self.form.is_valid():
            search['descr'] = self.form.cleaned_data['descr']
            search['city'] = self.form.cleaned_data['city']
            search['type'] = self.form.cleaned_data['type']
            search['group'] = self.form.cleaned_data['group']
            return search
        return None