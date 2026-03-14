# Law Open Data Dedicated MCP

Dedicated MCP server for Korean constitutional-law and administrative-law retrieval with strict source separation.

This project is designed for accuracy-sensitive legal use. It exposes exact tools instead of forcing all requests through a single integrated QA tool.

## Tool philosophy

- Use statute tools for statutes
- Use precedent tools for precedents
- Use interpretation tools for interpretation
- Keep mixed QA as optional, not primary

## Primary tools

- `health`
- `search_law_tool`
- `get_law_detail_tool`
- `get_law_article_tool`
- `search_precedent_tool`
- `get_precedent_tool`
- `search_constitutional_decision_tool`
- `get_constitutional_decision_tool`
- `search_administrative_appeal_tool`
- `get_administrative_appeal_tool`
- `search_administrative_rule_tool`
- `search_law_interpretation_tool`
- `get_law_interpretation_tool`

These tools are intended to support exam-style verification flows such as:

- verifying statute name + article number for constitutional/administrative law MCQs
- verifying Supreme Court case numbers for precedent-based options
- verifying Constitutional Court decisions for constitutional law options
- checking administrative appeals, administrative rules, and ministry interpretations for administrative-law edge cases

## Environment

```env
LAW_API_KEY=da
PORT=8099
LOG_LEVEL=INFO
RELOAD=false
```

## Run

```bash
pip install -r requirements.txt
python -m src.main
```

## Deploy

Render blueprint is included in `render.yaml`.
