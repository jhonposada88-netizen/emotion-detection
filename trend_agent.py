"""Agente que busca ideas tendencia en redes sociales para monetizar en Colombia.

Uso:
    pip install claude-agent-sdk
    export ANTHROPIC_API_KEY=...
    python trend_agent.py
    python trend_agent.py "TikTok y nichos de belleza"
"""
import asyncio
import sys

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
- Responde en español."""


async def main(tema: str) -> None:
    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        allowed_tools=["WebSearch", "WebFetch"],
        max_turns=15,
    )
    prompt = f"Dame ideas tendencia para monetizar en Colombia. Enfoque: {tema}"
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
        elif isinstance(message, ResultMessage) and message.total_cost_usd:
            print(f"\n(costo: ${message.total_cost_usd:.4f} USD)")


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "todas las redes y nichos"))
