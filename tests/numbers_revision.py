"""Reconstitui somente os cartões anteriores para conferir evidências históricas.
A revisão autorizada é validada separadamente; manifests antigos não são alterados.
"""
import copy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def restore_before_numbers(lessons):
 lessons=copy.deepcopy(lessons)
 for change in json.loads((ROOT/'docs/revisao-numeros-para-decorar.json').read_text())['alteracoes']:
  lesson=lessons[change['aula']-1];lesson['n']=copy.deepcopy(change['antes'])
  for unit in lesson.get('b',[]):
   if str(unit['id']) in change['blocos_antes']:unit['n']=copy.deepcopy(change['blocos_antes'][str(unit['id'])])
 return lessons
