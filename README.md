# Food-Calorie-Project
코드 공유를 위한 임시 repository



## 이미지 데이터 수집
**1. Clone this repository(또는 zip파일 다운로드)**
```bash
git clone https://github.com/gjustin40/Food-Calorie-Project.git
```

**2. Install Requirements**
- Python==3.8.5
- selenium==3.141.0
- chromeDriver==89.0.4389.23
[Download Chromedriver](https://chromedriver.chromium.org/)
```bash
pip install -r requirements.txt
```

**3. Run file**
```bash
python crawling.py --list 음식목록.txt --name 폴더이름  # 여러 가지 음식
```

or

```bash
python crawling.py --item americano,아메리카노 --name 폴더이름 # 한 가지 음식
```

**4. 결과**
```bash
├── new_data
    ├── americano
    │   ├── americano1.jpg
    │   ├── americano2.jpg
    │   ├── americano3.jpg
    │   └── americano4.jpg
    ├── cappuccino
    ├── ice_tea
    .
    .
    .
    └── latte_greentea
```

#### 주의사항
- 덮어쓰기 방지를 위해 new_data폴더가 이미 존재하면 작동 중지(--name 사용 권장)
- txt파일 작성 시 **영어**와 **한글** 둘 다 작성
- item 작성 시 **영어**,**한글** 둘 다 작성
```python
# drinks.txt

americano,cappuccino,..... #엔터
아메리카노, 카푸치노.....
```