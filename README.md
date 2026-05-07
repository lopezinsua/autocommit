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
python commit.py

Analizando cambios...

feat(indexer): add overlap parameter to chunk splitting

Añade parámetro `overlap` configurable al chunker. Mejora la
recuperación en documentos con secciones relacionadas.

¿Confirmar commit? [Y/n]: y
[main 3a4f2c1] feat(indexer): add overlap parameter to chunk splitting

# Confirmar automáticamente
python commit.py --yes

# Mensaje en inglés
python commit.py --lang en

# Solo ver el mensaje, sin hacer commit
python commit.py --dry-run
```

---

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
