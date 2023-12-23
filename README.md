# Tugas Besar Jaringan Komputer IF3130

> Implementasi Protokol TCP-Like Go-Back-N

## Anggota Kelompok
| Nama | NIM |
| ----------- | ----------- |
| Bintang Hijriawan | 13521003 |
| Jason Rivalino | 13521008 |
| Kartini Copa | 13521026

## Deskripsi Program
Program sederhana yang memanfaatkan socket programming sebagai fungsi utamanya. Pengiriman data sederhana lewat jaringan menggunakan protokol transport layer.

## Struktur File
```bash
📦tugas-besar-if3130-jaringan-komputer-jar_
 ┣ 📂docs
 ┃ ┗ 📜IF3130 - Tugas Besar 1
 ┣ 📂lib
 ┃ ┣ 📜client.py
 ┃ ┣ 📜connection.py
 ┃ ┣ 📜messageinfo.py
 ┃ ┣ 📜node.py
 ┃ ┣ 📜segment.py
 ┃ ┣ 📜segmentflag.py
 ┃ ┗ 📜server.py
 ┣ 📂output
 ┃ ┣ 📜hasiltest-flower.jpeg
 ┃ ┣ 📜hasiltest-ha.txt
 ┃ ┣ 📜hasiltest-home.mp3
 ┃ ┣ 📜hasiltest-pebble.png
 ┃ ┗ 📜hasiltest-video.webm
 ┣ 📂testcase
 ┃ ┣ 📜flower.jpeg
 ┃ ┣ 📜ha.txt
 ┃ ┣ 📜home.mp3
 ┃ ┣ 📜pebble.png
 ┃ ┗ 📜video.webm
 ┗ 📜README.md
 ```

## Tampilan Program
![Screenshot 2023-11-28 232041](https://github.com/Sister20/tugas-besar-if3130-jaringan-komputer-jar_/assets/91790457/700cb349-24ee-4b54-88b5-18a470891dc3)
![Screenshot 2023-11-28 234344](https://github.com/Sister20/tugas-besar-if3130-jaringan-komputer-jar_/assets/91790457/297718b0-cdad-4c71-bdb6-3e54a33eee55)

## Cara Menjalankan Program
<b>1. Clone repository ini terlebih dahulu</b>

<b>2. Membuka terminal dan sesuaikan directory dengan tempat clone _source code_ ini.</b>

<b>3. Menjalankan perintah berikut untuk menjalankan server.</b>
```
python lib/server.py [broadcast port] [path file input]
Contoh: python lib/server.py 12345 ./testcase/video.webm
```

Keterangan:
- Broadcast port: menandakan port untuk server
- Path file input: directory file yang dipilih untuk dikirimkan
<br>

<b>4. Kemudian, buka terminal baru dan jalankan perintah berikut.</b>
```
python lib/client.py [client port] [broadcast port] [path output]
Contoh: python lib/client.py 54213 12345 ./output/hasiltest-video.webm
```

Keterangan:
- Client port: menandakan port untuk client
- Broadcast port: menandakan port untuk server
- Path file output: directory tempat keluaran pengiriman file


## Acknowledgements
- Tuhan Yang Maha Esa
- Dosen Pengampu Mata Kuliah IF3130 Jaringan Komputer
- Kakak-Kakak Asisten Mata Kuliah IF3130 Jaringan Komputer
