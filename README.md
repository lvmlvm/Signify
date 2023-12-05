# Signify
**Cách thức cài đặt Signify khi không tải được Python và các thư viện liên quan:**
- Truy cập https://drive.google.com/drive/u/1/folders/1bqcxdLvMsgZwmTgAfDgg3bDzSbwxO31V
- Tải folder Signify về
- Giải nén nếu cần
- Chạy Signify.exe

**Cách deploy .exe**
1. Cài pyinstaller, mediapipe
2. Chạy pyinstaller Signify.spec
3. Có thể tự chỉnh file .spec, nếu không thì thực hiện từ bước 3.1:
    a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        ('path to site-pakages/mediapipe/modules','mediapipe/modules')
        ('assets','assets'),....
3.1 Vào AppData\Local\Programs\Python\Python311\Lib\site-packages\mediapipe, copy modules
3.2 Vào dist -> Signify -> _internal -> mediapipe, paste
4. Vào dist -> Signify -> _internal, cut assets, kivyfiles, local
5. Vào dist -> Signify, paste
6. Chạy .exe
