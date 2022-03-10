from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django_request_mapping import request_mapping
from board.models import Board, User, Wiki
from django.utils import timezone

@request_mapping("")
class MyView(View):

    @request_mapping("/", method="get")
    def home(self,request):
        objs = Board.objects.order_by('-board_date').all();
        context = {
            'objs': objs
        };

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
        wiki = request.POST['wiki'];
        try:
                data = Board(board_title=title, board='공지', user_id=request.session['sessionid'], wiki_id=wiki, board_content=text,
                             board_date=timezone.now());
                data.save()
                return render(request, 'notice/postok.html');
        except:  # id 값이 없으므로 에러가 남
            return render(request, 'notice/postfail.html');



    # ================================================================

    @request_mapping("/info/info", method="get") #정보게시판
    def info(self, request):
        objs = Board.objects.order_by('-board_date').filter(board='정보');
        page = request.GET.get('page', '1');
        paginator = Paginator(objs, '10');
        page_obj = paginator.get_page(page);
        context = {
            'objs': page_obj
        };
        return render(request, 'info/info.html', context);

    @request_mapping("/info/post", method="get")  # 공지사항
    def infopost(self, request):
        wiki = Wiki.objects.all()
        objs = [];
        for i in range(0, len(wiki)):
            objs.append(wiki[i].wiki_title)
        context = {
            'objs': objs
        }
        return render(request, 'info/post.html', context);

    @request_mapping("/info/info/p", method="post")  # 공지사항
    def info_post(self, request):
        wiki_title = request.POST['wiki'];
        wiki = Wiki.objects.get(wiki_title = wiki_title)
        title = request.POST['title'];
        text = request.POST['content'];
        try:
                data = Board(board_title=title, board='정보', user_id=request.session['sessionid'], wiki_id=wiki.wiki_id,
                             board_content=text,
                             board_date= timezone.now());
                data.save()
                return render(request, 'info/postok.html');
        except:  # id 값이 없으므로 에러가 남
            return render(request, 'postfail.html');



    # ================================================================
    @request_mapping("/free/free", method="get") #자유게시판
    def free(self, request):
        objs = Board.objects.order_by('-board_date').filter(board='자유');
        page = request.GET.get('page', '1');
        paginator = Paginator(objs, '10');
        page_obj = paginator.get_page(page);

        context = {
            'objs': page_obj
        };
        return render(request, 'free/free.html',context);

    @request_mapping("/free/post", method="get")  # 공지사항
    def freepost(self, request):
        wiki = Wiki.objects.all()
        objs = [];
        for i in range(0,len(wiki)):
            objs.append(wiki[i].wiki_title)
        context = {
            'objs':objs
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



    # ================================================================
    @request_mapping("/qna/qna", method="get") #질문게시판
    def qna(self, request):
        objs = Board.objects.order_by('-board_date').filter(board='질문');

        page = request.GET.get('page', '1');
        paginator = Paginator(objs, '10');
        page_obj = paginator.get_page(page);
        context = {
            'objs': page_obj
        };
        return render(request, 'qna/qna.html',context);

    @request_mapping("/qna/post", method="get")  # 공지사항
    def qnapost(self, request):
        wiki = Wiki.objects.all()
        objs = [];
        for i in range(0, len(wiki)):
            objs.append(wiki[i].wiki_title)
        context = {
            'objs': objs
        }
        return render(request, 'qna/post.html', context);

    @request_mapping("/qna/qna/p", method="post")  # 질문
    def qna_insert(self, request):
        title = request.POST['title'];
        text = request.POST['content'];
        wiki_title = request.POST['wiki'];
        wiki = Wiki.objects.get(wiki_title=wiki_title)
        try:
            data = Board(board_title=title, board='질문', user_id=request.session['sessionid'], wiki_id=wiki.wiki_id,
                         board_content=text,
                         board_date=timezone.now());
            data.save()
            return render(request, 'qna/postok.html');
        except:  # id 값이 없으므로 에러가 남
            return render(request, 'postfail.html');



    # ================================================================
    @request_mapping("/project/project", method="get") #프로젝트
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
                         board_date=timezone.now(),board_num = num, board_place = place,
                         board_recruitdate = recruitdate, board_time = time, board_on_off = on_off,
                         board_phone = phone);
            data.save()
            return render(request, 'project/postok.html');
        except:  # id 값이 없으므로 에러가 남
            return render(request, 'postfail.html');



    # ================================================================
    @request_mapping("/study/study", method="get") #스터디
    def study(self, request):
        objs = Board.objects.order_by('-board_date').filter(board='스터디');

        page = request.GET.get('page', '1');
        paginator = Paginator(objs, '10');
        page_obj = paginator.get_page(page);
        context = {
            'objs': page_obj
        };
        return render(request, 'study/study.html',context);

    @request_mapping("/study/post", method="get")  # 스터디로
    def studypost(self, request):
        wiki = Wiki.objects.all()
        objs = [];
        for i in range(0, len(wiki)):
            objs.append(wiki[i].wiki_title)
        context = {
            'objs': objs
        }
        return render(request, 'study/post.html', context);

    @request_mapping("/study/study/p", method="post")  # 질문
    def study_insert(self, request):
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
            data = Board(board_title=title, board='스터디', user_id=request.session['sessionid'], wiki_id=wiki.wiki_id,
                         board_content=content,
                         board_date=timezone.now(),board_num = num, board_place = place,
                         board_recruitdate = recruitdate, board_time = time, board_on_off = on_off,
                         board_phone = phone);
            data.save()
            return render(request, 'study/postok.html');
        except:  # id 값이 없으므로 에러가 남
            return render(request, 'postfail.html');



    # ================================================================
    @request_mapping("/post", method="get")
    def post(self, request):
        return render(request, 'post.html');

    @request_mapping("/wiki/wiki", method="get")
    def wiki(self, request):
        return render(request, 'wiki/wiki.html');

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