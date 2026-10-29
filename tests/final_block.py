"""Volume por aula interna e reconstrução histórica do bloco final."""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def unit_count():
    source = (ROOT / 'index.html').read_text().split('const AL=', 1)[1]
    return len(json.JSONDecoder().raw_decode(source)[0][12]['b'])

def before_private_credit(lessons, material):
    """Desfaz só as agregações novas; não reescreve os hashes de Riscos."""
    report = json.loads((ROOT / 'docs/aula-13-credito-privado-cobertura.json').read_text())
    lessons, material = copy.deepcopy(lessons), copy.deepcopy(material)
    lessons[12]['b'] = lessons[12]['b'][:1]
    lessons[12]['o'] = report['preservacao']['aula13_o']
    for key in ['r', 'd', 'p', 'n']:
        lessons[12][key] = copy.deepcopy(lessons[12]['b'][0][key])
    material['b'] = material['b'][:1]
    material['mm'][1] = copy.deepcopy(material['b'][0]['mm'][1])
    for key in ['dg', 'tb', 'tl', 'fc']:
        material[key] = copy.deepcopy(material['b'][0][key])
    return lessons, material
