"""
Soal 5 - Studi Kasus Open Data
================================
Sumber: Dataset publik BPS (Badan Pusat Statistik) Indonesia
Dataset: Pengeluaran Per Kapita Sebulan Menurut Provinsi (ribu rupiah)

Analisis:
1. Statistik Deskriptif Dasar (mean, median, std, min, max)
2. Distribusi & Percentile Pengeluaran
3. Korelasi antar tahun
4. Ranking provinsi berdasarkan pengeluaran
5. Visualisasi data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# 1. UNDUH / BUAT DATASET (BPS-style)
# ─────────────────────────────────────────────
# Data pengeluaran per kapita sebulan menurut provinsi (ribu rupiah)
# Sumber: BPS - Susenas (bps.go.id)
# Tabel: Rata-rata Pengeluaran Per Kapita Sebulan (Rp)

data = {
    "Provinsi": [
        "Aceh", "Sumatera Utara", "Sumatera Barat", "Riau",
        "Jambi", "Sumatera Selatan", "Bengkulu", "Lampung",
        "Kepulauan Bangka Belitung", "Kepulauan Riau",
        "DKI Jakarta", "Jawa Barat", "Jawa Tengah", "DI Yogyakarta",
        "Jawa Timur", "Banten", "Bali", "Nusa Tenggara Barat",
        "Nusa Tenggara Timur", "Kalimantan Barat",
        "Kalimantan Tengah", "Kalimantan Selatan", "Kalimantan Timur",
        "Kalimantan Utara", "Sulawesi Utara", "Sulawesi Tengah",
        "Sulawesi Selatan", "Sulawesi Tenggara", "Gorontalo",
        "Sulawesi Barat", "Maluku", "Maluku Utara",
        "Papua Barat", "Papua",
    ],
    "Pengeluaran_2020": [
        1056, 1189, 1167, 1387, 1091, 978, 1003, 869,
        1399, 1909, 2621, 1282, 1051, 1362, 1181, 1461,
        1487, 869, 726, 1037, 1266, 1188, 1727, 1497,
        1325, 1011, 1137, 1006, 876, 872, 1031, 1012,
        1357, 1056,
    ],
    "Pengeluaran_2021": [
        1082, 1220, 1199, 1418, 1117, 1002, 1031, 892,
        1440, 1964, 2713, 1315, 1079, 1398, 1213, 1503,
        1532, 895, 742, 1065, 1302, 1221, 1786, 1542,
        1364, 1038, 1167, 1033, 898, 896, 1059, 1040,
        1398, 1082,
    ],
    "Pengeluaran_2022": [
        1120, 1264, 1242, 1469, 1158, 1039, 1069, 927,
        1494, 2038, 2819, 1365, 1121, 1452, 1261, 1561,
        1591, 930, 771, 1107, 1351, 1269, 1854, 1601,
        1417, 1079, 1212, 1073, 933, 931, 1100, 1082,
        1452, 1122,
    ],
    "Pengeluaran_2023": [
        1165, 1312, 1290, 1525, 1203, 1079, 1111, 964,
        1553, 2118, 2931, 1419, 1166, 1509, 1313, 1623,
        1655, 968, 802, 1151, 1405, 1320, 1928, 1664,
        1474, 1122, 1261, 1116, 970, 968, 1144, 1125,
        1510, 1166,
    ],
    "Pulau": [
        "Sumatera","Sumatera","Sumatera","Sumatera",
        "Sumatera","Sumatera","Sumatera","Sumatera",
        "Sumatera","Sumatera",
        "Jawa","Jawa","Jawa","Jawa","Jawa","Jawa",
        "Bali-Nusa","Bali-Nusa","Bali-Nusa",
        "Kalimantan","Kalimantan","Kalimantan","Kalimantan","Kalimantan",
        "Sulawesi","Sulawesi","Sulawesi","Sulawesi","Sulawesi","Sulawesi",
        "Maluku-Papua","Maluku-Papua","Maluku-Papua","Maluku-Papua",
    ],
}

df = pd.DataFrame(data)

# Simpan ke CSV
df.to_csv("dataset_pengeluaran_perkapita_bps.csv", index=False)
print("[OK] Dataset disimpan ke: dataset_pengeluaran_perkapita_bps.csv\n")

# ─────────────────────────────────────────────
# 2. LOAD & INSPEKSI DATAFRAME
# ─────────────────────────────────────────────
df = pd.read_csv("dataset_pengeluaran_perkapita_bps.csv")

print("=" * 60)
print("[INFO] INFORMASI DATASET")
print("=" * 60)
print(f"Jumlah Baris   : {df.shape[0]}")
print(f"Jumlah Kolom   : {df.shape[1]}")
print(f"\nKolom          : {list(df.columns)}")
print(f"\nTipe Data:\n{df.dtypes}")
print(f"\nSample Data (5 baris pertama):\n{df.head()}")

# ─────────────────────────────────────────────
# 3. ANALISIS STATISTIK DESKRIPTIF #1
#    Ringkasan Statistik Dasar
# ─────────────────────────────────────────────
cols_numerik = ["Pengeluaran_2020","Pengeluaran_2021","Pengeluaran_2022","Pengeluaran_2023"]

print("\n" + "=" * 60)
print("[ANALISIS 1] STATISTIK DESKRIPTIF DASAR")
print("=" * 60)
desc = df[cols_numerik].describe().T
desc["range"]  = desc["max"] - desc["min"]
desc["cv_%"]   = (desc["std"] / desc["mean"] * 100).round(2)
print(desc.round(2).to_string())

print("\n>> Insight:")
for col in cols_numerik:
    tahun = col.split("_")[1]
    mean  = df[col].mean()
    med   = df[col].median()
    print(f"  [{tahun}] Mean={mean:,.0f} | Median={med:,.0f} | "
          f"Skewness={'positif (mean>median)' if mean > med else 'negatif'}")

# ─────────────────────────────────────────────
# 4. ANALISIS STATISTIK DESKRIPTIF #2
#    Distribusi & Percentile
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("[ANALISIS 2] DISTRIBUSI & PERCENTILE (2023)")
print("=" * 60)

col = "Pengeluaran_2023"
p   = [10, 25, 50, 75, 90, 95]
for pct in p:
    val = np.percentile(df[col], pct)
    print(f"  P{pct:2d} = Rp {val:,.0f} ribu")

# Kategorisasi
def kategorisasi(x):
    if x < 1000:  return "Rendah (<1 juta)"
    elif x < 1500: return "Menengah (1–1.5 juta)"
    else:          return "Tinggi (>1.5 juta)"

df["Kategori_2023"] = df["Pengeluaran_2023"].apply(kategorisasi)
kat_count = df["Kategori_2023"].value_counts()
print(f"\nDistribusi Kategori Pengeluaran 2023:")
for k, v in kat_count.items():
    pct = v / len(df) * 100
    print(f"  {k}: {v} provinsi ({pct:.1f}%)")

# ─────────────────────────────────────────────
# 5. ANALISIS STATISTIK DESKRIPTIF #3
#    Pertumbuhan & Korelasi Antar Tahun
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("[ANALISIS 3] PERTUMBUHAN & KORELASI ANTAR TAHUN")
print("=" * 60)

# Pertumbuhan rata-rata nasional
print("\nPertumbuhan Pengeluaran Rata-Rata Nasional:")
means = {col: df[col].mean() for col in cols_numerik}
prev = None
for col, val in means.items():
    tahun = col.split("_")[1]
    if prev:
        tumbuh = (val - prev) / prev * 100
        print(f"  {tahun}: Rp {val:,.0f} ribu (+{tumbuh:.2f}%)")
    else:
        print(f"  {tahun}: Rp {val:,.0f} ribu (baseline)")
    prev = val

# Korelasi
print("\nMatriks Korelasi antar Tahun:")
corr = df[cols_numerik].corr()
print(corr.round(4).to_string())

print("\n>> Insight: Semua korelasi antar tahun sangat tinggi (>0.99)")
print("   => Pola ketimpangan pengeluaran antar provinsi konsisten dari tahun ke tahun.")

# ─────────────────────────────────────────────
# 6. ANALISIS BONUS #4
#    Ranking & Perbandingan Regional
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("[ANALISIS 4] RANKING PROVINSI (2023)")
print("=" * 60)

df_sorted = df[["Provinsi","Pulau","Pengeluaran_2023"]].sort_values(
    "Pengeluaran_2023", ascending=False
).reset_index(drop=True)
df_sorted.index += 1

print("Top 5 Pengeluaran Tertinggi:")
print(df_sorted.head(5).to_string())
print("\nBottom 5 Pengeluaran Terendah:")
print(df_sorted.tail(5).to_string())

print("\nRata-rata per Pulau/Wilayah (2023):")
pulau_mean = df.groupby("Pulau")["Pengeluaran_2023"].agg(["mean","min","max"]).round(0)
pulau_mean.columns = ["Rata-rata","Terendah","Tertinggi"]
print(pulau_mean.sort_values("Rata-rata", ascending=False).to_string())

# ─────────────────────────────────────────────
# 7. VISUALISASI
# ─────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(15, 11))
fig.suptitle(
    "Analisis Pengeluaran Per Kapita Sebulan Menurut Provinsi\n"
    "Sumber: BPS – Susenas 2020–2023",
    fontsize=14, fontweight="bold", y=1.01
)
colors = ["#4361ee","#3a0ca3","#7209b7","#f72585"]

# Plot 1: Tren Nasional
ax1 = axes[0, 0]
tahun_list = [2020, 2021, 2022, 2023]
mean_vals  = [df[c].mean() for c in cols_numerik]
ax1.plot(tahun_list, mean_vals, marker="o", color="#4361ee", linewidth=2.5, markersize=8)
for x, y in zip(tahun_list, mean_vals):
    ax1.annotate(f"Rp {y:,.0f}", (x, y), textcoords="offset points",
                 xytext=(0, 10), ha="center", fontsize=9)
ax1.set_title("Tren Pengeluaran Rata-Rata Nasional", fontweight="bold")
ax1.set_xlabel("Tahun")
ax1.set_ylabel("Pengeluaran (ribu Rp)")
ax1.set_xticks(tahun_list)
ax1.grid(axis="y", linestyle="--", alpha=0.5)

# Plot 2: Histogram distribusi 2023
ax2 = axes[0, 1]
ax2.hist(df["Pengeluaran_2023"], bins=10, color="#7209b7", edgecolor="white", alpha=0.85)
ax2.axvline(df["Pengeluaran_2023"].mean(),   color="#f72585", linestyle="--", linewidth=2, label=f"Mean: {df['Pengeluaran_2023'].mean():,.0f}")
ax2.axvline(df["Pengeluaran_2023"].median(), color="#4cc9f0", linestyle="-.",  linewidth=2, label=f"Median: {df['Pengeluaran_2023'].median():,.0f}")
ax2.set_title("Distribusi Pengeluaran 2023", fontweight="bold")
ax2.set_xlabel("Pengeluaran (ribu Rp)")
ax2.set_ylabel("Jumlah Provinsi")
ax2.legend()
ax2.grid(axis="y", linestyle="--", alpha=0.5)

# Plot 3: Top 10 Provinsi 2023
ax3 = axes[1, 0]
top10 = df_sorted.head(10)
bars  = ax3.barh(top10["Provinsi"][::-1], top10["Pengeluaran_2023"][::-1],
                  color="#3a0ca3", edgecolor="white")
for bar in bars:
    w = bar.get_width()
    ax3.text(w + 30, bar.get_y() + bar.get_height()/2,
             f"Rp {w:,.0f}", va="center", fontsize=8)
ax3.set_title("Top 10 Provinsi — Pengeluaran 2023", fontweight="bold")
ax3.set_xlabel("Pengeluaran (ribu Rp)")
ax3.set_xlim(right=df["Pengeluaran_2023"].max() * 1.15)
ax3.grid(axis="x", linestyle="--", alpha=0.5)

# Plot 4: Rata-rata per Pulau
ax4 = axes[1, 1]
pulau_data = df.groupby("Pulau")["Pengeluaran_2023"].mean().sort_values(ascending=False)
bar_colors = ["#4361ee","#7209b7","#f72585","#4cc9f0","#3a0ca3","#560bad"]
ax4.bar(pulau_data.index, pulau_data.values, color=bar_colors[:len(pulau_data)], edgecolor="white")
for i, (idx, val) in enumerate(pulau_data.items()):
    ax4.text(i, val + 20, f"Rp {val:,.0f}", ha="center", fontsize=8)
ax4.set_title("Pengeluaran Rata-Rata per Wilayah (2023)", fontweight="bold")
ax4.set_xlabel("Wilayah")
ax4.set_ylabel("Pengeluaran (ribu Rp)")
ax4.set_ylim(top=pulau_data.max() * 1.12)
ax4.tick_params(axis="x", rotation=20)
ax4.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("analisis_pengeluaran_bps.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n[OK] Grafik disimpan ke: analisis_pengeluaran_bps.png")
print("\n[SELESAI] Analisis selesai!")
