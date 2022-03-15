from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django_request_mapping import request_mapping
from board.models import Board, User, Wiki, Revision, Comment
from django.utils import timezone

@request_mapping("")
class ClipView(View):
    # 20220314 코드 추가 ####################################################
    @request_mapping("/clip/delete/", method="post")
    def scrap_delete(self, request):
        """
        스크랩 삭제 함수
        """
        from .models import Clipping
        from django.http import JsonResponse
        import json

        if 'sessionid' in request.session:  # 로그인 체크

            try:
                data = json.loads(request.body)

                board = Board.objects.get(board_id=data)
                user = User.objects.get(user_id=request.session['sessionid'])
                clip = Clipping.objects.get(user_id=user,
                                            board_id=board)
                clip.delete()
                context = {
                    'result': data,
                }
            except:
                context = {
                    'result': 'fail',
                }
            return JsonResponse(context)

    #####################################################

    @request_mapping("/notice/scrap/", method="get")
    def notice_scrap(self, request):
        """
        스크랩 함수
        :param request:
        :return:
        """

        from .models import Clipping
        from django.shortcuts import get_object_or_404

        if 'sessionid' in request.session:
            type = request.GET['type']
            board = Board.objects.get(board_id=request.GET['board_id'])
            user = User.objects.get(user_id=request.session['sessionid'])
            try:
                cliped = Clipping.objects.get(user=user
                                              , board=board)  # 스크랩여부 체크
            except:
                cliped = None
            if not cliped:
                clip = Clipping(user=user,
                                board=board)
                clip.save()
                suc = 'Y'
            else:
                suc = 'dup'
            url = '/' + type + '/' + type
        else:
            url = '/login'
            suc = 'login'

        context = {'url': url,
                   'suc': suc}
        return render(request, 'clip/postok.html', context)

    @request_mapping("/scrap/scrap/", method="get")
    def scrap(self, request):
        """
        스크랩 리스트 화면
        """
        from django.shortcuts import redirect
        from .models import Clipping
        # 로그인 체크
        if 'sessionid' in request.session:
            user = User.objects.get(user_id=request.session['sessionid'])
            clips = Clipping.objects.filter(user_id=user)  # 로그인한 유저가 등록한 board_id 가져오기
            boards = []
            if clips:
                for clip in clips:
                    boards.append(Board.objects.get(board_id=clip.board_id))  # board_id를 이용하여 Board정보 가져오기

            page = request.GET.get('page', '1')
            paginator = Paginator(boards, '10')
            page_obj = paginator.get_page(page)
            context = {'objs': page_obj}

            return render(request, 'clip/clip.html', context)
        else:
            return redirect('/login')

    @request_mapping("/clip/detail/", method="get")
    def scrap_detail(self, request):
        from django.shortcuts import redirect
        commentpage = Comment.objects.filter(board_id=request.GET['board_id'])
        page = request.GET.get('page', '1');
        paginator = Paginator(commentpage, '10');
        page_obj = paginator.get_page(page);

        if 'sessionid' in request.session:
            board = Board.objects.get(board_id=request.GET['board_id'])  # board_id로 Board정보 가져오기
            comments = Comment.objects.filter(board=board.board_id)
            context = {'board': board, 'comments': comments, 'objs': page_obj}

            return render(request, 'clip/detail.html', context)
        else:
            return redirect('/login')

    @request_mapping("/wiki/detail/", method="get")
    def wiki_detail(self, request):
        from django.shortcuts import redirect
        wiki = Wiki.objects.get(wiki_id=request.GET['wiki_id'])  # board_id로 Board정보 가져오기
        context = {'wiki': wiki}
        return render(request, 'wiki/detail_wiki.html', context)

    # ======================================================= 댓글 CRUD
    @request_mapping("/clip/comment", method="post")
    def comment_add(self, request):
        from django.shortcuts import redirect
        if 'sessionid' in request.session:
            board = Board.objects.get(board_id=request.POST['board_id'])  # board_id로 Board정보 가져오기
            user = User.objects.get(user_id=request.session['sessionid'])

            comment = Comment();
            comment.user = user
            comment.comment_date = timezone.now()
            comment.board = board
            comment.comment_content = request.POST['content']
            comment.save()

            return redirect('/clip/detail?board_id={}'.format(request.POST['board_id']))
        else:
            return redirect('/login')

    @request_mapping("/clip/comment/uv/<int:b_id>/<int:c_id>/", method="get")
    def comment_updateView(self, request, b_id, c_id):
        from django.shortcuts import redirect
        if 'sessionid' in request.session:
            board = Board.objects.get(board_id=b_id)  # board_id로 Board정보 가져오기

            comments = Comment.objects.filter(board=board.board_id)
            comment = Comment.objects.get(comment_id=c_id);

            context = {'board': board,
                       'comment': comment,
                       'comments': comments}

            return render(request, 'clip/comment_update.html', context)
        else:
            return redirect('/login')

    @request_mapping("/clip/comment/u/<int:b_id>/<int:c_id>/", method="post")
    def comment_update(self, request, b_id, c_id):
        from django.shortcuts import redirect
        if 'sessionid' in request.session:
            board = Board.objects.get(board_id=b_id)  # board_id로 Board정보 가져오기

            comment = Comment.objects.get(comment_id=c_id);
            comment.comment_date = timezone.now()
            comment.comment_content = request.POST['content']
            comment.save()

            return redirect('/clip/detail?board_id={}'.format(b_id))
        else:
            return redirect('/login')

    @request_mapping("/clip/comment/d/<int:b_id>/<int:c_id>/", method="get")
    def comment_delete(self, request, b_id, c_id):
        from django.shortcuts import redirect
        if 'sessionid' in request.session:
            board = Board.objects.get(board_id=b_id)  # board_id로 Board정보 가져오기

            comment = Comment.objects.get(comment_id=c_id);
            comment.delete();

            return redirect('/clip/detail?board_id={}'.format(b_id))
        else:
            return redirect('/login')
