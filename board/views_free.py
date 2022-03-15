from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django_request_mapping import request_mapping
from board.models import Board, User, Wiki, Revision, Comment
from django.utils import timezone

@request_mapping("")
class freeView(View):
    @request_mapping("/free/free", method="get")  # 자유게시판
    def free(self, request):
        objs = Board.objects.order_by('-board_date').filter(board='자유');
        page = request.GET.get('page', '1');
        paginator = Paginator(objs, '10');
        page_obj = paginator.get_page(page);

        context = {
            'objs': page_obj
        };
        return render(request, 'free/free.html', context);

    @request_mapping("/free/post", method="get")  # 공지사항
    def freepost(self, request):
        wiki = Wiki.objects.all()
        objs = [];
        for i in range(0, len(wiki)):
            objs.append(wiki[i].wiki_title)
        context = {
            'objs': objs
        }
        return render(request, 'free/post.html', context);

    @request_mapping("/free/free/p", method="post")  # 공지사항
    def free_insert(self, request):
        title = request.POST['title'];
        text = request.POST['content'];
        objs = User.objects.all();
        wiki_title = request.POST['wiki'];
        wiki = Wiki.objects.get(wiki_title=wiki_title)
        try:
            data = Board(board_title=title, board='자유', user_id=request.session['sessionid'], wiki_id=wiki.wiki_id,
                         board_content=text,
                         board_date=timezone.now());
            data.save()
            return render(request, 'free/postok.html');
        except:  # id 값이 없으므로 에러가 남
            return render(request, 'postfail.html');


