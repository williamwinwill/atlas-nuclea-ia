---
name: sonar-fix
description: Use quando o usuário quiser investigar ou corrigir issues, regras, medidas ou Quality Gate do SonarQube em um repositório local. Consulte o MCP em modo somente leitura, confirme o problema no código atual e aplique apenas correções locais pequenas com testes.
---

# Consultar e corrigir problemas do SonarQube

Conecte o diagnóstico do Sonar ao código atual sem alterar o estado das issues no servidor.

## Fluxo

1. Determine `projectKey`, branch ou pull request e a análise relevante. Se houver ambiguidade material, obtenha a informação antes de editar.
2. Descubra as ferramentas realmente expostas pelo MCP; não invente nomes de ferramentas.
3. Consulte a issue, detalhes da regra e contexto necessário. Mantenha o acesso somente leitura.
4. Abra o arquivo e confirme que o problema ainda existe na versão local. Trate issue resolvida, linha deslocada ou análise antiga como evidência desatualizada.
5. Explique a causa, o impacto e a menor correção segura.
6. Edite somente o escopo necessário e execute os testes, linters ou builds proporcionais ao risco.
7. Apresente o diff, os testes e qualquer limitação. A confirmação final vem da nova análise no pipeline.

Leia [references/sonarqube-runbook.md](references/sonarqube-runbook.md) para autenticação, escopo e falhas comuns.

## Restrições

- Não altere status, severidade, assignee, false-positive ou aceitação de risco no SonarQube.
- Não exponha token em comando, arquivo, diff ou log.
- Não enfraqueça Quality Gate, regra ou teste para fazer o alerta desaparecer.
- Não declare sucesso apenas com base em análise local; aguarde o pipeline oficial quando essa confirmação for exigida.
- Se a correção exigir mudança ampla de arquitetura ou contrato, pare após o diagnóstico e apresente as opções.

