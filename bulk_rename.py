
from pathlib import Path
import re
import fitz

# Folder tempat PDF disimpan
BASE_DIR = Path(__file__).resolve().parent
PDF_DIR = BASE_DIR / "PDF"


def extract_reference(pdf_path):
    """Mengambil Nomor Referensi dari isi PDF."""

    try:
        with fitz.open(pdf_path) as doc:
            full_text = "\n".join(page.get_text() for page in doc)

        match = re.search(
            r"Referensi\s*:\s*(.+)",
            full_text,
            re.IGNORECASE
        )

        if not match:
            return None

        reference = match.group(1).strip()

        # Bersihkan tanda kurung di awal/akhir
        reference = reference.strip("() \t\r\n")

        # Hapus spasi, slash, dan backslash
        reference = re.sub(r"[\s/\\]", "", reference)

        # Validasi nama file
        if not reference:
            return None

        return reference

    except Exception as error:
        print(f"[ERROR] {pdf_path.name}: {error}")
        return None


def main():
    print("=" * 55)
    print("       BULK RENAME FAKTUR PAJAK - MAC")
    print("=" * 55)

    if not PDF_DIR.exists():
        print("[ERROR] Folder PDF tidak ditemukan.")
        return

    pdf_files = list(PDF_DIR.glob("*.pdf"))

    if not pdf_files:
        print("[INFO] Tidak ada file PDF.")
        return

    success = 0
    skipped = 0

    for pdf in pdf_files:
        print(f"\nProcessing: {pdf.name}")

        reference = extract_reference(pdf)

        if not reference:
            print("[WARNING] Nomor Referensi tidak ditemukan.")
            skipped += 1
            continue

        new_path = pdf.with_name(reference + ".pdf")

        if pdf.name == new_path.name:
            print("[INFO] Nama file sudah sesuai.")
            skipped += 1
            continue

        if new_path.exists():
            print(f"[WARNING] File tujuan sudah ada: {new_path.name}")
            skipped += 1
            continue

        try:
            pdf.rename(new_path)
            print(f"[SUCCESS] {pdf.name} -> {new_path.name}")
            success += 1

        except Exception as error:
            print(f"[ERROR] Gagal rename: {error}")
            skipped += 1

    print("\n" + "=" * 55)
    print(f"Berhasil : {success}")
    print(f"Dilewati : {skipped}")
    print("=" * 55)


if __name__ == "__main__":
    main()
