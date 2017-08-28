from django.views.generic import TemplateView,ListView
from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from .models import Idc

class CreateIdcView(TemplateView):
    template_name = "idc/add_idc.html"

    def post(self, request):
        print(request.POST)

        print(reverse("success", kwargs={"next":"user_list"}))
        #return redirect("success", next="user_list")
        errmsg = "人为的失败，请重新处理"
        return redirect("error",next="idc_add",msg="人为的失败，请重新处理")
        #return HttpResponse("")



class ListIdcView(ListView):
    template_name = "idc/list_idc.html"
    model = Idc
    
    paginate_by=10
    ordering = "id"

    before_page=3
    after_page=3


    def get_queryset(self):
        query_set = super(ListIdcView,self).get_queryset()
        search_name = self.request.GET.get("search_name",None)
        if search_name:
           try:
               query_set = query_set.filter(name__icontains=search_name)   
           except Exception as e:
               print(e)
               pass
        return query_set


    def get_context_data(self,**kwargs):
        context = super(ListIdcView,self).get_context_data(**kwargs)
        page_obj=context["page_obj"]
        context["page_range"] = self.get_page_range(page_obj) 

        search_name = self.request.GET.get("search_name","")
        context["search_name"] = search_name
        context["search_data"] = "&search_name={}".format(search_name)
        #print(context["search_data"]) 
        return context


    def get_page_range(self,page_obj):
        page_number = page_obj.number
        max_page_number = page_obj.paginator.num_pages
        print(max_page_number)
        temp_page = page_number - self.before_page
        if temp_page>0:
            start_page=temp_page
            temp_end_page = page_number + self.after_page
            if temp_end_page<max_page_number:
                end_page=temp_end_page+1
            else:
                end_page=max_page_number+1
                temp_start_page=max_page_number - self.before_page - self.after_page
                if temp_start_page>0:
                    start_page=temp_start_page
                else:
                    start_page=1
        else:
            start_page=1
            temp_end_page = self.before_page + self.after_page + start_page
            if temp_end_page<max_page_number:
                end_page=temp_end_page+1
            else:
                end_page=max_page_number+1



        #print(range(start_page,end_page))
        return range(start_page,end_page)


