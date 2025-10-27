import streamlit as st

st.set_page_config(page_title="Self Cashier Machine", page_icon="🛒", layout="centered")

st.title("🛒 SELF CASHIER MACHINE")
st.markdown("### Selamat datang di mesin kasir otomatis!")

# === Daftar harga ===
daftar_harga = {
    "A": ("Nasi Goreng", 15000),
    "B": ("Mie Ayam", 12000),
    "C": ("Es Teh", 5000),
    "D": ("Kopi", 7000)
}

# === Rekomendasi menu ===
rekomendasi = {
    "A": "💡 Es Teh cocok untuk menemani Nasi Goreng 🍹",
    "B": "💡 Es Teh dingin pas banget sama Mie Ayam 🍜",
    "C": "💡 Kopi panas enak diminum setelah Es Teh ☕",
    "D": "💡 Donat manis cocok untuk teman minum Kopi 🍩"
}

# === STATE penyimpanan sementara ===
if "keranjang" not in st.session_state:
    st.session_state.keranjang = {}

# --- PILIH MENU ---
st.header("📋 Pilih Menu")
for kode, (nama, harga) in daftar_harga.items():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"**{nama}**")
    with col2:
        st.write(f"Rp{harga}")
    with col3:
        jumlah = st.number_input(f"Jumlah {nama}", min_value=0, key=kode)
        if jumlah > 0:
            st.session_state.keranjang[kode] = jumlah
            if kode in rekomendasi:
                st.info(rekomendasi[kode])

# --- Tampilkan Ringkasan Pesanan ---
if st.session_state.keranjang:
    st.header("🧾 Ringkasan Pesanan")
    total = 0
    for kode, jumlah in st.session_state.keranjang.items():
        nama, harga = daftar_harga[kode]
        subtotal = harga * jumlah
        st.write(f"{nama} ({jumlah}x) = Rp{subtotal}")
        total += subtotal
    st.write(f"**Total sebelum diskon: Rp{total}**")

    # === SISTEM DISKON ===
    st.subheader("🎟️ Kode Diskon")
    use_diskon = st.checkbox("Pakai kode diskon?")
    diskon = 0
    if use_diskon:
        kode = st.text_input("Masukkan kode diskon (HEMAT10 / MAKAN20 / KOPI5K)").upper()
        if kode == "HEMAT10":
            diskon = total * 0.10
            st.success("✅ Kode diterima! Diskon 10%")
        elif kode == "MAKAN20":
            diskon = total * 0.20
            st.success("✅ Kode diterima! Diskon 20%")
        elif kode == "KOPI5K":
            diskon = 5000
            st.success("✅ Kode diterima! Potongan Rp5.000")
        elif kode:
            st.error("❌ Kode tidak valid.")
    total_setelah_diskon = total - diskon
    if diskon > 0:
        st.write(f"Total diskon: Rp{int(diskon)}")
    st.write(f"**Total setelah diskon: Rp{int(total_setelah_diskon)}**")

    # === PEMBAYARAN ===
    st.header("💰 Pembayaran")
    metode = st.radio("Pilih metode pembayaran:", ["Tunai", "Non Tunai (QRIS)"])
    if metode == "Tunai":
        bayar = st.number_input("Masukkan nominal uang:", min_value=0)
        if bayar:
            if bayar < total_setelah_diskon:
                st.warning("⚠️ Uang anda kurang!")
            elif bayar == total_setelah_diskon:
                st.success("✅ Pembayaran pas. Terima kasih!")
            else:
                kembalian = bayar - total_setelah_diskon
                st.success(f"✅ Pembayaran berhasil! Kembalian: Rp{kembalian}")
    else:
        st.info("💳 Silakan scan kode QR untuk pembayaran non-tunai.")

    # === SISTEM POIN ===
    poin = int(total_setelah_diskon // 10000)
    st.write(f"🎁 Anda mendapatkan **{poin} poin reward!**")

    # Simulasi penyimpanan poin
    if "total_poin" not in st.session_state:
        st.session_state.total_poin = 0
    st.session_state.total_poin += poin
    st.write(f"⭐ Total poin Anda saat ini: {st.session_state.total_poin}")

    # === STRUK PEMBELIAN ===
    st.header("🧾 Struk Pembelian")
    for kode, jumlah in st.session_state.keranjang.items():
        nama, harga = daftar_harga[kode]
        st.write(f"- {nama} ({jumlah}x) - Rp{harga * jumlah}")
    if diskon > 0:
        st.write(f"**Diskon diterapkan:** Rp{int(diskon)}")
    st.write(f"**Total Pembayaran:** Rp{int(total_setelah_diskon)}")
    st.write(f"**Poin Didapat:** {poin}")
    st.write(f"**Total Poin:** {st.session_state.total_poin}")

    st.success("Terima kasih telah berbelanja di Self Cashier Machine 💖")

else:
    st.info("Silakan pilih menu terlebih dahulu.")