import os
import argparse
import google.generativeai as genai
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("\n[!] ERROR: No se encontró la API Key de Google.")
        print("Por favor, agregá tu clave en el archivo .env como 'GOOGLE_API_KEY=tu_clave_aca'")
        return

    # Initialize Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')

    # Parse arguments
    parser = argparse.ArgumentParser(description="Consulta interna a la IA de Google para desarrollo.")
    parser.add_argument("prompt", help="Tu consulta o instrucción para la IA.")
    parser.add_argument("--file", help="Ruta de un archivo opcional para enviar como contexto.")
    args = parser.parse_args()

    context = ""
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
                context = f"\n\n--- CONTEXTO DEL ARCHIVO ({args.file}) ---\n{content}\n--- FIN DEL CONTEXTO ---\n"
        except Exception as e:
            print(f"[!] Error leyendo el archivo {args.file}: {e}")

    full_prompt = f"{args.prompt}\n{context}\nResponde siempre en español y de forma técnica pero directa."

    try:
        print("\n--- Consultando a Gemini... ---\n")
        response = model.generate_content(full_prompt)
        print(response.text)
    except Exception as e:
        print(f"[!] Error en la consulta a la API: {e}")

if __name__ == "__main__":
    main()
