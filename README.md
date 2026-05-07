# autocommit

Escribir buenos mensajes de commit lleva tiempo y disciplina. autocommit lee el diff staged y genera el mensaje por ti en formato Conventional Commits. Confirmas o no, y listo.

Usa `llama-3.1-8b-instant` via Groq. Necesitas una API key de GroqCloud (gratuita en https://console.groq.com).

---

## Instalación

```bash
git clone https://github.com/lopezinsua/autocommit
cd autocommit
pip install -r requirements.txt
cp .env.example .env   # añade tu GROQ_API_KEY
```

---

## Uso

```bash
# Uso básico — genera el mensaje y pregunta si confirmar
git add src/indexer.py
python autocommit.py

Analizando cambios...

feat(indexer): add overlap parameter to chunk splitting

Añade parámetro `overlap` configurable al chunker. Mejora la
recuperación en documentos con secciones relacionadas.

¿Confirmar commit? [Y/n]: y
[main 3a4f2c1] feat(indexer): add overlap parameter to chunk splitting

# Confirmar automáticamente
python autocommit.py --yes

# Mensaje en inglés
python autocommit.py --lang en

# Solo ver el mensaje, sin hacer commit
python autocommit.py --dry-run
```

---

## How it works

1. **Diff** — runs `git diff --staged` to get the exact changes queued for commit.
2. **Truncate** — caps the diff at 3000 characters to keep the API call fast and cheap.
3. **Generate** — sends the diff to Llama 3.1 8B (via Groq) with a system prompt that enforces Conventional Commits format.
4. **Confirm** — prints the message and asks for confirmation before running `git commit`.

## Flags

| Flag | Descripción |
|------|-------------|
| `--yes` / `-y` | Confirma el commit sin preguntar |
| `--lang` | Idioma del mensaje: `es` (default) o `en` |
| `--dry-run` | Muestra el mensaje generado pero no hace commit |

---

## Requisitos

- Python 3.11+
- API key de GroqCloud (`GROQ_API_KEY` en `.env`) — gratuita en https://console.groq.com

---

By [López Insua](https://github.com/lopezinsua)
