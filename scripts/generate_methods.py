#!/usr/bin/env python3
"""Draw original, bilingual conceptual diagrams for the website using native SVG."""
from pathlib import Path
from html import escape
R=Path(__file__).resolve().parents[1];out=R/'assets/methods';out.mkdir(exist_ok=True)
D={
'agenthazard':('AgentHazard',{'en':(['Harmful objectives','Multi-step tasks','Execution assessment'],['Risk × attack taxonomy','Plausible individual steps','Trajectory-level outcomes'],'MEASURE RISKS ACROSS THE WHOLE TRAJECTORY'),'zh':(['有害目标','多步骤任务','执行评估'],['风险 × 攻击分类','单步看似合理的行为','完整轨迹的实际结果'],'量化完整执行轨迹中的风险')}),
'vera':('VERA',{'en':(['Risk discovery','Executable tests','Evidence verification'],['Literature-driven taxonomy','Goals, state & verifiers','Actions → observable state'],'DISCOVER → CONSTRUCT → EXECUTE & VERIFY'),'zh':(['风险发现','可执行测试','证据验证'],['文献驱动的分类体系','目标、状态与验证器','动作 → 可观测状态'],'发现 → 构建 → 执行与验证')}),
'braveguard':('BraveGuard',{'en':(['Evolving threats','Agent trajectories','Guard training'],['Explore & validate tasks','Collect execution evidence','Learn from supervision'],'FEEDBACK CONNECTS VALIDATION AND THREAT DISCOVERY'),'zh':(['演化威胁','智能体轨迹','防护模型训练'],['探索并验证任务','采集执行证据','从轨迹监督中学习'],'通过验证反馈持续更新威胁发现')}),
'hazardauditor':('HazardAuditor',{'en':(['Executable threats','Shared evidence','GuardPO'],['Ground supervision in runs','Normalize agent interactions','Optimize safety decisions'],'EXECUTION EVIDENCE → TRAJECTORY-LEVEL AUDITING'),'zh':(['可执行威胁','统一行为证据','GuardPO'],['从执行中构建监督','规范跨框架交互','优化安全判决'],'执行证据 → 轨迹级安全审计')}),
'adaguard':('AdaGuard',{'en':(['User-defined policy','Agent trajectory','Violation set'],['Rules supplied at inference','Recorded actions & outcomes','Explanation + rule identifiers'],'ADAPTIVESAFETY + SafePO → POLICY-CONDITIONED GUARDS'),'zh':(['用户定义策略','智能体轨迹','违规规则集合'],['推理时提供规则','记录的动作与结果','解释 + 违规规则标识'],'AdaptiveSafety + SafePO → 策略条件下的防护模型')})}
for key,(name,langs) in D.items():
 for lang,(titles,subs,foot) in langs.items():
  parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="390" viewBox="0 0 1000 390" role="img"><title>{name} — {escape(foot)}</title><rect width="1000" height="390" rx="20" fill="#f8fafc"/><g font-family="Arial,PingFang SC,Microsoft YaHei,sans-serif"><text x="38" y="48" font-size="21" font-weight="700" fill="#112333">{name}</text><text x="962" y="46" text-anchor="end" font-size="11" letter-spacing="1" fill="#526879">'+('CONCEPTUAL METHOD OVERVIEW' if lang=='en' else '方法概念示意')+'</text>']
  for i,(title,sub) in enumerate(zip(titles,subs)):
   x=38+i*324;fill=['#e7f2fc','#dceffc','#fddeb1'][i]
   parts.append(f'<rect x="{x}" y="101" width="276" height="172" rx="14" fill="{fill}"/><text x="{x+20}" y="134" font-size="12" fill="#496275">0{i+1}</text><text x="{x+20}" y="184" font-size="21" font-weight="700" fill="#112333">{escape(title)}</text><text x="{x+20}" y="220" font-size="15" fill="#496275">{escape(sub)}</text>')
   if i<2:parts.append(f'<path d="M{x+286} 185h27m-8-6 8 6-8 6" fill="none" stroke="#1697e2" stroke-width="3"/>')
  if key=='braveguard':parts.append('<path d="M824 281v22H175v-22m-6 8 6-8 6 8" stroke="#1697e2" stroke-width="2" fill="none" stroke-dasharray="5 4"/>')
  parts.append(f'<text x="38" y="349" font-size="13" fill="#496275">{escape(foot)}</text></g></svg>')
  (out/f'{key}.{lang}.svg').write_text(''.join(parts))
print('Rendered ten original bilingual SVG method diagrams.')
