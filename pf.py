from question import subjects
from io import open
import json
import datetime as dt
''' 
    Phải import pm = ProfileManager() đã được khai báo
    Sau khi đăng nhập/đăng kí thì thao tác phía người dùng qua pm.user
'''

def json_default(o):
    if isinstance(o, dt.datetime):
        return dict(year=o.year, month=o.month, day=o.day, hour=o.hour, minute=o.minute, second=o.second)
    else:
        return o.__dict__

class Achievement:
    def __init__(self, name: str = '', description: str = '', __increment: bool = True,__current: int = 0, max: int = 0, weight = 0, img_url: str = 'assets/images/achievement/demo.png') -> None:
        self.name = name        #tên
        self.description = description  #mô tả
        self.__current = __current  #tiến độ hiện tại, dùng property self.current
        self.weight = weight    #Độ nổi bật aka độ khó, tạm thời dùng để sort, có thể dùng để tính tổng điểm achievement
        self.max = max          #tiến độ tối đa
        self.img_url = img_url  #url hình ảnh
        self.__increment = __increment  #chỉ tăng hoặc có thể giảm
    
    @property
    def completed(self) -> bool:
        return self.current >= self.max
    
    @property
    def current(self) -> int:
        return self.__current
    
    @current.setter
    def current(self, value: int):
        if (not self.__increment) or value > self.__current:
            if value >= self.max: 
                self.__current = self.max
                self.on_completed()
            elif value >= 0: self.__current = value
            else: self.__current = 0
    
    def on_completed(self):
        if pm.user == None: return
        for p in pm.profiles:
            if pm.user is p: continue
            if pm.user.achievements.champion.completed:
                if pm.user.achievements.total_score - p.achievements.total_score < 50:
                    pm.user.achievements.champion.__current = 0
            elif pm.user.achievements.total_score > p.achievements.total_score:
                pm.user.achievements.champion.__current = 1         #ko đc gọi setter

class AchievementSet:
    '''Một bộ Achievement, ứng với mỗi hồ sơ người dùng
    Cần sung phần cập qua việc gọi các hàm on_...() và hiển thị giao diện chung.
    Cái nào chưa cài đặt xong thì để đấy làm decoy,
    lúc demo tạo trước tài khoản xong edit file profiles.json
    '''
    def __init__(self, **kwargs) -> None:
        if kwargs.get('complete_first_quiz') != None:   #gọi on_quiz_done()
            self.complete_first_quiz = Achievement(**kwargs.get('complete_first_quiz'))
        else:
            self.complete_first_quiz = Achievement(max=100, weight=5, name='Điểm tuyệt đối đầu tiên!', description='Lần đầu tiên đạt điểm điểm tuyệt đối bài luyện tập.')
            
        if kwargs.get('complete_all_quiz') != None: #gọi on_quiz_done()
            self.complete_first_quiz = Achievement(**kwargs.get('complete_all_quiz'))
        else:
            self.complete_all_quiz = Achievement(max=len(subjects), weight=len(subjects)*5, name='Thành thạo!', description='Đạt điểm tuyệt đối cho tất cả chủ đề.')
        
        if kwargs.get('hardwork') != None:  #gọi on_quiz_done()
            self.hardwork = Achievement(**kwargs.get('hardwork'))
        else:
            self.hardwork = Achievement(max=10, weight=7, name='Siêng năng!', description='Thực hiện 10 bài luyện tập.')
        
        if kwargs.get('champion') != None:   #đại khái đã implement xong phần update
            self.champion = Achievement(**kwargs.get('champion'))
        else:
            self.champion = Achievement(max=1, weight=49, name='Vô địch!', description='Tích lũy nhiều điểm thành tích hơn tất cả những người khác.\nBạn phải tiếp tục bỏ xa họ ít nhất 50 điểm nếu muốn duy trì ngôi vị.\n')
        
        if kwargs.get('veteran') != None:   #đại khái đã implement xong phần update
            self.veteran = Achievement(**kwargs.get('veteran'))
        else:
            self.veteran = Achievement(max=100, weight=8, name='Kỳ cựu!', description='Là thành viên của đại gia đình Signify được 100 ngày.')
            
        if kwargs.get('famous') != None:   #đại khái đã implement xong phần update
            self.famous = Achievement(**kwargs.get('famous'))
        else:
            self.famous = Achievement(max=10, weight=8, name='Nổi tiếng!', description='Được 10 người theo dõi.')

        #Có thể dùng cho demo
        if kwargs.get('do_first_quiz') != None: #gọi on_exit_quiz()
            self.do_first_quiz = Achievement(**kwargs.get('do_first_quiz'))
        else:
            self.do_first_quiz= Achievement(max=1, weight=1, name='Thử thách đầu tiên!', description='Trải nghiệm bài luyện tập đầu tiên của Signify.')
        
        if kwargs.get('do_first_lesson') != None:   #gọi on_exit_lesson()
            self.do_first_lesson = Achievement(**kwargs.get('do_first_lesson'))
        else:
            self.do_first_lesson= Achievement(max=1, weight=1, name='Bài học đầu tiên!', description='Trải nghiệm bài học đầu tiên của Signify.')
        
        if kwargs.get('complete_first_question') != None:   #gọi on_correct()
            self.complete_first_question = Achievement(**kwargs.get('do_first_lesson'))
        else:
            self.complete_first_question = Achievement(max=1, weight=2, name='Chập chững!', description='Trả lời đúng câu hỏi đầu tiên.')
        
        if kwargs.get('near_complete_quiz') != None:    #gọi on_quiz_done()
            self.near_complete_quiz = Achievement(**kwargs.get('do_first_lesson'))
        else:
            self.near_complete_quiz = Achievement(max=80, weight=4, name='Gần được rồi!', description='Đạt ít nhất 80%% số điểm bài luyện tập.')
            
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
        ``lesson_current`` (str): Mục (aka item, từ) đang học dở trong bài học.\n
        ``quiz_completion`` (int): Tỉ lệ hoàn thiện bài luyện tập cao nhất 0-100. \n
        ``recency`` (datetime | None nếu chưa học/luyện tập lần nào): Thời điểm học/luyện tập gần nhất.
    """
    def __init__(self, lesson_current: str = None, __quiz_completion: int = 0, recency: dict = None) -> None:      
        self.lesson_current = lesson_current
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
        Update progress và achivements thông qua các hàm on_...()\n
        , gọi hàm cho các event tương ứng.\n
        ``email``,``password``,``name``: str\n
        ``achievements``: AchievementSet\n
        ``creation_date``: datetime.datetime\n
        ``region``: 'Vùng miền mặc định', 'Toàn quốc' nếu chưa chọn\n
        ``following_emails``: list[str] truy vấn qua phương thức của ProfileManger\n
        ``progress``: dict = {\n
            'Chủ đề': Progress\n
            ...\n
        }
    '''
    def __init__(self, email: str, password: str, name: str, region: str = 'Toàn quốc', following_emails: list[str] = [], progress: dict = None, achievements: dict = {}, creation_date: dict = None) -> None:
        
        self.email = email
        self.password = password
        self.name = name
        self.region = region
        self.following_emails = following_emails    #Truy vấn qua hàm trong ProfileManager
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
                self.on_login()        #Có thể chuyến sang lúc hiển thị giao diện sau khi login thành công
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
            print("PF's register called!")
            self.on_login()        #Có thể chuyến sang lúc hiển thị giao diện sau khi login thành công
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
    
    def get_followers(self, user: Profile) -> list[Profile]:
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
    
    def on_move_to_learing_item(self, subject: str, item: str):
        self.user.progress[subject].lesson_current = item
    
    def on_quiz_done(self, questionaire: str, score: int):
        progress = self.user.progress[questionaire['name']]
        
        #Cập nhật progress
        completion =  score * (100 / questionaire['size'])
        if completion < progress.quiz_completion: return
        progress.quiz_completion = completion
        
        #achievement hardwork
        self.user.achievements.hardwork.current += 1
        
        #achievement complete_first_quiz, do_first_quiz, 
        highest = 0
        for sbj in subjects:
            completion = self.user.progress[sbj].quiz_completion
            if completion > highest:
                highest = completion
        self.user.achievements.complete_first_quiz.current = highest
        self.user.achievements.do_first_quiz.current += 1
        self.user.achievements.near_complete_quiz.current = completion
                
        # Cập nhật achievements complete_all_quiz
        if progress.quiz_completion >= 100:
            completed_cnt = 0
            for sbj in subjects:
                if self.user.progress[sbj].quiz_completion >= 100:
                    completed_cnt += 1
            self.user.achievements.complete_all_quiz.current = completed_cnt
            
    def on_exit_lesson(self, subject: str):
        self.user.progress[subject].recency = dt.datetime.now()
        self.user.achievements.do_first_lesson += 1
        
    def on_exit_quiz(self, subject: str):
        self.user.progress[subject].recency = dt.datetime.now()
        self.user.achievements.do_first_quiz += 1
        
    def on_correct(self):
        self.user.achievements.complete_first_question += 1
        
    def on_login(self):#Đã gọi xong
        #achievement veteran, famous tạm thời update ở đây thay vì trong vòng lặp
        delta = dt.datetime.now() - self.user.creation_date
        self.user.achievements.veteran.current = delta.days
        self.user.achievements.famous.current = len(self.get_followers(self.user))

pm = ProfileManager()
# user = pm.register(name='Nguyễn Văn A', email='asd@gmail.com', password='123456')
# pm.logout()
# user = pm.login(email='asd@gmail.com', password='123456')
# print(user.achievements.total_score)
# pm.delete_user()