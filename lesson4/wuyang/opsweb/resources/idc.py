from django.views.generic import TemplateView,ListView,View
from django.shortcuts import redirect, reverse
from django.http import HttpResponse,JsonResponse,QueryDict
from .models import Idc
import logging


class CreateIdcView(TemplateView):
    template_name = "idc/add_idc.html"

    def post(self, request):
        name = request.POST.get("name",None)
        idc_name = request.POST.get("idc_name",None)
        address = request.POST.get("address",None)
        username = request.POST.get("username",None)
        phone = request.POST.get("phone",None)
        email = request.POST.get("email",None)
      
        print(name,idc_name,address,username,phone,email)
        if name and idc_name and address and username and phone and email:
            try:
                has_idc = Idc.objects.filter(name=name)
                print(has_idc)
            except Exception as e:
                print(e)
                #errmsg = "查询发生异常" 


            if has_idc:
                errmsg = "该机房名已存在，请更换"
                return redirect("error",next="idc_add",msg=errmsg)
            else:
            
                data = {"name":name,"idc_name":idc_name,"address":address,"username":username,"phone":phone,"email":email}
                try:
                    idc = Idc(**data)
                    idc.save()
                except Exception as e:
                    print(e)
                    errmsg = "保存idc数据发生异常"
                    return redirect("error",next="idc_add",msg=errmsg)
        else:
            errmsg = "name,idc_name,address,username,phone,email不可以为空"
            return redirect("error",next="idc_add",msg=errmsg)
     


        #print(request.POST)
        #print(reverse("success", kwargs={"next":"user_list"}))
        #return redirect("success", next="user_list")
        #errmsg = "人为的失败，请重新处理"
        #return redirect("error",next="idc_add",msg="人为的失败，请重新处理")
        return redirect("success", next="idc_list")




class ListIdcView(ListView):
    template_name = "idc/list_idc.html"
    model = Idc
    
    paginate_by=10
    ordering = "-id" # 逆排序

    before_page=3
    after_page=3
    
    def get_queryset(self):
        query_set = super(ListIdcView,self).get_queryset()
        search_name = self.request.GET.get("search_name",None)
        #logger = logging.getLogger(__name__)
        #logger.error('Something went wrong!')
        if search_name:
           try:
               query_set = query_set.filter(name__icontains=search_name)   
               #logger.error('wuyang test logging!')
           except Exception as e:
               print(e)
               pass
        return query_set


    def get_context_data(self,**kwargs):
        context = super(ListIdcView,self).get_context_data(**kwargs)
        page_obj=context["page_obj"]
        context["page_range"] = self.get_page_range(page_obj) 
        
        search_name = self.request.GET.get("search_name","")
        if search_name:
            context["search_name"] = search_name
            context["search_data"] = "&search_name={}".format(search_name)
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

class DeleteIdcView(View):
    def delete(self,request):
        res={"status":0}
        data=QueryDict(request.body) 
        name=data.get("name","")
        print(name)
        if name:
            try:
                idc = Idc.objects.get(name=name).delete() 
            except Exception as e:            
                print(e)
                res["status"]=1
                res["errmsg"]="用户不存在或删除异常"
                return JsonResponse(res)


        else:
            res["status"]=1
            res["errmsg"]="要删除的用户名未获取到"




        return JsonResponse(res)











