# ⚠️ GQPA CORE - BACKGROUND IP

## Status Prawny

**GQPA DIAMOND** jest utworem współautorskim:
- **Autorzy:** Jakub Szych & Michał Wojtków
- **Status:** Background IP (NIE podlega przeniesieniu praw)
- **Licencja:** Zobacz `LICENSE_GQPA.txt`

## Użycie

GQPA Core jest używane jako biblioteka zewnętrzna w projekcie hackathonowym.

### Import w projekcie hackathonowym:

```python
# Dodaj ścieżkę do system/
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'system'))

# Import GQPA Core
from gqpa_core import get_gqpa_info

# Użycie
info = get_gqpa_info()
print(f"Używana biblioteka: {info['name']}")
```

## Komponenty

Pełna implementacja GQPA znajduje się w plikach:
- `gqpa_part1.py` - Podstawowe typy danych
- `gqpa_part2.py` - HAMA2 Cognitive Core
- `gqpa_part3.py` - Moduły kognitywne
- `gqpa_part4.py` - Pamięć i model świata
- `gqpa_part5.py` - Emergent Cognitive Integrator
- `gqpa_part6.py` - Metodologia testowa
- `gqpa_part7.py` - Moduły dodatkowe
- `gqpa_deploy.py` - System deployment

## Uwaga

Ten moduł jest **Background IP** i nie podlega przeniesieniu praw w ramach hackathonu.

