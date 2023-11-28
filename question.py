from random import *
import pprint

'''Mỗi chủ đề có thể là một bài học. Tạo một bộ câu hỏi cho mỗi chủ đề qua hàm genQuestionaire().
    'ten chu de': {
        'level': 'Cơ bản' / 'Nâng cao',
        'multiChoiceCnt',...: số lượng câu hỏi của các dạng, chỉ dùng để gen câu hỏi
        'imageURL': url hình ảnh mô tả chủ đề
        'description': text,
        'content': {
            'ten khai niem': {
                'description': mo ta khai niem,
                'imageURL': 'assets/subjects/alphabet/image/a1.png', url hình ảnh mô tả k/n
                'videoURL': {url video hướng dẫn tùy theo vùng miền
                    'vung mien' (hoặc 'Toàn quốc' nếu ko chia ra): 'assets/subjects/alphabet/video/D0489.mp4'
                    ....
                }
            },
            ...
        }
    }
'''
subjects = {  # Bảng chữ cái, Ngày lễ, Chữ số
    'Bảng chữ cái': {
        'level': 'Cơ bản',
        'multiChoiceCnt': 10,  # dùng cho tạo câu hỏi
        'imageURL': 'assets/subjects/alphabet/image/alphabet.png',
        'description': 'Học cách nhận diện và biểu đạt dưới dạng ngôn ngữ ký hiệu các chữ cái',
        'content': {
            'a': {
                'description': 'Chữ a, A. Nằm ở vị trí thứ 1 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/a1.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0489.mp4'
                }
            },
            'ă': {
                'description': 'Chữ ă, Ă. Nằm ở vị trí thứ 2 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/a2.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/alphabet/video/D0490B.mp4',
                    'Miền Trung': 'assets/subjects/alphabet/video/D0490T.mp4',
                    'Miền Nam': 'assets/subjects/alphabet/video/D0490N.mp4'
                }
            },
            'â': {
                'description': 'Chữ â, Â. Nằm ở vị trí thứ 3 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/a3.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/alphabet/video/D0491B.mp4',
                    'Miền Trung': 'assets/subjects/alphabet/video/D0491T.mp4',
                    'Miền Nam': 'assets/subjects/alphabet/video/D0491N.mp4'
                }
            },
            'b': {
                'description': 'Chữ b, B. Nằm ở vị trí thứ 4 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/b.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0492.mp4'
                }
            },
            'c': {
                'description': 'Chữ c, C. Nằm ở vị trí thứ 5 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/c.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0493.mp4'
                }
            },
            'd': {
                'description': 'Chữ d, D. Nằm ở vị trí thứ 6 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/d1.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0494.mp4'
                }
            },
            'đ': {
                'description': 'Chữ đ, Đ. Nằm ở vị trí thứ 7 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/d2.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0495.mp4'
                }
            },
            'e': {
                'description': 'Chữ e, E. Nằm ở vị trí thứ 8 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/e1.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0496.mp4'
                }
            },
            'ê': {
                'description': 'Chữ ê, Ê. Nằm ở vị trí thứ 9 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/e2.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/alphabet/video/D0497B.mp4',
                    'Miền Trung': 'assets/subjects/alphabet/video/D0497T.mp4',
                    'Miền Nam': 'assets/subjects/alphabet/video/D0497N.mp4'
                }
            },
            'g': {
                'description': 'Chữ g, G. Nằm ở vị trí thứ 10 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/g.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0498B.mp4'
                }
            },
            'h': {
                'description': 'Chữ h, H. Nằm ở vị trí thứ 11 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/h.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/alphabet/video/D0500B.mp4',
                    'Miền Trung': 'assets/subjects/alphabet/video/D0500T.mp4',
                    'Miền Nam': 'assets/subjects/alphabet/video/D0500N.mp4'
                }
            },
            'i': {
                'description': 'Chữ i, I. Nằm ở vị trí thứ 12 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/i.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0501.mp4'
                }
            },
            'k': {
                'description': 'Chữ k, K. Nằm ở vị trí thứ 13 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/k.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0502.mp4'
                }
            },
            'l': {
                'description': 'Chữ l, L. Nằm ở vị trí thứ 14 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/l.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0503.mp4'
                }
            },
            'm': {
                'description': 'Chữ m, M. Nằm ở vị trí thứ 15 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/m.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0504.mp4'
                }
            },
            'n': {
                'description': 'Chữ n, N. Nằm ở vị trí thứ 16 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/n.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0505.mp4'
                }
            },
            'o': {
                'description': 'Chữ o, O. Nằm ở vị trí thứ 17 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/o1.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0506.mp4'
                }
            },
            'ô': {
                'description': 'Chữ ô, Ô. Nằm ở vị trí thứ 18 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/o2.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/alphabet/video/D0507B.mp4',
                    'Miền Trung': 'assets/subjects/alphabet/video/D0507T.mp4',
                    'Miền Nam': 'assets/subjects/alphabet/video/D0507N.mp4'
                }
            },
            'ơ': {
                'description': 'Chữ ơ, Ơ. Nằm ở vị trí thứ 19 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/o3.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0508N.mp4'
                }
            },
            'p': {
                'description': 'Chữ p, P. Nằm ở vị trí thứ 20 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/p.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/alphabet/video/D0509B.mp4',
                    'Miền Trung': 'assets/subjects/alphabet/video/D0509T.mp4',
                    'Miền Nam': 'assets/subjects/alphabet/video/D0509N.mp4'
                }
            },
            'q': {
                'description': 'Chữ q, Q. Nằm ở vị trí thứ 21 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/q.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0510.mp4'
                }
            },
            'r': {
                'description': 'Chữ r, R. Nằm ở vị trí thứ 22 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/r.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0511.mp4'
                }
            },
            's': {
                'description': 'Chữ s, S. Nằm ở vị trí thứ 23 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/s.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0512.mp4'
                }
            },
            't': {
                'description': 'Chữ t, T. Nằm ở vị trí thứ 24 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/t.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/alphabet/video/D0513B.mp4',
                    'Miền Trung': 'assets/subjects/alphabet/video/D0513T.mp4',
                    'Miền Nam': 'assets/subjects/alphabet/video/D0513N.mp4'
                }
            },
            'u': {
                'description': 'Chữ u, U. Nằm ở vị trí thứ 25 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/u1.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0514.mp4'
                }
            },
            'ư': {
                'description': 'Chữ ư, Ư. Nằm ở vị trí thứ 26 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/u2.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0515N.mp4'
                }
            },
            'v': {
                'description': 'Chữ v, V. Nằm ở vị trí thứ 27 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/v.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0516.mp4'
                }
            },
            'x': {
                'description': 'Chữ t, T. Nằm ở vị trí thứ 28 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/x.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/alphabet/video/D0517B.mp4',
                    'Miền Trung': 'assets/subjects/alphabet/video/D0517T.mp4',
                    'Miền Nam': 'assets/subjects/alphabet/video/D0517N.mp4'
                }
            },
            'y': {
                'description': 'Chữ y, Y. Nằm ở vị trí thứ 29 trong bảng chữ cái Quốc ngữ Việt Nam.',
                'imageURL': 'assets/subjects/alphabet/image/y.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0518N.mp4'
                }
            },
            'w': {
                'description': 'Chữ w, W. Là một chữ trong bảng chữ cái Latin, dùng trong một số từ mượn tiếng nước ngoài, thuật ngữ khoa học có tính quốc tế.',
                'imageURL': 'assets/subjects/alphabet/image/w.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0523.mp4'
                }
            },
            'z': {
                'description': 'Chữ z, Z. Là một chữ trong bảng chữ cái Latin, dùng trong một số từ mượn tiếng nước ngoài, thuật ngữ khoa học có tính quốc tế.',
                'imageURL': 'assets/subjects/alphabet/image/z.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0519.mp4'
                }
            },
            'dấu sắc': {
                'description': 'Dấu thanh sắc, được thêm vào các chữ cái để tạo ra thanh điệu.\nLưu ý: Đánh vần chữ cái trước rồi đến dấu thanh.',
                'imageURL': 'assets/subjects/alphabet/image/dau_sac.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/alphabet/video/D0525B.mp4',
                    'Miền Trung': 'assets/subjects/alphabet/video/D0525T.mp4',
                    'Miền Nam': 'assets/subjects/alphabet/video/D0525N.mp4'
                }
            },
            'dấu huyền': {
                'description': 'Dấu thanh huyền, được thêm vào các chữ cái để tạo ra thanh điệu.\nLưu ý: Đánh vần chữ cái trước rồi đến dấu thanh.',
                'imageURL': 'assets/subjects/alphabet/image/dau_huyen.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/alphabet/video/D0524B.mp4',
                    'Miền Trung': 'assets/subjects/alphabet/video/D0524T.mp4',
                    'Miền Nam': 'assets/subjects/alphabet/video/D0524N.mp4'
                }
            },
            'dấu hỏi': {
                'description': 'Dấu thanh hỏi, được thêm vào các chữ cái để tạo ra thanh điệu.\nLưu ý: Đánh vần chữ cái trước rồi đến dấu thanh.',
                'imageURL': 'assets/subjects/alphabet/image/dau_hoi.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/alphabet/video/D0526B.mp4',
                    'Miền Trung': 'assets/subjects/alphabet/video/D0526T.mp4',
                    'Miền Nam': 'assets/subjects/alphabet/video/D0526N.mp4'
                }
            },
            'dấu ngã': {
                'description': 'Dấu thanh ngã, được thêm vào các chữ cái để tạo ra thanh điệu.\nLưu ý: Đánh vần chữ cái trước rồi đến dấu thanh.',
                'imageURL': 'assets/subjects/alphabet/image/dau_nga.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/alphabet/video/D0527B.mp4',
                    'Miền Trung': 'assets/subjects/alphabet/video/D0527T.mp4',
                    'Miền Nam': 'assets/subjects/alphabet/video/D0527N.mp4'
                }
            },
            'dấu nặng': {
                'description': 'Dấu thanh nặng, được thêm vào các chữ cái để tạo ra thanh điệu.\nLưu ý: Đánh vần chữ cái trước rồi đến dấu thanh.',
                'imageURL': 'assets/subjects/alphabet/image/dau_nang.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/alphabet/video/D0528.mp4'
                }
            }
        }
    },
    'Ngày lễ': {
        'level': 'Nâng cao',
        'multiChoiceCnt': 10,  # dùng cho tạo câu hỏi
        'imageURL': 'assets/subjects/holiday/image/holiday.png',
        'description': 'Học cách nhận diện và biểu đạt dưới dạng ngôn ngữ ký hiệu các ngày lễ ở Việt Nam và trên Thế giới.',
        'content': {
            'Ngày Quốc tế Phụ nữ': {
                'description': 'Diễn ra vào ngày 8/3 hằng năm, còn gọi là Ngày Liên Hợp Quốc vì Nữ quyền và Hòa bình Quốc tế được tổ chức vào ngày 8 tháng 3 hằng năm với vai trò là tâm điểm trong phong trào đấu tranh vì quyền của phụ nữ, thu hút sự chú ý đến các vấn đề như bình đẳng giới, quyền sinh sản, bạo lực và lạm dụng đối với phụ nữ. Ở Việt Nam, ngày này thường là ngày phái nam tặng phụ nữ hoa và quà.',
                'imageURL': 'assets/subjects/holiday/image/8-3.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/holiday/video/D0042B.mp4',
                    'Miền Trung': 'assets/subjects/holiday/video/D0042T.mp4',
                    'Miền Nam': 'assets/subjects/holiday/video/D0042N.mp4'
                }
            },
            'Ngày giải phóng Thủ đô': {
                'description': 'Diễn ra vào ngày 10/10 hằng năm, ngày 10/10/1954 Thủ đô Hà Nội chính thức hoàn toàn được giải phóng khỏi thực dân Pháp.',
                'imageURL': 'assets/subjects/holiday/image/10-10.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/holiday/video/D0043B.mp4',
                    'Miền Trung': 'assets/subjects/holiday/video/D0043T.mp4',
                    'Miền Nam': 'assets/subjects/holiday/video/D0043N.mp4'
                }
            },
            'Ngày giải phóng miền Nam': {
                'description': 'Diễn ra vào ngày 30/4 hằng năm, kỷ niệm ngày 30/4/1975 Giải phóng Miền Nam, thống nhất đất nước.',
                'imageURL': 'assets/subjects/holiday/image/30-4.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/holiday/video/D0044B.mp4',
                    'Miền Trung': 'assets/subjects/holiday/video/D0044T.mp4',
                    'Miền Nam': 'assets/subjects/holiday/video/D0044N.mp4'
                }
            },
            'Ngày Người khuyết tật Việt Nam': {
                'description': 'Diễn ra vào ngày 18/4 hằng năm, ngày vì quyền lợi của người khuyết tật ở Việt Nam.',
                'imageURL': 'assets/subjects/holiday/image/18-4.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/holiday/video/D0045B.mp4',
                    'Miền Trung': 'assets/subjects/holiday/video/D0045T.mp4',
                    'Miền Nam': 'assets/subjects/holiday/video/D0045N.mp4'
                }
            },
            'Ngày Người khuyết tật Thế giới': {
                'description': 'Diễn ra vào ngày 3/12 hằng năm, là Ngày Quốc tế về Người Khuyết tật (IDPD), và vào Ngày này WHO cùng với các đối tác khác trên thế giới dành một ngày kỷ niệm cho tất cả mọi người.',
                'imageURL': 'assets/subjects/holiday/image/3-12.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/holiday/video/D0046B.mp4',
                    'Miền Trung': 'assets/subjects/holiday/video/D0046T.mp4',
                    'Miền Nam': 'assets/subjects/holiday/video/D0046N.mp4'
                }
            },
            'Ngày Phụ nữ Việt Nam': {
                'description': 'Diễn ra vào ngày 20/10 hằng năm, là ngày thành lập Hội Liên hiệp Phụ nữ Việt Nam và cũng là ngày tôn vinh phụ nữ Việt Nam ở cả trong và ngoài nước.',
                'imageURL': 'assets/subjects/holiday/image/20-10.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/holiday/video/D0049B.mp4',
                    'Miền Trung': 'assets/subjects/holiday/video/D0049T.mp4',
                    'Miền Nam': 'assets/subjects/holiday/video/D0049N.mp4'
                }
            },
            'Ngày thương bình liệt sĩ': {
                'description': 'Diễn ra vào ngày 27/7 hằng năm, là ngày thể hiện truyền thống “uống nước nhớ nguồn”, lòng quý trọng và biết ơn của Đảng, Quốc hội, Chính phủ và nhân dân ta đối với những chiến sỹ đã hy sinh vì nền độc lập, tự do và thống nhất của Tổ quốc.',
                'imageURL': 'assets/subjects/holiday/image/27-7.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/holiday/video/D0050B.mp4',
                    'Miền Trung': 'assets/subjects/holiday/video/D0050T.mp4',
                    'Miền Nam': 'assets/subjects/holiday/video/D0050N.mp4'
                }
            },
            'Ngày giỗ tổ Hùng Vương': {
                'description': 'Diễn ra vào ngày 10/3 âm lịch hằng năm, còn gọi là Lễ hội Đền Hùng hoặc Quốc giỗ. Là một ngày lễ của Việt Nam, là ngày hội truyền thống của Người Việt tưởng nhớ công lao dựng nước của Hùng Vương.',
                'imageURL': 'assets/subjects/holiday/image/10-3.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/holiday/video/D0051B.mp4',
                    'Miền Trung': 'assets/subjects/holiday/video/D0051T.mp4',
                    'Miền Nam': 'assets/subjects/holiday/video/D0051N.mp4'
                }
            },
            'Ngày Ngôn ngữ ký hiệu Quốc tế': {
                'description': 'Dưới sự vận động của Liên đoàn Người Điếc Thế giới (WFD) thì Liên Hiệp Quốc mới đây (2018) đã có một thông cáo chính thức rằng ngày 23 tháng 9 hằng năm sẽ là Ngày Quốc tế Ngôn ngữ Ký hiệu.',
                'imageURL': 'assets/subjects/holiday/image/23-9.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/holiday/video/D0052B.mp4',
                    'Miền Trung': 'assets/subjects/holiday/video/D0052T.mp4',
                    'Miền Nam': 'assets/subjects/holiday/video/D0052N.mp4'
                }
            },
            'Ngày Nhà giáo Việt Nam': {
                'description': 'Diễn ra vào ngày 20/11 hằng năm, là lễ hội của ngành Giáo dục và là Ngày Nhà giáo, ngày "tôn sư trọng đạo" nhằm mục đích để tôn vinh những người dạy học và những người trong ngành giáo dục.',
                'imageURL': 'assets/subjects/holiday/image/20-11.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/holiday/video/W02328T.mp4',
                    'Miền Trung': 'assets/subjects/holiday/video/W02328T.mp4',
                    'Miền Nam': 'assets/subjects/holiday/video/W02328N.mp4'
                }
            }
        },
    },
    'Chữ số': {
        'level': 'Cơ bản',
        'multiChoiceCnt': 10,  # dùng cho tạo câu hỏi
        'imageURL': 'assets/subjects/numeral/image/numeral.png',
        'description': 'Học cách nhận diện và biểu đạt các chữ số từ 0 đến 9.',
        'content': {
            '0': {
                'description': 'Chữ số không.',
                'imageURL': 'assets/subjects/numeral/image/0.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/numeral/video/D0529.mp4'
                }
            },
            '1': {
                'description': 'Chữ số một.',
                'imageURL': 'assets/subjects/numeral/image/1.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/numeral/video/D0530.mp4'
                }
            },
            '2': {
                'description': 'Chữ số hai.',
                'imageURL': 'assets/subjects/numeral/image/2.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/numeral/video/D0531.mp4'
                }
            },
            '3': {
                'description': 'Chữ số ba.',
                'imageURL': 'assets/subjects/numeral/image/3.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/numeral/video/D0532.mp4'
                }
            },
            '4': {
                'description': 'Chữ số bốn.',
                'imageURL': 'assets/subjects/numeral/image/4.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/numeral/video/D0533.mp4'
                }
            },
            '5': {
                'description': 'Chữ số năm.',
                'imageURL': 'assets/subjects/numeral/image/5.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/numeral/video/D0534.mp4'
                }
            },
            '6': {
                'description': 'Chữ số sáu.',
                'imageURL': 'assets/subjects/numeral/image/6.png',
                'videoURL': {
                    'Miền Bắc': 'assets/subjects/numeral/video/D0535B.mp4',
                    'Miền Trung': 'assets/subjects/numeral/video/D0535T.mp4',
                    'Miền Nam': 'assets/subjects/numeral/video/D0535N.mp4'
                }
            },
            '7': {
                'description': 'Chữ số bảy.',
                'imageURL': 'assets/subjects/numeral/image/7.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/numeral/video/D0536.mp4'
                }
            },
            '8': {
                'description': 'Chữ số tám.',
                'imageURL': 'assets/subjects/numeral/image/8.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/numeral/video/D0537.mp4'
                }
            },
            '9': {
                'description': 'Chữ số chín.',
                'imageURL': 'assets/subjects/numeral/image/9.png',
                'videoURL': {
                    'Toàn quốc': 'assets/subjects/numeral/video/D0538.mp4'
                }
            }
        }
    }
}


def genQuestionaire(sbjName: str):
    """Tạo một bộ câu hỏi ngẫu nhiên tương ứng với một chủ đề. Đảm bảo các đáp án không lặp lại.

    Args:
        sbjName (str): tên chủ đề

    Returns:
        Một dictionary là bộ câu hỏi có dạng:\n
        questionare = {
            'name': 'tên chủ đề'\n
            'size': số câu hỏi\n
            'description': 'mô tả'\n
            'content:{
                1(số thứ tự câu hỏi, int): {
                    'answer': 'đáp án',\n
                    'type': 'multiChoice'/... loại câu hỏi để check và hiển thị giao diện tương ứng
                    'videoURL': {
                        'vùng miền': 'url'
                        ...
                    },\n
                    'choices': {
                        'A': 'lựa chọn',
                        ...
                        'D': 'lựa chọn'
                    }
                }
                ...
            }
        }
    """
    sbj = subjects[sbjName]
    res = {
        'name': sbjName,
        'description': 'Thực hiện bài luyện tập cho chủ đề ' + sbjName + '.',
        'size': sbj['multiChoiceCnt'],
        'content': {}
    }
    answers = sample(list(sbj['content'].keys()), sbj['multiChoiceCnt'])

    for i in range(0, sbj['multiChoiceCnt']):
        res['content'][i + 1] = {}
        q = res['content'][i + 1]
        q['answer'] = answers[i]
        q['videoURL'] = sbj['content'][answers[i]]['videoURL']
        choices = sample(list(sbj['content'].keys()), 3)
        choices.insert(randint(0, 3), q['answer'])
        shuffle(choices)
        q['choices'] = {
            'A': choices[0],
            'B': choices[1],
            'C': choices[2],
            'D': choices[3]
        }
        q['description'] = 'Ngôn ngữ ký hiệu sau đây biểu diễn khái niệm gì?'
        q['type'] = 'multiChoice'

    return res


def getSubjectsOfLevel(level='Cơ bản'):
    """Trả về 1 dictionary gồm các chủ đề thuộc 1 level, format tương tự subjects
    """
    res = {}
    for e in subjects.keys():
        if subjects[e]['level'] == level:
            res[e] = subjects[e]
    return res


def testDict(d: dict):
    """test dict, xuất ra file src/test.txt
    """
    f = open('src/test.txt', 'w', encoding='utf-8')
    s = pprint.pformat(d)
    f.write(s.__str__())
    f.close()


# testDict(genQuestionaire('Bảng chữ cái'))
# testDict(getSubjectsOfLevel('Nâng cao'))

'''cần thì convert sang class với object
class Concept:
    def __init__(self, name = '', description = '', videoURL = {}, imageURL = ''):
        self.name = name
        self.description = description
        self.videoURL = videoURL
        self.imageURL = imageURL

class Subject:
    def __init__(self, name = '', description = '', iconURL = '', concepts = []):
        self.name = name
        self.description = description
        self.iconURL = iconURL
        self.concepts = concepts
        
    def genQuestionaire():
        ...
'''
