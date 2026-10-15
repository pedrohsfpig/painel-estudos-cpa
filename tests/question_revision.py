"""Encadeia o relatório de autoria às alterações de redação autorizadas."""
import copy
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FIELD_INDEX={'enunciado':3,'alternativa correta':4,'alternativa incorreta 1':5,
             'alternativa incorreta 2':6,'alternativa incorreta 3':7,
             'explicação geral':8,'dica':10,'feedbacks':11}

def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def _restore(current,filename):
    """Validar uma revisão e reconstruir a versão anterior pelos campos editados.

    Não atualiza relatórios históricos nem aceita conteúdo diferente do manifesto.
    Novas questões após os IDs cobertos pelo manifesto continuam disponíveis.
    """
    report=json.loads((ROOT/'docs'/filename).read_text())
    restored=copy.deepcopy(current)
    rows=report['questoes']
    assert [r['id'] for r in rows]==list(range(1,len(rows)+1))
    assert len(current)>=len(rows)
    for row in rows:
        id=row['id']
        assert digest(current[id-1])==row['hash_depois'],f'Conteúdo fora da revisão autorizada: {id}'
        for name,change in row['campos'].items():
            index=FIELD_INDEX[name]
            assert current[id-1][index]==change['depois'],f'Campo final divergente: {id}/{name}'
            restored[id-1][index]=change['antes']
        assert digest(restored[id-1])==row['hash_antes'],f'Proveniência anterior divergente: {id}'
    return restored

def questions_before_numeric_revision(current):
    return _restore(current,'revisao-feedbacks-numericos.json')

def bate_pronto_before_numeric_revision(current):
    report=json.loads((ROOT/'docs/revisao-feedbacks-numericos.json').read_text())
    restored=copy.deepcopy(current)
    for row in report['bate_pronto']:
        index=row['id']-100001
        assert digest(current[index])==row['hash_depois'],f'Bate-pronto fora do manifesto numérico: {row["id"]}'
        for field,change in row['campos'].items():
            assert current[index][int(field)]==change['depois']
            restored[index][int(field)]=change['antes']
        assert digest(restored[index])==row['hash_antes']
    return restored

def questions_before_grammar_revision(current):
    return _restore(questions_before_numeric_revision(current),'revisao-pistas-gramaticais.json')

def bate_pronto_before_grammar_revision(current):
    current=bate_pronto_before_numeric_revision(current)
    report=json.loads((ROOT/'docs/revisao-pistas-gramaticais.json').read_text())
    restored=copy.deepcopy(current)
    for row in report['bate_pronto']:
        index=row['id']-100001
        assert digest(current[index])==row['hash_depois'],f'Bate-pronto fora do manifesto: {row["id"]}'
        for field,change in row['campos'].items():
            assert current[index][int(field)]==change['depois']
            restored[index][int(field)]=change['antes']
        assert digest(restored[index])==row['hash_antes']
    return restored

def questions_before_teaching_revision(current):
    previous=questions_before_grammar_revision(current)
    return _restore(previous,'revisao-justificativas-contexto.json')

def questions_before_feedback_revision(current):
    latest=questions_before_teaching_revision(current)
    return _restore(latest,'revisao-alinhamento-feedbacks.json')

def questions_before_context_revision(current):
    # Cada revisão mantém seus hashes; não reescrever evidência histórica para
    # aceitar alterações posteriores. Primeiro desfazer a revisão mais recente.
    context=questions_before_feedback_revision(current)
    return _restore(context,'revisao-enunciados-autossuficientes.json')
