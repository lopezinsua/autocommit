# COMMIT-AI — Brief para Claude Code

> Brief autocontenido. Léelo entero antes de escribir una sola línea de código.

---

## Qué construir

Una herramienta CLI de Python que lee el `git diff --staged` del repositorio actual y genera automáticamente un mensaje de commit en formato Conventional Commits usando la API de OpenAI.

**Nombre del proyecto:** `commit-ai`
**Repositorio destino:** https://github.com/lopezinsua/commit-ai

---

## UX final

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

# Flag --yes para confirmar automáticamente
python commit.py --yes

# Flag --lang para cambiar idioma
python commit.py --lang en
```

- Si no hay nada staged: avisa y sale sin hacer nada
- Si el diff es demasiado largo: lo trunca inteligentemente y avisa
- El mensaje generado sigue Conventional Commits: `type(scope): description`

---

## Stack

| Componente | Librería | Notas |
|------------|----------|-------|
| LLM | `openai` (gpt-4o-mini) | sin streaming, respuesta corta |
| Git | `subprocess` (stdlib) | ejecuta `git diff --staged` y `git commit` |
| CLI | `argparse` (stdlib) | flags: --yes, --lang, --dry-run |
| Config | `python-dotenv` | `OPENAI_API_KEY` en `.env` |

**Python:** 3.11+
**Sin dependencias extra.** Todo con stdlib + openai + python-dotenv.

---

## Estructura de archivos

```
commit-ai/
├── commit.py         # Todo el código — un solo archivo
├── .env.example
├── requirements.txt
├── .gitignore
└── README.md
```

**Regla:** Todo en un solo archivo `commit.py`. Menos de 120 líneas total. Es una herramienta pequeña, no una aplicación.

---

## Lógica interna (implementar en este orden)

```python
# 1. Obtener el diff
diff = subprocess.run(['git', 'diff', '--staged'], capture_output=True, text=True).stdout
if not diff:
    print("Nada en el stage. Usa git add primero.")
    sys.exit(0)

# 2. Truncar si es muy largo (máx ~3000 chars para no gastar tokens)
if len(diff) > 3000:
    diff = diff[:3000] + "\n... [truncado]"

# 3. Llamar al LLM
message = call_openai(diff, lang=args.lang)

# 4. Mostrar + confirmar
print(message)
if args.yes or input("¿Confirmar commit? [Y/n]: ").lower() in ('', 'y'):
    subprocess.run(['git', 'commit', '-m', message])
```

---

## Prompt del sistema

```
Eres un experto en git y clean code.
Genera UN mensaje de commit en formato Conventional Commits:
  type(scope): descripción corta (máx 72 chars)

  Cuerpo opcional (máx 3 líneas, solo si es necesario).

Types válidos: feat, fix, refactor, docs, style, test, chore.
El scope es el módulo o archivo principal afectado.
Responde SOLO con el mensaje, sin explicaciones, sin markdown.
Si el idioma solicitado es 'es', escribe en español. Si es 'en', en inglés.
```

---

## Flags CLI

| Flag | Descripción |
|------|-------------|
| `--yes` / `-y` | Confirma el commit sin preguntar |
| `--lang` | Idioma del mensaje: `es` (default) o `en` |
| `--dry-run` | Muestra el mensaje generado pero no hace commit |

---

## README — lo que debe transmitir

- Problema: escribir buenos mensajes de commit es tedioso
- Solución: 1 comando, mensaje generado, confirmas o no
- Instalación: 3 comandos (clone, pip install, configurar .env)
- Uso: copiar los 3 ejemplos de la sección UX
- Nota honesta: usa gpt-4o-mini, necesitas API key de OpenAI

Tono: directo, útil, sin marketing. Sin emojis.

---

## Lo que NO hacer

- No crear interfaz web ni TUI
- No añadir soporte para múltiples LLMs (solo OpenAI)
- No gestionar el `.env` automáticamente
- No hardcodear la API key
- No tests
- No superar 120 líneas en `commit.py`

---

## Entregables

1. `commit.py` funcional (≤120 líneas)
2. `.env.example`
3. `requirements.txt` con versiones exactas
4. `README.md` con instalación + ejemplos reales

---

## Contexto del autor

- **Autor:** Lopez Insua — Estudiante de Ingeniería Informática, especialización IA
- **GitHub:** https://github.com/lopezinsua
- **Portfolio:** https://lopez-insua-portfolio.vercel.app
