"""
bmi_logic.py
Modul logika perhitungan, validasi, dan klasifikasi Indeks Massa Tubuh (IMT / BMI).
Sesuai standar Survei Kesehatan Indonesia (SKI) 2023 - Kementerian Kesehatan RI (Penduduk Dewasa).
"""

from typing import Tuple, Dict, Any, Optional

# Kategori IMT Dewasa menurut Standar SKI 2023 Kemenkes RI
KAT_KURANG = "Berat badan kurang (wasting)"
KAT_NORMAL = "Normal"
KAT_LEBIH = "Berat badan lebih (overweight)"
KAT_OBESITAS = "Obesitas"

# Detail tampilan dan edukasi tiap kategori
KATEGORI_INFO: Dict[str, Dict[str, Any]] = {
    KAT_KURANG: {
        "nama": KAT_KURANG,
        "badge": "Sangat Kurus",
        "badge_color": "#0284C7",       # Sky/Ocean Blue (sesuai referensi UI)
        "bg_badge": "#E0F2FE",
        "deskripsi": "Kekurangan berat badan tingkat berat. Dianjurkan untuk meningkatkan asupan nutrisi padat gizi berkonsultasi dengan ahli gizi.",
        "batas_tabel": "< 18.5"
    },
    KAT_NORMAL: {
        "nama": KAT_NORMAL,
        "badge": "Normal / Ideal",
        "badge_color": "#16A34A",       # Emerald Green
        "bg_badge": "#DCFCE7",
        "deskripsi": "Berat badan Anda berada dalam kategori normal dan ideal. Pertahankan pola makan bergizi seimbang dan aktivitas fisik secara teratur.",
        "batas_tabel": "18.5 – 24.9"
    },
    KAT_LEBIH: {
        "nama": KAT_LEBIH,
        "badge": "Gemuk (Ringan)",
        "badge_color": "#EA580C",       # Vibrant Orange
        "bg_badge": "#FFEDD5",
        "deskripsi": "Kelebihan berat badan tingkat ringan. Disarankan untuk membatasi konsumsi gula, garam, dan lemak, serta rutin berolahraga.",
        "batas_tabel": "25.0 – 26.9"
    },
    KAT_OBESITAS: {
        "nama": KAT_OBESITAS,
        "badge": "Obesitas (Berat)",
        "badge_color": "#DC2626",       # Red
        "bg_badge": "#FEE2E2",
        "deskripsi": "Berat badan Anda berada dalam kategori obesitas tingkat berat. Dianjurkan untuk berkonsultasi dengan dokter atau ahli gizi untuk penanganan lebih lanjut.",
        "batas_tabel": "≥ 27.0"
    }
}

# Data tabel batas kategori Kemenkes untuk tampilan tabel
TABEL_KATEGORI = [
    ("Berat badan kurang (wasting)", "< 18.5"),
    ("Normal", "18.5 – 24.9"),
    ("Berat badan lebih (overweight)", "25.0 – 26.9"),
    ("Obesitas", "≥ 27.0")
]

# Batas fisiologis input yang valid
MIN_WEIGHT = 1.0
MAX_WEIGHT = 350.0
MIN_HEIGHT = 30.0
MAX_HEIGHT = 260.0

ERR_WEIGHT_INVALID = f"Masukkan berat badan yang valid ({int(MIN_WEIGHT)} - {int(MAX_WEIGHT)} kg)."
ERR_HEIGHT_INVALID = f"Masukkan tinggi badan yang valid ({int(MIN_HEIGHT)} - {int(MAX_HEIGHT)} cm)."


def validate_weight(weight_str: str) -> Tuple[bool, Optional[str], Optional[float]]:
    """
    Memvalidasi input berat badan (kg).
    Returns: (is_valid, error_message, parsed_value)
    """
    if weight_str is None:
        return False, ERR_WEIGHT_INVALID, None
    
    clean_str = str(weight_str).strip().replace(',', '.')
    if not clean_str:
        return False, ERR_WEIGHT_INVALID, None

    try:
        val = float(clean_str)
    except ValueError:
        return False, ERR_WEIGHT_INVALID, None

    if val < MIN_WEIGHT or val > MAX_WEIGHT:
        return False, ERR_WEIGHT_INVALID, None

    return True, None, val


def validate_height(height_str: str) -> Tuple[bool, Optional[str], Optional[float]]:
    """
    Memvalidasi input tinggi badan (cm).
    Returns: (is_valid, error_message, parsed_value)
    """
    if height_str is None:
        return False, ERR_HEIGHT_INVALID, None

    clean_str = str(height_str).strip().replace(',', '.')
    if not clean_str:
        return False, ERR_HEIGHT_INVALID, None

    try:
        val = float(clean_str)
    except ValueError:
        return False, ERR_HEIGHT_INVALID, None

    if val < MIN_HEIGHT or val > MAX_HEIGHT:
        return False, ERR_HEIGHT_INVALID, None

    return True, None, val


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """
    Menghitung nilai Indeks Massa Tubuh (IMT / BMI).
    Rumus: IMT = berat (kg) / (tinggi (m))^2
    """
    if height_cm <= 0:
        raise ValueError("Tinggi badan harus lebih besar dari 0.")
    if weight_kg <= 0:
        raise ValueError("Berat badan harus lebih besar dari 0.")

    height_m = height_cm / 100.0
    return weight_kg / (height_m ** 2)


def classify_bmi(bmi: float) -> Dict[str, Any]:
    """
    Menentukan kategori IMT berdasarkan batas Kemenkes RI (SKI 2023):
    - IMT < 18.5: Berat badan kurang (wasting)
    - 18.5 <= IMT < 25.0: Normal
    - 25.0 <= IMT < 27.0: Berat badan lebih (overweight)
    - IMT >= 27.0: Obesitas
    """
    if bmi < 18.5:
        category = KAT_KURANG
    elif bmi < 25.0:
        category = KAT_NORMAL
    elif bmi < 27.0:
        category = KAT_LEBIH
    else:
        category = KAT_OBESITAS

    return KATEGORI_INFO[category]


def calculate_ideal_weight_range(height_cm: float) -> Tuple[float, float]:
    """
    Menghitung rentang berat badan normal/ideal berdasarkan batas IMT normal (18.5 - 25.0):
    - Batas bawah = 18.5 * (tinggi_m)^2
    - Batas atas = 25.0 * (tinggi_m)^2
    Hasil dibulatkan ke 1 desimal.
    """
    if height_cm <= 0:
        raise ValueError("Tinggi badan harus lebih besar dari 0.")

    height_m = height_cm / 100.0
    h_sq = height_m ** 2
    min_w = round(18.5 * h_sq, 1)
    max_w = round(25.0 * h_sq, 1)
    return min_w, max_w


def process_bmi(weight_str: str, height_str: str) -> Dict[str, Any]:
    """
    Fungsi orkestrasi untuk memvalidasi input, menghitung BMI,
    menentukan kategori, serta menghitung rentang berat badan ideal.
    """
    w_valid, w_err, weight = validate_weight(weight_str)
    h_valid, h_err, height = validate_height(height_str)

    if not w_valid or not h_valid:
        return {
            "success": False,
            "weight_error": w_err,
            "height_error": h_err,
            "bmi": None,
            "bmi_formatted": None,
            "category": None,
            "ideal_weight_min": None,
            "ideal_weight_max": None
        }

    # Hitung BMI asli (unrounded untuk evaluasi kategori)
    bmi_val = calculate_bmi(weight, height)
    cat_info = classify_bmi(bmi_val)
    ideal_min, ideal_max = calculate_ideal_weight_range(height)

    return {
        "success": True,
        "weight_error": None,
        "height_error": None,
        "bmi": bmi_val,
        "bmi_formatted": f"{bmi_val:.2f}",
        "bmi_formatted_1dec": f"{bmi_val:.1f}",
        "category": cat_info,
        "ideal_weight_min": ideal_min,
        "ideal_weight_max": ideal_max,
        "ideal_weight_text": f"{ideal_min:.1f} kg – {ideal_max:.1f} kg"
    }
