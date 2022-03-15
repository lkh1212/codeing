from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django_request_mapping import request_mapping
from board.models import Board, User, Wiki, Revision, Comment
from django.utils import timezone

@request_mapping("")
class NoticeView(View):
    @request_mapping("/notice/notice", method="get") #공지사항
    def notice(self, request):
        objs = Board.objects.order_by('-board_date').filter(board='공지');
        page = request.GET.get('page','1');
        paginator = Paginator(objs,'10');
        page_obj = paginator.get_page(page);
        context = {
            'objs': page_obj
        };
        return render(request, 'notice/notice.html', context);

    @request_mapping("/notice/post", method="get")  # 공지사항
    def noticepost(self, request):

        return render(request, 'notice/post.html');

    @request_mapping("/notice/notice/p", method="post")  # 공지사항
    def notice_post(self, request):
        title = request.POST['title'];
        text = request.POST['content'];
        try:
                data = Board(board_title=title, board='공지', user_id=request.session['sessionid'], wiki_id='1', board_content=text,
                             board_date=timezone.now());
                data.save()
                return render(request, 'notice/postok.html');
        except:  # id 값이 없으므로 에러가 남
            return render(request, 'postfail.html');