"""Volume por aula interna e reconstrução histórica do bloco final."""
from numbers_revision import restore_before_numbers,restore_before_investor_numbers
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def unit_count():
    source = (ROOT / 'index.html').read_text().split('const AL=', 1)[1]
    return len(json.JSONDecoder().raw_decode(source)[0][12]['b'])

def before_payment_flows(lessons, material):
    """Reconstrói o agregado das duas primeiras internas, preservando evidência."""
    report = json.loads((ROOT / 'docs/aula-13-fluxos-cobertura.json').read_text())
    lessons, material = restore_before_numbers(lessons), copy.deepcopy(material)
    lessons[12]['b'] = lessons[12]['b'][:2]
    lessons[12]['o'] = report['preservacao']['aula13_o']
    for key in ['r','d','p','n']:
        lessons[12][key] = [x for u in lessons[12]['b'] for x in u[key]]
    material['b'] = material['b'][:2]
    material['mm'][1] = [x for u in material['b'] for x in u['mm'][1]]
    for key in ['dg','tb','tl','fc']:
        material[key] = [x for u in material['b'] for x in u[key]]
    return lessons, material

def before_private_credit(lessons, material):
    """Desfaz só as agregações novas; não reescreve os hashes de Riscos."""
    report = json.loads((ROOT / 'docs/aula-13-credito-privado-cobertura.json').read_text())
    lessons, material = restore_before_numbers(lessons), copy.deepcopy(material)
    lessons[12]['b'] = lessons[12]['b'][:1]
    lessons[12]['o'] = report['preservacao']['aula13_o']
    for key in ['r', 'd', 'p', 'n']:
        lessons[12][key] = copy.deepcopy(lessons[12]['b'][0][key])
    material['b'] = material['b'][:1]
    material['mm'][1] = copy.deepcopy(material['b'][0]['mm'][1])
    for key in ['dg', 'tb', 'tl', 'fc']:
        material[key] = copy.deepcopy(material['b'][0][key])
    return lessons, material

def before_portfolio_lesson(lessons, material):
    """Reconstrói as três internas antes da revisão de números e da quarta aula."""
    report = json.loads((ROOT / 'docs/aula-13-carteiras-cobertura.json').read_text())
    lessons, material = restore_before_numbers(lessons), copy.deepcopy(material)
    lessons[12]['b'] = lessons[12]['b'][:3]
    lessons[12]['o'] = report['preservacao']['aula13_o']
    for key in ['r','d','p','n']:
        lessons[12][key] = [x for u in lessons[12]['b'] for x in u[key]]
    material['b'] = material['b'][:3]
    material['mm'][1] = [x for u in material['b'] for x in u['mm'][1]]
    for key in ['dg','tb','tl','fc']:
        material[key] = [x for u in material['b'] for x in u[key]]
    return lessons, material

def before_investor_lesson(lessons, material):
    """Entrega de carteiras, antes da quinta interna e da segunda limpeza numérica."""
    report=json.loads((ROOT/'docs/aula-13-investidores-cobertura.json').read_text())
    lessons,material=restore_before_investor_numbers(lessons),copy.deepcopy(material)
    lessons[12]['b']=lessons[12]['b'][:4]
    lessons[12]['o']=report['preservacao']['aula13_o']
    for key in ['r','d','p','n']:
        lessons[12][key]=[x for u in lessons[12]['b'] for x in u[key]]
    material['b']=material['b'][:4]
    material['mm'][1]=[x for u in material['b'] for x in u['mm'][1]]
    for key in ['dg','tb','tl','fc']:
        material[key]=[x for u in material['b'] for x in u[key]]
    return lessons,material
