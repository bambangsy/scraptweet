# scraptweet

1. Clone Repo
```
git clone https://github.com/bambangsy/scraptweet.git
```
2. Buka folder scraptweet
```
cd scraptweet
```
3. lihat versi browser chrome anda, ganti chromebrowser dengan versi yang sesuai dengan browser anda, link:
   https://googlechromelabs.github.io/chrome-for-testing/
   
4. buat virtual environment
```
py -m venv .venv
```

5. Use virtual environment
```
.venv\Scripts\activate
```

6. Install dependency
```
pip install requirements.txt
```

7. Ubah .env-example menjadi .env dan lengkapi dalamnya dengan username dan password twitter anda, lalu pilih proxy 

8. buka main.py, ubah title,from_date,to_date,limit_time sesuai dengan yang diinginkan

9. Jalankan main.py
```
python main.py
```

