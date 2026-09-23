# Runbook SonarQube

## Configuração esperada

- Use um user token fornecido por `SONARQUBE_TOKEN`.
- Para SonarQube Server, forneça `SONARQUBE_URL` e, quando conhecido, `SONARQUBE_PROJECT_KEY`.
- Mantenha `SONARQUBE_READ_ONLY=true`.
- Limite `SONARQUBE_TOOLSETS` ao necessário; `projects` é disponibilizado automaticamente pelo servidor.
- O manifesto consumidor, não esta skill, ativa o MCP explicitamente.

## Triagem

1. Confirme se a issue pertence à branch/PR atual.
2. Leia os detalhes da regra antes de mudar o código.
3. Verifique suppressions existentes e convenções do projeto.
4. Prefira remover a causa a adicionar `NOSONAR` ou exclusão.
5. Se suspeitar de falso positivo, documente a evidência, mas não mude o status pelo MCP.

## Falhas comuns

- Sem ferramenta MCP: confirme que `apm install` gerou `.kiro/settings/mcp.json` e que o Docker está disponível.
- Autenticação recusada: valide ambiente e permissões sem imprimir o token.
- Issue não encontrada: confira `projectKey`, branch/PR e idade da análise.
- Resultado divergente: o pipeline oficial é a autoridade para Quality Gate.

