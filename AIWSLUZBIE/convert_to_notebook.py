"""
Skrypt do konwersji pliku Python na notebook Jupyter
Użycie: python convert_to_notebook.py
"""

import json

def create_notebook_from_python(python_file, output_notebook):
    """Konwertuje plik Python na notebook Jupyter"""
    
    with open(python_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Podziel na komórki na podstawie komentarzy sekcji
    sections = content.split('\n# ============================================================================\n')
    
    cells = []
    
    # Pierwsza komórka - markdown z tytułem
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# 🏛️ Asystent AI dla Administracji\n",
            "\n",
            "## System wspierający orzeczników w Departamencie Turystyki MSiT\n",
            "\n",
            "Ten notebook zawiera kompleksowe rozwiązanie AI dla administracji państwowej."
        ]
    })
    
    # Komórki kodu
    current_code = []
    in_code_block = False
    
    for line in content.split('\n'):
        if line.strip().startswith('# ============================================================================'):
            if current_code:
                cells.append({
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": '\n'.join(current_code)
                })
                current_code = []
        else:
            current_code.append(line)
    
    # Ostatnia komórka
    if current_code:
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": '\n'.join(current_code)
        })
    
    # Utwórz notebook
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    with open(output_notebook, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print(f"✅ Notebook utworzony: {output_notebook}")

if __name__ == "__main__":
    create_notebook_from_python(
        "asystent_ai_administracja_complete.py",
        "asystent_ai_administracja.ipynb"
    )

