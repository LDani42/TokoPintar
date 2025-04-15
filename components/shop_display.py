"""
Shop visualization components for Toko Pintar application.
"""
import streamlit as st
from utils.config import get_config
from components.progress_dashboard import display_shop_growth_visualization

def display_shop(level=None):
    """Display a visual representation of the shop based on level.
    
    Args:
        level (int, optional): Shop level override. If None, uses session state.
    """
    if level is None:
        level = st.session_state.shop_level if hasattr(st.session_state, 'shop_level') else 1
    
    # Display the growth visualization
    display_shop_growth_visualization()
    
    # Shop images - will be replaced with actual assets
    shop_images = {
        1: "https://via.placeholder.com/800x300.png?text=Small+Shop+Level+1",
        2: "https://via.placeholder.com/800x300.png?text=Improved+Shop+Level+2",
        3: "https://via.placeholder.com/800x300.png?text=Advanced+Shop+Level+3",
        4: "https://via.placeholder.com/800x300.png?text=Professional+Shop+Level+4",
        5: "https://via.placeholder.com/800x300.png?text=Premium+Shop+Level+5"
    }
    
    # Shop descriptions
    shop_descriptions = {
        1: {
            "en": "Your small warung is just starting out with basic items. Keep learning to grow!",
            "id": "Warung kecil Anda baru saja dimulai dengan barang-barang dasar. Terus belajar untuk berkembang!"
        },
        2: {
            "en": "Your shop has better organization and more products. Customers are starting to notice!",
            "id": "Toko Anda memiliki organisasi yang lebih baik dan lebih banyak produk. Pelanggan mulai memperhatikan!"
        },
        3: {
            "en": "Your growing shop now has a good selection of products and improved displays.",
            "id": "Toko Anda yang berkembang sekarang memiliki pilihan produk yang baik dan tampilan yang lebih baik."
        },
        4: {
            "en": "Your shop is now well-established with an excellent inventory and loyal customers.",
            "id": "Toko Anda sekarang mapan dengan inventaris yang sangat baik dan pelanggan yang setia."
        },
        5: {
            "en": "Your premium shop is a neighborhood favorite with the best selection and service!",
            "id": "Toko premium Anda adalah favorit lingkungan dengan pilihan dan layanan terbaik!"
        }
    }
    
    # Shop features by level
    shop_features = {
        1: ["Basic shelving", "Limited inventory", "Simple cash box"],
        2: ["Better organization", "More inventory", "Calculator for transactions"],
        3: ["Product displays", "Varied inventory", "Proper cash register"],
        4: ["Marketing materials", "Full inventory", "Point of sale system"],
        5: ["Premium displays", "Premium products", "Full financial system"]
    }
    
    # Get language preference
    lang = get_config("app.default_language") or "en"
    
    # Display shop image
    st.markdown('<div class="shop-image-container">', unsafe_allow_html=True)
    st.image(shop_images.get(level, shop_images[1]), use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display shop info
    st.markdown(f'<p class="shop-level">Shop Level: {level}/5</p>', unsafe_allow_html=True)
    
    # Description based on language
    description = shop_descriptions.get(level, shop_descriptions[1]).get(lang, shop_descriptions[1]["en"])
    st.markdown(f"<p class='center-text'>{description}</p>", unsafe_allow_html=True)
    
    # Shop features
    if level in shop_features:
        st.markdown("### Shop Features")
        for feature in shop_features[level]:
            st.markdown(f"- {feature}")

def display_shop_upgrade_animation(old_level, new_level):
    """Display an animation for shop level upgrade.
    
    Args:
        old_level (int): Previous shop level
        new_level (int): New shop level
    """
    # Show a celebration
    st.balloons()
    
    # Get language preference
    lang = get_config("app.default_language") or "en"
    
    # Upgrade message
    if lang == "en":
        st.markdown(f"## 🎉 Shop Upgraded to Level {new_level}! 🎉")
        st.markdown("Your business is growing thanks to your improved skills!")
    else:
        st.markdown(f"## 🎉 Toko Ditingkatkan ke Level {new_level}! 🎉")
        st.markdown("Bisnis Anda berkembang berkat peningkatan keterampilan Anda!")
    
    # Show old and new shop side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### Level {old_level}")
        display_shop(old_level)
    
    with col2:
        st.markdown(f"#### Level {new_level}")
        display_shop(new_level)
    
    # Benefits of the upgrade
    st.markdown("### New Benefits")
    
    benefits = {
        2: {
            "en": ["Better organized products", "More customer traffic", "Improved cash handling"],
            "id": ["Produk yang lebih terorganisir", "Lebih banyak lalu lintas pelanggan", "Penanganan uang tunai yang lebih baik"]
        },
        3: {
            "en": ["Product displays", "More variety of goods", "Proper record keeping"],
            "id": ["Tampilan produk", "Lebih banyak variasi barang", "Pembukuan yang tepat"]
        },
        4: {
            "en": ["Marketing materials", "Brand recognition", "Basic financial analysis"],
            "id": ["Materi pemasaran", "Pengenalan merek", "Analisis keuangan dasar"]
        },
        5: {
            "en": ["Premium customer base", "Maximum profitability", "Business sustainability"],
            "id": ["Basis pelanggan premium", "Profitabilitas maksimum", "Keberlanjutan bisnis"]
        }
    }
    
    if new_level in benefits:
        benefit_list = benefits[new_level].get(lang, benefits[new_level]["en"])
        for benefit in benefit_list:
            st.markdown(f"- {benefit}")

def display_shop_inventory(products=None):
    """Display the shop's inventory.
    
    Args:
        products (list, optional): List of product dictionaries. If None, fetches from database.
    """
    if products is None:
        # Fetch products from database
        from utils.db import db
        products = db.get_products()
    
    if not products:
        st.info("No products in inventory yet.")
        return
    
    # Get language preference
    lang = get_config("app.default_language") or "en"
    
    # Display products by category
    categories = set(p["category"] for p in products)
    
    for category in sorted(categories):
        st.markdown(f"### {category}")
        
        # Filter products for this category
        category_products = [p for p in products if p["category"] == category]
        
        # Create a grid display (3 columns)
        cols = st.columns(3)
        
        for i, product in enumerate(category_products):
            with cols[i % 3]:
                # Use localized name if available
                name = product["name_id"] if lang == "id" and product.get("name_id") else product["name"]
                
                # Display product card
                st.markdown(f"""
                <div style="padding: 10px; margin-bottom: 10px; background-color: #f5f5f5; border-radius: 5px;">
                    <strong>{name}</strong><br>
                    Buy: Rp {product["buy_price"]:,}<br>
                    Sell: Rp {product["sell_price"]:,}<br>
                    Margin: {((product["sell_price"] - product["buy_price"]) / product["buy_price"] * 100):.1f}%
                </div>
                """, unsafe_allow_html=True)