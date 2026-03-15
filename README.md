# Law Open Data Dedicated MCP

Dedicated MCP server for Korean constitutional-law and administrative-law retrieval with strict source separation.

This project is designed for accuracy-sensitive legal use. It exposes exact tools instead of forcing all requests through a single integrated QA tool.

## Features

### 🔍 Legal Search
- **Statutes**: Search and retrieve Korean laws and articles
- **Precedents**: Court judgments with 4-step fallback search
- **Constitutional Decisions**: Constitutional Court rulings
- **Administrative Appeals**: Administrative review cases
- **Administrative Rules**: Ministry regulations and notices
- **Legal Interpretations**: Government legal interpretations

### 📅 Compliance Calendar
- Statutory deadlines (tax, labor, safety)
- Monthly recurring obligations
- iCalendar export for integration

### ✅ Compliance Checklists
- Startup checklist (6 items)
- Privacy compliance (6 items)
- Labor law compliance (6 items)
- Safety compliance (5 items)
- E-commerce compliance (3 items)
- Advertising compliance (2 items)

## Tool philosophy

- Use statute tools for statutes
- Use precedent tools for precedents
- Use interpretation tools for interpretation
- Keep mixed QA as optional, not primary

## Primary tools

### Legal Search Tools
- `search_law_tool` - Search statutes
- `get_law_detail_tool` - Get statute details
- `get_law_article_tool` - Get specific article
- `search_precedent_tool` - Search precedents (with fallback)
- `get_precedent_tool` - Get precedent details
- `search_constitutional_decision_tool` - Search constitutional decisions
- `get_constitutional_decision_tool` - Get decision details
- `search_administrative_appeal_tool` - Search administrative appeals
- `get_administrative_appeal_tool` - Get appeal details
- `search_administrative_rule_tool` - Search administrative rules
- `search_law_interpretation_tool` - Search legal interpretations
- `get_law_interpretation_tool` - Get interpretation details

### Compliance Tools (NEW)
- `get_compliance_calendar_tool` - Get compliance events
  - `days`: Get upcoming events within N days
  - `month`: Get events for specific month
  - `category`: Get events by category (tax, labor, etc.)
- `get_compliance_checklist_tool` - Get compliance checklists
  - `checklist_id`: Get specific checklist (startup, privacy, labor, etc.)
  - `keyword`: Search checklists by keyword

These tools are intended to support exam-style verification flows such as:

- verifying statute name + article number for constitutional/administrative law MCQs
- verifying Supreme Court case numbers for precedent-based options
- verifying Constitutional Court decisions for constitutional law options
- checking administrative appeals, administrative rules, and ministry interpretations for administrative-law edge cases
- tracking compliance deadlines for business operations
- verifying legal compliance with checklists

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

## Test

```bash
# Run all tests
pytest tests/ -v

# Run unit tests only
pytest tests/ -v -m "not integration"

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Deploy

Render blueprint is included in `render.yaml`.

## Documentation

- [DEPLOY.md](DEPLOY.md) - Deployment guide
- [MCP-SETUP.md](MCP-SETUP.md) - MCP client setup
- [CLAUDE.md](CLAUDE.md) - Claude integration guide
- [AGENTS.md](AGENTS.md) - AI agent integration guide
