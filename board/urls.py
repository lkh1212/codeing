from django_request_mapping import UrlPattern

from board.views import MyView
from board.views_clip import ClipView
from board.views_free import freeView
from board.views_info import InfoView
from board.views_notice import NoticeView
from board.views_project import ProjectView
from board.views_qna import QnaView
from board.views_study import StudyView
from board.views_wiki import WikiView

urlpatterns = UrlPattern();
urlpatterns.register(MyView);
urlpatterns.register(ClipView);
urlpatterns.register(freeView);
urlpatterns.register(InfoView);
urlpatterns.register(NoticeView);
urlpatterns.register(ProjectView);
urlpatterns.register(QnaView);
urlpatterns.register(StudyView);
urlpatterns.register(WikiView);

