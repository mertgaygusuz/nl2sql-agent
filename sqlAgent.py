import os
import time
import warnings
from sqlalchemy import exc

# 1. Çirkin uyarıları gizle
warnings.filterwarnings("ignore", category=exc.SAWarning)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 2. API Anahtarı
os.environ["GOOGLE_API_KEY"] = "BURAYA_API_ANAHTARI_GELECEK"

# 3. Veritabanı Bağlantısı
server = r'BURAYA_SUNUCU_ADI_GELECEK' # Örn: (localdb)\MSSQLLocalDB
database = 'BURAYA_VERITABANI_ADI_GELECEK'
db_uri = f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"

secilen_tablolar = [
    'BURAYA_TABLO_1', 'BURAYA_TABLO_2', 'BURAYA_TABLO_3' # Kullanılacak tabloları buraya yazın
]

db = SQLDatabase.from_uri(db_uri, include_tables=secilen_tablolar)

# !!! HIZLANDIRMA ADIMI 1: Şemayı döngü dışında bir kez alıyoruz !!!
print("⏳ Veritabanı şeması hafızaya alınıyor (Bu işlem bir kez yapılır)...")
sema_bilgisi = db.get_table_info() 
print(f"✅ Başarılı! {len(db.get_usable_table_names())} tablo hazır.")

# 4. Dil Modeli 
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# 5. SQL ÜRETEN ZİNCİR (sql_zinciri)
sql_sablonu = """Sen uzman bir İK SQL Geliştiricisisin.
Aşağıdaki şemayı kullanarak sadece geçerli bir MS SQL sorgusu yaz.

Kesin Kurallar:
1. Veritabanında SADECE okuma (SELECT) işlemi yapabilirsin. ASLA veriyi değiştirme!
2. İki veya daha fazla tabloyu ilgilendiren sorular sorulduğunda DAİMA tabloları INNER JOIN veya LEFT JOIN ile tek bir sorguda birleştir.
3. Kullanıcı tırnak içinde ("...") bir dönem adı veya isim verdiğinde (örneğin "Q4 Dönem"), bunu ASLA tarih, ay (month) veya zaman aralığı olarak yorumlayıp tarih formüllerine girme! 
4. İsimleri DAİMA doğrudan [BURAYA_HEDEF_TABLO_ADI_GELECEK] tablosunun [BURAYA_SUTUN_ADI_GELECEK] sütununda birebir metin olarak ara.
5. ASLA markdown (```sql) veya açıklama metni ekleme. Sadece SQL sorgusunu ver.

Şema Bilgisi: {schema}
Soru: {question}
SQL Sorgusu:"""

sql_prompt = PromptTemplate.from_template(sql_sablonu)
sql_zinciri = sql_prompt | llm | StrOutputParser() # Değişken ismi burada 'sql_zinciri' oldu

# 6. İNSANSI CEVAP ZİNCİRİ
cevap_sablonu = """Soru: {question}
Veritabanı Sonucu: {result}
Bu sonucu kullanarak doğal ve kısa bir Türkçe cevap yaz.
Cevap:"""

cevap_prompt = PromptTemplate.from_template(cevap_sablonu)
insansi_cevap_zinciri = cevap_prompt | llm | StrOutputParser()

# 7. Sohbet Döngüsü
print("\n" + "="*50)
print("🚀 SQL Sorgu Asistanı Hazır!")
print("="*50)

while True:
    soru = input("\nSorunuz (Çıkmak için 'q' yazın): ")
    if soru.lower() == 'q':
        break
    
    try:
        baslangic_zamani = time.time()
        
        # 1. SQL Üret (Sema bilgisini dışarıdan alıyor)
        uretilen_sql = sql_zinciri.invoke({"schema": sema_bilgisi, "question": soru})
        temiz_sql = uretilen_sql.replace("```sql", "").replace("```", "").strip()
        
        print(f"\n⚙️  Çalıştırılan SQL:\n{temiz_sql}\n")
        
        # 2. Veritabanında Çalıştır
        ham_sonuc = db.run(temiz_sql)
        
        # 3. İnsan Diline Çevir
        final_cevap = insansi_cevap_zinciri.invoke({"question": soru, "result": ham_sonuc})
        
        bitis_zamani = time.time()
        gecen_sure = bitis_zamani - baslangic_zamani
        
        print(f"🤖 [Yapay Zeka]: {final_cevap}")
        print(f"⏱️ [Yanıt {gecen_sure:.2f} saniyede hazırlandı]")
            
    except Exception as e:
        print(f"\n⚠️ Bir hata oluştu: {e}")