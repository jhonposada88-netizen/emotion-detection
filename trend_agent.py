"""Agente que busca ideas tendencia en redes sociales para monetizar en Colombia.

Uso:
    pip install claude-agent-sdk
    export ANTHROPIC_API_KEY=...
    python trend_agent.py
    python trend_agent.py "TikTok y nichos de belleza"
"""
import asyncio
import re
import sys
from datetime import date
from pathlib import Path

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    query,
)

SYSTEM_PROMPT = """Eres un estratega de contenido y monetización digital especializado en Colombia.

Tu trabajo: investigar en la web las tendencias ACTUALES en redes sociales
(TikTok, Instagram, YouTube, Facebook, X, WhatsApp Channels) y proponer ideas
concretas para monetizar en Colombia.

Para cada idea entrega:
1. Nombre de la idea y red social principal.
2. Por qué es tendencia ahora (con la fuente consultada).
3. Cómo monetizar: afiliados, UGC para marcas, venta de productos/servicios,
   suscripciones, publicidad, cursos, etc.
4. Inversión inicial estimada en COP y dificultad (baja/media/alta).
5. Primeros 3 pasos para empezar esta semana.
6. Medios de cobro viables en Colombia (Nequi, Daviplata, PSE, Mercado Pago,
   PayPal, Payoneer, etc.) y consideraciones legales/tributarias básicas (RUT, DIAN).

Reglas:
- Busca primero en la web; no inventes datos ni cifras. Si no hay dato, dilo.
- Prioriza ideas realistas para el mercado colombiano (poder adquisitivo,
  regionalismos, fechas como Black Friday, prima, Amor y Amistad, Navidad).
- Entrega entre 5 y 8 ideas ordenadas de mayor a menor potencial.
- Cuando el enfoque lo pida, combina cada idea con IA generativa para crear
  contenido (Gemini, Veo, Imagen, NotebookLM, etc.): qué parte del flujo
  automatiza la IA (guiones, imágenes, video, voz, subtítulos), costo/plan
  gratuito disponible y límites o riesgos (etiquetado de contenido sintético,
  derechos de autor, políticas de monetización de cada plataforma).
- Responde en español."""


async def main(tema: str) -> None:
    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        setting_sources=[],
        allowed_tools=["WebSearch", "WebFetch"],
        max_turns=15,
    )
    prompt = (
        f"Hoy es {date.today():%d-%m-%Y}. Dame ideas tendencia para monetizar "
        f"en Colombia. Enfoque: {tema}"
    )
    partes: list[str] = []
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
                    partes.append(block.text)
        elif isinstance(message, ResultMessage) and message.total_cost_usd:
            print(f"\n(costo: ${message.total_cost_usd:.4f} USD)")

    if partes:
        slug = re.sub(r"[^a-z0-9]+", "-", tema.lower()).strip("-")[:50] or "general"
        destino = Path("resultados") / f"{date.today():%Y-%m-%d}-{slug}.md"
        destino.parent.mkdir(exist_ok=True)
        destino.write_text("\n".join(partes), encoding="utf-8")
        print(f"\nGuardado en {destino}")


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "todas las redes y nichos"))
