import random
import json
import time
import os
from datetime import datetime

# --- KELİME HAVUZU (Örnek) ---
# JSON dosyasından kelime yükleyemezseniz bu örnek havuz kullanılır.
# Gerçek kelime havuzunu 'kelime_havuzu.json' dosyasına kaydedebilirsiniz.
DEFAULT_WORDS = [
  {
    "word": "mecaz",
    "meaning": "Bir kelimenin veya ifadenin gerçek anlamı dışında, benzetme veya başka bir ilişki yoluyla kullanılması."
  },
  {
    "word": "deyim",
    "meaning": "Genellikle gerçek anlamından uzaklaşarak kendine özgü bir anlam taşıyan, kalıplaşmış söz öbeği."
  },
  {
    "word": "atasözü",
    "meaning": "Uzun deneyim ve gözlemlere dayanarak oluşmuş, topluma öğüt veren, yol gösteren özlü söz."
  },
  {
    "word": "betimleme",
    "meaning": "Varlıkları, nesneleri veya olayları, okuyucunun zihninde canlanacak şekilde sözcüklerle resmetme."
  },
  {
    "word": "öznel",
    "meaning": "Kişisel görüşe, duyguya veya zevke dayanan, kişiden kişiye değişebilen düşünce veya yargı."
  },
  {
    "word": "nesnel",
    "meaning": "Kişiden bağımsız, kanıtlanabilir gerçeklere dayanan, herkes için geçerli olan bilgi veya yargı."
  },
  {
    "word": "uyak",
    "meaning": "Dize sonlarında veya aralarında bulunan, görev ve anlamları farklı sözcükler arasındaki ses benzerliği (kafiye)."
  },
  {
    "word": "ikileme",
    "meaning": "Anlamı pekiştirmek, güçlendirmek veya farklı bir anlam katmak için iki kelimenin arka arkaya kullanılması."
  },
  {
    "word": "terim",
    "meaning": "Bir bilim, sanat veya meslek dalına özgü, özel ve belirli bir anlam taşıyan kelime."
  },
  {
    "word": "anlam",
    "meaning": "Bir kelimenin, işaretin veya ifadenin temsil ettiği düşünce, fikir veya kavram."
  },
  {
    "word": "sözcük",
    "meaning": "Dildeki en küçük anlamlı birim; kelime."
  },
  {
    "word": "eş anlamlı",
    "meaning": "Yazılışları farklı olsa da aynı veya çok yakın anlamı taşıyan kelimeler."
  },
  {
    "word": "zıt anlamlı",
    "meaning": "Anlamca birbirinin karşıtı olan kelimeler (karşıt anlamlı)."
  },
  {
    "word": "köken",
    "meaning": "Bir kelimenin veya şeyin çıktığı, dayandığı yer; asıl başlangıç."
  },
  {
    "word": "çekim eki",
    "meaning": "Kelimenin anlamını değiştirmeyen, ancak görevini ve yerini belirleyen ek (çoğul, hâl, zaman ekleri vb.)."
  },
  {
    "word": "yapım eki",
    "meaning": "Eklendiği kelimenin anlamını veya türünü değiştirerek yeni bir kelime oluşturan ek."
  },
  {
    "word": "fonetik",
    "meaning": "Dilin seslerini inceleyen bilim dalı; ses bilimiyle ilgili olan."
  },
  {
    "word": "morfoloji",
    "meaning": "Kelime yapısını ve kelimelerin biçimsel özelliklerini inceleyen bilim dalı (biçim bilimi)."
  },
  {
    "word": "anlatım",
    "meaning": "Düşünceleri, duyguları veya olayları sözlü ya da yazılı olarak ifade etme biçimi."
  },
  {
    "word": "üslup",
    "meaning": "Bir yazarın veya konuşmacının anlatım tarzı, dili kullanma biçimi (stil)."
  },
  {
    "word": "nüans",
    "meaning": "Birbirine yakın şeyler arasındaki ince fark, küçük ayrım."
  },
  {
    "word": "tasvir",
    "meaning": "Bir şeyi sözle veya yazıyla somut biçimde anlatma, betimleme."
  },
  {
    "word": "mukayese",
    "meaning": "İki veya daha fazla şeyi benzerlikleri ve farklılıkları yönünden karşılaştırma."
  },
  {
    "word": "özgün",
    "meaning": "Kendine has, orijinal, başkasına benzemeyen niteliklere sahip."
  },
  {
    "word": "muhteva",
    "meaning": "Bir yazının, konuşmanın veya eserin içeriği, kapsamı."
  },
  {
    "word": "tevatür",
    "meaning": "Söylenti, kulaktan kulağa yayılan asılsız veya doğruluğu kesin olmayan haber."
  },
  {
    "word": "tevazu",
    "meaning": "Alçak gönüllülük, gösterişsiz olma durumu."
  },
  {
    "word": "münhasır",
    "meaning": "Yalnız bir kişiye veya şeye ait olan, özel, mahsus."
  },
  {
    "word": "muallak",
    "meaning": "Sonucu veya durumu belli olmayan, askıda kalmış, belirsiz."
  },
  {
    "word": "müstakil",
    "meaning": "Bağımsız, tek başına duran veya ayrı olan."
  },
  {
    "word": "mütehassıs",
    "meaning": "Belirli bir alanda uzmanlaşmış kişi (uzman)."
  },
  {
    "word": "mebzul",
    "meaning": "Çok, bol, bereketli, aşırı miktarda bulunan."
  },
  {
    "word": "müstesna",
    "meaning": "Eşi az bulunan, benzerlerinden üstün tutulan, ayrıcalıklı."
  },
  {
    "word": "ihtimam",
    "meaning": "Özen gösterme, dikkat ve itina ile davranma."
  },
  {
    "word": "tefekkür",
    "meaning": "Derin düşünme, düşünceye dalma, zihinsel olarak derinleşme."
  },
  {
    "word": "muğlak",
    "meaning": "Anlaşılması güç, karmaşık, belirsiz (kapalı)."
  },
  {
    "word": "mukadderat",
    "meaning": "Yazgı, alın yazısı, kader."
  },
  {
    "word": "muvaffakiyet",
    "meaning": "Başarı, bir işte istenilen sonucu elde etme."
  },
  {
    "word": "telaffuz",
    "meaning": "Bir kelimeyi veya sesi doğru bir şekilde söyleme biçimi."
  },
  {
    "word": "anlatıcı",
    "meaning": "Edebi bir eserde (hikâye, roman) olayı okuyucuya aktaran kişi veya ses."
  },
  {
    "word": "tema",
    "meaning": "Bir edebi eserin veya sanat eserinin ana düşüncesi, konusu (izlek)."
  },
  {
    "word": "tür",
    "meaning": "Benzer özellikler taşıyan nesnelerin veya eserlerin ortak adı, çeşidi."
  },
  {
    "word": "tecessüs",
    "meaning": "Merakla araştırma, gizli şeyleri öğrenme isteği."
  },
  {
    "word": "edebiyat",
    "meaning": "Olay, düşünce, duygu ve hayalleri dil aracılığıyla güzel ve etkili bir biçimde anlatan sanat dalı."
  },
  {
    "word": "hikaye",
    "meaning": "Gerçek veya hayali bir olayı anlatan, romandan kısa, edebi tür (öykü)."
  },
  {
    "word": "roman",
    "meaning": "İnsan hayatının geniş bir zaman dilimini kapsayan, olay örgüsü ve karakterleri detaylı edebi tür."
  },
  {
    "word": "şiir",
    "meaning": "Duygu, düşünce ve hayalleri, ahenkli ve ölçülü dizelerle ifade eden edebi tür."
  },
  {
    "word": "ritim",
    "meaning": "Bir eserdeki ses, vurgu veya hareketlerin düzenli ve ahenkli bir şekilde tekrarlanması (dizim)."
  },
  {
    "word": "vurgu",
    "meaning": "Bir kelimenin veya cümlenin belirli bir hecesini veya kısmını diğerlerinden daha kuvvetli söyleme."
  },
  {
    "word": "imge",
    "meaning": "Zihinde canlandırılan soyut veya somut tablo, hayal (poetik görüntü)."
  },
  {
    "word": "metafor",
    "meaning": "İki farklı şey arasında örtülü bir benzetme yaparak birini diğeriyle açıklama (eğretileme)."
  },
  {
    "word": "benzetme",
    "meaning": "İki şey arasında ortak bir özellik yönünden ilişki kurma (teşbih)."
  },
  {
    "word": "kinaye",
    "meaning": "Söylenenin tam tersini kastederek, üstü kapalı ve iğneleyici anlatım (dokundurma)."
  },
  {
    "word": "teşhis",
    "meaning": "İnsan dışındaki varlıklara insana özgü özellikler verme sanatı (kişileştirme)."
  },
  {
    "word": "intak",
    "meaning": "Cansız varlıkları veya hayvanları konuşturma sanatı."
  },
  {
    "word": "mübalağa",
    "meaning": "Bir şeyi olduğundan çok veya az gösterme, abartma sanatı."
  },
  {
    "word": "deneme",
    "meaning": "Yazarın herhangi bir konuda kesin hükümlere varmadan, kişisel düşüncelerini özgürce ifade ettiği yazı türü."
  },
  {
    "word": "makale",
    "meaning": "Bir konuyu ispatlama, bilgi verme veya görüş savunma amacıyla yazılan bilimsel veya ciddi yazı türü."
  },
  {
    "word": "eleştiri",
    "meaning": "Bir sanat veya düşünce eserinin iyi ve kötü yönlerini inceleyip değerlendirme yazısı."
  },
  {
    "word": "anı",
    "meaning": "Bir kişinin yaşadığı veya tanık olduğu önemli olayları, üzerinden zaman geçtikten sonra yazdığı edebi tür."
  },
  {
    "word": "biyografi",
    "meaning": "Tanınmış bir kişinin hayatını, eserlerini ve başarılarını anlatan yazı türü (yaşam öyküsü)."
  },
  {
    "word": "otobiyografi",
    "meaning": "Bir kişinin kendi yaşam öyküsünü kendisinin anlattığı yazı türü."
  },
  {
    "word": "söz öbeği",
    "meaning": "Birden çok kelimenin bir araya gelerek tek bir anlam birimi oluşturması (kelime grubu)."
  },
  {
    "word": "kalıp söz",
    "meaning": "Dilde belirli bir anlamı karşılamak üzere donmuş ve değişmez biçimde kullanılan söz."
  },
  {
    "word": "kaynak",
    "meaning": "Bilgi edinilen, beslenilen yer veya kişi; bir eserin temel alındığı eser."
  },
  {
    "word": "gizem",
    "meaning": "Sır, bilinmeyen, anlaşılması zor olan durum."
  },
  {
    "word": "vahiy",
    "meaning": "Tanrı'nın, peygamberleri aracılığıyla insanlara bildirdiği ilahi emirler ve bilgiler."
  },
  {
    "word": "ihtiyaç",
    "meaning": "Gereksinim duyulan, eksikliği hissedilen şey."
  },
  {
    "word": "temin",
    "meaning": "Sağlama, tedarik etme, elde etme."
  },
  {
    "word": "istisna",
    "meaning": "Genel kuralın veya durumun dışında kalan özel durum, kural dışı."
  },
  {
    "word": "teşekkür",
    "meaning": "Şükran duyma, minnettarlığı ifade etme."
  },
  {
    "word": "hissiyat",
    "meaning": "Duygular, hisler, içten gelen tepkiler."
  },
  {
    "word": "muhabbet",
    "meaning": "Sohbet etme, dostça konuşma; sevgi, dostluk."
  },
  {
    "word": "teklif",
    "meaning": "Bir işin yapılması için öne sürülen düşünce, öneri."
  },
  {
    "word": "mukavemet",
    "meaning": "Dayanıklılık, direnç gösterme gücü."
  },
  {
    "word": "tasarruf",
    "meaning": "Para veya malı dikkatli kullanma, biriktirme; ekonomik davranma."
  },
  {
    "word": "müstahak",
    "meaning": "Hak etmiş, layık olmuş (genellikle olumsuz durumlar için)."
  },
  {
    "word": "tecrübe",
    "meaning": "Deneyim, yaşanmışlık; bir işi yaparak elde edilen bilgi ve beceri."
  },
  {
    "word": "idrak",
    "meaning": "Anlama, kavrama yeteneği, akıl yoluyla gerçeği bulma."
  },
  {
    "word": "ferağat",
    "meaning": "Haktan veya yetkiden vazgeçme, terk etme."
  },
  {
    "word": "ittifak",
    "meaning": "Anlaşma, uzlaşma; görüş birliği içinde olma."
  },
  {
    "word": "iade",
    "meaning": "Geri verme, geri çevirme."
  },
  {
    "word": "imza",
    "meaning": "Bir yazının veya belgenin altına, onu yazanın veya onaylayanın adının el yazısıyla atılması."
  },
  {
    "word": "izhar",
    "meaning": "Açığa çıkarma, gösterme, belli etme."
  },
  {
    "word": "mukabil",
    "meaning": "Karşılık olarak, karşılıklı."
  },
  {
    "word": "nitelik",
    "meaning": "Bir şeyin nasıl olduğunu belirten özellik, vasıf, kalite."
  },
  {
    "word": "nicelik",
    "meaning": "Bir şeyin sayılabilen, ölçülebilen miktarı (miktar, kemiyet)."
  },
  {
    "word": "kavram",
    "meaning": "Bir nesnenin veya düşüncenin zihindeki soyut ve genel tasarımı."
  },
  {
    "word": "kriter",
    "meaning": "Bir yargıya varılırken veya bir değerlendirme yapılırken kullanılan ölçüt, ölçü."
  },
  {
    "word": "temel",
    "meaning": "Bir yapının veya düşüncenin en alt, dayandığı kısmı, esas."
  },
  {
    "word": "varsayım",
    "meaning": "Doğruluğu kanıtlanmadan kabul edilen önerme veya durum (faraziye)."
  },
  {
    "word": "teori",
    "meaning": "Olayları, olguları açıklayan, organize eden ve tahmin etmeye yarayan, birbiriyle ilişkili ilkeler bütünü (kuram)."
  },
  {
    "word": "hipotez",
    "meaning": "Bir olayı açıklamak için öne sürülen, doğruluğu henüz kanıtlanmamış geçici açıklama (varsayım)."
  },
  {
    "word": "analiz",
    "meaning": "Bir bütünü, onu oluşturan parçalara ayırarak inceleme, çözümleme."
  },
  {
    "word": "sentez",
    "meaning": "Parçaları birleştirerek yeni bir bütün oluşturma, bileşim."
  },
  {
    "word": "argüman",
    "meaning": "Bir düşünceyi veya tezi desteklemek için ileri sürülen kanıt, gerekçe."
  },
  {
    "word": "yöntem",
    "meaning": "Bir amaca ulaşmak için izlenen düzenli yol (metot)."
  },
  {
    "word": "teknik",
    "meaning": "Bir işi yapma tarzı, sanatsal veya bilimsel alanda kullanılan özel yöntemler."
  },
  {
    "word": "inovasyon",
    "meaning": "Yenilik, yenileşim, yeni veya önemli ölçüde geliştirilmiş bir ürün, süreç veya hizmetin uygulanması."
  },
  {
    "word": "prosedür",
    "meaning": "Bir işin, görevin veya sürecin nasıl yapılacağını adım adım gösteren resmi yol, işlem."
  },
  {
    "word": "kısıtlama",
    "meaning": "Bir şeyin kapsamını veya serbestliğini daraltma, sınırlama."
  },
  {
    "word": "istikrar",
    "meaning": "Denge, değişmezlik, süreklilik, sağlamlık (denge)."
  },
  {
    "word": "entegrasyon",
    "meaning": "Farklı parçaları veya unsurları birleştirme, bütünleştirme."
  },
  {
    "word": "adaptasyon",
    "meaning": "Uyum sağlama, çevreye veya koşullara ayak uydurma (uyarlama)."
  },
  {
    "word": "konsensüs",
    "meaning": "Görüş birliği, fikir birliği, uzlaşma."
  },
  {
    "word": "diyalektik",
    "meaning": "Tezler ve antitezler arasındaki karşıtlık yoluyla gerçeğe ulaşma yöntemi (karşıtlık sanatı)."
  },
  {
    "word": "paradigma",
    "meaning": "Bir bilim dalında veya düşünce sisteminde kabul gören temel bakış açısı, örnek model."
  },
  {
    "word": "retorik",
    "meaning": "Etkili ve güzel konuşma sanatı, söz söyleme becerisi."
  },
  {
    "word": "spekülasyon",
    "meaning": "Kesin bilgiye dayanmadan, yalnızca akıl yürütmeye veya tahmine dayalı düşünce."
  },
  {
    "word": "empati",
    "meaning": "Bir kişinin duygularını, düşüncelerini ve deneyimlerini anlama ve hissetme yeteneği (duygudaşlık)."
  },
  {
    "word": "asimilasyon",
    "meaning": "Farklı kültürlerin veya grupların zamanla baskın kültüre benzemesi, özümseme."
  },
  {
    "word": "etnik",
    "meaning": "Bir millete, halka veya ırka ait, kültürel farklılıkları belirten."
  },
  {
    "word": "konsolide",
    "meaning": "Birleştirilmiş, sağlamlaştırılmış, güçlendirilmiş."
  },
  {
    "word": "dejenere",
    "meaning": "Bozulmuş, yozlaşmış, asıl niteliğini kaybetmiş."
  },
  {
    "word": "şümul",
    "meaning": "Kapsam, alan, içine aldığı her şey."
  },
  {
    "word": "mütekabiliyet",
    "meaning": "Karşılıklılık, denklik esası (iki tarafın birbirine aynı şekilde davranması)."
  },
  {
    "word": "müteakip",
    "meaning": "Arkasından gelen, sonraki."
  },
  {
    "word": "sükûnet",
    "meaning": "Huzur, dinginlik, sessizlik, durgunluk."
  },
  {
    "word": "ibret",
    "meaning": "Yaşanmış bir olaydan ders çıkarma, örnek alma."
  },
  {
    "word": "seciye",
    "meaning": "Bir kişinin doğuştan gelen karakteri, huyları, özgün yapısı."
  },
  {
    "word": "mukavele",
    "meaning": "Sözleşme, anlaşma (genellikle ticari)."
  },
  {
    "word": "ihtilaf",
    "meaning": "Anlaşmazlık, uyuşmazlık, fikir ayrılığı."
  },
  {
    "word": "mevzu",
    "meaning": "Konu, bahsedilen şey (bahis)."
  },
  {
    "word": "vazife",
    "meaning": "Görev, sorumluluk, yapılması gereken iş."
  },
  {
    "word": "tekâmül",
    "meaning": "Olgunlaşma, gelişme, mükemmele doğru ilerleme (evrim)."
  },
  {
    "word": "tezyif",
    "meaning": "Küçümseme, alay etme, değersiz görme."
  },
  {
    "word": "teşvik",
    "meaning": "Cesaretlendirme, bir işi yapması için birini isteklendirme."
  },
  {
    "word": "iktibas",
    "meaning": "Başkasının eserinden alıntı yapma, aktarma."
  },
  {
    "word": "izole",
    "meaning": "Yalıtılmış, tek başına, çevresinden ayrılmış."
  },
  {
    "word": "münferit",
    "meaning": "Tek, ayrı ayrı, diğerlerinden bağımsız."
  },
  {
    "word": "intikal",
    "meaning": "Bir yerden başka bir yere geçme, aktarılma."
  },
  {
    "word": "temayül",
    "meaning": "Eğilim, yönelme, bir şeye karşı isteklilik."
  },
  {
    "word": "mütevazı",
    "meaning": "Alçak gönüllü, sade, gösterişsiz."
  },
  {
    "word": "mütefekkir",
    "meaning": "Düşünür, felsefi ve derin konular üzerine düşünen kişi."
  },
  {
    "word": "mukavele",
    "meaning": "Sözleşme, anlaşma."
  },
  {
    "word": "ihtiyat",
    "meaning": "Gelecekte olabilecek tehlikeleri göz önünde bulundurarak dikkatli davranma (önlem)."
  },
  {
    "word": "hiciv",
    "meaning": "Toplumun veya kişilerin kusurlu yanlarını alaycı bir dille eleştiren edebi tür (taşlama)."
  },
  {
    "word": "tevcih",
    "meaning": "Yöneltme, bir göreve atama, bir ödülü verme."
  },
  {
    "word": "vazgeçilmez",
    "meaning": "Ondan ayrılamayan, mutlak gerekli olan."
  },
  {
    "word": "ihmal",
    "meaning": "Gereken dikkati ve özeni göstermeme, savsaklama."
  },
  {
    "word": "ikmal",
    "meaning": "Tamamlama, eksik olanı yerine getirme, bitirme."
  },
  {
    "word": "iltifat",
    "meaning": "Güler yüz gösterme, nazikçe konuşma, birine değer verme."
  },
  {
    "word": "müessese",
    "meaning": "Kuruluş, kurum, tesis."
  },
  {
    "word": "tebliğ",
    "meaning": "Bildirme, resmi bir kararı duyurma."
  },
  {
    "word": "tedarik",
    "meaning": "Gerekli olan şeyleri sağlama, temin etme."
  },
  {
    "word": "tahkik",
    "meaning": "Doğruluğunu araştırma, soruşturma, inceleme."
  },
  {
    "word": "temyiz",
    "meaning": "Ayırt etme, yargı kararlarını üst mahkemede gözden geçirme (ayırt etme yeteneği)."
  },
  {
    "word": "infaz",
    "meaning": "Bir kararı veya emri yerine getirme, uygulama."
  },
  {
    "word": "müracaat",
    "meaning": "Başvuru, başvurma."
  },
  {
    "word": "tazim",
    "meaning": "Saygı gösterme, yüceltme."
  },
  {
    "word": "teveccüh",
    "meaning": "İlgi gösterme, yüzünü çevirme; lütuf, iyilik."
  },
  {
    "word": "müstesna",
    "meaning": "Benzerlerinden ayrı, özel, kural dışı."
  },
  {
    "word": "tekabül",
    "meaning": "Karşılık gelme, denge sağlama."
  },
  {
    "word": "izdiham",
    "meaning": "Aşırı kalabalık, yığılma, sıkışıklık."
  },
  {
    "word": "terkip",
    "meaning": "Birden çok şeyi bir araya getirme, bileşim, karışım."
  },
  {
    "word": "iade",
    "meaning": "Geri verme, yerine koyma."
  },
  {
    "word": "mukabele",
    "meaning": "Karşılık verme, karşılama."
  },
  {
    "word": "müessir",
    "meaning": "Etkili, tesirli, iz bırakan."
  },
  {
    "word": "tasavvur",
    "meaning": "Zihinde canlandırma, hayal etme, tasarlama."
  },
  {
    "word": "vukuat",
    "meaning": "Olaylar, meydana gelen hadiseler."
  },
  {
    "word": "tezahür",
    "meaning": "Ortaya çıkma, görünme, belirme."
  },
  {
    "word": "iltihak",
    "meaning": "Katılma, birleşme, dahil olma."
  },
  {
    "word": "iştirak",
    "meaning": "Ortak olma, katılma, pay alma."
  },
  {
    "word": "tasdik",
    "meaning": "Doğrulama, onaylama, uygun bulma."
  },
  {
    "word": "taviz",
    "meaning": "Ödün, karşılık beklemeden yapılan fedakârlık."
  },
  {
    "word": "itibar",
    "meaning": "Saygınlık, değer, güvenilirlik."
  },
  {
    "word": "vahamet",
    "meaning": "Bir durumun ciddiyeti, tehlikesi."
  },
  {
    "word": "ihsas",
    "meaning": "Hissettirme, sezdirme, duyurma."
  },
  {
    "word": "teşkil",
    "meaning": "Oluşturma, kurma, meydana getirme."
  },
  {
    "word": "tahayyül",
    "meaning": "Hayal etme, düş gücüyle zihinde canlandırma."
  },
  {
    "word": "müsamaha",
    "meaning": "Hoşgörü, görmezden gelme, göz yumma."
  },
  {
    "word": "mütemadiyen",
    "meaning": "Sürekli olarak, aralıksız bir şekilde."
  },
  {
    "word": "nefret",
    "meaning": "Şiddetli bir şekilde tiksinme, hoşlanmama, iğrenme."
  },
  {
    "word": "hüsran",
    "meaning": "Hayal kırıklığı, başarısızlık, umutların suya düşmesi."
  },
  {
    "word": "kifayet",
    "meaning": "Yeterlilik, elverişlilik, yetme durumu."
  },
  {
    "word": "kıymet",
    "meaning": "Değer, önem, paha."
  },
  {
    "word": "merhale",
    "meaning": "Aşama, safha, bir yolculuğun veya sürecin bölümü."
  },
  {
    "word": "muhtemel",
    "meaning": "Olası, gerçekleşmesi beklenen, olabilirlik taşıyan."
  },
  {
    "word": "nazım",
    "meaning": "Ölçülü, uyaklı, düzenli söz (şiir)."
  },
  {
    "word": "nesir",
    "meaning": "Ölçü ve uyak kaygısı taşımayan, düz yazı."
  },
  {
    "word": "telkin",
    "meaning": "Başkasının aklına bir fikir veya düşünce sokma, aşılama."
  },
  {
    "word": "tezat",
    "meaning": "Karşıtlık, çelişki, birbirine zıt olma durumu."
  },
  {
    "word": "töhmet",
    "meaning": "Suçlama, birine karşı yöneltilen asılsız veya kesin olmayan suç."
  },
  {
    "word": "tasvir",
    "meaning": "Bir şeyi sözle veya yazıyla somut biçimde anlatma, betimleme."
  },
  {
    "word": "teenni",
    "meaning": "Ağır başlılık, acele etmeme, düşünerek davranma."
  },
  {
    "word": "tereddüt",
    "meaning": "Kararsızlık, duraksama, şüphe etme."
  },
  {
    "word": "vahdet",
    "meaning": "Birlik, tek olma, teklik."
  },
  {
    "word": "yakınsama",
    "meaning": "Birbirine yaklaşma, bir noktada birleşme eğilimi."
  },
  {
    "word": "irfan",
    "meaning": "Kültür, bilgi ve görgü ile edinilen incelikli bilgelik."
  },
  {
    "word": "idame",
    "meaning": "Sürdürme, devam ettirme."
  },
  {
    "word": "istikamet",
    "meaning": "Doğru yol, yön, amaç."
  },
  {
    "word": "intiba",
    "meaning": "İzlenim, bir şeyden edinilen ilk fikir veya etki."
  },
  {
    "word": "ikame",
    "meaning": "Yerine koyma, yerine geçme, temsil etme."
  },
  {
    "word": "muhkem",
    "meaning": "Sağlam, dayanıklı, güçlü."
  },
  {
    "word": "muhtasar",
    "meaning": "Özetlenmiş, kısaltılmış, kısa ve öz."
  },
  {
    "word": "müstakbel",
    "meaning": "Gelecek, ileride olacak."
  },
  {
    "word": "mütekamil",
    "meaning": "Olgunlaşmış, gelişmiş, mükemmelliğe ulaşmış."
  },
  {
    "word": "müzakere",
    "meaning": "Bir konu üzerinde karşılıklı görüş alışverişinde bulunma, tartışma."
  },
  {
    "word": "nazar",
    "meaning": "Bakış, göz; kötü veya kıskanç bakışın etkisi."
  },
  {
    "word": "safahat",
    "meaning": "Evreler, aşamalar, dönemler."
  },
  {
    "word": "tahayyül",
    "meaning": "Hayal etme, zihinde canlandırma."
  },
  {
    "word": "vazıh",
    "meaning": "Açık, belirgin, net."
  },
  {
    "word": "tevekkül",
    "meaning": "Allah'a güvenme, olayların sonucunu sabırla bekleme."
  },
  {
    "word": "tecelli",
    "meaning": "Ortaya çıkma, görünme, belirme (özellikle ilahi gücün)."
  },
  {
    "word": "ihtimam",
    "meaning": "Özen gösterme, dikkat etme."
  },
  {
    "word": "iltizam",
    "meaning": "Taraf tutma, kayırma; gerekli görme."
  },
  {
    "word": "istifade",
    "meaning": "Yararlanma, faydalanma."
  },
  {
    "word": "ittifak",
    "meaning": "Anlaşma, uzlaşma."
  },
  {
    "word": "mukayyet",
    "meaning": "Kayıtlı, bağlı, sorumlu."
  },
  {
    "word": "müşahede",
    "meaning": "Gözlem, izleme, dikkatle bakma."
  },
  {
    "word": "mütekabiliyet",
    "meaning": "Karşılıklılık esası."
  },
  {
    "word": "mütevelli",
    "meaning": "Vakfın yönetiminden sorumlu kişi (yönetici)."
  },
  {
    "word": "teklif",
    "meaning": "Öneri, bir şeyin yapılmasını isteme."
  },
  {
    "word": "terennüm",
    "meaning": "Şarkı söyleme, mırıldanma; tatlı bir sesle dile getirme."
  },
  {
    "word": "vaat",
    "meaning": "Söz verme, bir şeyi yapacağını bildirme."
  },
  {
    "word": "vaziyet",
    "meaning": "Durum, hal, pozisyon."
  },
  {
    "word": "vukuf",
    "meaning": "Bilgi, bir şeyi iyi bilme, aşina olma."
  },
  {
    "word": "izale",
    "meaning": "Ortadan kaldırma, giderme, yok etme."
  },
  {
    "word": "münakaşa",
    "meaning": "Tartışma, fikir çatışması."
  },
  {
    "word": "münasebet",
    "meaning": "İlişki, bağlantı, uygunluk."
  },
  {
    "word": "nitelik",
    "meaning": "Bir şeyin nasıl olduğunu belirten özellik, vasıf."
  },
  {
    "word": "nicelik",
    "meaning": "Miktar, sayıca çokluk."
  },
  {
    "word": "objektif",
    "meaning": "Tarafsız, nesnel, kişisel görüşten bağımsız."
  },
  {
    "word": "sübjektif",
    "meaning": "Öznel, kişisel görüşe dayalı."
  },
  {
    "word": "tasavvuf",
    "meaning": "İslami mistisizm, Allah'a manevi yollarla ulaşmayı amaçlayan felsefi düşünce."
  },
  {
    "word": "teşkilat",
    "meaning": "Kuruluş, örgüt, düzenlenmiş yapı."
  },
  {
    "word": "tevcih",
    "meaning": "Yöneltme, bir göreve atama."
  },
  {
    "word": "töhmet",
    "meaning": "Suçlama, zan."
  },
  {
    "word": "uzlaşma",
    "meaning": "Anlaşma, ortak bir noktada buluşma."
  },
  {
    "word": "vaziyet",
    "meaning": "Durum, hal."
  },
  {
    "word": "zarafet",
    "meaning": "İncelik, şıklık, hoş görünüş."
  },
  {
    "word": "içerik",
    "meaning": "Bir şeyin içinde bulunanların bütünü, muhteva."
  },
  {
    "word": "hararet",
    "meaning": "Isı, sıcaklık; coşku, heyecan."
  },
  {
    "word": "hissikablelvuku",
    "meaning": "Bir olayın olmadan önce hissedilmesi, önsezi."
  },
  {
    "word": "husumet",
    "meaning": "Düşmanlık, kin, nefret."
  },
  {
    "word": "ibda",
    "meaning": "Yaratma, benzersiz bir şey ortaya çıkarma."
  },
  {
    "word": "icra",
    "meaning": "Yerine getirme, uygulama, yapma."
  },
  {
    "word": "iktidar",
    "meaning": "Yönetme gücü, siyasi güç; yetenek, güç."
  },
  {
    "word": "ihtimal",
    "meaning": "Olasılık, muhtemel olma durumu."
  },
  {
    "word": "iltica",
    "meaning": "Sığınma, başka bir ülkeye veya yere sığınma."
  },
  {
    "word": "inkâr",
    "meaning": "Kabul etmeme, yalanlama, reddetme."
  },
  {
    "word": "intikal",
    "meaning": "Geçme, aktarılma; anlama, kavrama."
  },
  {
    "word": "irtibat",
    "meaning": "Bağlantı, ilişki, iletişim."
  },
  {
    "word": "istek",
    "meaning": "Dilek, arzu, bir şeye karşı duyulan eğilim."
  },
  {
    "word": "iştiyak",
    "meaning": "Özlem, kuvvetli arzu, hasret."
  },
  {
    "word": "kanaat",
    "meaning": "Görüş, düşünce; elindekine razı olma durumu."
  },
  {
    "word": "kat'i",
    "meaning": "Kesin, net, tartışmasız."
  },
  {
    "word": "kıvanç",
    "meaning": "Övünç, gurur, sevinçle karışık övünme duygusu."
  },
  {
    "word": "kudret",
    "meaning": "Güç, kuvvet, iktidar."
  },
  {
    "word": "lüzum",
    "meaning": "Gereklilik, ihtiyaç."
  },
  {
    "word": "mağrur",
    "meaning": "Gururlu, kibirli, kendini beğenmiş."
  },
  {
    "word": "mahiyet",
    "meaning": "Bir şeyin aslı, iç yüzü, niteliği."
  },
  {
    "word": "maksat",
    "meaning": "Amaç, niyet, gaye."
  },
  {
    "word": "malum",
    "meaning": "Bilinen, belli, herkesçe tanınan."
  },
  {
    "word": "maneviyat",
    "meaning": "Ruhsal durum, moral, iç güç."
  },
  {
    "word": "merhamet",
    "meaning": "Acıma, şefkat, başkasının acısına ortak olma."
  },
  {
    "word": "mesai",
    "meaning": "Çalışma, iş görme; çalışma süresi."
  },
  {
    "word": "metanet",
    "meaning": "Dayanıklılık, direnç, güçlü durma."
  },
  {
    "word": "muhafaza",
    "meaning": "Koruma, saklama, kollama."
  },
  {
    "word": "mukavemet",
    "meaning": "Direnç, dayanıklılık, karşı koyma."
  },
  {
    "word": "müsbet",
    "meaning": "Olumlu, pozitif, iyi."
  },
  {
    "word": "müspet",
    "meaning": "Olumlu, pozitif, iyi (müsbet ile aynı anlamda kullanılır)."
  },
  {
    "word": "müşahede",
    "meaning": "Gözlem, izleme."
  },
  {
    "word": "müstesna",
    "meaning": "Eşi az bulunan, özel."
  },
  {
    "word": "mütenasip",
    "meaning": "Orantılı, uygun, yakışır."
  },
  {
    "word": "mütevazı",
    "meaning": "Alçak gönüllü, sade."
  },
  {
    "word": "nezaket",
    "meaning": "İncelik, kibarlık, saygılı davranış."
  },
  {
    "word": "noksan",
    "meaning": "Eksik, kusurlu, yetersiz."
  },
  {
    "word": "paye",
    "meaning": "Rütbe, derece, makam."
  },
  {
    "word": "sadakat",
    "meaning": "Bağlılık, doğruluk, vefa."
  },
  {
    "word": "safha",
    "meaning": "Evre, aşama, merhale."
  },
  {
    "word": "seciye",
    "meaning": "Karakter, huy, kişilik."
  },
  {
    "word": "şuur",
    "meaning": "Bilinç, farkındalık, idrak."
  },
  {
    "word": "takdir",
    "meaning": "Beğenme, değer verme; kader, alın yazısı."
  },
  {
    "word": "tasvir",
    "meaning": "Betimleme, resmetme."
  },
  {
    "word": "tecrübe",
    "meaning": "Deneyim, görgü."
  },
  {
    "word": "tefekkür",
    "meaning": "Derin düşünme."
  },
  {
    "word": "telkin",
    "meaning": "Aşılama, başkasının aklına sokma."
  },
  {
    "word": "temayül",
    "meaning": "Eğilim, yönelme."
  },
  {
    "word": "tercüme",
    "meaning": "Çeviri, bir dilden başka bir dile aktarma."
  },
  {
    "word": "tesadüf",
    "meaning": "Rastlantı, beklenmedik olay."
  },
  {
    "word": "teşebbüs",
    "meaning": "Girişim, bir işe başlama."
  },
  {
    "word": "tevazu",
    "meaning": "Alçak gönüllülük."
  },
  {
    "word": "tevil",
    "meaning": "Yorumlama, bir sözü başka bir anlama çekme."
  },
  {
    "word": "vazife",
    "meaning": "Görev, sorumluluk."
  },
  {
    "word": "veciz",
    "meaning": "Özlü, kısa ve anlamlı (söz)."
  },
  {
    "word": "yegane",
    "meaning": "Tek, biricik, eşsiz."
  },
  {
    "word": "zahir",
    "meaning": "Görünürde olan, dıştan belli olan."
  },
  {
    "word": "zamanla",
    "meaning": "Süreç içinde, yavaş yavaş, ilerleyen vakitte."
  },
  {
    "word": "zikir",
    "meaning": "Anma, hatırlama; Allah'ın adını anma."
  },
  {
    "word": "zuhur",
    "meaning": "Ortaya çıkma, görünme, belirme."
  },
  {
    "word": "hayal",
    "meaning": "Gerçekte var olmayan, zihinde canlandırılan görüntü, düş."
  },
  {
    "word": "düşünce",
    "meaning": "Akıl yoluyla ulaşılan fikir, zihinsel faaliyet sonucu oluşan sonuç."
  },
  {
    "word": "görüş",
    "meaning": "Bir konu hakkındaki kişisel fikir, bakış açısı."
  },
  {
    "word": "kavrayış",
    "meaning": "Anlama, idrak etme yeteneği."
  },
  {
    "word": "yargı",
    "meaning": "Bir konu, kişi veya durum hakkında varılan sonuç, hüküm."
  },
  {
    "word": "bilgi",
    "meaning": "Öğrenme, araştırma veya gözlem yoluyla elde edilen gerçek."
  },
  {
    "word": "tecrübe",
    "meaning": "Deneyim, yaşanmışlık."
  },
  {
    "word": "gözlem",
    "meaning": "Bir olayı veya durumu dikkatle izleme, müşahede."
  },
  {
    "word": "araştırma",
    "meaning": "Bir konu hakkında sistematik ve bilimsel bilgi toplama süreci."
  },
  {
    "word": "inceleme",
    "meaning": "Detaylı olarak bakma, tetkik etme."
  },
  {
    "word": "metot",
    "meaning": "Bir amaca ulaşmak için izlenen düzenli yol, yöntem."
  },
  {
    "word": "sistem",
    "meaning": "Birbiriyle ilişkili parçaların oluşturduğu düzenli bütün."
  },
  {
    "word": "proje",
    "meaning": "Belirli bir amaç için planlanmış, süresi ve bütçesi olan çalışma."
  },
  {
    "word": "girişim",
    "meaning": "Bir işi yapmaya başlama, teşebbüs."
  },
  {
    "word": "başarı",
    "meaning": "Bir işte istenilen sonucu elde etme, muvaffakiyet."
  },
  {
    "word": "azim",
    "meaning": "Bir işi yapmaya kararlı olma, sebat."
  },
  {
    "word": "kararlılık",
    "meaning": "Bir düşünce veya eylemde sabit olma, tereddütsüzlük."
  },
  {
    "word": "sebat",
    "meaning": "Direniş, bir işte ısrar etme."
  },
  {
    "word": "güven",
    "meaning": "Şüphe duymadan inanma, itimat."
  },
  {
    "word": "sadakat",
    "meaning": "Bağlılık, vefa."
  },
  {
    "word": "dürüstlük",
    "meaning": "Doğru sözlü olma, hile yapmama."
  },
  {
    "word": "saygı",
    "meaning": "Değer verme, hürmet, başkasına karşı kibar davranma."
  },
  {
    "word": "sevgi",
    "meaning": "Birine karşı duyulan yakınlık ve bağlılık duygusu, muhabbet."
  },
  {
    "word": "mutluluk",
    "meaning": "Sevinç, huzur, yaşama sevincini yansıtan duygu."
  },
  {
    "word": "hüzün",
    "meaning": "Üzüntü, keder, iç sıkıntısı."
  },
  {
    "word": "keder",
    "meaning": "Derin üzüntü, elem."
  },
  {
    "word": "pişmanlık",
    "meaning": "Yapılan bir hatadan dolayı duyulan üzüntü."
  },
  {
    "word": "öfke",
    "meaning": "Şiddetli kızgınlık, hiddet."
  },
  {
    "word": "neşe",
    "meaning": "Keyif, sevinç, şenlik."
  },
  {
    "word": "hayranlık",
    "meaning": "Beğenme, takdir etme duygusu."
  },
  {
    "word": "kıskançlık",
    "meaning": "Başkasına ait olan bir şeyi isteme, çekememezlik."
  },
  {
    "word": "çekingenlik",
    "meaning": "Utangaçlık, kendini geri çekme eğilimi."
  },
  {
    "word": "cesaret",
    "meaning": "Korkusuzluk, yüreklilik."
  },
  {
    "word": "korku",
    "meaning": "Tehlike karşısında duyulan endişe, ürküntü."
  },
  {
    "word": "endişe",
    "meaning": "Kaygı, tasa, huzursuzluk."
  },
  {
    "word": "huzur",
    "meaning": "Dinginlik, rahatlık, iç barışı."
  },
  {
    "word": "merak",
    "meaning": "Bir şeyi öğrenme veya görme isteği."
  },
  {
    "word": "sabır",
    "meaning": "Beklemeye, zorluğa dayanma gücü."
  },
  {
    "word": "şükür",
    "meaning": "Minnettarlık, iyiliğe karşı duyulan memnuniyet."
  },
  {
    "word": "minnet",
    "meaning": "Yapılan bir iyiliğe karşı duyulan borçluluk duygusu."
  },
  {
    "word": "vefa",
    "meaning": "Sözünde durma, bağlılık, sadakat."
  },
  {
    "word": "ihsan",
    "meaning": "Bağışlama, iyilik etme, lütuf."
  },
  {
    "word": "lütuf",
    "meaning": "İyilik, bağış, birine yapılan güzellik."
  },
  {
    "word": "kerem",
    "meaning": "Cömertlik, iyilik, asillik."
  },
  {
    "word": "cömertlik",
    "meaning": "Elde avuçta olanı esirgemeden verme, lütufkârlık."
  },
  {
    "word": "kanaatkâr",
    "meaning": "Elindekine razı olan, yetinen."
  },
  {
    "word": "açgözlülük",
    "meaning": "Doyumsuzluk, elindekine yetinmeme."
  },
  {
    "word": "tamah",
    "meaning": "Aşırı düşkünlük, açgözlülük."
  },
  {
    "word": "hırs",
    "meaning": "Aşırı istek, tutku, ihtiras."
  },
  {
    "word": "tutku",
    "meaning": "Şiddetli arzu, ihtiras."
  },
  {
    "word": "ihtiras",
    "meaning": "Aşırı ve güçlü istek, tutku."
  },
  {
    "word": "heves",
    "meaning": "Geçici istek, özenme."
  },
  {
    "word": "şevk",
    "meaning": "Coşku, istek, yaşama sevinci."
  },
  {
    "word": "coşku",
    "meaning": "Heyecan, şevk, taşkınlık."
  },
  {
    "word": "heyecan",
    "meaning": "Duygusal tepki, coşku, telaş."
  },
  {
    "word": "telaş",
    "meaning": "Acele etme, şaşkınlık, huzursuzluk."
  },
  {
    "word": "panik",
    "meaning": "Birdenbire oluşan aşırı korku ve telaş."
  },
  {
    "word": "kaygı",
    "meaning": "Endişe, tasa, üzüntü."
  },
  {
    "word": "hata",
    "meaning": "Yanlış, kusur, yanlışlık."
  },
  {
    "word": "kusur",
    "meaning": "Eksiklik, ayıp, noksan."
  },
  {
    "word": "ayıp",
    "meaning": "Utanç verici durum, kusur."
  },
  {
    "word": "utanma",
    "meaning": "Mahcubiyet, yapılan bir hatadan dolayı duyulan rahatsızlık."
  },
  {
    "word": "mahcup",
    "meaning": "Utangaç, çekingen."
  },
  {
    "word": "utangaç",
    "meaning": "Çekingen, mahcup."
  },
  {
    "word": "kibir",
    "meaning": "Büyüklük taslama, kendini üstün görme."
  },
  {
    "word": "tevazu",
    "meaning": "Alçak gönüllülük."
  },
  {
    "word": "gurur",
    "meaning": "Kendine güvenme, övünç; aşırı onur."
  },
  {
    "word": "onur",
    "meaning": "İnsanlık haysiyeti, şeref."
  },
  {
    "word": "şeref",
    "meaning": "İtibar, saygınlık, onur."
  },
  {
    "word": "itibar",
    "meaning": "Saygınlık, değer."
  },
  {
    "word": "değer",
    "meaning": "Kıymet, önem."
  },
  {
    "word": "önem",
    "meaning": "Ehemmiyet, kıymet."
  },
  {
    "word": "ehemmiyet",
    "meaning": "Önem, değer."
  },
  {
    "word": "öncelik",
    "meaning": "İlk sırada olma, öncelikli olma durumu."
  },
  {
    "word": "sürüncemede",
    "meaning": "Gecikme, sonuçlanmama, uzama."
  },
  {
    "word": "müphemlik",
    "meaning": "Belirsizlik, muğlaklık, kapalılık."
  },
  {
    "word": "teminat",
    "meaning": "Güvence, garanti, kefalet."
  },
  {
    "word": "tedbir",
    "meaning": "Önlem, ihtiyat, önceden alınan karar."
  },
  {
    "word": "ihtiyat",
    "meaning": "Önlem, dikkatlilik."
  },
  {
    "word": "itina",
    "meaning": "Özen, dikkat, ihtimam."
  },
  {
    "word": "basiret",
    "meaning": "Uzağı görme, ileriyi sezinleme yeteneği."
  },
  {
    "word": "firaset",
    "meaning": "Anlayış, zekâ, sezgi gücü."
  },
  {
    "word": "feraset",
    "meaning": "Uzağı görme, sezgi gücü."
  },
  {
    "word": "irade",
    "meaning": "İsteme, dileme gücü, karar verme yeteneği."
  },
  {
    "word": "hegemonya",
    "meaning": "Bir devletin veya grubun diğerleri üzerindeki siyasi ve askeri üstünlüğü, egemenlik."
  },
  {
    "word": "dominant",
    "meaning": "Baskın, egemen, önde gelen."
  },
  {
    "word": "alternatif",
    "meaning": "Seçenek, başka bir yol, diğer imkân."
  },
  {
    "word": "imkan",
    "meaning": "Olanak, mümkün olma durumu."
  },
  {
    "word": "olanak",
    "meaning": "İmkan, fırsat."
  },
  {
    "word": "fırsat",
    "meaning": "Uygun zaman, olanak."
  },
  {
    "word": "vesile",
    "meaning": "Sebep, bahane, aracı."
  },
  {
    "word": "sevk",
    "meaning": "Yönlendirme, gönderme, teşvik etme."
  },
  {
    "word": "tahrik",
    "meaning": "Kışkırtma, harekete geçirme, provoke etme."
  },
  {
    "word": "provokasyon",
    "meaning": "Kışkırtma, tahrik etme."
  },
  {
    "word": "muteber",
    "meaning": "İtibarlı, saygın, güvenilir."
  },
  {
    "word": "mukim",
    "meaning": "İkamet eden, oturan, yerleşik."
  },
  {
    "word": "ikamet",
    "meaning": "Oturma, yerleşme, konut edinme."
  },
  {
    "word": "mesken",
    "meaning": "Konut, ev, ikamet edilen yer."
  },
  {
    "word": "iştigal",
    "meaning": "Uğraşma, meşgul olma."
  },
  {
    "word": "mütekebbir",
    "meaning": "Kibirli, kendini beğenmiş, mağrur."
  },
  {
    "word": "müteessir",
    "meaning": "Etkilenmiş, üzülmüş, acı duymuş."
  },
  {
    "word": "tezkiye",
    "meaning": "Aklama, temize çıkarma; birinin iyi olduğunu onaylama."
  },
  {
    "word": "tahsis",
    "meaning": "Ayırma, özel olarak bir şeye veya birine ayırma."
  },
  {
    "word": "mukavele",
    "meaning": "Sözleşme, anlaşma."
  },
  {
    "word": "iltifat",
    "meaning": "Güler yüz gösterme, nazikçe konuşma."
  },
  {
    "word": "iltica",
    "meaning": "Sığınma, sığınacak yer arama."
  },
  {
    "word": "imtiyaz",
    "meaning": "Ayrıcalık, üstünlük, özel hak."
  },
  {
    "word": "israf",
    "meaning": "Gereksiz yere harcama, savurganlık."
  },
  {
    "word": "iktisat",
    "meaning": "Ekonomi, tutumluluk, tasarruf."
  },
  {
    "word": "iktibas",
    "meaning": "Alıntı, başkasından aktarma."
  },
  {
    "word": "mukayese",
    "meaning": "Karşılaştırma, kıyaslama."
  },
  {
    "word": "müebbet",
    "meaning": "Sonsuz, ebedi; ömür boyu (hapis)."
  },
  {
    "word": "münhasır",
    "meaning": "Sadece ona ait, özel."
  },
  {
    "word": "müteferrik",
    "meaning": "Çeşitli, dağınık, ayrı ayrı."
  },
  {
    "word": "mütevelli",
    "meaning": "Vakıf yöneticisi."
  },
  {
    "word": "necip",
    "meaning": "Soylu, temiz soydan gelen; değerli."
  },
  {
    "word": "nüfuz",
    "meaning": "Sözü geçerlilik, etki, derinlik."
  },
  {
    "word": "rıza",
    "meaning": "Razı olma, kabul etme, onay."
  },
  {
    "word": "safiyet",
    "meaning": "Temizlik, saflık, içtenlik."
  },
  {
    "word": "seciye",
    "meaning": "Karakter, huy."
  },
  {
    "word": "sükûnet",
    "meaning": "Sessizlik, dinginlik, huzur."
  },
  {
    "word": "şefaat",
    "meaning": "Birinin affedilmesi için aracılık etme."
  },
  {
    "word": "tahmin",
    "meaning": "Yaklaşık olarak hesaplama, kestirim."
  },
  {
    "word": "takdir",
    "meaning": "Değer verme, beğenme; kader."
  },
  {
    "word": "tanzim",
    "meaning": "Düzenleme, yoluna koyma, organize etme."
  },
  {
    "word": "tebellüğ",
    "meaning": "Alma, teslim alma, tebliğ edilen şeyi kabul etme."
  },
  {
    "word": "tecessüs",
    "meaning": "Merak, öğrenme isteği."
  },
  {
    "word": "tevdi",
    "meaning": "Verme, teslim etme, emanet etme."
  },
  {
    "word": "tevhit",
    "meaning": "Birleştirme, tek kılma; Allah'ın birliğine inanma."
  },
  {
    "word": "tezyif",
    "meaning": "Küçümseme, alay etme."
  },
  {
    "word": "vazgeçmek",
    "meaning": "Bir haktan, fikirden veya eylemden caymak, feragât etmek."
  },
  {
    "word": "vuku",
    "meaning": "Meydana gelme, olma, gerçekleşme."
  },
  {
    "word": "vukuf",
    "meaning": "Bilgi, bir şeyi iyi bilme."
  },
  {
    "word": "zannetmek",
    "meaning": "Sanmak, tahminde bulunmak, öyle olduğunu düşünmek."
  },
  {
    "word": "zımnen",
    "meaning": "Dolaylı olarak, üstü kapalı şekilde, ima yoluyla."
  },
  {
    "word": "zuhur",
    "meaning": "Ortaya çıkma, görünme."
  },
  {
    "word": "aciz",
    "meaning": "Güçsüz, beceriksiz, yeteneksiz."
  },
  {
    "word": "adalet",
    "meaning": "Hak ve hukuka uygunluk, doğruluk."
  },
  {
    "word": "akıl",
    "meaning": "Düşünme, anlama ve yargılama yeteneği, us."
  },
  {
    "word": "alelade",
    "meaning": "Sıradan, olağan, herhangi bir özellik taşımayan."
  },
  {
    "word": "anane",
    "meaning": "Gelenek, görenek, nesilden nesile aktarılan adet."
  },
  {
    "word": "arzu",
    "meaning": "İstek, dilek, güçlü yönelim."
  },
  {
    "word": "asır",
    "meaning": "Yüz yıllık zaman dilimi, çağ."
  },
  {
    "word": "aşina",
    "meaning": "Tanıdık, bildik, bir şeye alışık."
  },
  {
    "word": "avdet",
    "meaning": "Geri dönme, geri gelme."
  },
  {
    "word": "azami",
    "meaning": "En çok, en yüksek, maksimum."
  },
  {
    "word": "bedbin",
    "meaning": "Kötümser, karamsar."
  },
  {
    "word": "beşer",
    "meaning": "İnsan, insanoğlu."
  },
  {
    "word": "binaenaleyh",
    "meaning": "Bundan dolayı, bunun için, o halde."
  },
  {
    "word": "cür'et",
    "meaning": "Cesaret, yüreklilik, atılganlık."
  },
  {
    "word": "ciddi",
    "meaning": "Şaka olmayan, önemli, ağırbaşlı."
  },
  {
    "word": "deha",
    "meaning": "Yüksek ve üstün zekâ, olağanüstü yetenek."
  },
  {
    "word": "dirayet",
    "meaning": "Zekâ, anlayış, akıl gücü."
  },
  {
    "word": "ehemmiyet",
    "meaning": "Önem, değer."
  },
  {
    "word": "ekseriyet",
    "meaning": "Çoğunluk, büyük bir kısmı."
  },
  {
    "word": "esrar",
    "meaning": "Sırlar, gizemler; uyuşturucu madde."
  },
  {
    "word": "evvela",
    "meaning": "Öncelikle, ilk olarak, önce."
  },
  {
    "word": "fevkalade",
    "meaning": "Olağanüstü, beklenmedik derecede iyi."
  },
  {
    "word": "garip",
    "meaning": "Şaşırtıcı, tuhaf; yabancı, kimsesiz."
  },
  {
    "word": "gayret",
    "meaning": "Çaba, çalışma, uğraş."
  },
  {
    "word": "hadsiz",
    "meaning": "Sınırsız, ölçüsüz, çok fazla."
  },
  {
    "word": "hakikat",
    "meaning": "Gerçek, doğru, asıl olan."
  },
  {
    "word": "hissiyat",
    "meaning": "Duygular, hisler."
  },
  {
    "word": "hukuk",
    "meaning": "Yasa, adalet; bir bilimin kuralları."
  },
  {
    "word": "husus",
    "meaning": "Konu, mesele, özel durum."
  },
  {
    "word": "hülya",
    "meaning": "Tatlı düş, hayal, kuruntu."
  },
  {
    "word": "icap",
    "meaning": "Gereklilik, zorunluluk."
  },
  {
    "word": "ihtimal",
    "meaning": "Olasılık."
  },
  {
    "word": "ihya",
    "meaning": "Canlandırma, yeniden hayata döndürme."
  },
  {
    "word": "ikmal",
    "meaning": "Tamamlama, bitirme."
  },
  {
    "word": "iltizam",
    "meaning": "Kayırma, taraf tutma."
  },
  {
    "word": "imza",
    "meaning": "İmzalama, bir belgeyi onaylama."
  },
  {
    "word": "intizam",
    "meaning": "Düzen, nizam, tertip."
  },
  {
    "word": "irfan",
    "meaning": "Bilgelik, kültür, bilgi ve görgü."
  },
  {
    "word": "istek",
    "meaning": "Arzu, dilek."
  },
  {
    "word": "itimad",
    "meaning": "Güven, inanma."
  },
  {
    "word": "ittihad",
    "meaning": "Birlik, birleşme."
  },
  {
    "word": "iz'an",
    "meaning": "Anlayış, kavrayış, akıl."
  },
  {
    "word": "karar",
    "meaning": "Bir iş hakkında verilen kesin hüküm."
  },
  {
    "word": "kanaat",
    "meaning": "Görüş, düşünce; yetinme."
  },
  {
    "word": "keramet",
    "meaning": "Olağanüstü hal, mucize."
  },
  {
    "word": "kıymet",
    "meaning": "Değer, paha."
  },
  {
    "word": "lisan",
    "meaning": "Dil, konuşma aracı."
  },
  {
    "word": "maharet",
    "meaning": "Beceri, ustalık, hüner."
  },
  {
    "word": "malumat",
    "meaning": "Bilgi, haber, enformasyon."
  },
  {
    "word": "menfi",
    "meaning": "Olumsuz, negatif, kötü."
  },
  {
    "word": "merhale",
    "meaning": "Aşama, safha."
  },
  {
    "word": "muayyen",
    "meaning": "Belirli, belli, tayin edilmiş."
  },
  {
    "word": "muharrir",
    "meaning": "Yazar, edebi eser sahibi."
  },
  {
    "word": "mukaddes",
    "meaning": "Kutsal, dokunulmaz, saygıdeğer."
  },
  {
    "word": "münakaşa",
    "meaning": "Tartışma, çekişme."
  },
  {
    "word": "münasebet",
    "meaning": "İlişki, bağlantı."
  },
  {
    "word": "münferit",
    "meaning": "Tek, ayrı, bağımsız."
  },
  {
    "word": "müspet",
    "meaning": "Olumlu, pozitif."
  },
  {
    "word": "müstahkem",
    "meaning": "Sağlamlaştırılmış, tahkim edilmiş."
  },
  {
    "word": "naif",
    "meaning": "Saf, temiz, deneyimsiz."
  },
  {
    "word": "nasihat",
    "meaning": "Öğüt, tavsiye."
  },
  {
    "word": "nefaset",
    "meaning": "Güzellik, lezzet, hoşluk."
  },
  {
    "word": "nezaret",
    "meaning": "Gözetim, denetim, bakanlık."
  },
  {
    "word": "nihayet",
    "meaning": "Sonuçta, sonunda, nihai olarak."
  },
  {
    "word": "nizam",
    "meaning": "Düzen, kural, intizam."
  },
  {
    "word": "noksan",
    "meaning": "Eksik, kusurlu."
  },
  {
    "word": "sadakat",
    "meaning": "Bağlılık, vefa."
  },
  {
    "word": "safha",
    "meaning": "Aşama, evre."
  },
  {
    "word": "sükun",
    "meaning": "Huzur, dinginlik."
  },
  {
    "word": "şahıs",
    "meaning": "Kişi, ferd."
  },
  {
    "word": "şayan",
    "meaning": "Layık, değer, uygun."
  },
  {
    "word": "şiar",
    "meaning": "Parola, işaret; bir düşüncenin simgesi."
  },
  {
    "word": "şuur",
    "meaning": "Bilinç, farkındalık."
  },
  {
    "word": "tabiat",
    "meaning": "Doğa, yaratılış, huy."
  },
  {
    "word": "tahkik",
    "meaning": "Araştırma, soruşturma."
  },
  {
    "word": "tahrip",
    "meaning": "Yıkma, bozma, zarar verme."
  },
  {
    "word": "taltif",
    "meaning": "Ödüllendirme, iltifat etme."
  },
  {
    "word": "taraftar",
    "meaning": "Destekleyen, yandaş, hayran."
  },
  {
    "word": "tasavvur",
    "meaning": "Hayal etme, zihinde canlandırma."
  },
  {
    "word": "tavsiye",
    "meaning": "Öğüt, nasihat, yol gösterme."
  },
  {
    "word": "tereddüt",
    "meaning": "Kararsızlık, duraksama."
  },
  {
    "word": "teşvik",
    "meaning": "Cesaretlendirme, isteklendirme."
  },
  {
    "word": "tevazu",
    "meaning": "Alçak gönüllülük."
  },
  {
    "word": "teveccüh",
    "meaning": "İlgi, yüzünü çevirme."
  },
  {
    "word": "tevekkül",
    "meaning": "Allah'a güvenme, kadere razı olma."
  },
  {
    "word": "tevkif",
    "meaning": "Tutuklama, alıkoyma."
  },
  {
    "word": "töhmet",
    "meaning": "Suçlama, zan."
  },
  {
    "word": "vahim",
    "meaning": "Ciddi, tehlikeli, korkunç."
  },
  {
    "word": "vakar",
    "meaning": "Ağırbaşlılık, onur, ciddiyet."
  },
  {
    "word": "vaziyet",
    "meaning": "Durum, hal."
  },
  {
    "word": "vecize",
    "meaning": "Özlü söz, kısa ve anlamlı ifade."
  },
  {
    "word": "yasa",
    "meaning": "Kanun, kural, emir."
  },
  {
    "word": "yegane",
    "meaning": "Tek, biricik."
  },
  {
    "word": "zekâ",
    "meaning": "Akıl, anlama yeteneği."
  },
  {
    "word": "zaman",
    "meaning": "Süre, vakit."
  },
  {
    "word": "zira",
    "meaning": "Çünkü, sebep olarak."
  },
  {
    "word": "zulüm",
    "meaning": "Haksızlık, eziyet, baskı."
  },
  {
    "word": "özlem",
    "meaning": "Bir şeye duyulan yoğun istek, hasret."
  },
  {
    "word": "hasret",
    "meaning": "Özlem, ayrılık acısı."
  },
  {
    "word": "hicran",
    "meaning": "Ayrılık acısı, özlem."
  },
  {
    "word": "mahsul",
    "meaning": "Ürün, elde edilen sonuç."
  },
  {
    "word": "mahiyet",
    "meaning": "Nitelik, öz, iç yüzü."
  },
  {
    "word": "mutlak",
    "meaning": "Kesin, şüphesiz, sınırsız."
  },
  {
    "word": "nispeten",
    "meaning": "Görece, oranla, kıyasla."
  },
  {
    "word": "tefrik",
    "meaning": "Ayırma, fark etme, ayırt etme."
  },
  {
    "word": "tekamül",
    "meaning": "Gelişme, olgunlaşma."
  },
  {
    "word": "temin",
    "meaning": "Sağlama, tedarik etme."
  },
  {
    "word": "vazife",
    "meaning": "Görev, ödev."
  },
  {
    "word": "vaka",
    "meaning": "Olay, hadise."
  },
  {
    "word": "yönelim",
    "meaning": "Eğilim, temayül, bir tarafa doğru gitme."
  },
  {
    "word": "zenginlik",
    "meaning": "Bolluk, çokluk, varlık."
  },
  {
    "word": "zemin",
    "meaning": "Yer, toprak, ortam; bir konunun dayanağı."
  },
  {
    "word": "iade",
    "meaning": "Geri verme."
  },
  {
    "word": "ispat",
    "meaning": "Kanıtlama, doğru olduğunu gösterme."
  },
  {
    "word": "itiraz",
    "meaning": "Karşı çıkma, razı olmama."
  },
  {
    "word": "kabul",
    "meaning": "Onaylama, razı olma."
  },
  {
    "word": "kıstas",
    "meaning": "Ölçüt, kriter."
  },
  {
    "word": "muhtıra",
    "meaning": "Anımsatma yazısı, nota."
  },
  {
    "word": "mukadder",
    "meaning": "Yazgı, alın yazısı, kader."
  },
  {
    "word": "müsavi",
    "meaning": "Eşit, denk, aynı."
  },
  {
    "word": "tahayyül",
    "meaning": "Hayal etme."
  },
  {
    "word": "teşkil",
    "meaning": "Oluşturma, kurma."
  },
  {
    "word": "tezahür",
    "meaning": "Ortaya çıkma, belirme."
  },
  {
    "word": "üslup",
    "meaning": "Anlatım tarzı, stil."
  },
  {
    "word": "vukuf",
    "meaning": "Bilgi, bir şeyi iyi bilme."
  },
  {
    "word": "zımni",
    "meaning": "Dolaylı, üstü kapalı."
  },
  {
    "word": "anlık",
    "meaning": "Bir an süren, hemen olan, lahzavi."
  },
  {
    "word": "beklenti",
    "meaning": "Umut edilen, gerçekleşmesi istenen durum."
  },
  {
    "word": "denge",
    "meaning": "Ağırlıkların eşitliği, uyum, istikrar."
  },
  {
    "word": "etki",
    "meaning": "Tesir, bir şeyin başka bir şey üzerinde bıraktığı iz."
  },
  {
    "word": "farkındalık",
    "meaning": "Bilinçli olma, bir durumu anlama."
  },
  {
    "word": "gelişim",
    "meaning": "İlerleme, büyüme, tekâmül."
  },
  {
    "word": "geçerli",
    "meaning": "Kabul edilmiş, yürürlükte olan, muteber."
  },
  {
    "word": "güvenilirlik",
    "meaning": "İtimat edilebilirlik, muteberlik."
  },
  {
    "word": "hedef",
    "meaning": "Amaç, ulaşılmak istenen nokta."
  },
  {
    "word": "hizmet",
    "meaning": "Birine yarar sağlama, görev, servis."
  },
  {
    "word": "ilgi",
    "meaning": "Alaka, merak, bir şeye yönelme."
  },
  {
    "word": "ilişki",
    "meaning": "Bağlantı, münasebet, irtibat."
  },
  {
    "word": "kapsam",
    "meaning": "Şümul, bir şeyin içine aldığı alan."
  },
  {
    "word": "katılım",
    "meaning": "İştirak etme, bir etkinliğe dahil olma."
  },
  {
    "word": "kural",
    "meaning": "Yasa, kaide, bir işin yapılış biçimi."
  },
  {
    "word": "kültür",
    "meaning": "Toplumun maddi ve manevi değerlerinin bütünü."
  },
  {
    "word": "liderlik",
    "meaning": "Önderlik, yönlendirme, kılavuzluk."
  },
  {
    "word": "misyon",
    "meaning": "Görev, amaç, bir kurumun varlık nedeni."
  },
  {
    "word": "motivasyon",
    "meaning": "Güdülenme, isteklenme, teşvik."
  },
  {
    "word": "nitelik",
    "meaning": "Özellik, vasıf, kalite."
  },
  {
    "word": "planlama",
    "meaning": "Bir işin nasıl yapılacağını önceden tasarlama, düzenleme."
  },
  {
    "word": "potansiyel",
    "meaning": "Gizli güç, olası yetenek, mevcut imkan."
  },
  {
    "word": "prensipler",
    "meaning": "Temel kurallar, esaslar, ilkeler."
  },
  {
    "word": "problem",
    "meaning": "Sorun, çözülmesi gereken mesele."
  },
  {
    "word": "sorumluluk",
    "meaning": "Vazife, yükümlülük, hesap verme zorunluluğu."
  },
  {
    "word": "strateji",
    "meaning": "Uzun vadeli amaçlara ulaşmak için izlenen yol, plan."
  },
  {
    "word": "süreç",
    "meaning": "Devam eden olaylar dizisi, akış, proses."
  },
  {
    "word": "sürdürülebilir",
    "meaning": "Devam ettirilebilir, uzun ömürlü, kalıcı."
  },
  {
    "word": "takım",
    "meaning": "Ortak amaç için bir araya gelmiş grup, ekip."
  },
  {
    "word": "tanım",
    "meaning": "Bir kavramın ne olduğunu açıklayan ifade, tarif."
  },
  {
    "word": "uyum",
    "meaning": "Anlaşma, ahenk, adaptasyon."
  },
  {
    "word": "veri",
    "meaning": "Bilgi toplamak için kullanılan ham bilgi, data."
  },
  {
    "word": "yaratıcılık",
    "meaning": "Yeni fikirler, yöntemler veya nesneler ortaya çıkarma yeteneği."
  },
  {
    "word": "yönetim",
    "meaning": "İdare etme, sevk ve idare."
  },
  {
    "word": "yeterlilik",
    "meaning": "Kifayet, bir işi yapabilecek bilgi ve beceriye sahip olma."
  },
  {
    "word": "yükseliş",
    "meaning": "Artma, ilerleme, terakki."
  },
  {
    "word": "zamanlama",
    "meaning": "Bir işi doğru zamanda yapma, zamanı ayarlama."
  },
  {
    "word": "zorluk",
    "meaning": "Güçlük, sıkıntı, engel."
  },
  {
    "word": "çaba",
    "meaning": "Gayret, uğraş, emek."
  },
  {
    "word": "ödül",
    "meaning": "Bir başarıya karşılık verilen şey, mükafat."
  },
  {
    "word": "denetim",
    "meaning": "Kontrol, gözetim, teftiş."
  },
  {
    "word": "değişim",
    "meaning": "Farklılaşma, değişiklik, transformasyon."
  },
  {
    "word": "ön yargı",
    "meaning": "Peşin hüküm, bir kişi veya konu hakkında önceden oluşturulmuş olumsuz görüş."
  },
  {
    "word": "etkinlik",
    "meaning": "Faaliyet, hareket; tesir gücü."
  },
  {
    "word": "gerçeklik",
    "meaning": "Hakikat, var olan, sanal olmayan durum."
  },
  {
    "word": "güçlük",
    "meaning": "Zorluk, engel."
  },
  {
    "word": "ihlal",
    "meaning": "Çiğneme, bir kurala uymama."
  },
  {
    "word": "ikna",
    "meaning": "İnandırma, razı etme."
  },
  {
    "word": "kılavuz",
    "meaning": "Rehber, yol gösteren."
  },
  {
    "word": "kısıtlama",
    "meaning": "Sınırlama, daraltma."
  },
  {
    "word": "meslek",
    "meaning": "Uğraş, profesyonel iş."
  },
  {
    "word": "muhtemel",
    "meaning": "Olası, ihtimal dahilinde."
  },
  {
    "word": "müdahale",
    "meaning": "Karışma, araya girme."
  },
  {
    "word": "mükemmel",
    "meaning": "Kusursuz, eksiksiz, tam."
  },
  {
    "word": "öğrenim",
    "meaning": "Eğitim, ders alma."
  },
  {
    "word": "özveri",
    "meaning": "Fedakârlık, kendini adama."
  },
  {
    "word": "sistemli",
    "meaning": "Düzenli, planlı, yöntemli."
  },
  {
    "word": "sunum",
    "meaning": "Takdim, bir konuyu dinleyicilere aktarma."
  },
  {
    "word": "tecrübe",
    "meaning": "Deneyim."
  },
  {
    "word": "tehdit",
    "meaning": "Korkutma, gözdağı verme."
  },
  {
    "word": "uygulama",
    "meaning": "Pratik etme, tatbik etme."
  },
  {
    "word": "verimlilik",
    "meaning": "Randıman, üretkenlik, faydalılık."
  },
  {
    "word": "yasal",
    "meaning": "Hukuki, kanuna uygun."
  },
  {
    "word": "yükseltmek",
    "meaning": "Artırmak, daha üst seviyeye çıkarmak."
  },
  {
    "word": "zamanında",
    "meaning": "Vaktinde, tam olarak gereken anda."
  },
  {
    "word": "çatışma",
    "meaning": "Anlaşmazlık, ihtilaf, zıtlaşma."
  },
  {
    "word": "işbirliği",
    "meaning": "Ortak çalışma, kooperasyon."
  },
  {
    "word": "deneyim",
    "meaning": "Tecrübe, bir işi yaparak elde edilen bilgi."
  },
  {
    "word": "düzey",
    "meaning": "Seviye, mertebe."
  },
  {
    "word": "etkileşim",
    "meaning": "Karşılıklı etki, interaksiyon."
  },
  {
    "word": "geçici",
    "meaning": "Kalıcı olmayan, fani."
  },
  {
    "word": "kalıcı",
    "meaning": "Sürekli, daimî, baki."
  },
  {
    "word": "küresel",
    "meaning": "Evrensel, dünya çapında, global."
  },
  {
    "word": "yerel",
    "meaning": "Mahalli, bölgesel, lokal."
  },
  {
    "word": "uygarlık",
    "meaning": "Medeniyet, kültürel gelişmişlik."
  },
  {
    "word": "medeniyet",
    "meaning": "Uygarlık, kültürel ve sosyal gelişmişlik düzeyi."
  },
  {
    "word": "eski",
    "meaning": "Kadim, köhne, yeni olmayan."
  },
  {
    "word": "yeni",
    "meaning": "Modern, taze, eskinin karşıtı."
  },
  {
    "word": "modern",
    "meaning": "Çağdaş, yeni, güncel."
  },
  {
    "word": "çağdaş",
    "meaning": "Modern, aynı çağda yaşayan."
  },
  {
    "word": "güncel",
    "meaning": "Aktüel, şimdiye ait, yeni."
  },
  {
    "word": "aktüel",
    "meaning": "Güncel, şimdiye ait."
  },
  {
    "word": "geçmiş",
    "meaning": "Mazi, geçmiş zaman."
  },
  {
    "word": "gelecek",
    "meaning": "İstikbal, ileriki zaman."
  },
  {
    "word": "istikbal",
    "meaning": "Gelecek, ileriki zaman."
  },
  {
    "word": "şimdi",
    "meaning": "Hemen, şu an, mevcut zaman."
  },
  {
    "word": "mevcut",
    "meaning": "Var olan, hazır bulunan."
  },
  {
    "word": "hazır",
    "meaning": "Amade, mevcut."
  },
  {
    "word": "imza",
    "meaning": "Onaylama işareti, bir yazının altına atılan el yazısı."
  },
  {
    "word": "onay",
    "meaning": "Tasdik, kabul etme."
  },
  {
    "word": "tasdik",
    "meaning": "Onaylama, doğrulama."
  },
  {
    "word": "reddetmek",
    "meaning": "Geri çevirme, kabul etmeme, inkâr etme."
  },
  {
    "word": "inkâr",
    "meaning": "Kabul etmeme, yalanlama."
  },
  {
    "word": "kabul",
    "meaning": "Onaylama, razı olma."
  },
  {
    "word": "razı",
    "meaning": "İzinli, hoşnut, kabul etmiş."
  },
  {
    "word": "hoşnut",
    "meaning": "Memnun, razı."
  },
  {
    "word": "memnun",
    "meaning": "Hoşnut, sevinçli."
  },
  {
    "word": "üzüntü",
    "meaning": "Keder, hüzün, dert."
  },
  {
    "word": "sevinç",
    "meaning": "Mutluluk, neşe, hoşnutluk."
  },
  {
    "word": "dert",
    "meaning": "Sorun, sıkıntı, keder."
  },
  {
    "word": "sıkıntı",
    "meaning": "Dert, problem, huzursuzluk."
  },
  {
    "word": "huzursuzluk",
    "meaning": "Rahatsızlık, gerginlik."
  },
  {
    "word": "rahatlık",
    "meaning": "Huzur, konfor, sıkıntısızlık."
  },
  {
    "word": "konfor",
    "meaning": "Rahatlık, lüks."
  },
  {
    "word": "lüks",
    "meaning": "Gösteriş, gereksiz pahalı şeyler."
  },
  {
    "word": "gösteriş",
    "meaning": "Şatafat, ihtişam, hava atma."
  },
  {
    "word": "tevazu",
    "meaning": "Alçak gönüllülük."
  },
  {
    "word": "kibir",
    "meaning": "Büyüklük taslama, gurur."
  },
  {
    "word": "gurur",
    "meaning": "Övünç, onur; kibir."
  },
  {
    "word": "onur",
    "meaning": "Şeref, haysiyet."
  },
  {
    "word": "haysiyet",
    "meaning": "İtibar, şeref, onur."
  },
  {
    "word": "saygı",
    "meaning": "Hürmet, itibar."
  },
  {
    "word": "hürmet",
    "meaning": "Saygı, itibar."
  },
  {
    "word": "itaat",
    "meaning": "Söz dinleme, boyun eğme."
  },
  {
    "word": "isyankâr",
    "meaning": "Baş kaldıran, karşı gelen, itaat etmeyen."
  },
  {
    "word": "sadık",
    "meaning": "Bağlı, vefalı, dürüst."
  },
  {
    "word": "vefasız",
    "meaning": "Sözünde durmayan, bağlı olmayan, nankör."
  },
  {
    "word": "nankör",
    "meaning": "Vefasız, iyilik bilmeyen."
  },
  {
    "word": "vefalı",
    "meaning": "Sözünde duran, bağlı, sadık."
  },
  {
    "word": "iyilik",
    "meaning": "Hayırlı iş, güzellik, lütuf."
  },
  {
    "word": "kötülük",
    "meaning": "Şer, fenalık, yaramazlık."
  },
  {
    "word": "hayırlı",
    "meaning": "Uğurlu, iyi, faydalı."
  },
  {
    "word": "şer",
    "meaning": "Kötülük, fena."
  },
  {
    "word": "faydalı",
    "meaning": "Yararlı, kârlı, menfaatli."
  },
  {
    "word": "yararsız",
    "meaning": "Faydasız, işe yaramaz."
  },
  {
    "word": "kâr",
    "meaning": "Kazanç, fayda, çıkar."
  },
  {
    "word": "zarar",
    "meaning": "Hasar, kayıp, ziyan."
  },
  {
    "word": "kazanç",
    "meaning": "Kâr, gelir, menfaat."
  },
  {
    "word": "kayıp",
    "meaning": "Zarar, yitik, yokluk."
  },
  {
    "word": "gelir",
    "meaning": "Kazanç, hasılat."
  },
  {
    "word": "gider",
    "meaning": "Masraf, harcama."
  },
  {
    "word": "masraf",
    "meaning": "Harcama, gider."
  },
  {
    "word": "tasarruf",
    "meaning": "Tutum, biriktirme, ekonomik kullanma."
  },
  {
    "word": "tutum",
    "meaning": "Davranış, tavır; tasarruf etme."
  },
  {
    "word": "savurgan",
    "meaning": "Müsrif, israf eden."
  },
  {
    "word": "israf",
    "meaning": "Gereksiz harcama, savurganlık."
  },
  {
    "word": "cömert",
    "meaning": "Eli açık, bonkör, lütufkâr."
  },
  {
    "word": "cimri",
    "meaning": "Pinti, eli sıkı, hasis."
  },
  {
    "word": "pinti",
    "meaning": "Cimri, hasis."
  },
  {
    "word": "hasis",
    "meaning": "Cimri, pinti."
  },
  {
    "word": "bonkör",
    "meaning": "Cömert, eli açık."
  },
  {
    "word": "eli açık",
    "meaning": "Cömert, bonkör."
  },
  {
    "word": "eli sıkı",
    "meaning": "Cimri, pinti."
  },
  {
    "word": "açgözlü",
    "meaning": "Tamahkâr, doyumsuz."
  },
  {
    "word": "doyumsuz",
    "meaning": "Açgözlü, tamahkâr."
  },
  {
    "word": "kanaatkâr",
    "meaning": "Gözü tok, elindekine yetinen."
  },
  {
    "word": "gözü tok",
    "meaning": "Kanaatkâr, açgözlü olmayan."
  },
  {
    "word": "tamahkâr",
    "meaning": "Açgözlü, doyumsuz."
  },
  {
    "word": "misafirperver",
    "meaning": "Konuksever, ağırlamayı seven."
  },
  {
    "word": "konuksever",
    "meaning": "Misafirperver."
  },
  {
    "word": "mülteci",
    "meaning": "Sığınmacı, iltica eden kişi."
  },
  {
    "word": "sığınmacı",
    "meaning": "Mülteci, sığınan kişi."
  },
  {
    "word": "iltica",
    "meaning": "Sığınma, başka bir ülkeye sığınma."
  },
  {
    "word": "vatan",
    "meaning": "Yurt, ana yurdu."
  },
  {
    "word": "yurt",
    "meaning": "Vatan, memleket."
  },
  {
    "word": "memleket",
    "meaning": "Ülke, vatan."
  },
  {
    "word": "ülke",
    "meaning": "Memleket, devlet."
  },
  {
    "word": "devlet",
    "meaning": "Siyasi örgütlenme, ulusal yönetim."
  },
  {
    "word": "hükümet",
    "meaning": "Devleti yöneten kurul, iktidar."
  },
  {
    "word": "iktidar",
    "meaning": "Yönetme gücü, siyasi güç."
  },
  {
    "word": "muhalefet",
    "meaning": "Karşıt görüşlü siyasi grup, iktidarın karşıtı."
  },
  {
    "word": "siyaset",
    "meaning": "Politika, devlet işlerini yönetme sanatı."
  },
  {
    "word": "politika",
    "meaning": "Siyaset, izlenen yol."
  },
  {
    "word": "yasa",
    "meaning": "Kanun, hukuk kuralı."
  },
  {
    "word": "kanun",
    "meaning": "Yasa, hukuk."
  },
  {
    "word": "hukuk",
    "meaning": "Yasaların bütünü, adalet."
  },
  {
    "word": "adalet",
    "meaning": "Hak ve hukuka uygunluk."
  },
  {
    "word": "eşitsizlik",
    "meaning": "Adaletsizlik, denksizlik."
  },
  {
    "word": "eşitlik",
    "meaning": "Denklik, adalet."
  },
  {
    "word": "denk",
    "meaning": "Eşit, müsavi."
  },
  {
    "word": "müsavi",
    "meaning": "Eşit, denk."
  },
  {
    "word": "ayrıcalık",
    "meaning": "İmtiyaz, özel hak."
  },
  {
    "word": "imtiyaz",
    "meaning": "Ayrıcalık, üstünlük."
  },
  {
    "word": "üstünlük",
    "meaning": "Ayrıcalık, galebe."
  },
  {
    "word": "galebe",
    "meaning": "Üstünlük, yenme, zafer."
  },
  {
    "word": "yenilgi",
    "meaning": "Mağlubiyet, hezimet."
  },
  {
    "word": "zafer",
    "meaning": "Galebe, başarı, üstünlük."
  },
  {
    "word": "başarı",
    "meaning": "Muvaffakiyet, zafer."
  },
  {
    "word": "muvaffakiyet",
    "meaning": "Başarı, zafer."
  },
  {
    "word": "mağlubiyet",
    "meaning": "Yenilgi, hezimet."
  },
  {
    "word": "hezimet",
    "meaning": "Büyük yenilgi, mağlubiyet."
  },
  {
    "word": "imgelem",
    "meaning": "Hayal gücü, tahayyül yeteneği."
  },
  {
    "word": "mücerret",
    "meaning": "Soyut, elle tutulmaz, zihinsel."
  },
  {
    "word": "müşahhas",
    "meaning": "Somut, elle tutulur, somutlaştırılmış."
  },
  {
    "word": "vuzuh",
    "meaning": "Açıklık, netlik, vazıh olma durumu."
  },
  {
    "word": "mübalağa",
    "meaning": "Abartma, bir şeyi olduğundan fazla veya az gösterme."
  },
  {
    "word": "itiraf",
    "meaning": "Suçu veya hatayı kabul etme, bildirme."
  },
  {
    "word": "hisse",
    "meaning": "Pay, kısım, bir şeye ortaklık."
  },
  {
    "word": "iştirak",
    "meaning": "Ortak olma, pay alma."
  },
  {
    "word": "tebliğ",
    "meaning": "Bildirme, resmi olarak duyurma."
  },
  {
    "word": "tasavvur",
    "meaning": "Zihinde canlandırma, hayal etme."
  },
  {
    "word": "tedarik",
    "meaning": "Sağlama, temin etme."
  },
  {
    "word": "teminat",
    "meaning": "Güvence, garanti."
  },
  {
    "word": "izhar",
    "meaning": "Açığa çıkarma, gösterme."
  },
  {
    "word": "mukavemet",
    "meaning": "Direnç, dayanıklılık."
  },
  {
    "word": "müstesna",
    "meaning": "Ayrıcalıklı, kural dışı."
  },
  {
    "word": "tevcih",
    "meaning": "Yöneltme, bir göreve atama."
  },
  {
    "word": "vazıh",
    "meaning": "Açık, net, belirgin."
  },
  {
    "word": "zamanın",
    "meaning": "Vaktin, sürenin."
  },
  {
    "word": "acizlik",
    "meaning": "Güçsüzlük, beceriksizlik."
  },
  {
    "word": "ihtimam",
    "meaning": "Özen, dikkat."
  },
  {
    "word": "kanaat",
    "meaning": "Görüş, düşünce; yetinme."
  },
  {
    "word": "kıymet",
    "meaning": "Değer, paha."
  },
  {
    "word": "lüzumsuz",
    "meaning": "Gereksiz, boş, faydasız."
  },
  {
    "word": "maharet",
    "meaning": "Beceri, ustalık."
  },
  {
    "word": "münakaşa",
    "meaning": "Tartışma, çekişme."
  },
  {
    "word": "mütemadiyen",
    "meaning": "Sürekli olarak, aralıksız."
  },
  {
    "word": "mütevazı",
    "meaning": "Alçak gönüllü, sade."
  },
  {
    "word": "nezaket",
    "meaning": "İncelik, kibarlık."
  },
  {
    "word": "noksan",
    "meaning": "Eksik, kusurlu."
  },
  {
    "word": "sükûnet",
    "meaning": "Huzur, dinginlik."
  },
  {
    "word": "takdir",
    "meaning": "Beğenme, değer verme; kader."
  },
  {
    "word": "telkin",
    "meaning": "Aşılama, inandırma."
  },
  {
    "word": "tereddüt",
    "meaning": "Kararsızlık, duraksama."
  },
  {
    "word": "teşvik",
    "meaning": "Cesaretlendirme."
  },
  {
    "word": "tevazu",
    "meaning": "Alçak gönüllülük."
  },
  {
    "word": "vazgeçmek",
    "meaning": "Caymak, feragât etmek."
  },
  {
    "word": "yegane",
    "meaning": "Tek, biricik."
  },
  {
    "word": "zekâ",
    "meaning": "Akıl, anlama yeteneği."
  },
  {
    "word": "zira",
    "meaning": "Çünkü, sebep olarak."
  },
  {
    "word": "zulüm",
    "meaning": "Haksızlık, eziyet."
  },
  {
    "word": "ihmal",
    "meaning": "Gereken dikkati göstermeme."
  },
  {
    "word": "ihtiras",
    "meaning": "Aşırı istek, tutku."
  },
  {
    "word": "irade",
    "meaning": "İsteme, karar verme gücü."
  },
  {
    "word": "itikad",
    "meaning": "İnanç, iman."
  },
  {
    "word": "kabiliyet",
    "meaning": "Yetenek, beceri, istidat."
  },
  {
    "word": "kader",
    "meaning": "Yazgı, alın yazısı, mukadderat."
  },
  {
    "word": "muhakkak",
    "meaning": "Kesin, şüphesiz, mutlaka."
  },
  {
    "word": "münasip",
    "meaning": "Uygun, yakışır, yerinde."
  },
  {
    "word": "müteakip",
    "meaning": "Sonraki, arkadan gelen."
  },
  {
    "word": "nüfuz",
    "meaning": "Sözü geçerlilik, etki."
  },
  {
    "word": "rıza",
    "meaning": "Razı olma, onay."
  },
  {
    "word": "sebat",
    "meaning": "Direniş, kararlılık."
  },
  {
    "word": "şefkat",
    "meaning": "Merhamet, acıma duygusu."
  },
  {
    "word": "tahayyül",
    "meaning": "Hayal etme, imgelem."
  },
  {
    "word": "teşebbüs",
    "meaning": "Girişim, bir işe başlama."
  },
  {
    "word": "tezyif",
    "meaning": "Küçümseme, alay etme."
  },
  {
    "word": "vakar",
    "meaning": "Ağırbaşlılık, ciddiyet."
  },
  {
    "word": "vukuat",
    "meaning": "Olaylar, hadiseler."
  },
  {
    "word": "zarafet",
    "meaning": "İncelik, şıklık."
  },
  {
    "word": "zihin",
    "meaning": "Akıl, düşünce gücü."
  },
  {
    "word": "ahenk",
    "meaning": "Uyum, armoni, düzen."
  },
  {
    "word": "armoni",
    "meaning": "Ahenk, uyum."
  },
  {
    "word": "akort",
    "meaning": "Seslerin uyumu, ahenk."
  },
  {
    "word": "kontrast",
    "meaning": "Zıtlık, karşıtlık, tezat."
  },
  {
    "word": "tezat",
    "meaning": "Zıtlık, karşıtlık."
  },
  {
    "word": "çelişki",
    "meaning": "Tutarsızlık, tezat."
  },
  {
    "word": "tutarlı",
    "meaning": "Çelişkisiz, mantıklı, düzenli."
  },
  {
    "word": "mantık",
    "meaning": "Akıl yürütme, düşünme sanatı."
  },
  {
    "word": "akıl",
    "meaning": "Us, düşünme yeteneği."
  },
  {
    "word": "sağduyu",
    "meaning": "Akıl, mantık, ortak duyu."
  },
  {
    "word": "bilgelik",
    "meaning": "İrfan, hikmet, derin bilgi."
  },
  {
    "word": "hikmet",
    "meaning": "Bilgelik, derin anlam."
  },
  {
    "word": "irfan",
    "meaning": "Bilgelik, kültür."
  },
  {
    "word": "kültür",
    "meaning": "Toplumsal değerler bütünü."
  },
  {
    "word": "tarih",
    "meaning": "Geçmiş zaman, zaman bilimi."
  },
  {
    "word": "coğrafya",
    "meaning": "Yer bilimi, dünya yüzeyini inceleyen bilim."
  },
  {
    "word": "ekonomi",
    "meaning": "İktisat, üretim, tüketim, dağıtım bilimi."
  },
  {
    "word": "iktisat",
    "meaning": "Ekonomi, tutumluluk."
  },
  {
    "word": "sosyoloji",
    "meaning": "Toplum bilimi."
  },
  {
    "word": "psikoloji",
    "meaning": "Ruh bilimi, davranışları inceleyen bilim."
  },
  {
    "word": "felsefe",
    "meaning": "Bilgelik sevgisi, düşünce bilimi."
  },
  {
    "word": "bilim",
    "meaning": "İlim, sistematik bilgi."
  },
  {
    "word": "ilim",
    "meaning": "Bilim, bilgi."
  },
  {
    "word": "sanat",
    "meaning": "Yaratıcılık, estetik ifade."
  },
  {
    "word": "estetik",
    "meaning": "Güzellik, sanat felsefesi."
  },
  {
    "word": "güzellik",
    "meaning": "Estetik, hoş görünüş."
  },
  {
    "word": "çirkinlik",
    "meaning": "Kötü görünüş, estetikten uzaklık."
  },
  {
    "word": "iyi",
    "meaning": "Hayırlı, güzel, faydalı."
  },
  {
    "word": "kötü",
    "meaning": "Şer, fena, zararlı."
  },
  {
    "word": "yüksek",
    "meaning": "Ulu, yüce, yüksek seviyede."
  },
  {
    "word": "alçak",
    "meaning": "Düşük, aşağı seviyede; ahlaksız."
  },
  {
    "word": "ulvi",
    "meaning": "Yüce, yüksek, kutsal."
  },
  {
    "word": "süfli",
    "meaning": "Aşağılık, bayağı, adi."
  },
  {
    "word": "kutsal",
    "meaning": "Mukaddes, dokunulmaz."
  },
  {
    "word": "mukaddes",
    "meaning": "Kutsal, saygıdeğer."
  },
  {
    "word": "dindar",
    "meaning": "Dinî inançlara bağlı, sofu."
  },
  {
    "word": "laik",
    "meaning": "Din ve devlet işlerinin ayrı olması ilkesine bağlı."
  },
  {
    "word": "seküler",
    "meaning": "Dünyevi, din dışı, laik."
  },
  {
    "word": "dünyevi",
    "meaning": "Seküler, dünyaya ait."
  },
  {
    "word": "uhrevi",
    "meaning": "Ahirete ait, öteki dünyayla ilgili."
  },
  {
    "word": "maddi",
    "meaning": "Maddesel, fiziki, parasal."
  },
  {
    "word": "manevi",
    "meaning": "Ruhsal, soyut, duygusal."
  },
  {
    "word": "fiziki",
    "meaning": "Maddi, bedensel."
  },
  {
    "word": "bedensel",
    "meaning": "Fiziki, vücutla ilgili."
  },
  {
    "word": "ruhsal",
    "meaning": "Manevi, psikolojik."
  },
  {
    "word": "psikolojik",
    "meaning": "Ruhsal, zihinsel."
  },
  {
    "word": "zihinsel",
    "meaning": "Düşünsel, mental."
  },
  {
    "word": "düşünsel",
    "meaning": "Zihinsel, fikirle ilgili."
  },
  {
    "word": "soyut",
    "meaning": "Mücerret, zihinde var olan."
  },
  {
    "word": "somut",
    "meaning": "Müşahhas, elle tutulur."
  },
  {
    "word": "mücerret",
    "meaning": "Soyut."
  },
  {
    "word": "müşahhas",
    "meaning": "Somut."
  },
  {
    "word": "gerekli",
    "meaning": "Lüzumlu, zorunlu."
  },
  {
    "word": "lüzumlu",
    "meaning": "Gerekli, lazım."
  },
  {
    "word": "zorunlu",
    "meaning": "Mecburi, gerekli."
  },
  {
    "word": "mecburi",
    "meaning": "Zorunlu, şart."
  },
  {
    "word": "ihtiyaç",
    "meaning": "Gereksinim, lüzum."
  },
  {
    "word": "gereksinim",
    "meaning": "İhtiyaç, lüzum."
  },
  {
    "word": "olabilir",
    "meaning": "Muhtemel, ihtimal dahilinde."
  },
  {
    "word": "imkansız",
    "meaning": "Olanaksız, mümkün değil."
  },
  {
    "word": "mümkün",
    "meaning": "Olası, yapılabilir."
  },
  {
    "word": "mümkün değil",
    "meaning": "İmkansız."
  },
  {
    "word": "olanaklı",
    "meaning": "Mümkün, imkanlı."
  },
  {
    "word": "olası",
    "meaning": "Muhtemel, ihtimal dahilinde."
  },
  {
    "word": "kesin",
    "meaning": "Mutlak, kati, şüphesiz."
  },
  {
    "word": "kati",
    "meaning": "Kesin, mutlak."
  },
  {
    "word": "şüpheli",
    "meaning": "Kuşkulu, belirsiz."
  },
  {
    "word": "belirsiz",
    "meaning": "Muğlak, şüpheli."
  },
  {
    "word": "muğlak",
    "meaning": "Belirsiz, anlaşılması güç."
  },
  {
    "word": "açık",
    "meaning": "Vazıh, net, belirgin."
  },
  {
    "word": "net",
    "meaning": "Açık, anlaşılır."
  },
  {
    "word": "kapalılık",
    "meaning": "Muğlaklık, belirsizlik."
  },
  {
    "word": "vazıh",
    "meaning": "Açık, net."
  },
  {
    "word": "müphemlik",
    "meaning": "Belirsizlik, kapalılık."
  },
  {
    "word": "yalın",
    "meaning": "Basit, sade, gösterişsiz."
  },
  {
    "word": "sade",
    "meaning": "Yalın, basit."
  },
  {
    "word": "karmaşık",
    "meaning": "Komplike, karışık, girift."
  },
  {
    "word": "girift",
    "meaning": "Karmaşık, iç içe."
  },
  {
    "word": "basit",
    "meaning": "Yalın, kolay, karmaşık olmayan."
  },
  {
    "word": "kolay",
    "meaning": "Basit, güç olmayan."
  },
  {
    "word": "zor",
    "meaning": "Güç, meşakkatli, kolay olmayan."
  },
  {
    "word": "güç",
    "meaning": "Zor, kuvvet."
  },
  {
    "word": "kuvvet",
    "meaning": "Güç, enerji, takat."
  },
  {
    "word": "enerji",
    "meaning": "Güç, takat."
  },
  {
    "word": "takat",
    "meaning": "Güç, kuvvet, derman."
  },
  {
    "word": "derman",
    "meaning": "Güç, kuvvet, çare."
  },
  {
    "word": "çare",
    "meaning": "Derman, çözüm."
  },
  {
    "word": "çözüm",
    "meaning": "Hal, çare, bir sorunun giderilmesi."
  },
  {
    "word": "sorun",
    "meaning": "Problem, mesele, dert."
  },
  {
    "word": "mesele",
    "meaning": "Sorun, konu."
  },
  {
    "word": "konu",
    "meaning": "Mevzu, mesele, bahis."
  },
  {
    "word": "mevzu",
    "meaning": "Konu, bahis."
  },
  {
    "word": "bahis",
    "meaning": "Konu, mesele."
  },
  {
    "word": "durum",
    "meaning": "Vaziyet, hal, pozisyon."
  },
  {
    "word": "vaziyet",
    "meaning": "Durum, hal."
  },
  {
    "word": "hal",
    "meaning": "Durum, vaziyet."
  },
  {
    "word": "pozisyon",
    "meaning": "Durum, konum."
  },
  {
    "word": "konum",
    "meaning": "Pozisyon, yer."
  },
  {
    "word": "yer",
    "meaning": "Mekân, mahal."
  },
  {
    "word": "mekân",
    "meaning": "Yer, mahal."
  },
  {
    "word": "mahal",
    "meaning": "Yer, mekân."
  },
  {
    "word": "semt",
    "meaning": "Mahalle, bölge."
  },
  {
    "word": "bölge",
    "meaning": "Semt, mıntıka."
  },
  {
    "word": "mıntıka",
    "meaning": "Bölge, semt."
  },
  {
    "word": "aralık",
    "meaning": "Boşluk, fasıla, mesafe."
  },
  {
    "word": "boşluk",
    "meaning": "Hala, aralık, açıklık."
  },
  {
    "word": "dolu",
    "meaning": "Boş olmayan, tamamlanmış."
  },
  {
    "word": "tamam",
    "meaning": "Bütün, bitmiş, eksiksiz."
  },
  {
    "word": "bütün",
    "meaning": "Tamam, yekpare."
  },
  {
    "word": "parça",
    "meaning": "Kısım, cüz, bütünün bir bölümü."
  },
  {
    "word": "kısım",
    "meaning": "Parça, bölüm."
  },
  {
    "word": "bölüm",
    "meaning": "Kısım, parça."
  },
  {
    "word": "cüz",
    "meaning": "Parça, kısım."
  },
  {
    "word": "yekpare",
    "meaning": "Tek parça, bütün."
  },
  {
    "word": "eksik",
    "meaning": "Noksan, tamamlanmamış."
  },
  {
    "word": "noksan",
    "meaning": "Eksik."
  },
  {
    "word": "kusurlu",
    "meaning": "Noksanlı, hatalı."
  },
  {
    "word": "kusursuz",
    "meaning": "Mükemmel, hatasız."
  },
  {
    "word": "hata",
    "meaning": "Yanlış, kusur."
  },
  {
    "word": "yanlış",
    "meaning": "Hata, doğru olmayan."
  },
  {
    "word": "doğru",
    "meaning": "Hatasız, gerçek, dürüst."
  },
  {
    "word": "dürüst",
    "meaning": "Doğru sözlü, hilesiz."
  },
  {
    "word": "hile",
    "meaning": "Aldatma, oyun, düzen."
  },
  {
    "word": "aldatma",
    "meaning": "Hile, dolandırma."
  },
  {
    "word": "dürüstlük",
    "meaning": "Doğruluk, hilesizlik."
  },
  {
    "word": "gerçek",
    "meaning": "Hakikat, doğru, yalan olmayan."
  },
  {
    "word": "hakikat",
    "meaning": "Gerçek, doğru."
  },
  {
    "word": "yalan",
    "meaning": "Yanlış, gerçek olmayan söz."
  },
  {
    "word": "sahici",
    "meaning": "Gerçek, hakiki, orijinal."
  },
  {
    "word": "sahte",
    "meaning": "Taklit, yalan, gerçek olmayan."
  },
  {
    "word": "taklit",
    "meaning": "Kopya, sahte."
  },
  {
    "word": "kopya",
    "meaning": "Taklit, suret."
  },
  {
    "word": "suret",
    "meaning": "Kopya, biçim."
  },
  {
    "word": "biçim",
    "meaning": "Şekil, form."
  },
  {
    "word": "şekil",
    "meaning": "Biçim, form."
  },
  {
    "word": "form",
    "meaning": "Şekil, biçim."
  },
  {
    "word": "öz",
    "meaning": "Esas, çekirdek, asıl."
  },
  {
    "word": "esas",
    "meaning": "Öz, temel, asıl."
  },
  {
    "word": "asıl",
    "meaning": "Temel, esas, orijinal."
  },
  {
    "word": "temel",
    "meaning": "Esas, kök, dayanak."
  },
  {
    "word": "kök",
    "meaning": "Temel, esas; bir kelimenin en küçük anlamlı parçası."
  },
  {
    "word": "dayanak",
    "meaning": "Temel, destek."
  },
  {
    "word": "destek",
    "meaning": "Yardım, dayanak."
  },
  {
    "word": "yardım",
    "meaning": "Destek, muavenet."
  },
  {
    "word": "muavenet",
    "meaning": "Yardım, destek."
  },
  {
    "word": "engel",
    "meaning": "Mani, zorluk, kısıtlama."
  },
  {
    "word": "mani",
    "meaning": "Engel, kısıtlama."
  },
  {
    "word": "kısıtlama",
    "meaning": "Sınırlama, engel."
  },
  {
    "word": "sınırlama",
    "meaning": "Kısıtlama."
  },
  {
    "word": "geniş",
    "meaning": "Büyük, yaygın, dar olmayan."
  },
  {
    "word": "dar",
    "meaning": "Geniş olmayan, kısıtlı."
  },
  {
    "word": "büyük",
    "meaning": "Geniş, yüce, ulu."
  },
  {
    "word": "küçük",
    "meaning": "Ufak, minik, büyük olmayan."
  },
  {
    "word": "ufak",
    "meaning": "Küçük, minik."
  },
  {
    "word": "minik",
    "meaning": "Ufak, küçük."
  },
  {
    "word": "yüce",
    "meaning": "Ulu, yüksek."
  },
  {
    "word": "ulu",
    "meaning": "Yüce, büyük."
  },
  {
    "word": "üstün",
    "meaning": "Galebe, yüksek, yüce."
  },
  {
    "word": "aşağı",
    "meaning": "Alçak, düşük."
  },
  {
    "word": "yüksek",
    "meaning": "Üstün, yüce."
  },
  {
    "word": "düşük",
    "meaning": "Alçak, az."
  },
  {
    "word": "az",
    "meaning": "Düşük, cüzi, çok olmayan."
  },
  {
    "word": "çok",
    "meaning": "Fazla, gani, bol."
  },
  {
    "word": "fazla",
    "meaning": "Çok, aşırı."
  },
  {
    "word": "aşırı",
    "meaning": "Fazla, haddinden çok."
  },
  {
    "word": "haddinden",
    "meaning": "Limitinden, sınırından."
  },
  {
    "word": "sınır",
    "meaning": "Limit, had."
  },
  {
    "word": "limit",
    "meaning": "Sınır, had."
  },
  {
    "word": "had",
    "meaning": "Sınır, limit."
  },
  {
    "word": "bol",
    "meaning": "Çok, gani, fazla."
  },
  {
    "word": "gani",
    "meaning": "Bol, çok."
  },
  {
    "word": "cüzi",
    "meaning": "Az, küçük, önemsiz."
  },
  {
    "word": "önemli",
    "meaning": "Ehemmiyetli, değerli."
  },
  {
    "word": "önemsiz",
    "meaning": "Değersiz, cüzi."
  },
  {
    "word": "değerli",
    "meaning": "Kıymetli, önemli."
  },
  {
    "word": "kıymetli",
    "meaning": "Değerli, önemli."
  },
  {
    "word": "değersiz",
    "meaning": "Kıymetsiz, önemsiz."
  },
  {
    "word": "kıymetsiz",
    "meaning": "Değersiz, önemsiz."
  },
  {
    "word": "uzun",
    "meaning": "Geniş, kısa olmayan."
  },
  {
    "word": "kısa",
    "meaning": "Uzun olmayan, kısa süreli."
  },
  {
    "word": "süreli",
    "meaning": "Vakitli, zamanla sınırlı."
  },
  {
    "word": "süresiz",
    "meaning": "Zamansız, kalıcı."
  },
  {
    "word": "zamanlı",
    "meaning": "Vakitli, süreli."
  },
  {
    "word": "zamansız",
    "meaning": "Vakitsiz, süresiz."
  },
  {
    "word": "baki",
    "meaning": "Kalıcı, sonsuz, ebedi."
  },
  {
    "word": "fani",
    "meaning": "Geçici, ölümlü."
  },
  {
    "word": "ebedi",
    "meaning": "Sonsuz, baki."
  },
  {
    "word": "sonsuz",
    "meaning": "Ebedi, bitmeyen."
  },
  {
    "word": "biten",
    "meaning": "Son bulan, nihayete eren."
  },
  {
    "word": "başlayan",
    "meaning": "İptida eden, start alan."
  },
  {
    "word": "nihayet",
    "meaning": "Sonuç, son, bitiş."
  },
  {
    "word": "iptida",
    "meaning": "Başlangıç, ilk."
  },
  {
    "word": "sonuç",
    "meaning": "Nihayet, netice, akıbet."
  },
  {
    "word": "netice",
    "meaning": "Sonuç, akıbet."
  },
  {
    "word": "akıbet",
    "meaning": "Sonuç, netice."
  },
  {
    "word": "başlangıç",
    "meaning": "İptida, ilk nokta."
  },
  {
    "word": "ilk",
    "meaning": "Birinci, başlangıçtaki."
  },
  {
    "word": "son",
    "meaning": "Nihayet, bitiş."
  },
  {
    "word": "birinci",
    "meaning": "İlk, başlangıçtaki."
  },
  {
    "word": "tekrar",
    "meaning": "Yineleme, kez."
  },
  {
    "word": "yineleme",
    "meaning": "Tekrar, tekrarlama."
  },
  {
    "word": "devam",
    "meaning": "Sürdürme, devam etme."
  },
  {
    "word": "sürdürme",
    "meaning": "Devam ettirme."
  },
  {
    "word": "ara",
    "meaning": "Fasıla, mola, aralık."
  },
  {
    "word": "fasıla",
    "meaning": "Ara, mola."
  },
  {
    "word": "mola",
    "meaning": "Fasıla, ara."
  },
  {
    "word": "kesintisiz",
    "meaning": "Aralıksız, sürekli."
  },
  {
    "word": "sürekli",
    "meaning": "Daimi, kesintisiz."
  },
  {
    "word": "daimi",
    "meaning": "Sürekli, kalıcı."
  },
  {
    "word": "kesintili",
    "meaning": "Aralıklı, sürekli olmayan."
  },
  {
    "word": "aralıklı",
    "meaning": "Kesintili, fasılalı."
  },
  {
    "word": "geçici",
    "meaning": "Fani, kalıcı olmayan."
  },
  {
    "word": "geçmiş",
    "meaning": "Mazi, eski zaman."
  },
  {
    "word": "mazi",
    "meaning": "Geçmiş zaman."
  },
  {
    "word": "gelecek",
    "meaning": "İstikbal, sonraki zaman."
  },
  {
    "word": "şimdi",
    "meaning": "Mevcut, şu an."
  },
  {
    "word": "mevcut",
    "meaning": "Şimdiki, var olan."
  },
  {
    "word": "var",
    "meaning": "Mevcut, mevcut olan."
  },
  {
    "word": "yok",
    "meaning": "Mevcut olmayan, fani."
  },
  {
    "word": "varlık",
    "meaning": "Mevcudiyet, zenginlik."
  },
  {
    "word": "yokluk",
    "meaning": "Adem, mevcudiyet olmaması."
  },
  {
    "word": "mevcudiyet",
    "meaning": "Varlık, var olma durumu."
  },
  {
    "word": "adem",
    "meaning": "Yokluk."
  },
  {
    "word": "zenginlik",
    "meaning": "Varlık, bolluk."
  },
  {
    "word": "fakirlik",
    "meaning": "Yoksulluk, fukara olma durumu."
  },
  {
    "word": "yoksulluk",
    "meaning": "Fakirlik."
  },
  {
    "word": "fukara",
    "meaning": "Yoksul, fakir."
  },
  {
    "word": "fakir",
    "meaning": "Fukara, yoksul."
  },
  {
    "word": "zengin",
    "meaning": "Varlıklı, gani."
  },
  {
    "word": "varlıklı",
    "meaning": "Zengin."
  },
  {
    "word": "maddi",
    "meaning": "Parasal, fiziksel."
  },
  {
    "word": "parasal",
    "meaning": "Maddi, nakdi."
  },
  {
    "word": "nakdi",
    "meaning": "Parasal."
  },
  {
    "word": "manevi",
    "meaning": "Ruhsal, soyut."
  },
  {
    "word": "ruhsal",
    "meaning": "Manevi."
  },
  {
    "word": "fiziksel",
    "meaning": "Maddi, bedensel."
  },
  {
    "word": "bedensel",
    "meaning": "Fiziksel."
  },
  {
    "word": "hayat",
    "meaning": "Yaşam, ömür."
  },
  {
    "word": "yaşam",
    "meaning": "Hayat, ömür."
  },
  {
    "word": "ömür",
    "meaning": "Yaşam, hayat süresi."
  },
  {
    "word": "ölüm",
    "meaning": "Vefat, ecel."
  },
  {
    "word": "vefat",
    "meaning": "Ölüm, ecel."
  },
  {
    "word": "ecel",
    "meaning": "Ölüm zamanı, vefat."
  },
  {
    "word": "doğum",
    "meaning": "Veladet, dünyaya gelme."
  },
  {
    "word": "veladet",
    "meaning": "Doğum."
  },
  {
    "word": "giriş",
    "meaning": "Duhul, başlama noktası."
  },
  {
    "word": "çıkış",
    "meaning": "Huruç, bitiş noktası."
  },
  {
    "word": "duhul",
    "meaning": "Giriş."
  },
  {
    "word": "huruç",
    "meaning": "Çıkış."
  },
  {
    "word": "başlamak",
    "meaning": "İptida etmek, giriş yapmak."
  },
  {
    "word": "bitirmek",
    "meaning": "Nihayetlendirmek, sonlandırmak."
  },
  {
    "word": "nihayetlendirmek",
    "meaning": "Bitirmek."
  },
  {
    "word": "sonlandırmak",
    "meaning": "Bitirmek."
  },
  {
    "word": "iptida etmek",
    "meaning": "Başlamak."
  },
  {
    "word": "ilk adım",
    "meaning": "Başlangıç, başlangıç aşaması."
  },
  {
    "word": "son aşama",
    "meaning": "Bitiş, final."
  },
  {
    "word": "final",
    "meaning": "Son, bitiş."
  },
  {
    "word": "aşamalı",
    "meaning": "Merhaleli, evreli."
  },
  {
    "word": "merhaleli",
    "meaning": "Aşamalı."
  },
  {
    "word": "evreli",
    "meaning": "Aşamalı."
  },
  {
    "word": "aniden",
    "meaning": "Birdenbire, apansızın, ansızın."
  },
  {
    "word": "apansızın",
    "meaning": "Aniden, ansızın."
  },
  {
    "word": "yavaşça",
    "meaning": "Aheste, ağır ağır."
  },
  {
    "word": "aheste",
    "meaning": "Yavaşça."
  },
  {
    "word": "hızlı",
    "meaning": "Süratli, çabuk."
  },
  {
    "word": "süratli",
    "meaning": "Hızlı, çabuk."
  },
  {
    "word": "yavaş",
    "meaning": "Ağır, süratli olmayan."
  },
  {
    "word": "ağır",
    "meaning": "Yavaş, hafif olmayan."
  },
  {
    "word": "hafif",
    "meaning": "Ağır olmayan, kolay."
  },
  {
    "word": "kolaylık",
    "meaning": "Asanlık, rahatlık."
  },
  {
    "word": "zorluk",
    "meaning": "Güçlük, meşakkat."
  },
  {
    "word": "meşakkat",
    "meaning": "Zorluk, güçlük."
  },
  {
    "word": "asanlık",
    "meaning": "Kolaylık."
  },
  {
    "word": "güçlük",
    "meaning": "Zorluk."
  },
  {
    "word": "rahat",
    "meaning": "Huzurlu, kolay, konforlu."
  },
  {
    "word": "sıkıntılı",
    "meaning": "Huzursuz, zorlu."
  },
  {
    "word": "huzurlu",
    "meaning": "Rahat, dingin."
  },
  {
    "word": "dingin",
    "meaning": "Huzurlu, sakin."
  },
  {
    "word": "sakin",
    "meaning": "Dingin, sessiz."
  },
  {
    "word": "sessiz",
    "meaning": "Sakin, gürültüsüz."
  },
  {
    "word": "gürültülü",
    "meaning": "Sesli, patırtılı."
  },
  {
    "word": "sesli",
    "meaning": "Gürültülü, yüksek sesli."
  },
  {
    "word": "yüksek",
    "meaning": "Sesli, ulu, yüce."
  },
  {
    "word": "alçak",
    "meaning": "Düşük sesli, ahlaksız."
  },
  {
    "word": "ulu",
    "meaning": "Yüce, yüksek."
  },
  {
    "word": "yüce",
    "meaning": "Ulu, yüksek."
  },
  {
    "word": "ahlaklı",
    "meaning": "Erdemli, namuslu."
  },
  {
    "word": "ahlaksız",
    "meaning": "Alçak, namussuz."
  },
  {
    "word": "erdemli",
    "meaning": "Ahlaklı."
  },
  {
    "word": "namuslu",
    "meaning": "Ahlaklı, şerefli."
  },
  {
    "word": "namussuz",
    "meaning": "Ahlaksız."
  },
  {
    "word": "şerefli",
    "meaning": "Onurlu, namuslu."
  },
  {
    "word": "onurlu",
    "meaning": "Şerefli."
  },
  {
    "word": "haysiyetli",
    "meaning": "Onurlu, şerefli."
  },
  {
    "word": "haysiyetsiz",
    "meaning": "Onursuz, şerefsiz."
  },
  {
    "word": "itibarlı",
    "meaning": "Saygın, muteber."
  },
  {
    "word": "saygın",
    "meaning": "İtibarlı."
  },
  {
    "word": "muteber",
    "meaning": "Saygın."
  },
  {
    "word": "itibarsız",
    "meaning": "Saygın olmayan."
  },
  {
    "word": "değerli",
    "meaning": "Kıymetli."
  },
  {
    "word": "değersiz",
    "meaning": "Kıymetsiz."
  },
  {
    "word": "haklı",
    "meaning": "Hakkı olan, doğru olan."
  },
  {
    "word": "haksız",
    "meaning": "Hakkı olmayan, yanlış olan."
  },
  {
    "word": "doğruluk",
    "meaning": "Haklılık, dürüstlük."
  },
  {
    "word": "yanlışlık",
    "meaning": "Haksızlık, hata."
  },
  {
    "word": "adalet",
    "meaning": "Hukuk, doğruluk."
  },
  {
    "word": "zulüm",
    "meaning": "Haksızlık, eziyet."
  },
  {
    "word": "eziyet",
    "meaning": "Zulüm, cefa."
  },
  {
    "word": "cefa",
    "meaning": "Eziyet, sıkıntı."
  },
  {
    "word": "rahatlık",
    "meaning": "Huzur, konfor."
  },
  {
    "word": "huzur",
    "meaning": "Rahatlık, sükûnet."
  },
  {
    "word": "sükûnet",
    "meaning": "Huzur, dinginlik."
  },
  {
    "word": "dinginlik",
    "meaning": "Sükûnet."
  },
  {
    "word": "hareket",
    "meaning": "Eylem, devinim."
  },
  {
    "word": "eylem",
    "meaning": "Hareket, fiil."
  },
  {
    "word": "fiil",
    "meaning": "Eylem, hareket."
  },
  {
    "word": "devinim",
    "meaning": "Hareket."
  },
  {
    "word": "durgunluk",
    "meaning": "Hareketsizlik, dinginlik."
  },
  {
    "word": "hareketsizlik",
    "meaning": "Durgunluk."
  },
  {
    "word": "aktif",
    "meaning": "Etkin, hareketli."
  },
  {
    "word": "etkin",
    "meaning": "Aktif."
  },
  {
    "word": "pasif",
    "meaning": "Edilgen, hareketsiz."
  },
  {
    "word": "edilgen",
    "meaning": "Pasif."
  },
  {
    "word": "dinamik",
    "meaning": "Hareketli, aktif."
  },
  {
    "word": "statik",
    "meaning": "Durgun, hareketsiz."
  },
  {
    "word": "durgun",
    "meaning": "Statik."
  },
  {
    "word": "hata",
    "meaning": "Yanlış, kusur."
  },
  {
    "word": "yanlış",
    "meaning": "Hata."
  },
  {
    "word": "doğru",
    "meaning": "Hatasız."
  },
  {
    "word": "kusur",
    "meaning": "Hata."
  },
  {
    "word": "kusursuz",
    "meaning": "Mükemmel."
  },
  {
    "word": "mükemmel",
    "meaning": "Kusursuz."
  },
  {
    "word": "eksik",
    "meaning": "Noksan."
  },
  {
    "word": "noksan",
    "meaning": "Eksik."
  },
  {
    "word": "tam",
    "meaning": "Eksiksiz."
  },
  {
    "word": "eksiksiz",
    "meaning": "Tam."
  },
  {
    "word": "bütün",
    "meaning": "Tam, yekpare."
  },
  {
    "word": "parça",
    "meaning": "Kısım, cüz."
  },
  {
    "word": "kısım",
    "meaning": "Parça."
  },
  {
    "word": "tek",
    "meaning": "Yegane, biricik."
  },
  {
    "word": "yegane",
    "meaning": "Tek."
  },
  {
    "word": "biricik",
    "meaning": "Tek."
  },
  {
    "word": "çoğul",
    "meaning": "Birden çok, müteaddit."
  },
  {
    "word": "müteaddit",
    "meaning": "Çoğul."
  },
  {
    "word": "kalabalık",
    "meaning": "Yoğun, izdihamlı."
  },
  {
    "word": "izdiham",
    "meaning": "Kalabalık."
  },
  {
    "word": "boş",
    "meaning": "Müteaddit olmayan, dolu olmayan."
  },
  {
    "word": "dolu",
    "meaning": "Boş olmayan."
  },
  {
    "word": "yoğun",
    "meaning": "Kalabalık, sık."
  },
  {
    "word": "seyrek",
    "meaning": "Sık olmayan, az."
  },
  {
    "word": "sık",
    "meaning": "Yoğun, seyrek olmayan."
  },
  {
    "word": "ince",
    "meaning": "Zarif, kalın olmayan."
  },
  {
    "word": "kalın",
    "meaning": "İnce olmayan, kaba."
  },
  {
    "word": "zarif",
    "meaning": "İnce, kibar."
  },
  {
    "word": "kaba",
    "meaning": "Kalın, görgüsüz."
  },
  {
    "word": "kibar",
    "meaning": "Zarif, nazik."
  },
  {
    "word": "nazik",
    "meaning": "Kibar, ince."
  },
  {
    "word": "görgülü",
    "meaning": "Kibar, terbiyeli."
  },
  {
    "word": "görgüsüz",
    "meaning": "Kaba, terbiyesiz."
  },
  {
    "word": "terbiyeli",
    "meaning": "Görgülü."
  },
  {
    "word": "terbiyesiz",
    "meaning": "Görgüsüz."
  },
  {
    "word": "bilgili",
    "meaning": "Âlim, malumatlı."
  },
  {
    "word": "cahil",
    "meaning": "Bilgisiz, okumamış."
  },
  {
    "word": "âlim",
    "meaning": "Bilgili."
  },
  {
    "word": "malumatlı",
    "meaning": "Bilgili."
  },
  {
    "word": "bilgisiz",
    "meaning": "Cahil."
  },
  {
    "word": "okumuş",
    "meaning": "Bilgili, tahsilli."
  },
  {
    "word": "tahsilli",
    "meaning": "Okumuş."
  },
  {
    "word": "okumamış",
    "meaning": "Cahil."
  },
  {
    "word": "eğitimli",
    "meaning": "Tahsilli, bilgili."
  },
  {
    "word": "eğitimsiz",
    "meaning": "Cahil, okumamış."
  },
  {
    "word": "öğrenim",
    "meaning": "Eğitim."
  },
  {
    "word": "eğitim",
    "meaning": "Öğrenim."
  },
  {
    "word": "öğrenci",
    "meaning": "Talebe, talebat."
  },
  {
    "word": "talebe",
    "meaning": "Öğrenci."
  },
  {
    "word": "öğretmen",
    "meaning": "Muallim, hoca."
  },
  {
    "word": "muallim",
    "meaning": "Öğretmen."
  },
  {
    "word": "hoca",
    "meaning": "Öğretmen."
  },
  {
    "word": "okul",
    "meaning": "Mektep."
  },
  {
    "word": "mektep",
    "meaning": "Okul."
  },
  {
    "word": "ders",
    "meaning": "Teneffüs, öğrenim konusu."
  },
  {
    "word": "teneffüs",
    "meaning": "Mola, ara."
  },
  {
    "word": "sınav",
    "meaning": "İmtihan."
  },
  {
    "word": "imtihan",
    "meaning": "Sınav."
  },
  {
    "word": "başarı",
    "meaning": "Muvaffakiyet."
  },
  {
    "word": "başarısızlık",
    "meaning": "Hüsran."
  },
  {
    "word": "hüsran",
    "meaning": "Başarısızlık."
  },
  {
    "word": "zafer",
    "meaning": "Galebe."
  },
  {
    "word": "yenilgi",
    "meaning": "Mağlubiyet."
  },
  {
    "word": "muvaffakiyet",
    "meaning": "Başarı."
  },
  {
    "word": "mağlubiyet",
    "meaning": "Yenilgi."
  },
  {
    "word": "ödül",
    "meaning": "Mükafat."
  },
  {
    "word": "ceza",
    "meaning": "Müeyyide."
  },
  {
    "word": "mükafat",
    "meaning": "Ödül."
  },
  {
    "word": "müeyyide",
    "meaning": "Ceza."
  },
  {
    "word": "motivasyon",
    "meaning": "Güdülenme."
  },
  {
    "word": "güdülenme",
    "meaning": "Motivasyon."
  },
  {
    "word": "istek",
    "meaning": "Arzu."
  },
  {
    "word": "arzu",
    "meaning": "İstek."
  },
  {
    "word": "şevk",
    "meaning": "Coşku."
  },
  {
    "word": "coşku",
    "meaning": "Şevk."
  },
  {
    "word": "azim",
    "meaning": "Kararlılık."
  },
  {
    "word": "kararlılık",
    "meaning": "Azim."
  },
  {
    "word": "tereddüt",
    "meaning": "Kararsızlık."
  },
  {
    "word": "kararsızlık",
    "meaning": "Tereddüt."
  },
  {
    "word": "sebat",
    "meaning": "Direniş."
  },
  {
    "word": "direniş",
    "meaning": "Sebat."
  },
  {
    "word": "taviz",
    "meaning": "Ödün."
  },
  {
    "word": "ödün",
    "meaning": "Taviz."
  },
  {
    "word": "fedakârlık",
    "meaning": "Özveri."
  },
  {
    "word": "özveri",
    "meaning": "Fedakârlık."
  },
  {
    "word": "şefkat",
    "meaning": "Merhamet."
  },
  {
    "word": "merhamet",
    "meaning": "Şefkat."
  },
  {
    "word": "acımak",
    "meaning": "Merhamet etmek."
  },
  {
    "word": "acımasız",
    "meaning": "Merhametsiz."
  },
  {
    "word": "merhametsiz",
    "meaning": "Acımasız."
  },
  {
    "word": "sevimli",
    "meaning": "Şirin, tatlı."
  },
  {
    "word": "şirin",
    "meaning": "Sevimli."
  },
  {
    "word": "sevimsiz",
    "meaning": "İtici, antipatik."
  },
  {
    "word": "itici",
    "meaning": "Sevimsiz."
  },
  {
    "word": "hoş",
    "meaning": "Güzel, tatlı."
  },
  {
    "word": "nahoş",
    "meaning": "Hoş olmayan, kötü."
  },
  {
    "word": "güzel",
    "meaning": "Hoş, iyi."
  },
  {
    "word": "çirkin",
    "meaning": "Kötü, güzel olmayan."
  },
  {
    "word": "iyi",
    "meaning": "Güzel, doğru."
  },
  {
    "word": "kötü",
    "meaning": "Çirkin, yanlış."
  },
  {
    "word": "doğru",
    "meaning": "İyi, yanlış olmayan."
  },
  {
    "word": "yanlış",
    "meaning": "Kötü, doğru olmayan."
  },
  {
    "word": "gerçek",
    "meaning": "Hakiki."
  },
  {
    "word": "yalan",
    "meaning": "Sahte."
  },
  {
    "word": "hakiki",
    "meaning": "Gerçek."
  },
  {
    "word": "sahte",
    "meaning": "Yalan."
  },
  {
    "word": "mükemmel",
    "meaning": "Kusursuz, fevkalade."
  },
  {
    "word": "fevkalade",
    "meaning": "Mükemmel."
  },
  {
    "word": "vasat",
    "meaning": "Orta, sıradan."
  },
  {
    "word": "sıradan",
    "meaning": "Vasat."
  },
  {
    "word": "özgün",
    "meaning": "Orijinal, eşsiz."
  },
  {
    "word": "orijinal",
    "meaning": "Özgün."
  },
  {
    "word": "kopya",
    "meaning": "Taklit."
  },
  {
    "word": "taklit",
    "meaning": "Kopya."
  },
  {
    "word": "alışılmadık",
    "meaning": "Farklı, sıra dışı."
  },
  {
    "word": "sıra dışı",
    "meaning": "Alışılmadık."
  },
  {
    "word": "olağan",
    "meaning": "Normal, sıradan."
  },
  {
    "word": "normal",
    "meaning": "Olağan."
  },
  {
    "word": "harikulade",
    "meaning": "Olağanüstü."
  },
  {
    "word": "olağanüstü",
    "meaning": "Harikulade."
  },
  {
    "word": "genel",
    "meaning": "Umumi, yaygın."
  },
  {
    "word": "hususi",
    "meaning": "Özel, kişisel."
  },
  {
    "word": "umumi",
    "meaning": "Genel."
  },
  {
    "word": "özel",
    "meaning": "Hususi."
  },
  {
    "word": "kişisel",
    "meaning": "Özel."
  },
  {
    "word": "yaygın",
    "meaning": "Genel, geniş alana yayılmış."
  },
  {
    "word": "dar",
    "meaning": "Geniş olmayan."
  },
  {
    "word": "uzak",
    "meaning": "Irak, yakın olmayan."
  },
  {
    "word": "yakın",
    "meaning": "Uzak olmayan, civar."
  },
  {
    "word": "ırak",
    "meaning": "Uzak."
  },
  {
    "word": "civarda",
    "meaning": "Yakın yerde."
  },
  {
    "word": "iç",
    "meaning": "Dahili, iç kısım."
  },
  {
    "word": "dış",
    "meaning": "Harici, dış kısım."
  },
  {
    "word": "dahili",
    "meaning": "İç."
  },
  {
    "word": "harici",
    "meaning": "Dış."
  },
  {
    "word": "yukarı",
    "meaning": "Üst, yüksek."
  },
  {
    "word": "aşağı",
    "meaning": "Alt, alçak."
  },
  {
    "word": "üst",
    "meaning": "Yukarı."
  },
  {
    "word": "alt",
    "meaning": "Aşağı."
  },
  {
    "word": "ön",
    "meaning": "Evvel, başlangıç."
  },
  {
    "word": "arka",
    "meaning": "Geri, son."
  },
  {
    "word": "evvel",
    "meaning": "Ön."
  },
  {
    "word": "geri",
    "meaning": "Arka."
  },
  {
    "word": "sağ",
    "meaning": "Doğru, sağ taraf."
  },
  {
    "word": "sol",
    "meaning": "Sol taraf."
  },
  {
    "word": "sol",
    "meaning": "Sol taraf."
  },
  {
    "word": "doğu",
    "meaning": "Güneşin doğduğu yön."
  },
  {
    "word": "batı",
    "meaning": "Güneşin battığı yön."
  },
  {
    "word": "kuzey",
    "meaning": "Kutup yönü."
  },
  {
    "word": "güney",
    "meaning": "Kutup yönü."
  },
  {
    "word": "doğmak",
    "meaning": "Tulu etmek, dünyaya gelmek."
  },
  {
    "word": "batmak",
    "meaning": "Gurup etmek, çökmek."
  },
  {
    "word": "tulu",
    "meaning": "Doğuş."
  },
  {
    "word": "gurup",
    "meaning": "Batış."
  },
  {
    "word": "yükselmek",
    "meaning": "Artmak, yukarı çıkmak."
  },
  {
    "word": "alçalmak",
    "meaning": "Azalmak, aşağı inmek."
  },
  {
    "word": "artmak",
    "meaning": "Yükselmek, çoğalmak."
  },
  {
    "word": "azalmak",
    "meaning": "Alçalmak, eksilmek."
  },
  {
    "word": "çoğalmak",
    "meaning": "Artmak."
  },
  {
    "word": "eksilmek",
    "meaning": "Azalmak."
  },
  {
    "word": "fazlalaşmak",
    "meaning": "Çoğalmak."
  },
  {
    "word": "eksiltmek",
    "meaning": "Azaltmak."
  },
  {
    "word": "çoğaltmak",
    "meaning": "Artırmak."
  },
  {
    "word": "artırmak",
    "meaning": "Çoğaltmak."
  },
  {
    "word": "azaltmak",
    "meaning": "Eksiltmek."
  },
  {
    "word": "büyümek",
    "meaning": "Gelişmek, genişlemek."
  },
  {
    "word": "küçülmek",
    "meaning": "Daralmak, ufalmak."
  },
  {
    "word": "gelişmek",
    "meaning": "Büyümek."
  },
  {
    "word": "daralmak",
    "meaning": "Küçülmek."
  },
  {
    "word": "genişlemek",
    "meaning": "Büyümek."
  },
  {
    "word": "ufalmak",
    "meaning": "Küçülmek."
  },
  {
    "word": "genişletmek",
    "meaning": "Büyütmek."
  },
  {
    "word": "küçültmek",
    "meaning": "Daraltmak."
  },
  {
    "word": "büyütmek",
    "meaning": "Genişletmek."
  },
  {
    "word": "daraltmak",
    "meaning": "Küçültmek."
  },
  {
    "word": "güçlü",
    "meaning": "Kuvvetli, kudretli."
  },
  {
    "word": "zayıf",
    "meaning": "Güçsüz, kuvvetsiz."
  },
  {
    "word": "kuvvetli",
    "meaning": "Güçlü."
  },
  {
    "word": "kuvvetsiz",
    "meaning": "Zayıf."
  },
  {
    "word": "kudretli",
    "meaning": "Güçlü."
  },
  {
    "word": "güçsüz",
    "meaning": "Zayıf."
  },
  {
    "word": "zengin",
    "meaning": "Varlıklı."
  },
  {
    "word": "fakir",
    "meaning": "Yoksul."
  },
  {
    "word": "varlıklı",
    "meaning": "Zengin."
  },
  {
    "word": "yoksul",
    "meaning": "Fakir."
  },
  {
    "word": "bolluk",
    "meaning": "Refah."
  },
  {
    "word": "refah",
    "meaning": "Bolluk."
  },
  {
    "word": "kıtlık",
    "meaning": "Yokluk."
  },
  {
    "word": "yokluk",
    "meaning": "Kıtlık."
  },
  {
    "word": "ışık",
    "meaning": "Nur, aydınlık."
  },
  {
    "word": "nur",
    "meaning": "Işık."
  },
  {
    "word": "karanlık",
    "meaning": "Zulmet, ışıksızlık."
  },
  {
    "word": "zulmet",
    "meaning": "Karanlık."
  },
  {
    "word": "aydınlık",
    "meaning": "Işık."
  },
  {
    "word": "ışıksızlık",
    "meaning": "Karanlık."
  },
  {
    "word": "sıcak",
    "meaning": "Hararetli."
  },
  {
    "word": "hararetli",
    "meaning": "Sıcak."
  },
  {
    "word": "soğuk",
    "meaning": "Serin."
  },
  {
    "word": "serin",
    "meaning": "Soğuk."
  },
  {
    "word": "su",
    "meaning": "Hava, sıvı."
  },
  {
    "word": "hava",
    "meaning": "Su, gaz."
  },
  {
    "word": "ateş",
    "meaning": "Od, yanma."
  },
  {
    "word": "od",
    "meaning": "Ateş."
  },
  {
    "word": "toprak",
    "meaning": "Huma, yer."
  },
  {
    "word": "huma",
    "meaning": "Toprak."
  },
  {
    "word": "aşk",
    "meaning": "Sevgi, muhabbet, tutku."
  },
  {
    "word": "sevgi",
    "meaning": "Aşk."
  },
  {
    "word": "muhabbet",
    "meaning": "Sevgi."
  },
  {
    "word": "nefret",
    "meaning": "Kin, düşmanlık."
  },
  {
    "word": "kin",
    "meaning": "Nefret."
  },
  {
    "word": "düşmanlık",
    "meaning": "Husumet."
  },
  {
    "word": "husumet",
    "meaning": "Düşmanlık."
  },
  {
    "word": "dostluk",
    "meaning": "Arkadaşlık."
  },
  {
    "word": "arkadaşlık",
    "meaning": "Dostluk."
  },
  {
    "word": "vefa",
    "meaning": "Sadakat."
  },
  {
    "word": "sadakat",
    "meaning": "Vefa."
  },
  {
    "word": "ihanet",
    "meaning": "Hıyanet."
  },
  {
    "word": "hıyanet",
    "meaning": "İhanet."
  },
  {
    "word": "doğru",
    "meaning": "Dürüst, hakikatli."
  },
  {
    "word": "dürüst",
    "meaning": "Doğru."
  },
  {
    "word": "yalancı",
    "meaning": "Sahtekâr."
  },
  {
    "word": "sahtekâr",
    "meaning": "Yalancı."
  },
  {
    "word": "hakikatli",
    "meaning": "Doğru."
  },
  {
    "word": "yalan",
    "meaning": "Yanlış."
  },
  {
    "word": "gerçek",
    "meaning": "Hakikat."
  },
  {
    "word": "hakikat",
    "meaning": "Gerçek."
  },
  {
    "word": "rüya",
    "meaning": "Düş, hayal."
  },
  {
    "word": "düş",
    "meaning": "Rüya."
  },
  {
    "word": "hayal",
    "meaning": "Rüya."
  },
  {
    "word": "tasavvur",
    "meaning": "Hayal etme."
  },
  {
    "word": "tasavvur",
    "meaning": "Hayal etme."
  },
  {
    "word": "hayalperest",
    "meaning": "Düş kuran."
  },
  {
    "word": "pragmatik",
    "meaning": "Uygulamacı, faydacı."
  },
  {
    "word": "faydacı",
    "meaning": "Pragmatik."
  },
  {
    "word": "idealist",
    "meaning": "Ülkücü, hayalci."
  },
  {
    "word": "ülkücü",
    "meaning": "İdealist."
  },
  {
    "word": "hayalci",
    "meaning": "İdealist."
  },
  {
    "word": "düzenli",
    "meaning": "Nizamlı, intizamlı."
  },
  {
    "word": "nizamlı",
    "meaning": "Düzenli."
  },
  {
    "word": "intizamlı",
    "meaning": "Düzenli."
  },
  {
    "word": "düzensiz",
    "meaning": "Nizamsız."
  },
  {
    "word": "nizamsız",
    "meaning": "Düzensiz."
  },
  {
    "word": "tertip",
    "meaning": "Düzen."
  },
  {
    "word": "tertipsiz",
    "meaning": "Düzensiz."
  },
  {
    "word": "kaotik",
    "meaning": "Kargaşalı."
  },
  {
    "word": "kargaşalı",
    "meaning": "Kaotik."
  },
  {
    "word": "sakin",
    "meaning": "Dingin."
  },
  {
    "word": "karmaşa",
    "meaning": "Kargaşa."
  },
  {
    "word": "anlaşılmaz",
    "meaning": "Muamma, esrarengiz."
  },
  {
    "word": "muamma",
    "meaning": "Anlaşılmaz."
  },
  {
    "word": "esrarengiz",
    "meaning": "Gizemli."
  },
  {
    "word": "gizemli",
    "meaning": "Esrarengiz."
  },
  {
    "word": "açık",
    "meaning": "Anlaşılır, sarih."
  },
  {
    "word": "sarih",
    "meaning": "Açık."
  },
  {
    "word": "örtülü",
    "meaning": "Gizli, kapalı."
  },
  {
    "word": "gizli",
    "meaning": "Örtülü."
  },
  {
    "word": "kapalı",
    "meaning": "Örtülü."
  },
  {
    "word": "görünür",
    "meaning": "Açık, bariz."
  },
  {
    "word": "bariz",
    "meaning": "Görünür."
  },
  {
    "word": "farklı",
    "meaning": "Değişik, ayrım."
  },
  {
    "word": "değişik",
    "meaning": "Farklı."
  },
  {
    "word": "aynı",
    "meaning": "Benzer, tıpkı."
  },
  {
    "word": "benzer",
    "meaning": "Aynı."
  },
  {
    "word": "tıpkı",
    "meaning": "Aynı."
  },
  {
    "word": "ayrım",
    "meaning": "Farklılık."
  },
  {
    "word": "farklılık",
    "meaning": "Ayrım."
  },
  {
    "word": "benzerlik",
    "meaning": "Aynı olma durumu."
  },
  {
    "word": "birlik",
    "meaning": "Vahdet."
  },
  {
    "word": "vahdet",
    "meaning": "Birlik."
  },
  {
    "word": "ayrılık",
    "meaning": "Farklılık."
  },
  {
    "word": "uzlaşma",
    "meaning": "Anlaşma."
  },
  {
    "word": "anlaşmazlık",
    "meaning": "İhtilaf."
  },
  {
    "word": "ihtilaf",
    "meaning": "Anlaşmazlık."
  },
  {
    "word": "ittifak",
    "meaning": "Anlaşma."
  },
  {
    "word": "ittifak",
    "meaning": "Anlaşma."
  },
  {
    "word": "ortak",
    "meaning": "Müşterek."
  },
  {
    "word": "müşterek",
    "meaning": "Ortak."
  },
  {
    "word": "tek",
    "meaning": "Yegane."
  },
  {
    "word": "yegane",
    "meaning": "Tek."
  },
  {
    "word": "ikili",
    "meaning": "Çift."
  },
  {
    "word": "çift",
    "meaning": "İkili."
  },
  {
    "word": "çoklu",
    "meaning": "Müteaddit."
  },
  {
    "word": "müteaddit",
    "meaning": "Çoklu."
  }
]

WORDS_FILE = 'kelime_havuzu.json'
LEADERBOARD_FILE = 'liderlik_tablosu.json'

def load_words():
    """Kelime havuzunu dosyadan yükler veya varsayılanı kullanır."""
    if os.path.exists(WORDS_FILE):
        try:
            with open(WORDS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Hata: Kelime havuzu dosyası yüklenemedi ({e}). Varsayılan havuz kullanılıyor.")
            return DEFAULT_WORDS
    return DEFAULT_WORDS

def load_leaderboard():
    """Liderlik tablosunu dosyadan yükler."""
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_leaderboard(leaderboard):
    """Liderlik tablosunu dosyaya kaydeder."""
    with open(LEADERBOARD_FILE, 'w', encoding='utf-8') as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=4)

def build_questions(word_list, count):
    """Oyun için soru ve seçenekleri oluşturur."""
    if count > len(word_list):
        count = len(word_list)

    # Karıştırılmış kelime havuzundan gerekli sayıda kelime seçilir
    selected_words = random.sample(word_list, count)
    all_meanings = [w['meaning'] for w in word_list]
    questions = []

    for item in selected_words:
        correct_meaning = item['meaning']
        # Doğru anlam dışındaki anlamlar
        other_meanings = [m for m in all_meanings if m != correct_meaning]
        
        # 3 yanlış anlam seçilir
        wrong_meanings = random.sample(other_meanings, min(3, len(other_meanings)))
        
        # Seçenekler oluşturulur ve karıştırılır
        options = [correct_meaning] + wrong_meanings
        random.shuffle(options)
        
        questions.append({
            'word': item['word'],
            'correct': correct_meaning,
            'options': options
        })
    return questions

def display_question(q, current_q, total_q):
    """Soruyu ve seçenekleri ekrana yazdırır."""
    print("\n" + "-"*50)
    print(f"❓ Soru {current_q}/{total_q} | Puan: {state['score']}")
    print(f"\n** \"{q['word']}\" kelimesinin anlamı hangisidir? **")
    
    # Seçenekleri numaralandırarak yazdırır
    for i, option in enumerate(q['options'], 1):
        print(f"  {i}. {option}")
    print("-" * 50)

def get_user_answer(option_count):
    """Kullanıcıdan geçerli bir cevap (sayı) alır."""
    while True:
        try:
            choice = input(f"Cevabınız (1-{option_count}) veya (q)uit: ").strip().lower()
            if choice == 'q':
                return 'quit'
            choice_int = int(choice)
            if 1 <= choice_int <= option_count:
                return choice_int
            else:
                print(f"Geçersiz giriş. Lütfen 1 ile {option_count} arasında bir sayı girin.")
        except ValueError:
            print("Geçersiz giriş. Lütfen bir sayı girin.")

def play_game(word_list):
    """Oyunun ana döngüsünü çalıştırır."""
    print("🌟 Kelime & Anlam Eşleştirme Oyunu Başlıyor!")
    
    student_name = input("Öğrenci Adınız: ").strip() or "İsimsiz"
    school_name = input ("Okulunuz: ").strip() or "İsimsiz"
    while True:
        try:
            q_count_input = input(f"Soru sayısı ({len(word_list)}'e kadar): ").strip() or "10"
            q_count = int(q_count_input)
            if 1 <= q_count <= len(word_list):
                break
            else:
                print(f"Lütfen 1 ile {len(word_list)} arasında bir sayı girin.")
        except ValueError:
            print("Geçersiz giriş. Lütfen bir sayı girin.")

    global state
    state = {'student': student_name, 'qCount': q_count, 'current': 0, 'score': 0}
    questions = build_questions(word_list, q_count)
    
    # Zamanlayıcı başlatılır
    start_time = time.time()
    
    for i, q in enumerate(questions):
        state['current'] = i
        display_question(q, i + 1, state['qCount'])
        
        answer = get_user_answer(len(q['options']))
        
        if answer == 'quit':
            print("\n❌ Oyundan vazgeçildi.")
            return

        chosen_meaning = q['options'][answer - 1]
        
        if chosen_meaning == q['correct']:
            state['score'] += 1
            print("✅ Doğru!")
        else:
            print(f"❌ Yanlış! Doğru cevap: **{q['correct']}**")
        
        # Her sorudan sonra kısa bir bekleme
        time.sleep(0.5)

    # Oyun bitiş zamanı
    end_time = time.time()
    total_time = end_time - start_time
    
    # --- Oyun Sonucu ---
    print("\n" + "="*50)
    print("🏆 OYUN BİTTİ!")
    print(f"Öğrenci: {state['student']}")
    print(f"Puanınız: {state['score']}/{state['qCount']}")
    print(f"Süre: {total_time:.2f} saniye")
    print("="*50)
    
    # Skor kaydetme
    save_score(state['student'],  state['score'], state['qCount'], total_time)

def save_score(name, score, total, duration):
    """Skoru liderlik tablosuna kaydeder."""
    leaderboard = load_leaderboard()
    entry = {
        'name': name,
        'score': score,
        'total': total,
        'duration': f"{duration:.2f} saniye",
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    leaderboard.append(entry)
    # Skor/Toplam oranına göre sıralama
    leaderboard.sort(key=lambda x: x['score'] / x['total'], reverse=True)
    save_leaderboard(leaderboard)
    print("🎉 Skorunuz Liderlik Tablosuna eklendi.")

def view_leaderboard():
    """Liderlik tablosunu ekrana yazdırır."""
    leaderboard = load_leaderboard()
    
    print("\n" + "📊 LİDERLİK TABLOSU ".center(50, '='))
    if not leaderboard:
        print("Tablo boş.")
        return

    # Sütun başlıkları
    header = f"{'ÖĞRENCİ':<20} {'PUAN':<10}{'SÜRE':<15}{'TARİH':<20}"
    print(header)
    print("-" * len(header))

    for entry in leaderboard[:10]: # İlk 10'u göster
        score_str = f"{entry['score']}/{entry['total']}"
        print(f"{entry['name'][:20]:<20}{score_str:<10}{entry['duration']:<15}{entry['date']:<20}")
    print("="*50 + "\n")

def main_menu():
    """Ana menüyü gösterir ve kullanıcı seçimini işler."""
    word_list = load_words()
    
    while True:
        print("\n" + "🧠 DİLİMİZİN ZENGİNLİKLERİ - MENÜ ".center(50, '-'))
        print(f"Toplam Kelime Sayısı: {len(word_list)}")
        print("1. Oyunu Başlat")
        print("2. Liderlik Tablosu")
        print("3. Çıkış")
        print("-" * 50)
        
        choice = input("Seçiminiz (1/2/3): ").strip()
        
        if choice == '1':
            play_game(word_list)
        elif choice == '2':
            view_leaderboard()
        elif choice == '3':
            print("Güle güle!")
            break
        else:
            print("Geçersiz seçim. Lütfen 1, 2 veya 3 girin.")

if __name__ == "__main__":
    main_menu()
