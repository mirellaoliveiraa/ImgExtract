import os
from pdf2image import convert_from_path
from PIL import Image

POPPLER_PATH = r"C:\Users\Mirella Chaves\Desktop\poppler-24.08.0\Library\bin"

BASE = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(BASE, "input_pdfs")
OUTPUT = os.path.join(BASE, "output_images")
WIDTH, HEIGHT = 1080, 1920
import os
import csv
from pdf2image import convert_from_path
from PIL import Image

POPPLER_PATH = r"C:\Users\Mirella Chaves\Desktop\poppler-24.08.0\Library\bin"
BASE = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(BASE, "input_pdfs")
OUTPUT = os.path.join(BASE, "output_images")
LOG_CSV = os.path.join(BASE, "log.csv")
WIDTH, HEIGHT = 1080, 1920

def converter():
    print("[INFO] Iniciando conversão...")
    os.makedirs(INPUT, exist_ok=True)
    os.makedirs(OUTPUT, exist_ok=True)

    arquivos = [f for f in os.listdir(INPUT) if f.lower().endswith(".pdf")]
    if not arquivos:
        print("[ERRO] Nenhum PDF encontrado em input_pdfs/")
        return

    with open(LOG_CSV, "w", newline="", encoding="utf-8") as logfile:
        writer = csv.writer(logfile)
        writer.writerow(["nome_pdf", "total_paginas", "caminho_da_imagem"])

        for pdf in arquivos:
            try:
                print(f"[...] Convertendo: {pdf}")
                caminho = os.path.join(INPUT, pdf)
                nome = os.path.splitext(pdf)[0]
                paginas = convert_from_path(caminho, poppler_path=POPPLER_PATH)

                if len(paginas) == 1:
                    img = paginas[0].resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
                    saida = os.path.join(OUTPUT, f"{nome}.jpg")
                    img.save(saida)
                    writer.writerow([pdf, 1, saida])
                    print(f"[OK] Salvo: {saida}")
                else:
                    pasta = os.path.join(OUTPUT, nome)
                    os.makedirs(pasta, exist_ok=True)
                    for i, pagina in enumerate(paginas):
                        img = pagina.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
                        saida = os.path.join(pasta, f"{nome}_page_{i+1}.jpg")
                        img.save(saida)
                        writer.writerow([pdf, len(paginas), saida])
                    print(f"[OK] {len(paginas)} páginas salvas em: {pasta}")
            except Exception as e:
                print(f"[ERRO] {pdf}: {e}")

if __name__ == "__main__":
    converter()
