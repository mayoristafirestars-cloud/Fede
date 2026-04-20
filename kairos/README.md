# Kairos — SEO Content-as-a-Service

> Pipeline de agentes IA que publica contenido SEO que rankea.
> Target: SaaS B2B 10-200 empleados. Retainer US$ 1.5-5k/mes.

Ver investigación completa en [`../investigaciones/empresa-01/`](../investigaciones/empresa-01/).

## Estructura

```
kairos/
├── kairos/
│   ├── agents/
│   │   └── keyword_researcher.py   # Agente #1 del pipeline
│   ├── clients/
│   │   └── dataforseo.py           # Cliente API (con fallback a mock)
│   ├── schemas.py                  # Modelos Pydantic I/O
│   └── cli.py                      # CLI para correr agentes
├── examples/
│   └── research_example.py         # Ejemplo de uso
├── requirements.txt
└── .env.example
```

## Estado actual

**MVP del Agente #1: Keyword Researcher** ✅

Input: dominio + seed topic + audiencia
Output: cluster de keywords con primary, secondary, PAA, intención y notas de gap

## Setup

```bash
cd kairos
pip install -r requirements.txt
cp .env.example .env
# Editar .env con tu ANTHROPIC_API_KEY
```

Para correr sin DataForSEO (modo mock):

```bash
python -m kairos.cli research \
  --domain acme.com \
  --topic "customer onboarding automation" \
  --audience "SaaS customer success managers"
```

Con DataForSEO (cuando tengas las credenciales):

```bash
export DATAFORSEO_LOGIN=your-login
export DATAFORSEO_PASSWORD=your-password
python -m kairos.cli research --domain ... --real-data
```

## Próximos agentes

- [ ] Outline Writer
- [ ] Drafter
- [ ] Fact-Checker
- [ ] SEO Optimizer
- [ ] Publisher (WordPress primero)

Spec técnica completa: [`../investigaciones/empresa-01/stack-tecnico-agentes.md`](../investigaciones/empresa-01/stack-tecnico-agentes.md).

## Modelo usado

- **Claude Opus 4.7** con adaptive thinking para razonamiento SEO estratégico
- Efecto: el agente decide dinámicamente cuánto pensar por cluster
- Costo estimado por ejecución: US$ 0.10-0.30
