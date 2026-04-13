# AI Pathfinding Visualizer (BFS vs DFS)

Bu proje, temel yapay zeka arama algoritmaları olan Breadth-First Search (BFS) ve Depth-First Search (DFS) algoritmalarının nasıl çalıştığını görselleştirmek amacıyla Python ve Tkinter kullanılarak geliştirilmiş bir masaüstü uygulamasıdır.

## 1. Projenin Amacı
Projenin temel amacı, karmaşık algoritmaları somut bir görsel düzlemde simüle ederek kullanıcıya bu algoritmaların "arama derinliği" ve "düğüm ziyaret sırası" farklarını doğrudan göstermektir. Özellikle eğitim amaçlı bir araç olarak tasarlanmıştır.

## 2. Kullanılan Teknolojiler
- **Python**: Çekirdek programlama dili.
- **Tkinter**: Görsel arayüz (GUI) tasarımı için kullanılmıştır.
- **Collections (deque)**: BFS algoritmasının kuyruk (queue) yapısını optimize etmek için kullanılmıştır.
- **Random**: "Random Maze" özelliği ile rastgele engeller oluşturmak için kullanılmıştır.

## 3. Temel Özellikler
- **Interaktif Izgara (20x20)**: Kullanıcılar fare tıklamalarıyla başlangıç noktası, bitiş noktası ve engeller (duvarlar) yerleştirebilirler.
- **BFS (Breadth-First Search)**: Başlangıç noktasından itibaren tüm komşu düğümleri seviye seviye tarayan algoritma. Genellikle en kısa yolu bulma garantisi verir.
- **DFS (Depth-First Search)**: Bir koldan derinlemesine giderek arama yapan algoritma (LIFO mantığı). En kısa yolu garanti etmez ancak farklı bir arama stratejisi sergiler.
- **Hız Kontrolü (Speed Slider)**: Simülasyon hızını gerçek zamanlı olarak ayarlayabilme imkanı sunar.
- **Rastgele Labirent Oluşturucu**: Izgara üzerine %30 yoğunlukta rastgele engeller atayarak test senaryoları yaratır.
- **İstatistik Paneli**: Algoritma tamamlandığında ziyaret edilen toplam düğüm sayısını ve bulunan yolun uzunluğunu kullanıcıya sunar.
- **Canlı Durum Çubuğu**: Uygulamanın o anki modunu ve algoritma durumunu anlık olarak gösterir.

## 4. Teknik Detaylar

### Algoritmaların Çalışma Mantığı
- **BFS**: Bir `deque` veri yapısı kullanır. Ziyaret edilen düğümler işaretlenir ve her komşu bir kuyruğa eklenir. Görselleştirmede "dalga dalga" yayılan bir efekt oluşur.
- **DFS**: Bir `stack` (yığın) yapısı kullanır (Python listesi ile simüle edilmiştir). Derinlemesine ilerlediği için görsellemede "yılan gibi" tek bir hat üzerinde uzanan bir efekt görülür.

### Görselleştirme Döngüsü
Uygulama, algoritmaların çalışmasını `self.root.update()` ve `self.root.after(delay)` metodlarıyla asenkron bir görünüm kazandırarak yavaşlatır. Bu sayede her düğüm ziyareti kullanıcı tarafından takip edilebilir.

### Yol Yeniden Yapılandırma (Path Reconstruction)
Her iki algoritma da ziyaret ettikleri düğümleri bir `came_from` sözlüğünde (key: mevcut düğüm, value: gelinen düğüm) saklar. Hedef bulunduğunda bu sözlük geriye doğru taranarak başlangıçtan bitişe en net yol (sarı hücreler) ortaya çıkarılır.

## 5. Uygulama Nasıl Çalıştırılır?
1. Bilgisayarınızda Python yüklü olmalıdır.
2. Terminal veya komut istemcisini açın.
3. Proje dizinine gidin.
4. `python main.py` komutunu çalıştırın.

---
*Bu doküman, proje raporu hazırlamak için gerekli teknik detayları ve fonksiyonel özellikleri içermektedir.*
