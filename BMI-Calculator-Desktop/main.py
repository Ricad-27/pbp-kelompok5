"""
main.py
Aplikasi Desktop: Kalkulator BMI Indonesia
Sesuai standar Survei Kesehatan Indonesia (SKI) 2023 - Kementerian Kesehatan RI.
Dibangun menggunakan Python 3 & Tkinter (Pure Standard Library).
"""

import sys
import os
import tkinter as tk
from tkinter import font

from bmi_logic import (
    process_bmi,
    TABEL_KATEGORI,
    MIN_WEIGHT,
    MAX_WEIGHT,
    MIN_HEIGHT,
    MAX_HEIGHT,
    ERR_WEIGHT_INVALID,
    ERR_HEIGHT_INVALID
)


def get_resource_path(relative_path: str) -> str:
    """
    Mendapatkan path absolut ke file resource (seperti icon.ico).
    Mendukung mode pengembangan (development) dan mode bundle PyInstaller (_MEIPASS).
    """
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


class BMICalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Kalkulator BMI Indonesia")
        self.geometry("450x720")
        self.minsize(400, 600)

        # Palet Warna Sesuai Desain Referensi
        self.COLOR_BG = "#F4F6F9"          # Abu-abu sangat muda untuk background luar
        self.COLOR_CARD = "#FFFFFF"        # Putih untuk card utama
        self.COLOR_CARD_BORDER = "#E2E8F0" # Border tipis abu-abu kebiruan
        self.COLOR_TEXT_TITLE = "#0F172A"  # Biru tua / Slate 900
        self.COLOR_TEXT_MUTED = "#64748B"  # Slate 500
        self.COLOR_PRIMARY = "#7C3AED"     # Ungu utama tombol Hitung BMI
        self.COLOR_PRIMARY_HOVER = "#6D28D9"
        self.COLOR_PILL_BG = "#F3E8FF"     # Ungu muda badge Standar Kemenkes
        self.COLOR_PILL_TEXT = "#7C3AED"   # Teks ungu badge
        self.COLOR_RESET_BORDER = "#C4B5FD"# Border tombol Reset
        self.COLOR_RESET_HOVER = "#F5F3FF"
        self.COLOR_ERROR = "#EF4444"       # Merah pesan validasi
        self.COLOR_ERROR_BG = "#FEF2F2"    # Background input saat error
        self.COLOR_LINK = "#4F46E5"        # Biru keunguan teks link
        self.COLOR_IDEAL_BG = "#FAF5FF"    # Card ungu muda rentang berat ideal
        self.COLOR_IDEAL_BORDER = "#E9D5FF"
        self.COLOR_IDEAL_TEXT = "#581C87"

        self.configure(bg=self.COLOR_BG)
        self.set_app_icon()
        self.center_window(450, 720)

        # State aplikasi
        self.table_visible = False
        self.result_visible = False

        self.create_widgets()

    def set_app_icon(self):
        """Memasang ikon aplikasi jika file icon.ico tersedia."""
        icon_path = get_resource_path(os.path.join("assets", "icon.ico"))
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

    def center_window(self, width: int, height: int):
        """Menengahkan posisi jendela aplikasi di layar monitor pengguna."""
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = max(0, (sw - width) // 2)
        y = max(0, (sh - height) // 2 - 20)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        """Membangun seluruh komponen antarmuka grafis."""
        # Canvas utama dengan Scrollbar agar responsif pada semua ukuran monitor
        self.main_canvas = tk.Canvas(self, bg=self.COLOR_BG, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.main_canvas.yview)
        
        self.scroll_content = tk.Frame(self.main_canvas, bg=self.COLOR_BG)
        self.scroll_content.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )

        self.canvas_window_id = self.main_canvas.create_window(
            (0, 0), window=self.scroll_content, anchor="n"
        )
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.main_canvas.bind("<Configure>", self._on_canvas_configure)
        self.main_canvas.pack(side="left", fill="both", expand=True)

        # Mouse wheel listener
        self.bind_all("<MouseWheel>", self._on_mousewheel)

        # Container Luar pembungkus Card Utama
        outer_pad = tk.Frame(self.scroll_content, bg=self.COLOR_BG, padx=16, pady=20)
        outer_pad.pack(fill="both", expand=True)

        # ==================== CARD UTAMA ====================
        self.card = tk.Frame(
            outer_pad,
            bg=self.COLOR_CARD,
            highlightthickness=1,
            highlightbackground=self.COLOR_CARD_BORDER,
            padx=22,
            pady=22
        )
        self.card.pack(fill="x", expand=True)

        # 1. Pill Badge "STANDAR KEMENKES RI"
        pill_frame = tk.Frame(self.card, bg=self.COLOR_CARD)
        pill_frame.pack(anchor="center", pady=(0, 10))

        lbl_pill = tk.Label(
            pill_frame,
            text="STANDAR KEMENKES RI",
            font=("Segoe UI", 8, "bold"),
            bg=self.COLOR_PILL_BG,
            fg=self.COLOR_PILL_TEXT,
            padx=12,
            pady=3
        )
        lbl_pill.pack()

        # 2. Judul Besar: "Kalkulator BMI"
        lbl_title = tk.Label(
            self.card,
            text="Kalkulator BMI",
            font=("Segoe UI", 18, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT_TITLE
        )
        lbl_title.pack(anchor="center", pady=(0, 4))

        # 3. Deskripsi Singkat
        lbl_desc = tk.Label(
            self.card,
            text="Ketahui indeks massa tubuh dan rentang berat badan ideal tinggi badan Anda.",
            font=("Segoe UI", 9),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT_MUTED,
            wraplength=340,
            justify="center"
        )
        lbl_desc.pack(anchor="center", pady=(0, 16))

        # 4. Input Field: Berat Badan
        lbl_w_title = tk.Label(
            self.card,
            text="Berat Badan",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT_TITLE
        )
        lbl_w_title.pack(anchor="w", pady=(0, 4))

        self.box_weight = tk.Frame(
            self.card,
            bg=self.COLOR_CARD,
            highlightthickness=1,
            highlightbackground="#CBD5E1",
            padx=10,
            pady=7
        )
        self.box_weight.pack(fill="x", pady=(0, 2))

        self.var_weight = tk.StringVar()
        self.entry_weight = tk.Entry(
            self.box_weight,
            textvariable=self.var_weight,
            font=("Segoe UI", 10),
            bg=self.COLOR_CARD,
            fg="#94A3B8",
            bd=0,
            relief="flat"
        )
        self.entry_weight.insert(0, "Contoh: 65")
        self.entry_weight.pack(side="left", fill="x", expand=True)

        self.lbl_unit_w = tk.Label(
            self.box_weight,
            text="kg",
            font=("Segoe UI", 9),
            bg=self.COLOR_CARD,
            fg="#475569"
        )
        self.lbl_unit_w.pack(side="right")

        self.lbl_err_weight = tk.Label(
            self.card,
            text="",
            font=("Segoe UI", 8),
            bg=self.COLOR_CARD,
            fg=self.COLOR_ERROR,
            anchor="w"
        )
        self.lbl_err_weight.pack(anchor="w", pady=(2, 8))

        # Binding placeholder & enter key untuk berat badan
        self.entry_weight.bind("<FocusIn>", self._on_weight_focus_in)
        self.entry_weight.bind("<FocusOut>", self._on_weight_focus_out)
        self.entry_weight.bind("<Return>", lambda e: self.calculate())

        # 5. Input Field: Tinggi Badan
        lbl_h_title = tk.Label(
            self.card,
            text="Tinggi Badan",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT_TITLE
        )
        lbl_h_title.pack(anchor="w", pady=(0, 4))

        self.box_height = tk.Frame(
            self.card,
            bg=self.COLOR_CARD,
            highlightthickness=1,
            highlightbackground="#CBD5E1",
            padx=10,
            pady=7
        )
        self.box_height.pack(fill="x", pady=(0, 2))

        self.var_height = tk.StringVar()
        self.entry_height = tk.Entry(
            self.box_height,
            textvariable=self.var_height,
            font=("Segoe UI", 10),
            bg=self.COLOR_CARD,
            fg="#94A3B8",
            bd=0,
            relief="flat"
        )
        self.entry_height.insert(0, "Contoh: 170")
        self.entry_height.pack(side="left", fill="x", expand=True)

        self.lbl_unit_h = tk.Label(
            self.box_height,
            text="cm",
            font=("Segoe UI", 9),
            bg=self.COLOR_CARD,
            fg="#475569"
        )
        self.lbl_unit_h.pack(side="right")

        self.lbl_err_height = tk.Label(
            self.card,
            text="",
            font=("Segoe UI", 8),
            bg=self.COLOR_CARD,
            fg=self.COLOR_ERROR,
            anchor="w"
        )
        self.lbl_err_height.pack(anchor="w", pady=(2, 12))

        # Binding placeholder & enter key untuk tinggi badan
        self.entry_height.bind("<FocusIn>", self._on_height_focus_in)
        self.entry_height.bind("<FocusOut>", self._on_height_focus_out)
        self.entry_height.bind("<Return>", lambda e: self.calculate())

        # 6. Tombol Aksi: Hitung BMI & Reset
        btn_frame = tk.Frame(self.card, bg=self.COLOR_CARD)
        btn_frame.pack(fill="x", pady=(0, 14))

        self.btn_calc = tk.Button(
            btn_frame,
            text="Hitung BMI",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_PRIMARY,
            fg="#FFFFFF",
            activebackground=self.COLOR_PRIMARY_HOVER,
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            pady=9,
            cursor="hand2",
            command=self.calculate
        )
        self.btn_calc.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_reset = tk.Button(
            btn_frame,
            text="Reset",
            font=("Segoe UI", 10, "bold"),
            bg="#FFFFFF",
            fg=self.COLOR_PRIMARY,
            activebackground=self.COLOR_RESET_HOVER,
            activeforeground=self.COLOR_PRIMARY_HOVER,
            relief="solid",
            bd=1,
            highlightthickness=0,
            pady=8,
            cursor="hand2",
            command=self.reset_form
        )
        self.btn_reset.pack(side="right", fill="x", expand=True, padx=(6, 0))

        # 7. Garis Pemisah Tipis (Ditampilkan saat ada hasil)
        self.divider = tk.Frame(self.card, bg="#F1F5F9", height=1)

        # 8. Frame Area Hasil (Awalnya tersembunyi)
        self.result_frame = tk.Frame(self.card, bg=self.COLOR_CARD)

        # Header Hasil: Label "HASIL INDEKS ANDA" + Badge Kategori
        res_header = tk.Frame(self.result_frame, bg=self.COLOR_CARD)
        res_header.pack(fill="x", pady=(0, 8))

        lbl_res_tag = tk.Label(
            res_header,
            text="HASIL INDEKS ANDA",
            font=("Segoe UI", 8, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT_MUTED
        )
        lbl_res_tag.pack(side="left")

        self.lbl_badge = tk.Label(
            res_header,
            text="",
            font=("Segoe UI", 8, "bold"),
            bg="#0284C7",
            fg="#FFFFFF",
            padx=10,
            pady=2
        )
        self.lbl_badge.pack(side="right")

        # Angka BMI Besar + Satuan
        bmi_row = tk.Frame(self.result_frame, bg=self.COLOR_CARD)
        bmi_row.pack(anchor="w", pady=(0, 6))

        self.lbl_bmi_number = tk.Label(
            bmi_row,
            text="0.0",
            font=("Segoe UI", 26, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT_TITLE
        )
        self.lbl_bmi_number.pack(side="left")

        lbl_bmi_unit = tk.Label(
            bmi_row,
            text=" kg/m²",
            font=("Segoe UI", 10),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT_MUTED
        )
        lbl_bmi_unit.pack(side="left", pady=(8, 0))

        # Deskripsi Kategori Edukatif
        self.lbl_category_desc = tk.Label(
            self.result_frame,
            text="",
            font=("Segoe UI", 9),
            bg=self.COLOR_CARD,
            fg="#334155",
            wraplength=340,
            justify="left"
        )
        self.lbl_category_desc.pack(anchor="w", pady=(0, 12))

        # Card Ungu Muda: Rentang Berat Ideal Anda
        self.card_ideal = tk.Frame(
            self.result_frame,
            bg=self.COLOR_IDEAL_BG,
            highlightthickness=1,
            highlightbackground=self.COLOR_IDEAL_BORDER,
            padx=14,
            pady=10
        )
        self.card_ideal.pack(fill="x", pady=(0, 10))

        ideal_left = tk.Frame(self.card_ideal, bg=self.COLOR_IDEAL_BG)
        ideal_left.pack(side="left", fill="x", expand=True)

        lbl_ideal_title = tk.Label(
            ideal_left,
            text="Rentang Berat Ideal Anda",
            font=("Segoe UI", 8, "bold"),
            bg=self.COLOR_IDEAL_BG,
            fg=self.COLOR_PRIMARY
        )
        lbl_ideal_title.pack(anchor="w")

        self.lbl_ideal_value = tk.Label(
            ideal_left,
            text="0.0 kg – 0.0 kg",
            font=("Segoe UI", 11, "bold"),
            bg=self.COLOR_IDEAL_BG,
            fg=self.COLOR_IDEAL_TEXT
        )
        self.lbl_ideal_value.pack(anchor="w", pady=(2, 0))

        lbl_ideal_icon = tk.Label(
            self.card_ideal,
            text="⚖",
            font=("Segoe UI", 18),
            bg=self.COLOR_IDEAL_BG,
            fg=self.COLOR_PRIMARY
        )
        lbl_ideal_icon.pack(side="right", padx=(8, 0))

        # 9. Teks Link: "Lihat Batas Kategori Kemenkes"
        self.link_frame = tk.Frame(self.card, bg=self.COLOR_CARD)
        self.link_frame.pack(fill="x", pady=(8, 4))

        self.lbl_toggle_link = tk.Label(
            self.link_frame,
            text="Lihat Batas Kategori Kemenkes",
            font=("Segoe UI", 9, "underline"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_LINK,
            cursor="hand2"
        )
        self.lbl_toggle_link.pack(anchor="center")
        self.lbl_toggle_link.bind("<Button-1>", lambda e: self.toggle_category_table())

        # 10. Frame Tabel Kategori Kemenkes (Awalnya tersembunyi)
        self.table_card = tk.Frame(
            self.card,
            bg="#F8FAFC",
            highlightthickness=1,
            highlightbackground="#E2E8F0",
            padx=14,
            pady=10
        )

        # Header Tabel
        tbl_hdr = tk.Frame(self.table_card, bg="#F8FAFC")
        tbl_hdr.pack(fill="x", pady=(2, 6))

        lbl_hdr_cat = tk.Label(
            tbl_hdr,
            text="Kategori",
            font=("Segoe UI", 9, "bold"),
            bg="#F8FAFC",
            fg=self.COLOR_TEXT_TITLE
        )
        lbl_hdr_cat.pack(side="left")

        lbl_hdr_val = tk.Label(
            tbl_hdr,
            text="Batas IMT",
            font=("Segoe UI", 9, "bold"),
            bg="#F8FAFC",
            fg=self.COLOR_TEXT_TITLE
        )
        lbl_hdr_val.pack(side="right")

        # Garis pemisah header tabel
        tk.Frame(self.table_card, bg="#E2E8F0", height=1).pack(fill="x", pady=(0, 4))

        # Baris-baris Tabel
        for idx, (cat_name, cat_range) in enumerate(TABEL_KATEGORI):
            row_f = tk.Frame(self.table_card, bg="#F8FAFC")
            row_f.pack(fill="x", pady=4)

            lbl_c = tk.Label(
                row_f,
                text=cat_name,
                font=("Segoe UI", 9),
                bg="#F8FAFC",
                fg="#334155"
            )
            lbl_c.pack(side="left")

            lbl_v = tk.Label(
                row_f,
                text=cat_range,
                font=("Segoe UI", 9),
                bg="#F8FAFC",
                fg="#334155"
            )
            lbl_v.pack(side="right")

            if idx < len(TABEL_KATEGORI) - 1:
                tk.Frame(self.table_card, bg="#F1F5F9", height=1).pack(fill="x", pady=(2, 2))

    # --- Scroll & Resize Handlers ---
    def _on_canvas_configure(self, event):
        """Memastikan lebar scrollable frame mengikuti lebar jendela canvas."""
        canvas_width = event.width
        self.main_canvas.itemconfig(self.canvas_window_id, width=canvas_width)

    def _on_mousewheel(self, event):
        """Dukungan scroll mousewheel vertikal di Windows."""
        if self.main_canvas.winfo_exists():
            self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # --- Placeholder Handlers ---
    def _on_weight_focus_in(self, event):
        if self.entry_weight.get() == "Contoh: 65":
            self.entry_weight.delete(0, tk.END)
            self.entry_weight.config(fg="#0F172A")

    def _on_weight_focus_out(self, event):
        if not self.entry_weight.get().strip():
            self.entry_weight.insert(0, "Contoh: 65")
            self.entry_weight.config(fg="#94A3B8")

    def _on_height_focus_in(self, event):
        if self.entry_height.get() == "Contoh: 170":
            self.entry_height.delete(0, tk.END)
            self.entry_height.config(fg="#0F172A")

    def _on_height_focus_out(self, event):
        if not self.entry_height.get().strip():
            self.entry_height.insert(0, "Contoh: 170")
            self.entry_height.config(fg="#94A3B8")

    # --- Logika Hitung & Reset ---
    def calculate(self):
        """Eksekusi validasi, kalkulasi BMI, dan pembaruan tampilan."""
        # Ambil nilai input asli (abaikan placeholder)
        raw_w = self.entry_weight.get()
        if raw_w == "Contoh: 65":
            raw_w = ""

        raw_h = self.entry_height.get()
        if raw_h == "Contoh: 170":
            raw_h = ""

        res = process_bmi(raw_w, raw_h)

        if not res["success"]:
            # Tampilkan pesan error pada input yang bermasalah
            if res["weight_error"]:
                self.lbl_err_weight.config(text=res["weight_error"])
                self.box_weight.config(highlightbackground=self.COLOR_ERROR, bg=self.COLOR_ERROR_BG)
                self.entry_weight.config(bg=self.COLOR_ERROR_BG)
                self.lbl_unit_w.config(bg=self.COLOR_ERROR_BG)
            else:
                self.lbl_err_weight.config(text="")
                self.box_weight.config(highlightbackground="#CBD5E1", bg=self.COLOR_CARD)
                self.entry_weight.config(bg=self.COLOR_CARD)
                self.lbl_unit_w.config(bg=self.COLOR_CARD)

            if res["height_error"]:
                self.lbl_err_height.config(text=res["height_error"])
                self.box_height.config(highlightbackground=self.COLOR_ERROR, bg=self.COLOR_ERROR_BG)
                self.entry_height.config(bg=self.COLOR_ERROR_BG)
                self.lbl_unit_h.config(bg=self.COLOR_ERROR_BG)
            else:
                self.lbl_err_height.config(text="")
                self.box_height.config(highlightbackground="#CBD5E1", bg=self.COLOR_CARD)
                self.entry_height.config(bg=self.COLOR_CARD)
                self.lbl_unit_h.config(bg=self.COLOR_CARD)

            # Sembunyikan area hasil jika kalkulasi tidak valid
            self._hide_result()
            return

        # Jika valid, bersihkan styling error
        self.lbl_err_weight.config(text="")
        self.box_weight.config(highlightbackground="#CBD5E1", bg=self.COLOR_CARD)
        self.entry_weight.config(bg=self.COLOR_CARD)
        self.lbl_unit_w.config(bg=self.COLOR_CARD)

        self.lbl_err_height.config(text="")
        self.box_height.config(highlightbackground="#CBD5E1", bg=self.COLOR_CARD)
        self.entry_height.config(bg=self.COLOR_CARD)
        self.lbl_unit_h.config(bg=self.COLOR_CARD)

        # Update komponen tampilan hasil
        cat = res["category"]
        self.lbl_badge.config(text=cat["badge"], bg=cat["badge_color"])
        self.lbl_bmi_number.config(text=res["bmi_formatted"])
        self.lbl_category_desc.config(text=cat["deskripsi"])
        self.lbl_ideal_value.config(text=res["ideal_weight_text"])

        self._show_result()

    def _show_result(self):
        """Menampilkan divider dan card hasil di atas link kategori."""
        if not self.result_visible:
            # Repack divider dan result_frame sebelum link_frame
            self.link_frame.pack_forget()
            if self.table_visible:
                self.table_card.pack_forget()

            self.divider.pack(fill="x", pady=(6, 14))
            self.result_frame.pack(fill="x", pady=(0, 6))

            self.link_frame.pack(fill="x", pady=(8, 4))
            if self.table_visible:
                self.table_card.pack(fill="x", pady=(6, 4))

            self.result_visible = True
            self.update_idletasks()
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

    def _hide_result(self):
        """Menyembunyikan area hasil."""
        if self.result_visible:
            self.divider.pack_forget()
            self.result_frame.pack_forget()
            self.result_visible = False
            self.update_idletasks()
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

    def reset_form(self):
        """Mengosongkan form input, menyembunyikan hasil, dan membersihkan pesan error."""
        self.entry_weight.delete(0, tk.END)
        self.entry_weight.insert(0, "Contoh: 65")
        self.entry_weight.config(fg="#94A3B8", bg=self.COLOR_CARD)
        self.box_weight.config(highlightbackground="#CBD5E1", bg=self.COLOR_CARD)
        self.lbl_unit_w.config(bg=self.COLOR_CARD)
        self.lbl_err_weight.config(text="")

        self.entry_height.delete(0, tk.END)
        self.entry_height.insert(0, "Contoh: 170")
        self.entry_height.config(fg="#94A3B8", bg=self.COLOR_CARD)
        self.box_height.config(highlightbackground="#CBD5E1", bg=self.COLOR_CARD)
        self.lbl_unit_h.config(bg=self.COLOR_CARD)
        self.lbl_err_height.config(text="")

        self._hide_result()

    def toggle_category_table(self):
        """Membuka atau menutup tabel batas kategori Kemenkes."""
        if self.table_visible:
            self.table_card.pack_forget()
            self.lbl_toggle_link.config(text="Lihat Batas Kategori Kemenkes")
            self.table_visible = False
        else:
            self.table_card.pack(fill="x", pady=(6, 4))
            self.lbl_toggle_link.config(text="Tutup Batas Kategori Kemenkes")
            self.table_visible = True

        self.update_idletasks()
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

    # --- Helper methods untuk otomasi pengujian unit ---
    def set_input_weight(self, val: str):
        self.entry_weight.delete(0, tk.END)
        self.entry_weight.insert(0, val)
        self.entry_weight.config(fg="#0F172A")

    def set_input_height(self, val: str):
        self.entry_height.delete(0, tk.END)
        self.entry_height.insert(0, val)
        self.entry_height.config(fg="#0F172A")

    def get_input_weight(self) -> str:
        txt = self.entry_weight.get()
        return "" if txt == "Contoh: 65" else txt

    def get_input_height(self) -> str:
        txt = self.entry_height.get()
        return "" if txt == "Contoh: 170" else txt

    def get_weight_error(self) -> str:
        return self.lbl_err_weight.cget("text")

    def get_height_error(self) -> str:
        return self.lbl_err_height.cget("text")

    def is_result_visible(self) -> bool:
        return self.result_visible

    def is_table_visible(self) -> bool:
        return self.table_visible

    def get_toggle_link_text(self) -> str:
        return self.lbl_toggle_link.cget("text")


def main():
    app = BMICalculatorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
