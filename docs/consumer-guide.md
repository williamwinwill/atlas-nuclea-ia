# Guia do consumidor

## Arquivos versionados

O projeto consumidor mantém no Git:

- `apm.yml` com o pacote e MCPs explícitos;
- `apm.lock.yaml` gerado pelo APM;
- arquivos gerados para o Kiro, se essa for a convenção da organização.

`apm_modules/` não deve ser versionado.

## Adesão pelo Atlas

O Atlas abre uma PR contendo:

1. dependência do kit ou skill individual;
2. path exato no monorepo;
3. SHA completo da release aprovada;
4. declaração MCP explícita quando necessária;
5. identificação do projeto Sonar sem credencial;
6. lockfile e arquivos Kiro resultantes.

Depois do merge, o desenvolvedor fornece `SONARQUBE_TOKEN` no ambiente e executa `apm install`. Outros desenvolvedores restauram os mesmos bytes com o mesmo comando.

## Atualização

Uma versão do kit não se atualiza silenciosamente. O Atlas abre uma nova PR que troca o SHA, regenera o lockfile e mostra o diff. Para desfazer, o projeto retorna ao SHA anterior.

## Kiro

O APM entrega skills em `.kiro/skills/<nome>/SKILL.md` e configuração MCP em `.kiro/settings/mcp.json`. O manifesto consumidor é a fonte de verdade; não edite o MCP gerado diretamente.

