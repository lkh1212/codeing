from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django_request_mapping import request_mapping
from board.models import Board, User, Wiki, Revision, Comment
from django.utils import timezone

@request_mapping("")
class ProjectView(View):
    @request_mapping("/project/project", method="get")  # 프로젝트
    def project(self, request):
        objs = Board.objects.order_by('-board_date').filter(board='프로젝트');

        page = request.GET.get('page', '1');
        paginator = Paginator(objs, '10');
        page_obj = paginator.get_page(page);
        context = {
            'objs': page_obj
        };
        return render(request, 'project/project.html', context);

    @request_mapping("/project/post", method="get")  #
    def projectpost(self, request):
        wiki = Wiki.objects.all()
        objs = [];
        for i in range(0, len(wiki)):
            objs.append(wiki[i].wiki_title)
        context = {
            'objs': objs
        }
        return render(request, 'project/post.html', context);

    @request_mapping("/project/project/p", method="post")  # 질문
    def project_insert(self, request):
        title = request.POST['board_title'];
        content = request.POST['board_content'];
        num = request.POST['board_num'];
        place = request.POST['board_place'];
        recruitdate = request.POST['board_recruitdate'];
        time = request.POST['board_time'];
        on_off = request.POST['board_on_off'];
        phone = request.POST['board_phone'];
        wiki_title = request.POST['wiki'];
        wiki = Wiki.objects.get(wiki_title=wiki_title)
        try:
            data = Board(board_title=title, board='프로젝트', user_id=request.session['sessionid'], wiki_id=wiki.wiki_id,
                         board_content=content,
                         board_date=timezone.now(), board_num=num, board_place=place,
                         board_recruitdate=recruitdate, board_time=time, board_on_off=on_off,
                         board_phone=phone);
            data.save()
            return render(request, 'project/postok.html');
        except:  # id 값이 없으므로 에러가 남
            return render(request, 'postfail.html');
