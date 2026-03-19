# 💰 Monetų Skaičiuoklė

Web aplikacija, kuri naudoja kamerą ir OpenCV atpažinti 1€ ir 2€ monetas realiuoju laiku.

## Paleidimas lokaliai

```bash
pip install -r requirements.txt
python app.py
```

Atidaryti naršyklėje: http://localhost:5000

---

## Deploy į Render.com (nemokamai)

1. **Sukurti GitHub repozitoriją** ir įkelti visus failus:
   ```
   monetu_svetaine/
   ├── app.py
   ├── requirements.txt
   ├── Procfile
   └── templates/
       └── index.html
   ```

2. **Eiti į** https://render.com → **New → Web Service**

3. **Prijungti GitHub repozitoriją**

4. Nustatymai:
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2`

5. Spausti **Deploy** — po ~2 min svetainė veiks!

> ⚠️ **Svarbu:** Kamera naršyklėje veikia tik per HTTPS.
> Render automatiškai suteikia HTTPS, todėl viskas veiks.

---

## Kaip veikia

- Naršyklė siunčia kameros kadrą (JPEG base64) į `/aptikti` endpoint'ą kas 300ms
- Flask + OpenCV aptinka apskritimus (Hough Circles)
- Grąžina monetų koordinates ir vertes JSON formatu
- Naršyklė piešia rezultatus ant Canvas sluoksnio
