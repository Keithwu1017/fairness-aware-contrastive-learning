import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {parseCSV,validateRows,summarize} from '../site/app.mjs';
const demo=readFileSync(new URL('../site/data/demo_metrics.csv',import.meta.url),'utf8');

test('browser calculations agree with known reference values',()=> {
  const rows=validateRows(parseCSV(demo));
  const summary=summarize(rows.filter(r=>r.scenario===rows[0].scenario));
  assert.ok(Math.abs(summary[0].eopp-.22)<1e-10);
  assert.ok(Math.abs(summary[1].eopp-.02)<1e-10);
  assert.ok(Math.abs(summary[0].ebacc-.14)<1e-10);
  assert.ok(Math.abs(summary[1].ebacc-.015)<1e-10);
});
test('CSV supports BOM, quoted commas and escaped quotes',()=> {
  const rows=parseCSV('\ufeffscenario,model,group,auroc,tpr,tnr,n\r\n"a,b",Baseline,"a""b",.9,.8,.7,10\r\n');
  assert.equal(rows[0].scenario,'a,b');assert.equal(rows[0].group,'a"b');
  assert.throws(()=>parseCSV('scenario,model,group,auroc,tpr,tnr,n\n"unfinished'),/引號/);
  assert.throws(()=>parseCSV('scenario,model,group,auroc,tpr,tnr,n\n"bad"x,b,g,1,1,1,10'),/引號/);
});
test('reject invalid and unpaired cohort results',()=> {
  const rows=parseCSV(demo);
  for(const [key,value] of [['tpr','1.1'],['n','1.5'],['tnr','Infinity'],['auroc',''],['group',''],['model','Other']]) {
    const copy=structuredClone(rows);copy[0][key]=value;assert.throws(()=>validateRows(copy));
  }
  assert.throws(()=>validateRows([...rows,rows[0]]),/重複/);
  assert.throws(()=>validateRows(rows.slice(1)),/群體/);
  const copy=structuredClone(rows);copy[0].n='199';assert.throws(()=>validateRows(copy),/相同/);
});
