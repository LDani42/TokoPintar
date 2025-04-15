"""
Certificates module for Toko Pintar application.
Generates and displays skill certificates for completed learning paths.
"""
import streamlit as st
from datetime import datetime
from utils.config import get_config
from utils.skills import get_skill_name, get_skill_icon

def generate_certificate(path_id, milestone_level):
    """Generate a certificate for a completed learning path milestone.
    
    Args:
        path_id (str): Identifier for the learning path
        milestone_level (int): Level of the completed milestone
    
    Returns:
        dict: Certificate data or None if not eligible
    """
    from components.learning.learning_paths import LEARNING_PATHS, get_path_progress
    
    # Check if path and milestone exist
    if path_id not in LEARNING_PATHS:
        return None
    
    path = LEARNING_PATHS[path_id]
    
    if milestone_level >= len(path["milestones"]):
        return None
    
    milestone = path["milestones"][milestone_level]
    
    # Check if this milestone offers a certificate
    if not milestone.get("certificate", False):
        return None
    
    # Check if user has completed the milestone
    progress = get_path_progress(path_id)
    if progress["current_level"] < milestone_level:
        return None
    
    # Generate certificate
    lang = get_config("app.default_language") or "en"
    
    path_name = path["name"][lang] if lang in path["name"] else path["name"]["en"]
    milestone_name = milestone["name"][lang] if lang in milestone["name"] else milestone["name"]["en"]
    
    certificate = {
        "id": f"{path_id}_{milestone_level}",
        "path_id": path_id,
        "milestone_level": milestone_level,
        "title": f"{path_name}: {milestone_name}",
        "player_name": st.session_state.player_name,
        "issue_date": datetime.now().strftime("%Y-%m-%d"),
        "icon": path["icon"]
    }
    
    # Save to session state if not exists
    if "earned_certificates" not in st.session_state:
        st.session_state.earned_certificates = {}
    
    certificate_id = certificate["id"]
    if certificate_id not in st.session_state.earned_certificates:
        st.session_state.earned_certificates[certificate_id] = certificate
        
        # Save to database if user is logged in
        if hasattr(st.session_state, 'user_id'):
            from utils.db import db
            db_data = {
                "path_id": path_id,
                "milestone_level": milestone_level,
                "certificate_data": certificate
            }
            # Assuming db has add_certificate method
            if hasattr(db, 'add_certificate'):
                db.add_certificate(st.session_state.user_id, certificate_id, db_data)
    
    return certificate

def display_certificate_preview(path_id, milestone_level):
    """Display a preview of the certificate.
    
    Args:
        path_id (str): Identifier for the learning path
        milestone_level (int): Level of the completed milestone
    """
    # Generate/retrieve certificate
    certificate = generate_certificate(path_id, milestone_level)
    if not certificate:
        return
    
    lang = get_config("app.default_language") or "en"
    
    # Get skill information
    from utils.skills import get_skill_name
    skill_name = get_skill_name(path_id, lang)
    
    # Get skill-specific design elements
    skill_colors = {
        "inventory_management": {"primary": "#4CAF50", "secondary": "#E8F5E9", "accent": "#2E7D32"},
        "cash_handling": {"primary": "#FFC107", "secondary": "#FFF8E1", "accent": "#FF8F00"},
        "pricing_strategy": {"primary": "#7E57C2", "secondary": "#EDE7F6", "accent": "#5E35B1"}
    }
    
    colors = skill_colors.get(path_id, {"primary": "#5C6BC0", "secondary": "#E8EAF6", "accent": "#3949AB"})
    
    # Get skill-specific achievements based on level
    skill_achievements = {
        "inventory_management": {
            1: {
                "en": ["Basic inventory counting", "Product organization", "Stock rotation principles"],
                "id": ["Penghitungan inventaris dasar", "Organisasi produk", "Prinsip rotasi stok"]
            },
            3: {
                "en": ["Advanced inventory tracking", "ABC classification", "Inventory forecasting", "Loss prevention"],
                "id": ["Pelacakan inventaris lanjutan", "Klasifikasi ABC", "Perkiraan inventaris", "Pencegahan kerugian"]
            },
            5: {
                "en": ["Inventory optimization", "Just-in-time inventory", "Dynamic reordering", "Multi-location management", "Inventory metrics analysis"],
                "id": ["Optimasi inventaris", "Inventaris just-in-time", "Pemesanan kembali dinamis", "Manajemen multi-lokasi", "Analisis metrik inventaris"]
            }
        },
        "cash_handling": {
            1: {
                "en": ["Basic change making", "Cash counting", "Cash drawer organization"],
                "id": ["Pembuatan kembalian dasar", "Penghitungan tunai", "Organisasi laci kas"]
            },
            3: {
                "en": ["POS system operation", "Cash reconciliation", "Cash security protocols", "Discrepancy resolution"],
                "id": ["Operasi sistem POS", "Rekonsiliasi kas", "Protokol keamanan kas", "Resolusi perbedaan"]
            },
            5: {
                "en": ["Advanced cash management", "Cash flow forecasting", "Bank deposit procedures", "Loss prevention strategies", "Cash handling training"],
                "id": ["Manajemen kas lanjutan", "Peramalan arus kas", "Prosedur setoran bank", "Strategi pencegahan kerugian", "Pelatihan penanganan kas"]
            }
        },
        "pricing_strategy": {
            1: {
                "en": ["Basic markup calculation", "Cost-plus pricing", "Competitor analysis"],
                "id": ["Perhitungan markup dasar", "Penetapan harga biaya-plus", "Analisis pesaing"]
            },
            3: {
                "en": ["Price elasticity principles", "Value-based pricing", "Promotional pricing", "Bundle pricing strategies"],
                "id": ["Prinsip elastisitas harga", "Penetapan harga berbasis nilai", "Penetapan harga promosi", "Strategi penetapan harga bundel"]
            },
            5: {
                "en": ["Advanced pricing optimization", "Dynamic pricing", "Market segmentation", "Price psychology", "Strategic discount planning"],
                "id": ["Optimasi harga lanjutan", "Harga dinamis", "Segmentasi pasar", "Psikologi harga", "Perencanaan diskon strategis"]
            }
        }
    }
    
    # Get the closest level for achievements
    achievements = []
    if path_id in skill_achievements:
        level_keys = sorted(skill_achievements[path_id].keys())
        closest_level = level_keys[0]
        for level_key in level_keys:
            if level_key <= milestone_level:
                closest_level = level_key
        
        achievements = skill_achievements[path_id][closest_level].get(lang, skill_achievements[path_id][closest_level]["en"])
    
    # Translate certificate text based on language
    certificate_title = "Certificate of Achievement" if lang == "en" else "Sertifikat Prestasi"
    certifies_that = "This certifies that" if lang == "en" else "Menyatakan bahwa"
    has_completed = "has successfully completed" if lang == "en" else "telah berhasil menyelesaikan"
    issued_on = "Issued on" if lang == "en" else "Diterbitkan pada"
    skills_acquired = "Skills Acquired" if lang == "en" else "Keterampilan yang Diperoleh"
    
    # Create more visually appealing certificate with achievements
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {colors['secondary']}, white); 
         border: 3px solid {colors['primary']}; border-radius: 12px;
         padding: 40px 30px; text-align: center; margin: 20px 0; position: relative;
         box-shadow: 0 8px 16px rgba(0,0,0,0.15);">
        
        <!-- Certificate Badge -->
        <div style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%);
             background: linear-gradient(135deg, {colors['primary']}, {colors['accent']}); 
             padding: 8px 25px; border: 2px solid white; 
             border-radius: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <span style="color: white; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">CERTIFICATE</span>
        </div>
        
        <!-- Border Design -->
        <div style="position: absolute; top: 10px; left: 10px; right: 10px; bottom: 10px; 
             border: 1px dashed {colors['primary']}; border-radius: 8px; pointer-events: none;"></div>
        
        <!-- Icon with Background -->
        <div style="display: inline-block; font-size: 3.5rem; margin: 15px auto 20px;
             background-color: {colors['secondary']}; width: 80px; height: 80px; 
             border-radius: 50%; line-height: 80px; box-shadow: 0 3px 6px rgba(0,0,0,0.1);">
            {certificate["icon"]}
        </div>
        
        <!-- Certificate Title -->
        <h2 style="color: {colors['accent']}; margin-bottom: 5px; font-family: serif; 
                  font-size: 2rem; letter-spacing: 1px; text-transform: uppercase;">{certificate_title}</h2>
        
        <!-- Certificate Body -->
        <p style="color: #666; font-style: italic; margin-bottom: 10px;">{certifies_that}</p>
        
        <h3 style="color: #333; font-family: serif; font-size: 2.2rem; margin-bottom: 10px;
                  background: -webkit-linear-gradient({colors['primary']}, {colors['accent']});
                  -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            {certificate["player_name"]}
        </h3>
        
        <p style="color: #666; margin-bottom: 10px;">{has_completed}</p>
        
        <h3 style="color: {colors['primary']}; margin-bottom: 15px; padding: 5px 15px;
                  display: inline-block; border-bottom: 2px solid {colors['primary']};">
            {certificate["title"]}
        </h3>
        
        <!-- Achievement Section -->
        <div style="margin: 25px auto; background-color: white; border-radius: 8px; 
             border: 1px solid #ddd; padding: 15px; max-width: 90%; text-align: left;">
            <h4 style="color: {colors['primary']}; margin-top: 0; margin-bottom: 10px; text-align: center;">
                {skills_acquired}
            </h4>
            <ul style="margin: 0; padding-left: 20px; columns: 2;">
    """, unsafe_allow_html=True)
    
    # Add skill items dynamically
    for achievement in achievements:
        st.markdown(f"""
            <li style="margin-bottom: 5px; color: #555;">{achievement}</li>
        """, unsafe_allow_html=True)
    
    # Close the achievements section and add the footer
    st.markdown(f"""
            </ul>
        </div>
        
        <!-- Date Section -->
        <p style="color: #666; margin-bottom: 5px;">{issued_on}</p>
        <p style="color: #333; font-weight: bold; margin-bottom: 20px;">
            {certificate["issue_date"]}
        </p>
        
        <!-- Signature Section -->
        <div style="display: flex; justify-content: space-between; margin-top: 30px; padding: 0 20px;">
            <div style="text-align: center;">
                <div style="border-top: 1px solid #999; width: 150px; padding-top: 5px; 
                     color: #666; font-style: italic;">Student</div>
            </div>
            
            <div style="text-align: center;">
                <div style="border-top: 1px solid #999; width: 150px; padding-top: 5px; 
                     color: #666; font-style: italic;">Toko Pintar</div>
            </div>
        </div>
        
        <!-- Certificate ID -->
        <div style="margin-top: 20px; font-size: 0.8rem; color: #999;">
            Certificate ID: {certificate["id"]}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Download button (mock for now)
    download_text = "Download Certificate" if lang == "en" else "Unduh Sertifikat"
    if st.button(download_text, key=f"download_{certificate['id']}"):
        st.success("Certificate downloaded successfully!")

def get_earned_certificates():
    """Get all certificates earned by the player.
    
    Returns:
        dict: Dictionary of earned certificates
    """
    if "earned_certificates" not in st.session_state:
        st.session_state.earned_certificates = {}
    
    return st.session_state.earned_certificates

def show_certificates_tab():
    """Display a tab showing all earned certificates."""
    lang = get_config("app.default_language") or "en"
    
    certificates = get_earned_certificates()
    
    if not certificates:
        no_cert_text = "You haven't earned any certificates yet" if lang == "en" else "Anda belum mendapatkan sertifikat apa pun"
        complete_path_text = "Complete learning paths to earn skill certificates" if lang == "en" else "Selesaikan jalur pembelajaran untuk mendapatkan sertifikat keterampilan"
        st.info(f"{no_cert_text}. {complete_path_text}!")
        return
    
    # Header
    certificates_text = "Your Skill Certificates" if lang == "en" else "Sertifikat Keterampilan Anda"
    st.markdown(f"## {certificates_text}")
    
    # Display certificates in a grid
    col1, col2 = st.columns(2)
    
    for i, (cert_id, certificate) in enumerate(certificates.items()):
        # Alternate between columns
        col = col1 if i % 2 == 0 else col2
        
        with col:
            # Display mini certificate
            st.markdown(f"""
            <div style="background-color: #FEFCF7; border: 1px solid #DBC49A; border-radius: 8px;
                 padding: 15px; text-align: center; margin-bottom: 20px;">
                <div style="font-size: 1.5rem; margin-bottom: 5px;">{certificate["icon"]}</div>
                <h3 style="margin: 0 0 5px 0; font-size: 1rem;">{certificate["title"]}</h3>
                <p style="color: #666; font-size: 0.8rem; margin: 0;">
                    Issued: {certificate["issue_date"]}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # View certificate button
            view_text = "View Certificate" if lang == "en" else "Lihat Sertifikat"
            if st.button(view_text, key=f"view_{cert_id}"):
                st.session_state.selected_certificate = cert_id
                st.rerun()

def show_certificate_details(certificate_id):
    """Show detailed view of a certificate.
    
    Args:
        certificate_id (str): Identifier for the certificate
    """
    certificates = get_earned_certificates()
    if certificate_id not in certificates:
        st.error("Certificate not found!")
        return
    
    certificate = certificates[certificate_id]
    
    lang = get_config("app.default_language") or "en"
    
    # Display full certificate
    display_certificate_preview(certificate["path_id"], certificate["milestone_level"])
    
    # Back button
    back_text = "Back to Certificates" if lang == "en" else "Kembali ke Sertifikat"
    if st.button(back_text, key="back_to_certificates"):
        st.session_state.selected_certificate = None
        st.rerun()