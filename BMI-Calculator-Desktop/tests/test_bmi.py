"""
test_bmi.py
Unit testing untuk logika BMI dan antarmuka Kalkulator BMI Indonesia.
Menggunakan modul standard unittest.
"""

import sys
import os
import unittest

# Menambahkan parent directory ke sys.path agar dapat mengimpor bmi_logic dan main
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from bmi_logic import (
    calculate_bmi,
    classify_bmi,
    calculate_ideal_weight_range,
    validate_weight,
    validate_height,
    process_bmi,
    KAT_KURANG,
    KAT_NORMAL,
    KAT_LEBIH,
    KAT_OBESITAS,
    ERR_WEIGHT_INVALID,
    ERR_HEIGHT_INVALID
)


class TestBMILogic(unittest.TestCase):
    """Pengujian unit untuk modul bmi_logic.py."""

    def test_normal_bmi_calculation(self):
        """Uji perhitungan BMI normal (Contoh spesifikasi: 45 kg, 165 cm -> ~16.53)."""
        bmi = calculate_bmi(45.0, 165.0)
        self.assertAlmostEqual(bmi, 16.5289, places=3)
        self.assertEqual(f"{bmi:.2f}", "16.53")

        # Kasus normal lainnya: 60 kg, 170 cm -> 20.76
        bmi_normal = calculate_bmi(60.0, 170.0)
        self.assertAlmostEqual(bmi_normal, 20.7612, places=3)
        self.assertEqual(f"{bmi_normal:.2f}", "20.76")

    def test_category_boundary_18_5(self):
        """Uji kategori IMT tepat di bawah dan tepat pada batas 18.5."""
        # Tepat di bawah 18.5 -> Berat badan kurang (wasting)
        under_res = classify_bmi(18.49)
        self.assertEqual(under_res["nama"], KAT_KURANG)

        # Tepat pada batas 18.5 -> Normal
        exact_res = classify_bmi(18.50)
        self.assertEqual(exact_res["nama"], KAT_NORMAL)

    def test_category_boundary_25_0(self):
        """Uji kategori IMT tepat di bawah dan tepat pada batas 25.0."""
        # Tepat di bawah 25.0 -> Normal
        below_res = classify_bmi(24.99)
        self.assertEqual(below_res["nama"], KAT_NORMAL)

        # Tepat pada batas 25.0 -> Berat badan lebih (overweight)
        exact_res = classify_bmi(25.00)
        self.assertEqual(exact_res["nama"], KAT_LEBIH)

    def test_category_boundary_27_0(self):
        """Uji kategori IMT tepat di bawah dan tepat pada batas 27.0."""
        # Tepat di bawah 27.0 -> Berat badan lebih (overweight)
        below_res = classify_bmi(26.99)
        self.assertEqual(below_res["nama"], KAT_LEBIH)

        # Tepat pada batas 27.0 -> Obesitas
        exact_res = classify_bmi(27.00)
        self.assertEqual(exact_res["nama"], KAT_OBESITAS)

        # Di atas 27.0 -> Obesitas
        above_res = classify_bmi(32.5)
        self.assertEqual(above_res["nama"], KAT_OBESITAS)

    def test_empty_inputs(self):
        """Uji validasi jika input kosong atau hanya spasi."""
        w_ok, w_err, _ = validate_weight("")
        self.assertFalse(w_ok)
        self.assertEqual(w_err, ERR_WEIGHT_INVALID)

        w_ok, _, _ = validate_weight("   ")
        self.assertFalse(w_ok)

        h_ok, h_err, _ = validate_height("")
        self.assertFalse(h_ok)
        self.assertEqual(h_err, ERR_HEIGHT_INVALID)

        res = process_bmi("", "")
        self.assertFalse(res["success"])
        self.assertIsNotNone(res["weight_error"])
        self.assertIsNotNone(res["height_error"])

    def test_non_numeric_inputs(self):
        """Uji validasi jika input berupa teks non-numerik."""
        w_ok, w_err, _ = validate_weight("abc")
        self.assertFalse(w_ok)
        self.assertEqual(w_err, ERR_WEIGHT_INVALID)

        h_ok, h_err, _ = validate_height("seratus tujuh puluh")
        self.assertFalse(h_ok)
        self.assertEqual(h_err, ERR_HEIGHT_INVALID)

    def test_zero_and_negative_inputs(self):
        """Uji validasi nilai nol dan nilai negatif."""
        # Nilai 0
        w_zero_ok, _, _ = validate_weight("0")
        self.assertFalse(w_zero_ok)

        h_zero_ok, _, _ = validate_height("0")
        self.assertFalse(h_zero_ok)

        # Nilai negatif
        w_neg_ok, _, _ = validate_weight("-55")
        self.assertFalse(w_neg_ok)

        h_neg_ok, _, _ = validate_height("-165")
        self.assertFalse(h_neg_ok)

        # Pengecekan pada fungsi perhitungan langsung
        with self.assertRaises(ValueError):
            calculate_bmi(-50, 160)
        with self.assertRaises(ValueError):
            calculate_bmi(60, 0)

    def test_ideal_weight_range(self):
        """
        Uji perhitungan rentang berat badan normal (IMT 18.5 - 25.0).
        Tinggi 165 cm:
        18.5 * (1.65^2) = 50.36625 -> 50.4 kg
        25.0 * (1.65^2) = 68.0625  -> 68.1 kg
        """
        min_w, max_w = calculate_ideal_weight_range(165.0)
        self.assertEqual(min_w, 50.4)
        self.assertEqual(max_w, 68.1)

        # Tinggi 170 cm:
        # 18.5 * (1.70^2) = 53.465 -> 53.5 kg
        # 25.0 * (1.70^2) = 72.25  -> 72.2 atau 72.3 kg
        min_w_170, max_w_170 = calculate_ideal_weight_range(170.0)
        self.assertEqual(min_w_170, 53.5)
        self.assertEqual(max_w_170, 72.2 or 72.3)

    def test_process_bmi_full_workflow(self):
        """Uji alur lengkap proses BMI dengan input contoh referensi (45 kg, 165 cm)."""
        res = process_bmi("45", "165")
        self.assertTrue(res["success"])
        self.assertEqual(res["bmi_formatted"], "16.53")
        self.assertEqual(res["category"]["nama"], KAT_KURANG)
        self.assertEqual(res["ideal_weight_text"], "50.4 kg – 68.1 kg")


class TestGUIComponents(unittest.TestCase):
    """Pengujian komponen antarmuka GUI (Reset, Toggle Tabel, Validasi)."""

    def setUp(self):
        """Inisialisasi aplikasi Tkinter untuk pengujian headless/in-memory."""
        import tkinter as tk
        from main import BMICalculatorApp
        self.app = BMICalculatorApp()
        self.app.withdraw()  # Sembunyikan window selama pengujian

    def tearDown(self):
        """Hancurkan window setelah pengujian selesai."""
        if hasattr(self, "app"):
            self.app.destroy()

    def test_reset_button(self):
        """Uji tombol Reset: mengosongkan input, hasil, dan pesan error."""
        # Berikan nilai awal
        self.app.set_input_weight("70")
        self.app.set_input_height("175")
        self.app.calculate()

        # Pastikan area hasil sempat muncul
        self.assertTrue(self.app.is_result_visible())

        # Panggil tombol reset
        self.app.reset_form()

        # Verifikasi input kosong, pesan error kosong, hasil tersembunyi
        self.assertEqual(self.app.get_input_weight(), "")
        self.assertEqual(self.app.get_input_height(), "")
        self.assertEqual(self.app.get_weight_error(), "")
        self.assertEqual(self.app.get_height_error(), "")
        self.assertFalse(self.app.is_result_visible())

    def test_toggle_kategori_table(self):
        """Uji tabel kategori dapat dibuka dan ditutup via klik teks tautan."""
        # Awalnya tertutup
        self.assertFalse(self.app.is_table_visible())
        self.assertEqual(self.app.get_toggle_link_text(), "Lihat Batas Kategori Kemenkes")

        # Klik untuk membuka
        self.app.toggle_category_table()
        self.assertTrue(self.app.is_table_visible())
        self.assertEqual(self.app.get_toggle_link_text(), "Tutup Batas Kategori Kemenkes")

        # Klik lagi untuk menutup
        self.app.toggle_category_table()
        self.assertFalse(self.app.is_table_visible())
        self.assertEqual(self.app.get_toggle_link_text(), "Lihat Batas Kategori Kemenkes")


if __name__ == "__main__":
    unittest.main()
