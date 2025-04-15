"""
Learning path components for Toko Pintar application.
"""
from .learning_paths import (
    show_learning_paths, 
    get_available_paths, 
    get_path_progress, 
    show_learning_module
)
from .certificates import (
    generate_certificate, 
    display_certificate_preview, 
    get_earned_certificates
)
from .real_world_tips import (
    get_tips_for_skill,
    get_real_world_applications,
    display_pro_tip
)

__all__ = [
    'show_learning_paths',
    'get_available_paths',
    'get_path_progress',
    'show_learning_module',
    'generate_certificate',
    'display_certificate_preview',
    'get_earned_certificates',
    'get_tips_for_skill',
    'get_real_world_applications',
    'display_pro_tip'
]