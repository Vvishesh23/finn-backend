// Synthetic delayed responses exercise the real frontend code, without a browser.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const vm=require('node:vm');
const fs=require('node:fs');
function setup(preview=false){
  const nodes=new Map();
  const node=selector=>{if(!nodes.has(selector))nodes.set(selector,{innerHTML:'',value:'WIPRO',disabled:false,classList:{toggle(){}},showModal(){this.open=true}});return nodes.get(selector)};
  const context=vm.createContext({document:{querySelector:node,querySelectorAll:()=>[],addEventListener(){}},localStorage:{getItem(){return null}},URLSearchParams,Intl,Date,JSON,console,fetch:()=>new Promise(()=>{})});
  if(preview){context.previewCalls=0;context.fetch=()=>{context.previewCalls++;throw Error('Frontend preview must not call a backend')};vm.runInContext(fs.readFileSync('frontend/preview.js','utf8'),context)}
  vm.runInContext(fs.readFileSync('frontend/app.js','utf8'),context);
  return {node,context,run:code=>vm.runInContext(code,context)};
}
const flush=()=>new Promise(resolve=>setImmediate(resolve));
test('late brief cannot replace the research screen',async()=>{
 const h=setup();h.run('var pending=[];api=()=>new Promise(resolve=>pending.push(resolve));navigate("brief")');
 await h.run('navigate("research")');const screen=h.node('#content').innerHTML;
 h.run('pending[0]({events:[],count:0});pending[1]({alerts:[],filingAlerts:[]})');await flush();
 assert.equal(h.node('#content').innerHTML,screen);
 assert.match(screen,/Ask better questions/);
});
test('static frontend preview boots and all tabs navigate without API requests',async()=>{
 const h=setup(true);await flush();
 assert.match(h.node('#content').innerHTML,/Frontend preview/);
 for(const view of ['companies','research','settings','brief']){
  await h.run('navigate('+JSON.stringify(view)+')');
  assert.match(h.node('#content').innerHTML,/Frontend preview/);
  assert.match(h.node('#content').innerHTML,/backend is not connected yet/i);
 }
 assert.equal(h.context.previewCalls,0);
 await h.run('navigate("research")');
 assert.match(h.node('#content').innerHTML,/preview-question[^>]*disabled/);
 assert.match(h.node('#content').innerHTML,/Backend connection required/);
});
test('older brief filter response cannot replace a newer one',async()=>{
 const h=setup();h.run('var pending=[];api=()=>new Promise(resolve=>pending.push(resolve));brief();brief()');
 h.run('pending[2]({events:[],count:22});pending[3]({alerts:[],filingAlerts:[]})');await flush();
 assert.match(h.node('#content').innerHTML,/22 grouped disclosures/);
 h.run('pending[0]({events:[],count:11});pending[1]({alerts:[],filingAlerts:[]})');await flush();
 assert.match(h.node('#content').innerHTML,/22 grouped disclosures/);
});
test('late research failure does not alter another view',async()=>{
 const h=setup();await h.run('navigate("research")');
 h.run('var rejectAnswer;api=()=>new Promise((resolve,reject)=>{rejectAnswer=reject});ask("FY25 PAT")');
 await h.run('navigate("settings")');const screen=h.node('#content').innerHTML;
 h.run('rejectAnswer(new Error("provider unavailable"))');await flush();
 assert.equal(h.node('#content').innerHTML,screen);
 assert.equal(h.node('#notice').innerHTML,'');
});
test('newest company selection wins over older delayed response',async()=>{
 const h=setup();h.run('var pending=[];api=()=>new Promise(resolve=>pending.push(resolve));openCompany("NTPC");openCompany("WIPRO")');
 h.run('pending[1]({symbol:"WIPRO",documents:[],financials:{metrics:[]}})');await flush();
 h.run('pending[0]({symbol:"NTPC",documents:[],financials:{metrics:[]}})');await flush();
 assert.match(h.node('#detail-content').innerHTML,/WIPRO/);
 assert.doesNotMatch(h.node('#detail-content').innerHTML,/NTPC/);
});
test('historical replay excludes later EOD and current filing alerts',async()=>{
 const h=setup();h.run('s.window="replay";api=async path=>path.startsWith("/api/brief")?{events:[],count:0,from:"2025-04-17T00:00:00Z",asOf:"2025-04-23T00:00:00Z"}:{alerts:[{symbol:"DRREDDY",date:"2026-10-26",kind:"price",price_pct:6.62}],filingAlerts:[]}');
 await h.run('brief()');
 assert.doesNotMatch(h.node('#content').innerHTML,/6.62% close-to-close/);
 assert.match(h.node('#content').innerHTML,/not replayed as April 2025 prices/);
});
test('latest-import window is pinned to actual filing timestamp',async()=>{
 const h=setup();h.run('s.health={latestFilingAt:"2026-10-27T12:00:00Z"};var paths=[];api=async path=>{paths.push(path);return path.startsWith("/api/brief")?{events:[],count:0}:{alerts:[],filingAlerts:[]}}');
 await h.run('brief()');
 assert.match(h.run('paths[0]'),/end=2026-10-27T12%3A00%3A00Z/);
 assert.match(h.node('#content').innerHTML,/Latest import/);
});
for(const status of [429,503])test('inference HTTP '+status+' preserves evidence in research UI',async()=>{
 const h=setup();await h.run('navigate("research")');
 const data={plan:{intent:'financial_trajectory'},httpStatus:status,status:'PARTIAL',route:'retrieval_only',modelCalls:0,answer:'Reasoning unavailable. Retrieved source notes remain available.',citations:[{id:'public-id',url:'https://issuer.example/report.pdf',title:'Original public evidence',text:'Reviewed public source.'}]};
 h.context.responseFixture=data;
 h.run('fetch=async()=>({ok:false,status:responseFixture.httpStatus,json:async()=>responseFixture})');
 await h.run('ask("Explain FY25 revenue")');
 assert.match(h.node('#answer').innerHTML,/Original public evidence/);
 assert.match(h.node('#notice').innerHTML,new RegExp('HTTP '+status));
 assert.equal(h.node('#ask-button').disabled,false);
});
