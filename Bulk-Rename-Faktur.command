
#!/bin/bash

cd "$(dirname "$0")" || exit 1

echo "================================================"
echo "       BULK RENAME FAKTUR PAJAK - macOS"
echo "================================================"
echo ""

# Detect Python 3
PYTHON="$(command -v python3)"

if [ -z "$PYTHON" ]; then
    echo "[ERROR] Python 3 tidak ditemukan."
    echo "Install Python 3 terlebih dahulu."
    read -r -p "Tekan Enter untuk keluar..."
    exit 1
fi

echo "[INFO] Python: $("$PYTHON" --version)"

# Check PyMuPDF
if ! "$PYTHON" -c "import fitz" >/dev/null 2>&1; then
    echo "[INFO] PyMuPDF belum tersedia."
    echo "[INFO] Menginstall PyMuPDF 1.24.14..."

    if ! "$PYTHON" -m pip install --user "pymupdf==1.24.14"; then
        echo ""
        echo "[ERROR] Instalasi PyMuPDF gagal."
        echo "Periksa koneksi internet dan Python."
        read -r -p "Tekan Enter untuk keluar..."
        exit 1
    fi
fi

# Verify dependency
if ! "$PYTHON" -c "import fitz" >/dev/null 2>&1; then
    echo "[ERROR] PyMuPDF tidak dapat diakses."
    read -r -p "Tekan Enter untuk keluar..."
    exit 1
fi

echo "[SUCCESS] PyMuPDF siap digunakan."
echo ""

# Execute rename script
"$PYTHON" bulk_rename.py
RESULT=$?

echo ""

if [ "$RESULT" -eq 0 ]; then
    echo "[SUCCESS] Proses rename selesai."
else
    echo "[ERROR] Proses rename mengalami kegagalan."
fi

echo ""
read -r -p "Tekan Enter untuk menutup..."
exit "$RESULT"
