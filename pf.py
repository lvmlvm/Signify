from question import subjects
from io import *
import json
import datetime as dt
''' Tạo pm = ProjectManager() lúc khởi tạo app
    Sau khi đăng nhập/đăng kí thì thao tác phía người dùng qua pm.user: Profile
'''

def json_default(o):
    if isinstance(o, dt.datetime):
        return dict(year=o.year, month=o.month, day=o.day, hour=o.hour, minute=o.minute, second=o.second)
    else:
        return o.__dict__

class Achievement:
    def __init__(self, name: str = '', description: str = '', __current: int = 0, max: int = 0, weight = 0, img_url: str = 'assets/images/achievement/demo.png') -> None:
        self.name = name        #tên
        self.description = description  #mô tả
        self.__current = __current  #tiến độ hiện tại, dùng property self.current
        self.weight = weight    #Độ nổi bật aka độ khó, tạm thời dùng để sort, có thể dùng để tính tổng điểm achievement
        self.max = max          #tiến độ tối đa
        self.img_url = img_url  #url hình ảnh
    
    @property
    def completed(self) -> bool:
        return self.current >= self.max
    
    @property
    def current(self) -> int:
        return self.__current
    
    @current.setter
    def current(self, value: int):
        if value > self.__current:
            if value >= self.max: self.__current = self.max
            elif value >= 0: self.__current = value
            else: self.__current = 0

class AchievementSet:
    '''Một bộ Achievement, ứng với mỗi hồ sơ người dùng
    Đã cài đặt phần cập nhật:
    '''
    def __init__(self, **kwargs) -> None:
        if kwargs.get('complete_first_quiz') != None:
            self.complete_first_quiz = Achievement(**kwargs.get('complete_first_quiz'))
        else:
            self.complete_first_quiz = Achievement(max=100, weight=2, name='Điểm tuyệt đối đầu tiên', description='Lần đầu tiên hoàn thiện 100%% một bài luyện tập.')
            
        if kwargs.get('complete_all_quiz') != None:
            self.complete_first_quiz = Achievement(**kwargs.get('complete_all_quiz'))
        else:
            self.complete_all_quiz = Achievement(max=len(subjects), weight=len(subjects)*2, name='Thành thạo', description='Hoàn thiện 100%% các bài luyện tập của tất cả chủ đề.')
        
        #Dùng cho demo
        if kwargs.get('do_first_quiz') != None:
            self.do_first_quiz = Achievement(**kwargs.get('do_first_quiz'))
        else:
            self.do_first_quiz= Achievement(max=1, weight=1, name='Chập chững', description='Trải nghiệm bài luyện tập đầu tiên của bạn.')
        
        if kwargs.get('hardwork') != None:
            self.hardwork = Achievement(**kwargs.get('hardwork'))
        else:
            self.hardwork = Achievement(max=10, weight=2, name='Chăm chỉ', description='Thực hiện 10 bài luyện tập.')
        
        if kwargs.get('veteran') != None:
            self.veteran = Achievement(**kwargs.get('veteran'))
        else:
            self.veteran = Achievement(max=100, weight=5, name='Kỳ cựu', description='Là thành viên của đại gia đình Signify được 100 ngày.')
            
    @property
    def total_score(self) -> int:
        res = 0
        for attribute in vars(self):
            achievement: Achievement = getattr(self, attribute)
            if achievement.completed:
                res += achievement.weight
        return res
        
    def get_list(self, sorted = True) -> list[Achievement]:
        '''Trả về một list MỚI chứa toàn bộ Achievement của profile hiện tại, được sắp xếp từ lớn->bé theo completion -> weight.
        '''
        res: list[Achievement] = []
        for attribute in vars(self):
            res.append(getattr(self, attribute))
        
        if sorted:
            res.sort(reverse=True, key=lambda a: (a.completed, a.weight))
        
        return res
    
class Progress:    #Tiến độ học của một chủ đề
    """
        ``learn_current`` (str): Mục (aka item, từ) đang học dở trong bài học.\n
        ``quiz_completion`` (int): Tỉ lệ hoàn thiện bài luyện tập cao nhất 0-100. \n
        ``recency`` (datetime | None nếu chưa học/luyện tập lần nào): Thời điểm học/luyện tập gần nhất.
    """
    def __init__(self, learn_current: str = None, __quiz_completion: int = 0, recency: dict = None) -> None:      
        self.learn_current = learn_current
        self.__quiz_completion = __quiz_completion  #Dùng property
        if recency != None:
            self.recency = dt.datetime(**recency)
        else:
            self.recency = None
    
    @property
    def quiz_completion(self) -> int:
        return self.__quiz_completion
    
    @quiz_completion.setter
    def current(self, value: int):
        if value > self.__quiz_completion:
            if value >= 100: self.__quiz_completion = 100
            elif value >= 0: self.__quiz_completion = value
            else: self.__quiz_completion = 0

class Setting:
    pass

class Profile:
    '''Mỗi profile ứng với 1 người dùng\n
        Update progress và achivements thông qua các hàm on_...(), gọi hàm cho các event tương ứng.\n
        ``email``,``password``,``name``: str\n
        ``achievements``: AchievementSet\n
        ``creation_date``: datetime.datetime\n
        ``region``: str, None nếu chưa chọn\n
        ``following_emails``: list[str] truy vấn qua phương thức của ProfileManger\n
        ``progress``: dict = {\n
            'Chủ đề': Progress\n
            ...\n
        }
    '''
    def __init__(self, email: str, password: str, name: str, region: str = None, following_emails: list[str] = [], progress: dict = None, achievements: dict = {}, creation_date: dict = None) -> None:
        
        self.email = email
        self.password = password
        self.name = name
        self.region = region
        self.following_emails = following_emails                #Truy vấn qua hàm trong ProfileManager
        self.achievements = AchievementSet(**achievements)
        self.progress: dict[str, Progress] = {}
        
        if progress != None:   
            for subject in subjects:
                self.progress[subject] = Progress(**progress[subject])
        else:
            for subject in subjects:
                self.progress[subject] = Progress()
        
        if creation_date != None:
            self.creation_date = dt.datetime(**creation_date)
        else:
            self.creation_date = dt.datetime.now()
            
    def on_move_to_learing_item(self, subject: str, item: str):
        self.progress[subject].learn_current = item
    
    def on_quiz_done(self, questionaire: str, score: int):
        progress = self.progress[questionaire['name']]
        
        #Cập nhật progress
        completion =  score * (100 / questionaire['size'])
        if completion < progress.quiz_completion: return
        progress.quiz_completion = completion
        
        #achievement hardwork
        self.achievements.hardwork.current += 1
        
        #achievement complete_first_quiz, do_first_quiz
        highest = 0
        for sbj in subjects:
            completion = self.progress[sbj].quiz_completion
            if completion > highest:
                highest = completion
        self.achievements.complete_first_quiz.current = highest
        self.achievements.do_first_quiz.current += 1
                
        # Cập nhật achievements complete_all_quiz
        if progress.quiz_completion >= 100:
            completed_cnt = 0
            for sbj in subjects:
                if self.progress[sbj].quiz_completion >= 100:
                    completed_cnt += 1
            self.achievements.complete_all_quiz.current = completed_cnt
            
    def on_open_learn_or_quiz(self, subject: str):
        self.progress[subject].recency = dt.datetime.now()
        
    def on_login(self):#Đã gọi xong
        #achievement veteran, tạm thời update ở đây thay vì trong vòng lặp
        delta = dt.datetime.now() - self.creation_date
        self.achievements.veteran.current = delta.days
        
class ProfileManager:
    '''Quản lý hồ sơ người dùng hiện tại và toàn bộ người dùng.\n
    Tạo 1 đối tượng duy nhất lúc khởi tạo app.\n
    Có thể gọi hàm load(), safe() trong lúc app chạy,\n
    hoặc để constructor với destructor lo (chỉ load 1 lần lúc gọi constructor và save 1 lần lúc gọi destructor).
    '''
    def __init__(self) -> None:
        self.user: Profile = None                   #Người dùng hiện tại (đang đăng nhập)
        self.profiles: list['Profile'] = []           #Tất cả hồ sơ
        self._path = 'local/profiles.json'
        self.load()
        
    def __del__(self):
        self.save()
    
    def load(self):
        '''load dữ liệu từ _path, update profiles và user
        '''
        print('Loading from ' + self._path + '...')
        self.profiles.clear()
        with open(self._path, 'r', encoding='utf-8') as f:
            raw: list[dict] = json.load(f)
            for raw_element in raw:
                profile = Profile(**raw_element)
                self.profiles.append(profile)
            
            if (self.user != None):
                self.user = self.search_email(self.user.email)
            
    def save(self):
        '''save dữ liệu vào path
        '''
        print('Saving to ' + self._path + '...')
        with open(self._path, 'w', encoding='utf-8') as f:
            json.dump(self.profiles, f, default=json_default, indent=4, ensure_ascii=False)
        
    def login(self, email: str, password: str) -> Profile | str:
        """return: Nếu type() là str thì là thông báo lỗi, nếu ko thì là Profile của user
        """        
        profile = self.search_email(email)
        if profile != None:
            if (profile.password == password):
                self.user = profile
                self.user.on_login()        #Có thể chuyến sang lúc hiển thị giao diện sau khi login thành công
                return self.user
            return 'Sai mật khẩu. Vui lòng nhập lại.'
        return 'Tài khoản không tồn tại.'
    
    def logout(self):
        self.user = None
    
    def register(self, name: str, email: str, password: str) -> Profile | str:
        """return: Nếu type() là str thì là thông báo lỗi, nếu ko thì là Profile của user
        """
        profile = self.search_email(email)
        if profile == None:
            self.user = Profile(email=email, password=password, name=name)
            self.profiles.append(self.user)
            self.user.on_login()        #Có thể chuyến sang lúc hiển thị giao diện sau khi login thành công
            return self.user
        return 'Email đã tồn tại. Vui lòng chọn email khác.'
    
    def delete_user(self):
        '''Xóa tài khoản hiện tại
        '''
        if self.user != None:
            self.profiles.remove(self.user)
            self.user = None
    
    def search_email(self, email: str, suggestion_mode: bool = False) -> Profile | None | list[Profile] :
        if suggestion_mode == False:         #Tìm exact match
            for profile in self.profiles:
                if email == profile.email:
                    return profile
            return None
        else:                               #Tìm gợi ý
            matchings: list[Profile] = []
            for profile in self.profiles:
                if email.lower() in profile.email.lower():
                    matchings.append(profile)
            return matchings
    
    def search_name(self, name: str, suggestion_mode: bool = False) -> list[Profile]:
        matchings: list[Profile] = []
        for profile in self.profiles:
            if suggestion_mode == False:          
                if (suggestion_mode == False and name == profile.name) or (suggestion_mode == True and name.lower() in profile.name.lower()):
                    matchings.append(profile)
        return matchings
    
    def get_follower(self, user: Profile) -> list[Profile]:
        followers: list[Profile] = []
        for p in self.profiles:
            if p.following_emails == None: continue
            if user.email in p.following_emails:
                followers.append(p)
        return followers
    
    def get_following(self, user: Profile) -> list[Profile]:
        following: list[Profile] = []
        if user.following_emails == None: return following
        for p in self.profiles:
            if p.email in user.following_emails:
                following.append(p)
        return following

# pm = ProfileManager()
# user = pm.register(name='Nguyễn Văn A', email='asd@gmail.com', password='123456')
# pm.logout()
# user = pm.login(email='asd@gmail.com', password='123456')
# pm.delete_user()
# print(user.achievements.total_score)