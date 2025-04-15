"""
Real-world tips and practical applications for Toko Pintar skills.
"""
import streamlit as st
import random
from utils.config import get_config

# Practical tips by skill and level
SKILL_TIPS = {
    "inventory_management": {
        1: [
            {
                "title": {
                    "en": "Start with a Daily Count",
                    "id": "Mulai dengan Penghitungan Harian"
                },
                "content": {
                    "en": "Count your best-selling items every day to catch discrepancies early.",
                    "id": "Hitung produk terlaris Anda setiap hari untuk menangkap perbedaan lebih awal."
                }
            },
            {
                "title": {
                    "en": "Organize Your Space",
                    "id": "Atur Ruang Anda"
                },
                "content": {
                    "en": "Group similar items together on shelves to make counting faster and more accurate.",
                    "id": "Kelompokkan barang serupa di rak untuk membuat penghitungan lebih cepat dan akurat."
                }
            }
        ],
        2: [
            {
                "title": {
                    "en": "Use the FIFO Method",
                    "id": "Gunakan Metode FIFO"
                },
                "content": {
                    "en": "First In, First Out - place new stock behind older stock to ensure older products sell first.",
                    "id": "First In, First Out - tempatkan stok baru di belakang stok lama untuk memastikan produk lama terjual lebih dulu."
                }
            },
            {
                "title": {
                    "en": "Create a Simple Inventory Sheet",
                    "id": "Buat Lembar Inventaris Sederhana"
                },
                "content": {
                    "en": "Use a notebook to track: Product Name, Starting Count, Additions, Sales, and Ending Count.",
                    "id": "Gunakan buku catatan untuk melacak: Nama Produk, Jumlah Awal, Penambahan, Penjualan, dan Jumlah Akhir."
                }
            }
        ],
        3: [
            {
                "title": {
                    "en": "Identify Your ABC Items",
                    "id": "Identifikasi Item ABC Anda"
                },
                "content": {
                    "en": "A - High value/profit items: count daily\nB - Medium value: count weekly\nC - Low value: count monthly",
                    "id": "A - Item nilai/keuntungan tinggi: hitung harian\nB - Nilai sedang: hitung mingguan\nC - Nilai rendah: hitung bulanan"
                }
            },
            {
                "title": {
                    "en": "Minimum Stock Levels",
                    "id": "Level Stok Minimum"
                },
                "content": {
                    "en": "Establish minimum stock levels for each product based on sales rate and reorder time.",
                    "id": "Tetapkan level stok minimum untuk setiap produk berdasarkan tingkat penjualan dan waktu pemesanan ulang."
                }
            }
        ],
        4: [
            {
                "title": {
                    "en": "Seasonal Inventory Planning",
                    "id": "Perencanaan Inventaris Musiman"
                },
                "content": {
                    "en": "Stock up on seasonal items 1-2 months before peak demand periods (holidays, festivals, etc.).",
                    "id": "Stok barang musiman 1-2 bulan sebelum periode permintaan puncak (liburan, festival, dll)."
                }
            },
            {
                "title": {
                    "en": "Vendor Management",
                    "id": "Manajemen Vendor"
                },
                "content": {
                    "en": "Keep backup suppliers for critical products in case your primary vendor has delivery issues.",
                    "id": "Simpan pemasok cadangan untuk produk penting jika vendor utama Anda memiliki masalah pengiriman."
                }
            }
        ],
        5: [
            {
                "title": {
                    "en": "Inventory Turnover Ratio",
                    "id": "Rasio Perputaran Inventaris"
                },
                "content": {
                    "en": "Calculate how many times you sell through your inventory each month: (Cost of Goods Sold ÷ Average Inventory Value)",
                    "id": "Hitung berapa kali Anda menjual inventaris Anda setiap bulan: (Harga Pokok Penjualan ÷ Nilai Rata-Rata Inventaris)"
                }
            },
            {
                "title": {
                    "en": "Dead Stock Management",
                    "id": "Manajemen Stok Mati"
                },
                "content": {
                    "en": "For items not selling for 90+ days: discount heavily, bundle with popular items, or return to vendor if possible.",
                    "id": "Untuk barang yang tidak terjual selama 90+ hari: diskon besar, bundel dengan barang populer, atau kembalikan ke vendor jika memungkinkan."
                }
            }
        ]
    },
    "cash_handling": {
        1: [
            {
                "title": {
                    "en": "Always Count Twice",
                    "id": "Selalu Hitung Dua Kali"
                },
                "content": {
                    "en": "Count all cash twice before handing change to customers to avoid errors.",
                    "id": "Hitung semua uang tunai dua kali sebelum memberikan kembalian kepada pelanggan untuk menghindari kesalahan."
                }
            },
            {
                "title": {
                    "en": "Organize Your Cash Drawer",
                    "id": "Atur Laci Kas Anda"
                },
                "content": {
                    "en": "Keep each denomination in its own compartment with bills facing the same direction.",
                    "id": "Simpan setiap denominasi di kompartemen sendiri dengan uang kertas menghadap ke arah yang sama."
                }
            }
        ],
        2: [
            {
                "title": {
                    "en": "Announce the Total",
                    "id": "Umumkan Total"
                },
                "content": {
                    "en": "Say the total out loud and count change back to customers step by step.",
                    "id": "Katakan total dengan suara keras dan hitung kembalian kembali ke pelanggan langkah demi langkah."
                }
            },
            {
                "title": {
                    "en": "Start with a Base Amount",
                    "id": "Mulai dengan Jumlah Dasar"
                },
                "content": {
                    "en": "Begin each day with a consistent amount in your cash drawer (e.g., 500,000 Rp).",
                    "id": "Mulai setiap hari dengan jumlah yang konsisten di laci kas Anda (mis., 500.000 Rp)."
                }
            }
        ],
        3: [
            {
                "title": {
                    "en": "Daily Cash Reconciliation",
                    "id": "Rekonsiliasi Kas Harian"
                },
                "content": {
                    "en": "At day's end, count your cash and compare to sales records to catch discrepancies.",
                    "id": "Di akhir hari, hitung uang tunai Anda dan bandingkan dengan catatan penjualan untuk menangkap perbedaan."
                }
            },
            {
                "title": {
                    "en": "Handle Large Bills Carefully",
                    "id": "Tangani Uang Kertas Besar dengan Hati-hati"
                },
                "content": {
                    "en": "For large denominations, verify authenticity and keep them visible until the transaction is complete.",
                    "id": "Untuk denominasi besar, verifikasi keaslian dan simpan terlihat sampai transaksi selesai."
                }
            }
        ],
        4: [
            {
                "title": {
                    "en": "Secure Cash Storage",
                    "id": "Penyimpanan Uang yang Aman"
                },
                "content": {
                    "en": "Regularly move excess cash from your drawer to a more secure location throughout the day.",
                    "id": "Secara teratur memindahkan kelebihan uang tunai dari laci Anda ke lokasi yang lebih aman sepanjang hari."
                }
            },
            {
                "title": {
                    "en": "Cash Handling Roles",
                    "id": "Peran Penanganan Uang"
                },
                "content": {
                    "en": "If possible, separate responsibilities: one person handles sales while another manages banking/deposits.",
                    "id": "Jika memungkinkan, pisahkan tanggung jawab: satu orang menangani penjualan sementara yang lain mengelola perbankan/deposito."
                }
            }
        ],
        5: [
            {
                "title": {
                    "en": "Digital Payments Integration",
                    "id": "Integrasi Pembayaran Digital"
                },
                "content": {
                    "en": "Offer digital payment options to reduce cash handling risks and improve record keeping.",
                    "id": "Tawarkan opsi pembayaran digital untuk mengurangi risiko penanganan uang tunai dan meningkatkan pencatatan."
                }
            },
            {
                "title": {
                    "en": "Cash Flow Forecasting",
                    "id": "Perkiraan Arus Kas"
                },
                "content": {
                    "en": "Predict peak cash periods to ensure you have enough change and security measures in place.",
                    "id": "Prediksi periode kas puncak untuk memastikan Anda memiliki cukup perubahan dan langkah-langkah keamanan."
                }
            }
        ]
    },
    "pricing_strategy": {
        1: [
            {
                "title": {
                    "en": "Know Your Costs",
                    "id": "Ketahui Biaya Anda"
                },
                "content": {
                    "en": "Always include all costs when calculating your selling price (purchase price, transport, storage, etc.).",
                    "id": "Selalu sertakan semua biaya saat menghitung harga jual Anda (harga beli, transportasi, penyimpanan, dll.)."
                }
            },
            {
                "title": {
                    "en": "Start with Standard Margins",
                    "id": "Mulai dengan Margin Standar"
                },
                "content": {
                    "en": "Begin with industry-standard margins for your product categories (typically 20-50% for retail).",
                    "id": "Mulai dengan margin standar industri untuk kategori produk Anda (biasanya 20-50% untuk ritel)."
                }
            }
        ],
        2: [
            {
                "title": {
                    "en": "Price Psychology",
                    "id": "Psikologi Harga"
                },
                "content": {
                    "en": "Use prices ending in 9 or 5 (9,900 Rp instead of 10,000 Rp) to create a perception of better value.",
                    "id": "Gunakan harga yang berakhir dengan 9 atau 5 (9.900 Rp bukan 10.000 Rp) untuk menciptakan persepsi nilai yang lebih baik."
                }
            },
            {
                "title": {
                    "en": "Different Margins for Different Products",
                    "id": "Margin Berbeda untuk Produk Berbeda"
                },
                "content": {
                    "en": "Use higher margins for unique items and lower margins for competitive products customers compare across shops.",
                    "id": "Gunakan margin lebih tinggi untuk item unik dan margin lebih rendah untuk produk kompetitif yang pelanggan bandingkan antar toko."
                }
            }
        ],
        3: [
            {
                "title": {
                    "en": "Competitor Price Monitoring",
                    "id": "Pemantauan Harga Pesaing"
                },
                "content": {
                    "en": "Check competitor prices weekly for key products, keeping yours within 5-10% if competing on price.",
                    "id": "Periksa harga pesaing mingguan untuk produk kunci, menjaga Anda dalam 5-10% jika bersaing pada harga."
                }
            },
            {
                "title": {
                    "en": "Bundle Pricing",
                    "id": "Harga Bundle"
                },
                "content": {
                    "en": "Create product bundles that offer a small discount but increase total purchase value.",
                    "id": "Buat bundle produk yang menawarkan diskon kecil tetapi meningkatkan nilai pembelian total."
                }
            }
        ],
        4: [
            {
                "title": {
                    "en": "Seasonal Pricing Strategy",
                    "id": "Strategi Harga Musiman"
                },
                "content": {
                    "en": "Adjust prices based on seasonal demand - increase during high demand, discount during slow periods.",
                    "id": "Sesuaikan harga berdasarkan permintaan musiman - tingkatkan selama permintaan tinggi, diskon selama periode lambat."
                }
            },
            {
                "title": {
                    "en": "Price Anchoring",
                    "id": "Jangkar Harga"
                },
                "content": {
                    "en": "Display premium products next to standard ones to make the standard price seem more reasonable.",
                    "id": "Tampilkan produk premium di sebelah yang standar untuk membuat harga standar tampak lebih masuk akal."
                }
            }
        ],
        5: [
            {
                "title": {
                    "en": "Value-Based Pricing",
                    "id": "Penetapan Harga Berbasis Nilai"
                },
                "content": {
                    "en": "For some products, set prices based on the value to customers rather than just cost plus margin.",
                    "id": "Untuk beberapa produk, tetapkan harga berdasarkan nilai bagi pelanggan daripada hanya biaya plus margin."
                }
            },
            {
                "title": {
                    "en": "Loyalty Pricing",
                    "id": "Harga Loyalitas"
                },
                "content": {
                    "en": "Develop special pricing or discounts for your regular customers to encourage loyalty.",
                    "id": "Kembangkan harga khusus atau diskon untuk pelanggan tetap Anda untuk mendorong loyalitas."
                }
            }
        ]
    }
}

# Real-world applications by skill and level
REAL_WORLD_APPLICATIONS = {
    "inventory_management": {
        1: {
            "en": """
            ## Real Shop Examples
            
            **Small Food Stall (Warung)**
            - A warung owner in Jakarta counts their instant noodles each morning
            - They record the count in a simple notebook
            - When they run low, they visit their supplier that afternoon
            
            **Minimarket**
            - Uses colored stickers on products indicating when they were received
            - Organizes shelves with oldest products in front for easy rotation
            
            **Implementation Strategy**
            1. Start by focusing on your 10 most popular products
            2. Create a simple daily count sheet with columns for: Product, Beginning Count, Sold, Received, Ending Count
            3. Count these items at the same time each day
            4. Use this information to predict when you'll need to restock
            """,
            "id": """
            ## Contoh Toko Nyata
            
            **Warung Kecil**
            - Pemilik warung di Jakarta menghitung mie instan mereka setiap pagi
            - Mereka mencatat jumlahnya di buku catatan sederhana
            - Ketika stok menipis, mereka mengunjungi pemasok mereka sore itu
            
            **Minimarket**
            - Menggunakan stiker berwarna pada produk yang menunjukkan kapan mereka diterima
            - Mengatur rak dengan produk tertua di depan untuk rotasi yang mudah
            
            **Strategi Implementasi**
            1. Mulai dengan fokus pada 10 produk terlaris Anda
            2. Buat lembar penghitungan harian sederhana dengan kolom: Produk, Jumlah Awal, Terjual, Diterima, Jumlah Akhir
            3. Hitung item-item ini pada waktu yang sama setiap hari
            4. Gunakan informasi ini untuk memprediksi kapan Anda perlu mengisi ulang stok
            """
        },
        2: {
            "en": """
            ## Organized Inventory Systems
            
            **Phone Accessory Shop**
            - Groups inventory by product category (cases, chargers, screen protectors)
            - Uses a color-coding system for different price ranges
            - Rotates display items monthly to prevent sun damage and dust accumulation
            
            **Bakery**
            - Tracks ingredients inventory separately from finished products
            - Calculates "yield rates" (how many products can be made from raw materials)
            - Uses production planning sheets to prepare exact amounts needed each day
            
            **Implementation Strategy**
            1. Create a map or diagram of your storage areas
            2. Assign specific locations for each product category
            3. Label shelves clearly with product names and maximum quantities
            4. Schedule a weekly "15-minute tidy" to maintain organization
            """,
            "id": """
            ## Sistem Inventaris Terorganisir
            
            **Toko Aksesoris Ponsel**
            - Mengelompokkan inventaris berdasarkan kategori produk (case, charger, pelindung layar)
            - Menggunakan sistem kode warna untuk berbagai rentang harga
            - Merotasi item display bulanan untuk mencegah kerusakan akibat sinar matahari dan akumulasi debu
            
            **Toko Roti**
            - Melacak inventaris bahan baku secara terpisah dari produk jadi
            - Menghitung "tingkat hasil" (berapa banyak produk yang dapat dibuat dari bahan baku)
            - Menggunakan lembar perencanaan produksi untuk menyiapkan jumlah yang tepat yang diperlukan setiap hari
            
            **Strategi Implementasi**
            1. Buat peta atau diagram area penyimpanan Anda
            2. Tetapkan lokasi spesifik untuk setiap kategori produk
            3. Beri label rak dengan jelas dengan nama produk dan jumlah maksimum
            4. Jadwalkan "merapikan 15 menit" mingguan untuk mempertahankan organisasi
            """
        },
        3: {
            "en": """
            ## Advanced Inventory Practices
            
            **Medium-Sized Grocery Store**
            - Creates a "par level" sheet listing the minimum stock needed for each product
            - Checks high-value items (meat, fish, etc.) twice daily
            - Uses a dedicated storage area for overflow stock with clear labeling
            - Analyzes sales data to identify slow-moving products for clearance promotions
            
            **Clothing Boutique**
            - Takes photos of display arrangements before restocking
            - Tracks inventory by size/color/style to identify popular variants
            - Maintains a "back stock" ratio of 2:1 for best-selling items
            - Uses a monthly "category review" to identify trends and adjust purchasing
            
            **Implementation Strategy**
            1. Establish minimum and maximum inventory levels for each product
            2. Create a weekly inventory schedule (which categories to count on which days)
            3. Set up a simple inventory management spreadsheet with formulas for reorder points
            4. Implement a "first expired, first out" system for perishable goods
            """,
            "id": """
            ## Praktik Inventaris Lanjutan
            
            **Toko Kelontong Menengah**
            - Membuat lembar "level par" yang mencantumkan stok minimum yang diperlukan untuk setiap produk
            - Memeriksa barang bernilai tinggi (daging, ikan, dll.) dua kali sehari
            - Menggunakan area penyimpanan khusus untuk stok berlebih dengan pelabelan yang jelas
            - Menganalisis data penjualan untuk mengidentifikasi produk yang lambat bergerak untuk promosi penjualan
            
            **Butik Pakaian**
            - Mengambil foto pengaturan tampilan sebelum mengisi ulang
            - Melacak inventaris berdasarkan ukuran/warna/gaya untuk mengidentifikasi varian populer
            - Mempertahankan rasio "stok belakang" 2:1 untuk item terlaris
            - Menggunakan "tinjauan kategori" bulanan untuk mengidentifikasi tren dan menyesuaikan pembelian
            
            **Strategi Implementasi**
            1. Tetapkan tingkat inventaris minimum dan maksimum untuk setiap produk
            2. Buat jadwal inventaris mingguan (kategori mana yang dihitung pada hari apa)
            3. Siapkan spreadsheet manajemen inventaris sederhana dengan rumus untuk titik pemesanan ulang
            4. Terapkan sistem "pertama kadaluarsa, pertama keluar" untuk barang yang mudah rusak
            """
        },
        4: {
            "en": """
            ## Strategic Inventory Management
            
            **Pharmacy**
            - Uses ABC analysis (A items = high value/critical, B = moderate, C = low value)
            - Conducts daily counts of A items, weekly for B items, monthly for C items
            - Tracks expiration dates in a digital calendar with 3-month advance warnings
            - Has emergency supplier relationships for critical medications
            
            **Hardware Store**
            - Maintains seasonal inventory forecasts based on previous years' data
            - Adjusts stock levels based on upcoming construction projects in the area
            - Cross-trains all staff on inventory procedures to ensure consistency
            - Uses "red tag" system to identify items that haven't sold in 6+ months
            
            **Implementation Strategy**
            1. Categorize your inventory into A, B, and C items based on value and importance
            2. Develop different counting schedules and procedures for each category
            3. Implement cycle counting - count a portion of inventory each day instead of all at once
            4. Create a seasonal forecasting tool based on last year's sales patterns
            """,
            "id": """
            ## Manajemen Inventaris Strategis
            
            **Apotek**
            - Menggunakan analisis ABC (item A = nilai tinggi/kritis, B = sedang, C = nilai rendah)
            - Melakukan penghitungan harian untuk item A, mingguan untuk item B, bulanan untuk item C
            - Melacak tanggal kedaluwarsa dalam kalender digital dengan peringatan 3 bulan di muka
            - Memiliki hubungan pemasok darurat untuk obat-obatan penting
            
            **Toko Peralatan**
            - Mempertahankan perkiraan inventaris musiman berdasarkan data tahun-tahun sebelumnya
            - Menyesuaikan tingkat stok berdasarkan proyek konstruksi yang akan datang di area
            - Melatih silang semua staf tentang prosedur inventaris untuk memastikan konsistensi
            - Menggunakan sistem "tag merah" untuk mengidentifikasi item yang belum terjual dalam 6+ bulan
            
            **Strategi Implementasi**
            1. Kategorikan inventaris Anda menjadi item A, B, dan C berdasarkan nilai dan kepentingan
            2. Kembangkan jadwal dan prosedur penghitungan yang berbeda untuk setiap kategori
            3. Terapkan penghitungan siklus - hitung sebagian inventaris setiap hari alih-alih sekaligus
            4. Buat alat perkiraan musiman berdasarkan pola penjualan tahun lalu
            """
        },
        5: {
            "en": """
            ## Professional Inventory Systems
            
            **Successful Supermarket Chain**
            - Uses inventory management software on tablets for real-time updates
            - Analyzes "inventory turns" metrics (how often stock sells through completely)
            - Implements automatic reordering when inventory reaches minimum levels
            - Conducts quarterly full inventory audits to reconcile system with reality
            - Uses predictive analytics to adjust order quantities based on sales trends
            
            **Electronics Store**
            - Uses barcode scanning to track all inventory movement
            - Classifies products by profit margin and turnover rate
            - Conducts cycle counting (counting a portion of inventory each day)
            - Integrates inventory with point-of-sale system for real-time updates
            - Implements "just-in-time" inventory for high-value items to reduce holding costs
            
            **Implementation Strategy**
            1. Research inventory management software solutions appropriate for your business size
            2. Develop key performance indicators (KPIs) for inventory management
            3. Implement barcode or QR code tracking for all products
            4. Create dashboard reports showing inventory health metrics
            5. Train staff on inventory management as a profit-driving function, not just counting
            """,
            "id": """
            ## Sistem Inventaris Profesional
            
            **Jaringan Supermarket Sukses**
            - Menggunakan perangkat lunak manajemen inventaris di tablet untuk pembaruan real-time
            - Menganalisis metrik "perputaran inventaris" (seberapa sering stok terjual sepenuhnya)
            - Menerapkan pemesanan ulang otomatis ketika inventaris mencapai level minimum
            - Melakukan audit inventaris penuh triwulanan untuk merekonsiliasi sistem dengan kenyataan
            - Menggunakan analitik prediktif untuk menyesuaikan jumlah pesanan berdasarkan tren penjualan
            
            **Toko Elektronik**
            - Menggunakan pemindaian barcode untuk melacak semua pergerakan inventaris
            - Mengklasifikasikan produk berdasarkan margin keuntungan dan tingkat perputaran
            - Melakukan penghitungan siklus (menghitung sebagian inventaris setiap hari)
            - Mengintegrasikan inventaris dengan sistem point-of-sale untuk pembaruan real-time
            - Menerapkan inventaris "just-in-time" untuk item bernilai tinggi untuk mengurangi biaya penyimpanan
            
            **Strategi Implementasi**
            1. Riset solusi perangkat lunak manajemen inventaris yang sesuai untuk ukuran bisnis Anda
            2. Kembangkan indikator kinerja utama (KPI) untuk manajemen inventaris
            3. Terapkan pelacakan barcode atau kode QR untuk semua produk
            4. Buat laporan dashboard yang menunjukkan metrik kesehatan inventaris
            5. Latih staf tentang manajemen inventaris sebagai fungsi pendorong keuntungan, bukan hanya penghitungan
            """
        }
    },
    "cash_handling": {
        1: {
            "en": """
            ## Basic Cash Handling Practices
            
            **Corner Food Stall**
            - Keeps a dedicated cash box with compartments for different bills
            - Starts each day with 200,000 Rp in small bills for making change
            - Counts money twice before giving change to customers
            
            **Neighborhood Store**
            - Places large bills under the tray to prevent mixing with change
            - Uses a calculator for each transaction
            - Always provides a handwritten receipt
            
            **Implementation Strategy**
            1. Purchase a secure cash box with separate compartments
            2. Create a standard "starting cash" amount for each day
            3. Develop a habit of announcing amounts clearly to customers
            4. Count cash-in-drawer at the beginning and end of each day
            """,
            "id": """
            ## Praktik Penanganan Kas Dasar
            
            **Warung Pojok**
            - Menyimpan kotak kas khusus dengan kompartemen untuk berbagai tagihan
            - Memulai setiap hari dengan 200.000 Rp dalam pecahan kecil untuk membuat perubahan
            - Menghitung uang dua kali sebelum memberikan kembalian kepada pelanggan
            
            **Toko Lingkungan**
            - Menempatkan tagihan besar di bawah nampan untuk mencegah pencampuran dengan perubahan
            - Menggunakan kalkulator untuk setiap transaksi
            - Selalu memberikan tanda terima tulisan tangan
            
            **Strategi Implementasi**
            1. Beli kotak kas yang aman dengan kompartemen terpisah
            2. Buat jumlah "uang awal" standar untuk setiap hari
            3. Kembangkan kebiasaan mengumumkan jumlah dengan jelas kepada pelanggan
            4. Hitung uang di laci pada awal dan akhir setiap hari
            """
        },
        2: {
            "en": """
            ## Intermediate Cash Management
            
            **Café Business**
            - Uses a simple point-of-sale app on a tablet
            - Keeps a daily cash log recording starting cash, sales, and ending cash
            - Has a secure lockbox for excess cash throughout the day
            - Counts cash drawer during shift changes with both employees present
            
            **Mobile Vendor**
            - Uses a designated money belt with separate pockets for different denominations
            - Takes photos of large bills when accepting them to prevent disputes
            - Creates end-of-day reports comparing digital records to cash on hand
            
            **Implementation Strategy**
            1. Create a cash handling procedures document for employees
            2. Implement a "cash drop" system for removing excess cash from the register
            3. Develop a standard form for reconciling cash at the end of each day
            4. Consider a basic point-of-sale system that tracks cash transactions
            """,
            "id": """
            ## Manajemen Kas Menengah
            
            **Bisnis Kafe**
            - Menggunakan aplikasi point-of-sale sederhana di tablet
            - Menyimpan catatan kas harian yang mencatat uang awal, penjualan, dan uang akhir
            - Memiliki kotak kunci yang aman untuk kelebihan uang sepanjang hari
            - Menghitung laci kas selama pergantian shift dengan kedua karyawan hadir
            
            **Vendor Keliling**
            - Menggunakan ikat pinggang uang dengan saku terpisah untuk denominasi berbeda
            - Mengambil foto tagihan besar saat menerimanya untuk mencegah perselisihan
            - Membuat laporan akhir hari yang membandingkan catatan digital dengan uang tunai di tangan
            
            **Strategi Implementasi**
            1. Buat dokumen prosedur penanganan uang tunai untuk karyawan
            2. Terapkan sistem "penyetoran uang tunai" untuk mengeluarkan kelebihan uang tunai dari kasir
            3. Kembangkan formulir standar untuk merekonsiliasi uang tunai di akhir setiap hari
            4. Pertimbangkan sistem point-of-sale dasar yang melacak transaksi tunai
            """
        },
        3: {
            "en": """
            ## Advanced Cash Procedures
            
            **Popular Restaurant**
            - Uses a digital POS system with integrated cash drawer
            - Maintains a cash management log tracking each sale and denomination counts
            - Has specific cash handling roles (cashier, manager for verifications)
            - Conducts surprise cash counts during shifts to prevent theft
            - Uses a secure time-delay safe for large deposits
            
            **Retail Store**
            - Balances registers 3 times daily (opening, mid-day, closing)
            - Uses bank-quality cash counting procedures with independent verification
            - Tracks cash shrinkage rates and investigates discrepancies
            - Has written procedures for handling counterfeit bills
            
            **Implementation Strategy**
            1. Create a cash management schedule with multiple counts throughout the day
            2. Implement a dual-control system for cash verification (two people always count)
            3. Develop written procedures for handling discrepancies
            4. Train staff to recognize counterfeit currency
            5. Use a dedicated safe with drop capabilities for excess cash
            """,
            "id": """
            ## Prosedur Kas Lanjutan
            
            **Restoran Populer**
            - Menggunakan sistem POS digital dengan laci kas terintegrasi
            - Memelihara log manajemen kas yang melacak setiap penjualan dan hitungan denominasi
            - Memiliki peran penanganan kas spesifik (kasir, manajer untuk verifikasi)
            - Melakukan penghitungan kas kejutan selama shift untuk mencegah pencurian
            - Menggunakan brankas dengan penundaan waktu yang aman untuk setoran besar
            
            **Toko Ritel**
            - Menyeimbangkan register 3 kali sehari (pembukaan, tengah hari, penutupan)
            - Menggunakan prosedur penghitungan uang tunai kualitas bank dengan verifikasi independen
            - Melacak tingkat penyusutan uang tunai dan menyelidiki perbedaan
            - Memiliki prosedur tertulis untuk menangani tagihan palsu
            
            **Strategi Implementasi**
            1. Buat jadwal manajemen kas dengan beberapa hitungan sepanjang hari
            2. Terapkan sistem kontrol ganda untuk verifikasi uang tunai (dua orang selalu menghitung)
            3. Kembangkan prosedur tertulis untuk menangani perbedaan
            4. Latih staf untuk mengenali mata uang palsu
            5. Gunakan brankas khusus dengan kemampuan penyetoran untuk kelebihan uang tunai
            """
        },
        4: {
            "en": """
            ## Professional Cash Security
            
            **Small Supermarket**
            - Uses smart safes that count and validate bills automatically
            - Implements comprehensive cash handling training for all staff
            - Has strict cash limits at registers with automated alerts
            - Uses armored car service for bank deposits
            - Conducts daily reconciliation of POS data with physical cash
            
            **Mall Kiosk Business**
            - Employs end-to-end cash tracking from customer to bank deposit
            - Uses tamper-evident deposit bags with unique serial numbers
            - Maintains cash verification logs requiring dual signatures
            - Has detailed procedures for cash variances with escalation protocols
            
            **Implementation Strategy**
            1. Invest in a more secure safe with drop slot and time-delay features
            2. Create a cash handling manual with clear procedures for all scenarios
            3. Implement a cash discrepancy reporting system with threshold triggers
            4. Consider cash management services from your bank for larger deposits
            5. Train managers on cash investigation procedures
            """,
            "id": """
            ## Keamanan Kas Profesional
            
            **Supermarket Kecil**
            - Menggunakan brankas pintar yang menghitung dan memvalidasi tagihan secara otomatis
            - Menerapkan pelatihan penanganan uang tunai komprehensif untuk semua staf
            - Memiliki batas uang tunai yang ketat di kasir dengan peringatan otomatis
            - Menggunakan layanan mobil lapis baja untuk setoran bank
            - Melakukan rekonsiliasi harian data POS dengan uang tunai fisik
            
            **Bisnis Kios Mal**
            - Menggunakan pelacakan uang tunai end-to-end dari pelanggan hingga setoran bank
            - Menggunakan tas setoran anti-rusak dengan nomor seri unik
            - Memelihara log verifikasi uang tunai yang memerlukan tanda tangan ganda
            - Memiliki prosedur terperinci untuk varian uang tunai dengan protokol eskalasi
            
            **Strategi Implementasi**
            1. Investasikan pada brankas yang lebih aman dengan slot drop dan fitur penundaan waktu
            2. Buat manual penanganan uang tunai dengan prosedur yang jelas untuk semua skenario
            3. Terapkan sistem pelaporan perbedaan uang tunai dengan pemicu ambang batas
            4. Pertimbangkan layanan manajemen uang tunai dari bank Anda untuk setoran yang lebih besar
            5. Latih manajer tentang prosedur investigasi uang tunai
            """
        },
        5: {
            "en": """
            ## Enterprise Cash Management
            
            **Multi-Branch Retail Chain**
            - Utilizes networked cash management system across all locations
            - Implements predictive cash forecasting for optimized cash-on-hand
            - Uses real-time cash monitoring with automated exception alerts
            - Employs smart safes with bank-integration for provisional credit
            - Conducts cash handling audits with statistical analysis
            
            **Large Food Market**
            - Uses cash recyclers that dispense change and accept deposits
            - Implements biometric access controls for cash storage areas
            - Monitors cash metrics including handling time and error rates
            - Has centralized cash management team monitoring all locations
            - Employs cashless transaction incentives to reduce cash handling
            
            **Implementation Strategy**
            1. Consider cash recycling technology if cash volume justifies the investment
            2. Implement a system for forecasting cash needs by day of week/season
            3. Develop key performance indicators for cash handling efficiency
            4. Create cash handling certification program for staff
            5. Consider banking relationships that offer provisional credit or same-day deposits
            """,
            "id": """
            ## Manajemen Kas Enterprise
            
            **Rantai Ritel Multi-Cabang**
            - Menggunakan sistem manajemen uang tunai yang terhubung di semua lokasi
            - Menerapkan perkiraan uang tunai prediktif untuk mengoptimalkan uang tunai di tangan
            - Menggunakan pemantauan uang tunai real-time dengan peringatan pengecualian otomatis
            - Menggunakan brankas pintar dengan integrasi bank untuk kredit sementara
            - Melakukan audit penanganan uang tunai dengan analisis statistik
            
            **Pasar Makanan Besar**
            - Menggunakan daur ulang uang tunai yang mengeluarkan perubahan dan menerima setoran
            - Menerapkan kontrol akses biometrik untuk area penyimpanan uang tunai
            - Memantau metrik uang tunai termasuk waktu penanganan dan tingkat kesalahan
            - Memiliki tim manajemen uang tunai terpusat yang memantau semua lokasi
            - Menggunakan insentif transaksi tanpa uang tunai untuk mengurangi penanganan uang tunai
            
            **Strategi Implementasi**
            1. Pertimbangkan teknologi daur ulang uang tunai jika volume uang tunai membenarkan investasi
            2. Terapkan sistem untuk memperkirakan kebutuhan uang tunai berdasarkan hari dalam seminggu/musim
            3. Kembangkan indikator kinerja utama untuk efisiensi penanganan uang tunai
            4. Buat program sertifikasi penanganan uang tunai untuk staf
            5. Pertimbangkan hubungan perbankan yang menawarkan kredit sementara atau setoran hari yang sama
            """
        }
    },
    "pricing_strategy": {
        1: {
            "en": """
            ## Simple Pricing Approaches
            
            **Local Vegetable Vendor**
            - Adds 30% to the wholesale market price for all vegetables
            - Rounds prices to the nearest 500 Rp for easy calculations
            - Offers slight discounts for bulk purchases
            
            **Neighborhood Shop**
            - Uses standard 25% markup on packaged goods
            - Prices commonly compared items (rice, oil, sugar) competitively
            - Adds higher markup (40-50%) on unique or specialty products
            
            **Implementation Strategy**
            1. Calculate your true product costs (purchase price + transportation + storage)
            2. Research competitors' prices for similar products
            3. Start with a standard markup percentage based on your industry
            4. Adjust prices to end in 9s or 5s for psychological appeal
            """,
            "id": """
            ## Pendekatan Harga Sederhana
            
            **Penjual Sayuran Lokal**
            - Menambahkan 30% ke harga pasar grosir untuk semua sayuran
            - Membulatkan harga ke 500 Rp terdekat untuk perhitungan mudah
            - Menawarkan sedikit diskon untuk pembelian dalam jumlah besar
            
            **Toko Lingkungan**
            - Menggunakan markup standar 25% pada barang kemasan
            - Harga barang yang sering dibandingkan (beras, minyak, gula) secara kompetitif
            - Menambahkan markup lebih tinggi (40-50%) pada produk unik atau khusus
            
            **Strategi Implementasi**
            1. Hitung biaya produk sebenarnya (harga pembelian + transportasi + penyimpanan)
            2. Riset harga pesaing untuk produk serupa
            3. Mulai dengan persentase markup standar berdasarkan industri Anda
            4. Sesuaikan harga untuk diakhiri dengan angka 9 atau 5 untuk daya tarik psikologis
            """
        },
        2: {
            "en": """
            ## Category-Based Pricing
            
            **Convenience Store**
            - Uses different markup percentages for different product categories:
              - Beverages: 40-50% markup (high turnover)
              - Snacks: 35-45% markup (impulse purchases)
              - Household basics: 25-30% markup (price-sensitive)
            - Creates bundle deals (drink + snack) at slight discount
            
            **Cosmetics Shop**
            - Prices premium brands at manufacturer's suggested retail price
            - Offers house brands at 30% below comparable name brands
            - Creates "good-better-best" pricing tiers within each category
            
            **Implementation Strategy**
            1. Group your products into logical categories based on customer perception
            2. Research typical margins for each category in your industry
            3. Create a pricing matrix with different markup strategies by category
            4. Test bundle pricing on complementary products
            """,
            "id": """
            ## Penetapan Harga Berbasis Kategori
            
            **Toko Kelontong**
            - Menggunakan persentase markup berbeda untuk kategori produk berbeda:
              - Minuman: markup 40-50% (perputaran tinggi)
              - Camilan: markup 35-45% (pembelian impulsif)
              - Kebutuhan rumah tangga dasar: markup 25-30% (sensitif terhadap harga)
            - Membuat penawaran bundel (minuman + camilan) dengan sedikit diskon
            
            **Toko Kosmetik**
            - Menetapkan harga merek premium pada harga eceran yang disarankan produsen
            - Menawarkan merek rumah 30% di bawah merek terkenal yang sebanding
            - Membuat tingkatan harga "baik-lebih baik-terbaik" dalam setiap kategori
            
            **Strategi Implementasi**
            1. Kelompokkan produk Anda ke dalam kategori logis berdasarkan persepsi pelanggan
            2. Riset margin tipikal untuk setiap kategori di industri Anda
            3. Buat matriks harga dengan strategi markup berbeda berdasarkan kategori
            4. Uji harga bundel pada produk komplementer
            """
        },
        3: {
            "en": """
            ## Competitive Pricing Strategies
            
            **Cell Phone Shop**
            - Matches competitor prices on identical models (price matching)
            - Makes profit on accessories with 50-70% margins
            - Offers value-added services like screen protection installation
            - Uses loss leaders (products priced below cost) to drive store traffic
            
            **Clothing Retailer**
            - Researches competitor pricing weekly for comparable items
            - Positions most items 5-10% below department store prices
            - Uses dynamic pricing during slow periods (midweek specials)
            - Increases margins on exclusive items not available elsewhere
            
            **Implementation Strategy**
            1. Identify your key value items (KVIs) that customers use to compare prices
            2. Create a regular schedule for competitor price checks on these items
            3. Develop a price matching policy with clear guidelines
            4. Identify high-margin products that can balance lower margins on competitive items
            5. Create a promotional calendar with planned discount periods
            """,
            "id": """
            ## Strategi Harga Kompetitif
            
            **Toko Ponsel**
            - Menyamakan harga pesaing pada model identik (pencocokan harga)
            - Menghasilkan keuntungan pada aksesoris dengan margin 50-70%
            - Menawarkan layanan nilai tambah seperti pemasangan pelindung layar
            - Menggunakan loss leader (produk dengan harga di bawah biaya) untuk mendorong lalu lintas toko
            
            **Pengecer Pakaian**
            - Meneliti harga pesaing mingguan untuk item yang sebanding
            - Memposisikan sebagian besar item 5-10% di bawah harga department store
            - Menggunakan harga dinamis selama periode lambat (promo tengah minggu)
            - Meningkatkan margin pada item eksklusif yang tidak tersedia di tempat lain
            
            **Strategi Implementasi**
            1. Identifikasi item nilai kunci (KVI) Anda yang digunakan pelanggan untuk membandingkan harga
            2. Buat jadwal rutin untuk pemeriksaan harga pesaing pada item-item ini
            3. Kembangkan kebijakan pencocokan harga dengan pedoman yang jelas
            4. Identifikasi produk dengan margin tinggi yang dapat menyeimbangkan margin yang lebih rendah pada item kompetitif
            5. Buat kalender promosi dengan periode diskon yang direncanakan
            """
        },
        4: {
            "en": """
            ## Advanced Pricing Techniques
            
            **Electronics Store Chain**
            - Uses price skimming for new technology (high initial prices, gradually lowered)
            - Implements psychological pricing ($499 instead of $500)
            - Creates "good-better-best" options in each product category
            - Offers price-matching guarantee with an additional 5% discount
            - Uses dynamic pricing during holiday seasons versus slow periods
            
            **Specialty Food Shop**
            - Conducts price sensitivity testing for premium products
            - Implements prestige pricing for gourmet and imported items
            - Creates multi-tier pricing based on quality grades
            - Uses anchor pricing (displaying expensive items near moderately-priced ones)
            - Offers subscription pricing for regular customers (5% discount for monthly orders)
            
            **Implementation Strategy**
            1. Segment your product line into distinct price tiers
            2. Experiment with psychological pricing points
            3. Consider seasonal pricing strategies based on demand fluctuations
            4. Test premium pricing on selected products with unique attributes
            5. Evaluate the potential for subscription or membership pricing models
            """,
            "id": """
            ## Teknik Penetapan Harga Lanjutan
            
            **Rantai Toko Elektronik**
            - Menggunakan price skimming untuk teknologi baru (harga awal tinggi, kemudian diturunkan secara bertahap)
            - Menerapkan harga psikologis (Rp 499.000 alih-alih Rp 500.000)
            - Menciptakan opsi "baik-lebih baik-terbaik" di setiap kategori produk
            - Menawarkan jaminan pencocokan harga dengan diskon tambahan 5%
            - Menggunakan harga dinamis selama musim liburan versus periode lambat
            
            **Toko Makanan Khusus**
            - Melakukan pengujian sensitivitas harga untuk produk premium
            - Menerapkan harga prestise untuk item gourmet dan impor
            - Menciptakan harga multi-tier berdasarkan tingkat kualitas
            - Menggunakan harga jangkar (menampilkan item mahal di dekat yang berharga sedang)
            - Menawarkan harga langganan untuk pelanggan tetap (diskon 5% untuk pesanan bulanan)
            
            **Strategi Implementasi**
            1. Segmentasikan lini produk Anda ke dalam tingkatan harga yang berbeda
            2. Bereksperimen dengan poin harga psikologis
            3. Pertimbangkan strategi harga musiman berdasarkan fluktuasi permintaan
            4. Uji harga premium pada produk tertentu dengan atribut unik
            5. Evaluasi potensi untuk model harga langganan atau keanggotaan
            """
        },
        5: {
            "en": """
            ## Strategic Value-Based Pricing
            
            **High-End Furniture Retailer**
            - Implements value-based pricing rather than cost-plus
            - Uses price analytics software to optimize margins
            - Practices dynamic pricing based on real-time demand
            - Offers personalized pricing for loyal customers
            - Develops tiered service packages with premium pricing options
            
            **Multi-Location Restaurant**
            - Uses menu engineering to analyze profitability and popularity of each dish
            - Implements different pricing in different locations based on local economics
            - Adjusts prices based on elasticity measurements (how price changes affect sales)
            - Uses decoy pricing (strategically priced options that make others look better)
            - Tests new pricing strategies in single locations before wider rollout
            
            **Implementation Strategy**
            1. Develop a systematic approach to measure customer value perception
            2. Identify customer segments with different price sensitivities
            3. Create a framework for testing price elasticity in your market
            4. Implement tools to measure the impact of price changes on sales volume
            5. Develop a pricing optimization model that balances revenue, profit, and volume
            6. Consider professional pricing software or consulting for comprehensive strategy
            """,
            "id": """
            ## Penetapan Harga Strategis Berbasis Nilai
            
            **Pengecer Furnitur Kelas Atas**
            - Menerapkan penetapan harga berbasis nilai daripada berdasarkan biaya plus
            - Menggunakan perangkat lunak analitik harga untuk mengoptimalkan margin
            - Mempraktikkan harga dinamis berdasarkan permintaan real-time
            - Menawarkan harga yang dipersonalisasi untuk pelanggan setia
            - Mengembangkan paket layanan berjenjang dengan opsi harga premium
            
            **Restoran Multi-Lokasi**
            - Menggunakan rekayasa menu untuk menganalisis profitabilitas dan popularitas setiap hidangan
            - Menerapkan harga berbeda di lokasi berbeda berdasarkan ekonomi lokal
            - Menyesuaikan harga berdasarkan pengukuran elastisitas (bagaimana perubahan harga memengaruhi penjualan)
            - Menggunakan harga umpan (opsi yang dihargai secara strategis yang membuat yang lain terlihat lebih baik)
            - Menguji strategi harga baru di lokasi tunggal sebelum penerapan yang lebih luas
            
            **Strategi Implementasi**
            1. Kembangkan pendekatan sistematis untuk mengukur persepsi nilai pelanggan
            2. Identifikasi segmen pelanggan dengan sensitivitas harga yang berbeda
            3. Buat kerangka kerja untuk menguji elastisitas harga di pasar Anda
            4. Terapkan alat untuk mengukur dampak perubahan harga pada volume penjualan
            5. Kembangkan model optimasi harga yang menyeimbangkan pendapatan, keuntungan, dan volume
            6. Pertimbangkan perangkat lunak atau konsultasi harga profesional untuk strategi komprehensif
            """
        }
    }
}

def get_tips_for_skill(skill_key, level):
    """Get tips for a specific skill at a specific level.
    
    Args:
        skill_key (str): Skill identifier
        level (int): Skill level
    
    Returns:
        list: List of tips or empty list if none available
    """
    if skill_key not in SKILL_TIPS:
        return []
    
    # Convert level to int and cap at 5
    level_int = min(5, max(1, int(level)))
    
    # Get all tips for this level and below
    all_tips = []
    for i in range(1, level_int + 1):
        if i in SKILL_TIPS[skill_key]:
            all_tips.extend(SKILL_TIPS[skill_key][i])
    
    return all_tips

def get_real_world_applications(skill_key, level):
    """Get real-world applications for a specific skill at a specific level.
    
    Args:
        skill_key (str): Skill identifier
        level (int): Skill level
    
    Returns:
        dict: Dictionary with language keys and content or None if not available
    """
    if skill_key not in REAL_WORLD_APPLICATIONS:
        return None
    
    # Convert level to int and cap at 5
    level_int = min(5, max(1, int(level)))
    
    # Find the closest level that has content
    while level_int > 0:
        if level_int in REAL_WORLD_APPLICATIONS[skill_key]:
            return REAL_WORLD_APPLICATIONS[skill_key][level_int]
        level_int -= 1
    
    return None

def display_pro_tip(tip):
    """Display a professional tip with styling.
    
    Args:
        tip (dict): Tip data with title and content
    """
    lang = get_config("app.default_language") or "en"
    
    # Get title and content in the right language
    title = tip["title"][lang] if lang in tip["title"] else tip["title"]["en"]
    content = tip["content"][lang] if lang in tip["content"] else tip["content"]["en"]
    
    # Display the tip
    st.markdown(f"""
    <div style="background-color: #E8F5E9; border-left: 4px solid #66BB6A; 
         padding: 15px; margin-bottom: 15px; border-radius: 4px;">
        <h4 style="color: #2E7D32; margin: 0 0 10px 0;">💡 {title}</h4>
        <p style="margin: 0;">{content}</p>
    </div>
    """, unsafe_allow_html=True)