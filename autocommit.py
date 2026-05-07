import argparse
import subprocess
import sys

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

SYSTEM_PROMPT = (
    "Eres un experto en git y clean code.\n"
    "Genera UN mensaje de commit en formato Conventional Commits:\n"
    "  type(scope): descripción corta (máx 72 chars)\n\n"
    "  Cuerpo opcional (máx 3 líneas, solo si es necesario).\n\n"
    "Types válidos: feat, fix, refactor, docs, style, test, chore.\n"
    "El scope es el módulo o archivo principal afectado.\n"
    "Responde SOLO con el mensaje, sin explicaciones, sin markdown.\n"
    "Si el idioma solicitado es 'es', escribe en español. Si es 'en', en inglés."
)

MAX_DIFF_CHARS = 3000


def get_staged_diff() -> str:
    result = subprocess.run(
        ["git", "diff", "--staged"], capture_output=True, text=True
    )
    return result.stdout


def generate_message(diff: str, lang: str) -> str:
    client = Groq()
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Idioma: {lang}\n\nDiff:\n{diff}"},
        ],
        max_tokens=200,
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera mensajes de commit automáticamente.")
    parser.add_argument("--yes", "-y", action="store_true", help="Confirma sin preguntar")
    parser.add_argument(
        "--lang", default="es", choices=["es", "en"], help="Idioma del mensaje (default: es)"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Muestra el mensaje pero no hace commit"
    )
    args = parser.parse_args()

    diff = get_staged_diff()
    if not diff:
        print("Nada en el stage. Usa git add primero.")
        sys.exit(0)

    if len(diff) > MAX_DIFF_CHARS:
        diff = diff[:MAX_DIFF_CHARS] + "\n... [truncado]"
        print("Aviso: diff muy largo, truncado a 3000 caracteres.")

    print("Analizando cambios...")

    try:
        message = generate_message(diff, lang=args.lang)
    except Exception as e:
        print(f"Error al generar el mensaje: {e}")
        sys.exit(1)

    if not message:
        print("No se pudo generar un mensaje. Intenta de nuevo.")
        sys.exit(1)

    print(f"\n{message}\n")

    if args.dry_run:
        sys.exit(0)

    confirmed = args.yes or input("¿Confirmar commit? [Y/n]: ").strip().lower() in ("", "y")
    if confirmed:
        subprocess.run(["git", "commit", "-m", message], check=False)


if __name__ == "__main__":
    main()
