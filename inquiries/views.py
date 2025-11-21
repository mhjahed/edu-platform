from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Inquiry, InquiryMessage


class InboxView(LoginRequiredMixin, ListView):
    model = Inquiry
    template_name = 'inquiries/inbox.html'
    context_object_name = 'inquiries'
    paginate_by = 20
    
    def get_queryset(self):
        return Inquiry.objects.filter(recipient=self.request.user)


class SentInquiriesView(LoginRequiredMixin, ListView):
    model = Inquiry
    template_name = 'inquiries/sent.html'
    context_object_name = 'inquiries'
    paginate_by = 20
    
    def get_queryset(self):
        return Inquiry.objects.filter(sender=self.request.user)


class CreateInquiryView(LoginRequiredMixin, CreateView):
    model = Inquiry
    fields = ['subject', 'recipient', 'exam', 'priority']
    template_name = 'inquiries/create.html'
    success_url = reverse_lazy('inquiries:sent')
    
    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)


class InquiryDetailView(LoginRequiredMixin, DetailView):
    model = Inquiry
    template_name = 'inquiries/detail.html'
    context_object_name = 'inquiry'


class ReplyToInquiryView(LoginRequiredMixin, CreateView):
    model = InquiryMessage
    fields = ['message', 'attachment']
    template_name = 'inquiries/reply.html'
    
    def form_valid(self, form):
        inquiry = get_object_or_404(Inquiry, pk=self.kwargs['pk'])
        form.instance.inquiry = inquiry
        form.instance.sender = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('inquiries:detail', kwargs={'pk': self.kwargs['pk']})


class CloseInquiryView(LoginRequiredMixin, View):
    def post(self, request, pk):
        inquiry = get_object_or_404(Inquiry, pk=pk)
        inquiry.status = 'closed'
        inquiry.save()
        messages.success(request, 'Inquiry closed successfully.')
        return redirect('inquiries:inbox')


class DeleteInquiryView(LoginRequiredMixin, DeleteView):
    model = Inquiry
    template_name = 'inquiries/delete.html'
    success_url = reverse_lazy('inquiries:inbox')


class MarkReadView(LoginRequiredMixin, View):
    def post(self, request):
        message_id = request.POST.get('message_id')
        if message_id:
            try:
                message = InquiryMessage.objects.get(id=message_id)
                message.is_read = True
                message.save()
                return JsonResponse({'status': 'success'})
            except InquiryMessage.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Message not found'})
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})


class GetUnreadCountView(LoginRequiredMixin, View):
    def get(self, request):
        unread_count = InquiryMessage.objects.filter(
            inquiry__recipient=request.user,
            is_read=False
        ).count()
        return JsonResponse({'unread_count': unread_count})
