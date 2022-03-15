from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django_request_mapping import request_mapping
from board.models import Board, User, Wiki, Revision, Comment
from django.utils import timezone

@request_mapping("")
class MyView(View):

    # 홈

    @request_mapping("/", method="get")
    def home(self,request):
        objs_notice = Board.objects.order_by('-board_date').filter(board='공지')[:5];
        objs_info = Board.objects.order_by('-board_date').filter(board='정보')[:5];
        objs_free = Board.objects.order_by('-board_date').filter(board='자유')[:5];
        objs_qna = Board.objects.order_by('-board_date').filter(board='질문')[:5];
        objs_study = Board.objects.order_by('-board_date').filter(board='스터디')[:5];
        objs_project = Board.objects.order_by('-board_date').filter(board='프로젝트')[:5];
        context = {
            'objs_notice':objs_notice,
            'objs_info': objs_info,
            'objs_free':objs_free,
            'objs_qna' : objs_qna,
            'objs_study':objs_study,
            'objs_project':objs_project
        }
        return render(request,'home.html',context);

    # 검색
    @request_mapping("/search", method="get")
    def search(self,request):
        context =[];
        search_type = request.GET['type']
        search_word = request.GET['q']
        board_list = Board.objects.select_related('user');
        print(search_type, search_word)
        print(board_list.query)
        print('----------------')

        if search_word:
            if len(search_word) > 1 :
                if search_type == 'all':
                    search_board_list = board_list.filter(Q (board_title__icontains=search_word) | Q (board_content__icontains=search_word) | Q (user__user_id__icontains=search_word))
                elif search_type == 'title_content':
                    search_board_list = board_list.filter(Q (board_title__icontains=search_word) | Q (board_content__icontains=search_word))
                elif search_type == 'title':
                    search_board_list = board_list.filter(board_title__icontains=search_word)
                elif search_type == 'content':
                    search_board_list = board_list.filter(board_content__icontains=search_word)
                elif search_type == 'writer':
                    search_board_list = board_list.filter(user__user_id__icontains=search_word)

                print(search_board_list)
                print(type(search_board_list))
                context={
                    'search_boards':search_board_list,
                    'search_term':search_word
                }
            else:
                context={'message':'검색어는 2글자 이상 입력해주세요.'}
                # messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return render(request,'search_board.html', context);



    # ================================================================
    @request_mapping("/post", method="get")
    def post(self, request):
        return render(request, 'post.html');


    # ================================================================
    @request_mapping("/register", method="get")  # 회원가입
    def register(self, request):
        return render(request, 'register.html');

    @request_mapping("/registerimpl", method="post")
    def registerimpl(self, request):
        user_id = request.POST['user_id'];
        user_pwd = request.POST['user_pwd'];
        user_name = request.POST['user_name'];
        user_email = request.POST['user_email'];
        user_phone = request.POST['user_phone'];
        favcom1 = request.POST['favcom1'];
        favcom2 = request.POST['favcom2'];
        favlang1 = request.POST['favlang1'];
        favlang2 = request.POST['favlang2'];

        context = {}
        try:
            User.objects.get(user_id=user_id)
            context['center'] = 'registerfail.html'
        except:
            User(user_id=user_id, user_pwd=user_pwd, user_name=user_name, user_email=user_email,
                 user_phone=user_phone, favcom1=favcom1, favcom2=favcom2, favlang1=favlang1, favlang2=favlang2).save()
            context['center'] = 'registerok.html'

        return render(request, 'home.html', context)

    @request_mapping("/login", method="get")  # 공지사항
    def login(self, request):
        return render(request, 'login.html');

    @request_mapping("/loginimpl", method="post")  # 공지사항
    def loginimpl(self, request):

        user_id = request.POST['id']
        user_pwd = request.POST['pwd']

        try:
            user = User.objects.get(user_id=user_id)
            if user.user_pwd == user_pwd:
                request.session['sessionid'] = user.user_id;
                request.session['sessionname'] = user.user_name;
                return render(request, 'home.html');
            else:
                raise Exception
        except:
            return render(request, 'loginfail.html');

    @request_mapping("/logout", method="get")
    def logout(self, request):
        if request.session['sessionid'] != None:
            del request.session['sessionid']

        return render(request, 'home.html')