import os
import cv2
import shutil
import hashlib
from icrawler.builtin import BingImageCrawler

output_root = "C:/Users/anais/OneDrive/Escritorio/TareaIA/InteligenciArtificial/Animales/mariquitas" 
size = (28, 28)
max_images_per_keyword = 800 

keywords = {
    "Mariquitas": [ "Coccinella septempunctata","ladybug","catarina","Harmonia axyridis","Adalia bipunctata","Chilocorus stigma","Psyllobora vigintiduopunctata",
                   "Hippodamia convergens","Chilocorus","Propylea quatuordecimpunctata","Epilachna","Novius cardinalis" , "ladybug eating aphid",
                   "Coccinellidae underside view","ladybug elytra open","ladybug macro photography head","ladybug 7 spot" ,"ladybug 2 spot" ,"ladybug 13 spot",
              "yellow ladybird black spots","black ladybug red spots","unspotted ladybug","ladybug orange color"  
  
    ]
    
}

def download_images(keyword, folder, max_num):
    """Descarga imágenes desde Bing."""
    print(f"🔍 Descargando: {keyword}")
    crawler = BingImageCrawler(storage={"root_dir": folder})
    crawler.crawl(keyword=keyword, max_num=max_num)

def resize_and_clean(folder):
    """Redimensiona imágenes a 28x28 y elimina duplicadas o dañadas."""
    print(f"🧹 Limpiando y redimensionando en: {folder}")
    hashes = set()
    count = 0
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        try:
            img = cv2.imread(path)
            if img is None:
                os.remove(path)
                continue

            # Redimensionar
            img = cv2.resize(img, size)

            # Eliminar duplicadas (hash)
            img_hash = hashlib.md5(img.tobytes()).hexdigest()
            if img_hash in hashes:
                os.remove(path)
                continue
            hashes.add(img_hash)

            # Sobrescribir imagen limpia
            cv2.imwrite(path, img)
            count += 1

        except Exception as e:
            # print(f"⚠️ Error con {filename}: {e}") # Se comenta para no saturar la consola
            if os.path.exists(path):
                os.remove(path)
    print(f"✅ Total de imágenes válidas en '{os.path.basename(folder)}': {count}")

def unir_subcarpetas(categoria):
    """Une todas las subcarpetas de una categoría en una carpeta final."""
    carpeta_categoria = os.path.join(output_root, categoria)
    carpeta_final = os.path.join(output_root, f"{categoria}_final")
    os.makedirs(carpeta_final, exist_ok=True)
    
    contador = 0
    for subdir in os.listdir(carpeta_categoria):
        subruta = os.path.join(carpeta_categoria, subdir)
        if os.path.isdir(subruta):
            for file in os.listdir(subruta):
                origen = os.path.join(subruta, file)
                if os.path.isfile(origen):
                    nuevo_nombre = f"{categoria}_{contador}.jpg"
                    destino = os.path.join(carpeta_final, nuevo_nombre)
                    # Usamos shutil.move para evitar la duplicación de espacio si el origen y el destino están en la misma unidad
                    # Si no quieres mover, cambia a shutil.copy(origen, destino)
                    shutil.move(origen, destino) 
                    contador += 1
    print(f"📦 '{os.path.basename(carpeta_final)}' creado con {contador} imágenes.")


if __name__ == "__main__":
    for animal, palabras in keywords.items():
        print(f"\n🐾 === Procesando {animal} ===")
        animal_folder = os.path.join(output_root, animal)
        os.makedirs(animal_folder, exist_ok=True)

        # Descargar y limpiar
        for palabra in palabras:
            keyword_folder = os.path.join(animal_folder, palabra.replace(" ", "_"))
            os.makedirs(keyword_folder, exist_ok=True)
            download_images(palabra, keyword_folder, max_images_per_keyword)
            # Limpiar y redimensionar
            resize_and_clean(keyword_folder)

        # Unir en una carpeta final
        unir_subcarpetas(animal)

    print("\n🎉 Proceso de recolección completo. Revisa tu carpeta de salida para el total de imágenes.")
