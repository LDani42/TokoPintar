"""
Interactive learning exercises for Toko Pintar application.
Provides scenario-based practice for business skills with immediate feedback.
"""
import streamlit as st
import random
from utils.config import get_config

# Interactive exercises by skill and level
INTERACTIVE_EXERCISES = {
    "inventory_management": {
        1: [
            {
                "title": {
                    "en": "Basic Inventory Count",
                    "id": "Penghitungan Inventaris Dasar"
                },
                "scenario": {
                    "en": "You have 15 bottles of shampoo on display and 10 bottles in storage. A customer buys 3 bottles. How many total bottles do you have now?",
                    "id": "Anda memiliki 15 botol sampo di display dan 10 botol di penyimpanan. Seorang pelanggan membeli 3 botol. Berapa total botol yang Anda miliki sekarang?"
                },
                "options": {
                    "en": ["22 bottles", "25 bottles", "18 bottles", "28 bottles"],
                    "id": ["22 botol", "25 botol", "18 botol", "28 botol"]
                },
                "correct_answer": 0,
                "explanation": {
                    "en": "15 bottles (display) + 10 bottles (storage) - 3 bottles (sold) = 22 bottles total remaining.",
                    "id": "15 botol (display) + 10 botol (penyimpanan) - 3 botol (terjual) = 22 botol total yang tersisa."
                }
            },
            {
                "title": {
                    "en": "Product Rotation",
                    "id": "Rotasi Produk"
                },
                "scenario": {
                    "en": "You receive 10 new bottles of cooking oil with expiration dates 6 months from now. You already have 5 bottles that expire in 2 months. How should you arrange them on the shelf?",
                    "id": "Anda menerima 10 botol minyak goreng baru dengan tanggal kedaluwarsa 6 bulan dari sekarang. Anda sudah memiliki 5 botol yang kedaluwarsa dalam 2 bulan. Bagaimana seharusnya Anda mengaturnya di rak?"
                },
                "options": {
                    "en": [
                        "Place older bottles (2-month expiry) at the front, newer bottles at the back",
                        "Place newer bottles (6-month expiry) at the front for a fresher look",
                        "Mix them randomly on the shelf",
                        "Keep the older bottles in storage and only display the new ones"
                    ],
                    "id": [
                        "Tempatkan botol yang lebih lama (kedaluwarsa 2 bulan) di depan, botol yang lebih baru di belakang",
                        "Tempatkan botol yang lebih baru (kedaluwarsa 6 bulan) di depan untuk tampilan yang lebih segar",
                        "Campurkan secara acak di rak",
                        "Simpan botol yang lebih lama di penyimpanan dan hanya tampilkan yang baru"
                    ]
                },
                "correct_answer": 0,
                "explanation": {
                    "en": "Always follow the FIFO (First In, First Out) principle for perishable goods. Place older inventory at the front so it sells first, reducing the risk of expired products.",
                    "id": "Selalu ikuti prinsip FIFO (First In, First Out) untuk barang yang mudah rusak. Tempatkan inventaris yang lebih lama di depan agar terjual lebih dulu, mengurangi risiko produk kedaluwarsa."
                }
            }
        ],
        3: [
            {
                "title": {
                    "en": "Inventory Analysis",
                    "id": "Analisis Inventaris"
                },
                "scenario": {
                    "en": "You analyze your inventory and find these patterns:\n- Product A: Sells 50 units/month, costs 10,000 Rp/unit\n- Product B: Sells 20 units/month, costs 50,000 Rp/unit\n- Product C: Sells 5 units/month, costs 200,000 Rp/unit\nWhich product should receive the most frequent inventory counts?",
                    "id": "Anda menganalisis inventaris Anda dan menemukan pola berikut:\n- Produk A: Terjual 50 unit/bulan, biaya 10.000 Rp/unit\n- Produk B: Terjual 20 unit/bulan, biaya 50.000 Rp/unit\n- Produk C: Terjual 5 unit/bulan, biaya 200.000 Rp/unit\nProduk mana yang harus menerima penghitungan inventaris paling sering?"
                },
                "options": {
                    "en": ["Product C", "Product B", "Product A", "All should be counted equally often"],
                    "id": ["Produk C", "Produk B", "Produk A", "Semua harus dihitung dengan frekuensi yang sama"]
                },
                "correct_answer": 0,
                "explanation": {
                    "en": "Product C has the highest value per unit (200,000 Rp) and represents the highest financial risk if stolen or lost. High-value items should be counted more frequently, following the ABC analysis approach where 'A' items (highest value) receive the most attention.",
                    "id": "Produk C memiliki nilai tertinggi per unit (200.000 Rp) dan merepresentasikan risiko finansial tertinggi jika dicuri atau hilang. Item bernilai tinggi harus dihitung lebih sering, mengikuti pendekatan analisis ABC di mana item 'A' (nilai tertinggi) menerima perhatian paling banyak."
                }
            }
        ],
        5: [
            {
                "title": {
                    "en": "Inventory Turnover Analysis",
                    "id": "Analisis Perputaran Inventaris"
                },
                "scenario": {
                    "en": "Your store has the following data for last quarter:\n- Average Inventory Value: 25,000,000 Rp\n- Cost of Goods Sold: 75,000,000 Rp\n- Operating Period: 90 days\nWhat is your inventory turnover ratio, and what does it mean?",
                    "id": "Toko Anda memiliki data berikut untuk kuartal terakhir:\n- Nilai Rata-rata Inventaris: 25.000.000 Rp\n- Harga Pokok Penjualan: 75.000.000 Rp\n- Periode Operasi: 90 hari\nBerapa rasio perputaran inventaris Anda, dan apa artinya?"
                },
                "options": {
                    "en": [
                        "3.0 - You sell through your entire inventory 3 times per quarter, indicating good turnover",
                        "0.33 - You sell through only 33% of your inventory each quarter, indicating slow movement",
                        "12.0 - You sell through your entire inventory 12 times per year, which is excellent",
                        "30 - You replace your inventory every 30 days on average"
                    ],
                    "id": [
                        "3,0 - Anda menjual seluruh inventaris Anda 3 kali per kuartal, menunjukkan perputaran yang baik",
                        "0,33 - Anda menjual hanya 33% dari inventaris Anda setiap kuartal, menunjukkan pergerakan lambat",
                        "12,0 - Anda menjual seluruh inventaris Anda 12 kali per tahun, yang sangat baik",
                        "30 - Anda mengganti inventaris Anda setiap 30 hari rata-rata"
                    ]
                },
                "correct_answer": 0,
                "explanation": {
                    "en": "Inventory Turnover Ratio = Cost of Goods Sold ÷ Average Inventory Value\n= 75,000,000 ÷ 25,000,000 = 3.0\n\nThis means you sell through and replace your entire inventory 3 times per quarter (or 12 times per year), which indicates healthy inventory movement and efficient capital use.",
                    "id": "Rasio Perputaran Inventaris = Harga Pokok Penjualan ÷ Nilai Rata-rata Inventaris\n= 75.000.000 ÷ 25.000.000 = 3,0\n\nIni berarti Anda menjual dan mengganti seluruh inventaris Anda 3 kali per kuartal (atau 12 kali per tahun), yang menunjukkan pergerakan inventaris yang sehat dan penggunaan modal yang efisien."
                }
            }
        ]
    },
    "cash_handling": {
        1: [
            {
                "title": {
                    "en": "Making Change",
                    "id": "Memberikan Kembalian"
                },
                "scenario": {
                    "en": "A customer buys items totaling 37,500 Rp and gives you a 50,000 Rp bill. What is the correct change?",
                    "id": "Seorang pelanggan membeli barang seharga total 37.500 Rp dan memberi Anda uang 50.000 Rp. Berapa kembalian yang benar?"
                },
                "options": {
                    "en": ["12,500 Rp", "13,500 Rp", "12,000 Rp", "13,000 Rp"],
                    "id": ["12.500 Rp", "13.500 Rp", "12.000 Rp", "13.000 Rp"]
                },
                "correct_answer": 0,
                "explanation": {
                    "en": "50,000 Rp - 37,500 Rp = 12,500 Rp\n\nThe best way to count this change back would be:\n- One 10,000 Rp note\n- One 2,000 Rp note\n- One 500 Rp coin",
                    "id": "50.000 Rp - 37.500 Rp = 12.500 Rp\n\nCara terbaik untuk menghitung kembalian ini adalah:\n- Satu lembar 10.000 Rp\n- Satu lembar 2.000 Rp\n- Satu koin 500 Rp"
                }
            }
        ],
        3: [
            {
                "title": {
                    "en": "Cash Reconciliation",
                    "id": "Rekonsiliasi Kas"
                },
                "scenario": {
                    "en": "At the end of the day, your cash register shows total sales of 3,450,000 Rp. You started with 500,000 Rp in your cash drawer. You count 3,870,000 Rp at closing. Is there a discrepancy, and if so, how much?",
                    "id": "Di akhir hari, kasir Anda menunjukkan total penjualan 3.450.000 Rp. Anda mulai dengan 500.000 Rp di laci kas Anda. Anda menghitung 3.870.000 Rp saat penutupan. Apakah ada perbedaan, dan jika ya, berapa banyak?"
                },
                "options": {
                    "en": [
                        "80,000 Rp short", 
                        "80,000 Rp over", 
                        "There is no discrepancy", 
                        "370,000 Rp over"
                    ],
                    "id": [
                        "Kurang 80.000 Rp", 
                        "Lebih 80.000 Rp", 
                        "Tidak ada perbedaan", 
                        "Lebih 370.000 Rp"
                    ]
                },
                "correct_answer": 1,
                "explanation": {
                    "en": "Expected cash at end of day = Starting cash + Sales\n= 500,000 Rp + 3,450,000 Rp = 3,950,000 Rp\n\nActual cash = 3,870,000 Rp\n\nDiscrepancy = 3,950,000 Rp - 3,870,000 Rp = 80,000 Rp short\n\nThis means there is 80,000 Rp missing from what should be in the drawer. This requires investigation.",
                    "id": "Uang tunai yang diharapkan di akhir hari = Uang awal + Penjualan\n= 500.000 Rp + 3.450.000 Rp = 3.950.000 Rp\n\nUang tunai aktual = 3.870.000 Rp\n\nPerbedaan = 3.950.000 Rp - 3.870.000 Rp = 80.000 Rp kurang\n\nIni berarti ada 80.000 Rp yang hilang dari yang seharusnya ada di laci. Ini memerlukan penyelidikan."
                }
            }
        ]
    },
    "pricing_strategy": {
        1: [
            {
                "title": {
                    "en": "Basic Margin Calculation",
                    "id": "Perhitungan Margin Dasar"
                },
                "scenario": {
                    "en": "You buy a product for 8,000 Rp. You want to achieve a 25% profit margin on the selling price. What should your selling price be?",
                    "id": "Anda membeli produk seharga 8.000 Rp. Anda ingin mencapai margin keuntungan 25% pada harga jual. Berapa harga jual Anda seharusnya?"
                },
                "options": {
                    "en": ["10,667 Rp", "10,000 Rp", "12,000 Rp", "9,600 Rp"],
                    "id": ["10.667 Rp", "10.000 Rp", "12.000 Rp", "9.600 Rp"]
                },
                "correct_answer": 0,
                "explanation": {
                    "en": "To achieve a 25% profit margin on the selling price:\n\nSelling Price = Cost ÷ (1 - Desired Margin)\nSelling Price = 8,000 ÷ (1 - 0.25)\nSelling Price = 8,000 ÷ 0.75 = 10,667 Rp\n\nAt this price, the profit is 2,667 Rp, which is 25% of the 10,667 Rp selling price.",
                    "id": "Untuk mencapai margin keuntungan 25% pada harga jual:\n\nHarga Jual = Biaya ÷ (1 - Margin yang Diinginkan)\nHarga Jual = 8.000 ÷ (1 - 0,25)\nHarga Jual = 8.000 ÷ 0,75 = 10.667 Rp\n\nPada harga ini, keuntungannya adalah 2.667 Rp, yang merupakan 25% dari harga jual 10.667 Rp."
                }
            },
            {
                "title": {
                    "en": "Markup vs. Margin",
                    "id": "Markup vs. Margin"
                },
                "scenario": {
                    "en": "You buy a product for 12,000 Rp and sell it for 15,000 Rp. What is your markup percentage and your profit margin percentage?",
                    "id": "Anda membeli produk seharga 12.000 Rp dan menjualnya seharga 15.000 Rp. Berapa persentase markup dan persentase margin keuntungan Anda?"
                },
                "options": {
                    "en": [
                        "25% markup, 20% profit margin",
                        "20% markup, 25% profit margin",
                        "25% markup, 25% profit margin",
                        "20% markup, 20% profit margin"
                    ],
                    "id": [
                        "25% markup, 20% margin keuntungan",
                        "20% markup, 25% margin keuntungan",
                        "25% markup, 25% margin keuntungan",
                        "20% markup, 20% margin keuntungan"
                    ]
                },
                "correct_answer": 0,
                "explanation": {
                    "en": "Markup percentage = (Selling Price - Cost) ÷ Cost\n= (15,000 - 12,000) ÷ 12,000\n= 3,000 ÷ 12,000 = 0.25 = 25%\n\nProfit margin percentage = (Selling Price - Cost) ÷ Selling Price\n= (15,000 - 12,000) ÷ 15,000\n= 3,000 ÷ 15,000 = 0.20 = 20%\n\nThis illustrates the important difference between markup (based on cost) and margin (based on selling price).",
                    "id": "Persentase markup = (Harga Jual - Biaya) ÷ Biaya\n= (15.000 - 12.000) ÷ 12.000\n= 3.000 ÷ 12.000 = 0,25 = 25%\n\nPersentase margin keuntungan = (Harga Jual - Biaya) ÷ Harga Jual\n= (15.000 - 12.000) ÷ 15.000\n= 3.000 ÷ 15.000 = 0,20 = 20%\n\nIni mengilustrasikan perbedaan penting antara markup (berdasarkan biaya) dan margin (berdasarkan harga jual)."
                }
            }
        ],
        3: [
            {
                "title": {
                    "en": "Price Elasticity",
                    "id": "Elastisitas Harga"
                },
                "scenario": {
                    "en": "You currently sell a product for 10,000 Rp and sell 100 units per week. You increase the price to 12,000 Rp and sales drop to 80 units per week. Is this product elastic or inelastic?",
                    "id": "Anda saat ini menjual produk seharga 10.000 Rp dan menjual 100 unit per minggu. Anda menaikkan harga menjadi 12.000 Rp dan penjualan turun menjadi 80 unit per minggu. Apakah produk ini elastis atau inelastis?"
                },
                "options": {
                    "en": [
                        "Elastic - the percentage change in quantity exceeds the percentage change in price", 
                        "Inelastic - the percentage change in price exceeds the percentage change in quantity", 
                        "Unit elastic - the percentage changes are equal", 
                        "Cannot be determined from this information"
                    ],
                    "id": [
                        "Elastis - persentase perubahan kuantitas melebihi persentase perubahan harga", 
                        "Inelastis - persentase perubahan harga melebihi persentase perubahan kuantitas", 
                        "Elastis unit - persentase perubahan sama", 
                        "Tidak dapat ditentukan dari informasi ini"
                    ]
                },
                "correct_answer": 0,
                "explanation": {
                    "en": "Price Elasticity = (% Change in Quantity) ÷ (% Change in Price)\n\n% Change in Price = (12,000 - 10,000) ÷ 10,000 = 0.2 = 20%\n% Change in Quantity = (80 - 100) ÷ 100 = -0.2 = -20%\n\nElasticity = |-0.2 ÷ 0.2| = 1.0\n\nSince the elasticity is 1.0, this product is actually unit elastic, meaning the percentage change in quantity equals the percentage change in price. This is the borderline between elastic and inelastic.\n\nImportantly, total revenue remains the same (100 × 10,000 = 1,000,000 and 80 × 12,000 = 960,000).",
                    "id": "Elastisitas Harga = (% Perubahan Kuantitas) ÷ (% Perubahan Harga)\n\n% Perubahan Harga = (12.000 - 10.000) ÷ 10.000 = 0,2 = 20%\n% Perubahan Kuantitas = (80 - 100) ÷ 100 = -0,2 = -20%\n\nElastisitas = |-0,2 ÷ 0,2| = 1,0\n\nKarena elastisitas adalah 1,0, produk ini sebenarnya elastis unit, yang berarti persentase perubahan kuantitas sama dengan persentase perubahan harga. Ini adalah perbatasan antara elastis dan inelastis.\n\nYang penting, total pendapatan tetap sama (100 × 10.000 = 1.000.000 dan 80 × 12.000 = 960.000)."
                }
            },
            {
                "title": {
                    "en": "Break-Even Analysis",
                    "id": "Analisis Titik Impas"
                },
                "scenario": {
                    "en": "Your shop has monthly fixed costs of 5,000,000 Rp. You sell a product that costs you 15,000 Rp and you sell it for 25,000 Rp. How many units must you sell each month to break even?",
                    "id": "Toko Anda memiliki biaya tetap bulanan 5.000.000 Rp. Anda menjual produk yang biayanya 15.000 Rp dan Anda menjualnya seharga 25.000 Rp. Berapa unit yang harus Anda jual setiap bulan untuk mencapai titik impas?"
                },
                "options": {
                    "en": ["500 units", "200 units", "333 units", "250 units"],
                    "id": ["500 unit", "200 unit", "333 unit", "250 unit"]
                },
                "correct_answer": 0,
                "explanation": {
                    "en": "Break-Even Quantity = Fixed Costs ÷ Contribution Margin per Unit\n\nContribution Margin per Unit = Selling Price - Variable Cost per Unit\n= 25,000 Rp - 15,000 Rp = 10,000 Rp\n\nBreak-Even Quantity = 5,000,000 Rp ÷ 10,000 Rp = 500 units\n\nYou must sell 500 units per month to cover your fixed costs. Each unit contributes 10,000 Rp toward fixed costs, so 500 units contribute the full 5,000,000 Rp needed.",
                    "id": "Kuantitas Titik Impas = Biaya Tetap ÷ Margin Kontribusi per Unit\n\nMargin Kontribusi per Unit = Harga Jual - Biaya Variabel per Unit\n= 25.000 Rp - 15.000 Rp = 10.000 Rp\n\nKuantitas Titik Impas = 5.000.000 Rp ÷ 10.000 Rp = 500 unit\n\nAnda harus menjual 500 unit per bulan untuk menutupi biaya tetap Anda. Setiap unit menyumbang 10.000 Rp untuk biaya tetap, jadi 500 unit menyumbang 5.000.000 Rp penuh yang dibutuhkan."
                }
            }
        ]
    }
}

def get_exercise_for_skill(skill_key, level):
    """Get an interactive exercise for a specific skill at a specific level.
    
    Args:
        skill_key (str): Skill identifier
        level (int): Skill level (1-5)
        
    Returns:
        dict: Exercise data or None if not available
    """
    if skill_key not in INTERACTIVE_EXERCISES:
        return None
    
    # Convert level to int and cap at 5
    level_int = min(5, max(1, int(level)))
    
    # Find the closest level that has exercises
    available_levels = sorted(INTERACTIVE_EXERCISES[skill_key].keys())
    
    # If no levels are available, return None
    if not available_levels:
        return None
    
    # Find the closest available level that doesn't exceed the requested level
    closest_level = None
    for l in available_levels:
        if l <= level_int and (closest_level is None or l > closest_level):
            closest_level = l
    
    # If we couldn't find a level below or equal to the requested level,
    # just take the lowest available level
    if closest_level is None:
        closest_level = min(available_levels)
    
    # Get exercises for this level
    exercises = INTERACTIVE_EXERCISES[skill_key][closest_level]
    
    # Return a random exercise if available
    if exercises:
        return random.choice(exercises)
    return None

def show_interactive_exercise(skill_key, level):
    """Display an interactive exercise with options and feedback.
    
    Args:
        skill_key (str): Skill identifier
        level (int): Skill level
        
    Returns:
        bool: True if the exercise was displayed, False otherwise
    """
    exercise = get_exercise_for_skill(skill_key, level)
    if not exercise:
        return False
    
    lang = get_config("app.default_language") or "en"
    
    # Get title and scenario in the right language
    title = exercise["title"][lang] if lang in exercise["title"] else exercise["title"]["en"]
    scenario = exercise["scenario"][lang] if lang in exercise["scenario"] else exercise["scenario"]["en"]
    options = exercise["options"][lang] if lang in exercise["options"] else exercise["options"]["en"]
    
    # Determine the correct answer
    correct_answer = exercise["correct_answer"]
    explanation = exercise["explanation"][lang] if lang in exercise["explanation"] else exercise["explanation"]["en"]
    
    # Create a unique exercise key for the session state
    exercise_key = f"exercise_{skill_key}_{level}_{title.replace(' ', '_')}"
    
    # Initialize state for this exercise if needed
    if exercise_key not in st.session_state:
        st.session_state[exercise_key] = {
            "selected_option": None,
            "submitted": False
        }
    
    # Display the exercise
    st.markdown(f"""
    <div style="background-color: #f5f5f5; padding: 20px; border-radius: 10px; margin-bottom: 20px; 
         border-left: 5px solid #7E57C2;">
        <h3 style="color: #7E57C2; margin-top: 0;">{title}</h3>
        <p style="margin-bottom: 20px;">{scenario}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a container for the options
    options_container = st.container()
    
    # Create state for tracking radio button value
    if "selected_option" not in st.session_state[exercise_key]:
        st.session_state[exercise_key]["selected_option"] = None
    
    # Display options as radio buttons
    with options_container:
        selected = st.radio(
            "Select your answer:",
            options,
            key=f"radio_{exercise_key}"
        )
        
        # Get the index of the selected option
        selected_index = options.index(selected) if selected in options else None
        st.session_state[exercise_key]["selected_option"] = selected_index
    
    # Submit button
    submit_text = "Check Answer" if lang == "en" else "Periksa Jawaban"
    if st.button(submit_text, key=f"submit_{exercise_key}"):
        st.session_state[exercise_key]["submitted"] = True
    
    # Display feedback if the user has submitted an answer
    if st.session_state[exercise_key].get("submitted", False) and st.session_state[exercise_key]["selected_option"] is not None:
        is_correct = st.session_state[exercise_key]["selected_option"] == correct_answer
        
        if is_correct:
            st.success("✅ Correct!")
            
            # Calculate skill points (higher levels give more points)
            skill_points = level * 2
            
            # Update skills if this is the first time getting it correct
            if not st.session_state[exercise_key].get("awarded_points", False):
                from utils.skills import update_skills
                update_skills(skill_key, skill_points)
                st.session_state[exercise_key]["awarded_points"] = True
                
                points_text = "points" if lang == "en" else "poin"
                st.markdown(f"🏆 You earned {skill_points} {points_text}!")
        else:
            st.error("❌ Incorrect. Try again!")
        
        # Show explanation
        st.markdown(f"""
        <div style="background-color: #e8f5e9; padding: 15px; border-radius: 8px; margin-top: 15px;">
            <h4 style="margin-top: 0;">Explanation</h4>
            <p style="white-space: pre-line;">{explanation}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Try another button
        another_text = "Try Another Exercise" if lang == "en" else "Coba Latihan Lain"
        if st.button(another_text, key=f"another_{exercise_key}"):
            # Clear the session state for this exercise to get a new one
            if exercise_key in st.session_state:
                del st.session_state[exercise_key]
            st.rerun()
    
    return True

def show_exercise_set(skill_key, count=3):
    """Display a set of interactive exercises for a skill.
    
    Args:
        skill_key (str): Skill identifier
        count (int): Number of exercises to show
        
    Returns:
        int: Number of exercises successfully displayed
    """
    lang = get_config("app.default_language") or "en"
    
    # Get the current skill level
    skill_level = 1
    if hasattr(st.session_state, 'skill_levels') and skill_key in st.session_state.skill_levels:
        skill_level = st.session_state.skill_levels[skill_key]
    
    # Set up exercise tracking in session state
    if "active_exercises" not in st.session_state:
        st.session_state.active_exercises = {
            "skill_key": skill_key,
            "current_index": 0,
            "exercises_shown": 0
        }
    # Reset if we're switching skills
    elif st.session_state.active_exercises["skill_key"] != skill_key:
        st.session_state.active_exercises = {
            "skill_key": skill_key,
            "current_index": 0,
            "exercises_shown": 0
        }
    
    # Display header
    exercises_text = "Interactive Practice Exercises" if lang == "en" else "Latihan Interaktif"
    st.markdown(f"## {exercises_text}")
    
    # Explanation text
    practice_text = "Apply your knowledge to these real-world scenarios. Each correct answer earns skill points!" if lang == "en" else "Terapkan pengetahuan Anda pada skenario dunia nyata ini. Setiap jawaban yang benar mendapatkan poin keterampilan!"
    st.markdown(f"_{practice_text}_")
    
    # Display current exercise
    current_index = st.session_state.active_exercises["current_index"]
    
    # Try to show an exercise at the current skill level
    showed_exercise = show_interactive_exercise(skill_key, skill_level)
    
    # If we successfully showed an exercise, increment the counter
    if showed_exercise:
        st.session_state.active_exercises["exercises_shown"] += 1
    
    # Update progress
    st.markdown("---")
    progress = min(1.0, st.session_state.active_exercises["exercises_shown"] / count)
    
    progress_text = f"Progress: {st.session_state.active_exercises['exercises_shown']}/{count} exercises completed"
    if lang == "id":
        progress_text = f"Kemajuan: {st.session_state.active_exercises['exercises_shown']}/{count} latihan selesai"
    
    st.progress(progress)
    st.caption(progress_text)
    
    return st.session_state.active_exercises["exercises_shown"]