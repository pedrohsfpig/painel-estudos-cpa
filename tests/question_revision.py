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

def questions_before_context_revision(current):
    """Validar o banco atual e reconstruir a versão anterior pelos campos editados.

    Não atualiza relatórios históricos nem aceita conteúdo diferente do manifesto.
    Novas questões após os IDs cobertos pelo manifesto continuam disponíveis.
    """
    report=json.loads((ROOT/'docs/revisao-enunciados-autossuficientes.json').read_text())
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
